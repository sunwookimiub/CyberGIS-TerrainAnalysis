import gdal
import time
import numpy as np
from worker_util import *
from mpi4py import MPI
from gdalconst import *



def write_to_file(data, x_size, y_size, 
                  output_file_name, input_driver_name):
    """Write analysed data to output file

    Keyword argument:
    data              -- analysed data, 3 dimensional numpy array
    x_size            -- size in x dimension for output raster band
    y_size            -- size in y dimension for output raster band
    output_file_name  -- file name for output data
    input_driver_name -- output file format
    """
    driver = gdal.GetDriverByName(input_driver_name)
    output_dataset = driver.Create(output_file_name, x_size, 
                                   y_size, 10, gdal.GDT_Float32)
    for i in range(data.shape[0]):
        output_dataset.GetRasterBand(i+1).WriteArray(data[i], 1, 1)
    output_dataset = None

def run_mpi_jobs (file, p, output):
    """ Assign roughly equally divided data chunk to each process

    Keyword argument:
    file   -- input file name
    p      -- pixel size
    output -- output file name
    """
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    dataset = gdal.Open(file, GA_ReadOnly)
    input_driver_name = dataset.GetDriver().ShortName
    band = dataset.GetRasterBand(1)
    geotransform = dataset.GetGeoTransform()
    # if using default pixel size, get pixel size from data
    if p == 0:
        p = geotransform[1]
        cols = dataset.RasterXSize
        rows = dataset.RasterYSize
        # roughly assign equal number of rows to each process
        proc_rows = rows/size
        # each process is assigned with same number of columns as original data
        x_size = dataset.RasterXSize

    # the process with highest rank get the last chunk of data
    if rank == size - 1:
        # in order to process boundaries get one more row of data from left neighbor
        y_offset = rank*proc_rows - 1
        y_size = rows - proc_rows*(size-1) + 1
        output_data = process_bands(band, p, y_offset, x_size, y_size)

        # process with lowest rank get the first chunk of data
    elif rank == 0:
        # in order to process boundaries, get one more row of data from right neighbor
        y_offset = 0
        y_size = proc_rows + 1
        output_data = process_bands(band, p, y_offset, x_size, y_size)
    else:
        # get two more rows of data from neighbors to process boundaries
        y_offset = rank*proc_rows - 1
        y_size = proc_rows + 2
        output_data = process_bands(band, p, y_offset, x_size, y_size)

    # wait for all processes finish processing
    comm.Barrier()
    # close input dataset
    dataset = None
    # rank 0 gathers all processed data
    data = comm.gather(output_data, root=0)
    if rank == 0:
        # output processed data
        data = np.concatenate(data, axis=1)
        write_to_file(data, cols, rows, output, input_driver_name)
