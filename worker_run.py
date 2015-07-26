import sys
import gdal
import time
import numpy as np
import logging
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

def create_raster(x_size, y_size, output_file_name, 
                  input_driver_name, georef, proj):
    """Create the output raster file
    
    Keyword argument:
    x_size              -- size in x dimension for output raster band
    y_size              -- size in y dimension for output raster band
    output_file_name    -- file name for output data
    input_driver_name   -- output file format
    georef              -- geo reference from input data
    proj                -- projection from input data

    Return value:
    output_dataset      -- output data set 
    """
    driver = gdal.GetDriverByName(input_driver_name)
    output_dataset = driver.Create(output_file_name, x_size, 
                                   y_size, 10, gdal.GDT_Float32)
    output_dataset.SetGeoTransform(georef)
    output_dataset.SetProjection(proj)
    return output_dataset
        
    
def write_raster(dataset, data, x_offset, 
                 y_offset, nodata):
    """ Write data to 10 bands of output file 
            
    Keyword arguments:
    dataset             -- output data set
    data                -- data to be write, numpy array 
    x_offset            -- x offset for each band 
    y_offset            -- y offset for each band
    nodata              -- nodata value for each band
    """
    for i in range(data.shape[0]):
        dataset.GetRasterBand(i+1).WriteArray(data[i], x_offset, y_offset)
        dataset.GetRasterBand(i+1).SetNoDataValue(nodata)
    

def run_mpi_jobs (file, output, nodata, band_index):
    """ Assign roughly equally divided data chunk to each process

    Keyword argument:
    file   -- input file name
    output -- output file name
    nodata -- nodata value for missing data points
    band   -- input raster band
    """
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    dataset = gdal.Open(file, GA_ReadOnly)
    input_driver_name = dataset.GetDriver().ShortName # get file format for output
    if not band_index:
        band_index = 1
    band = dataset.GetRasterBand(band_index)
    
    if not nodata:
        nodata = band.GetNoDataValue()

    geotransform = dataset.GetGeoTransform()
    proj = dataset.GetProjection()
    
    cols = dataset.RasterXSize
    rows = dataset.RasterYSize

    # compute corner coordinates
    minx = geotransform[0]
    miny = geotransform[3] + cols*geotransform[4] + rows*geotransform[5]
    maxx = geotransform[0] + cols*geotransform[1] + rows*geotransform[2]
    maxy = geotransform[3]

    # compute pixel sizes 
    px, py = get_pixel(proj, geotransform) 
    
    # print useful geo infomation
    if rank == 0:
        logging.info("Coordinate system is: %s", dataset.GetProjection())
        logging.info("Corner Coordinates:")
        logging.info("Upper left: (%f, %f)", minx, maxy)
        logging.info("Upper right: (%f, %f)", maxx, maxy)
        logging.info("Lower left: (%f, %f)", minx, miny)
        logging.info("Upper right: (%f, %f)", maxx, miny)
        logging.info("nodata is: %g", nodata)
        logging.info("pixel size = (%f, %f)", px, py)

    # data required for process
    proc_rows = rows/size
    x_size = dataset.RasterXSize
    y_size = 0
    x_offset = 0
    y_offset = 0

    if rank == 0:
        t1 = time.time()

    
    if size == 1 :
        y_offset = 0
        y_size = proc_rows
        output_data = calculate_operations(band, px, py, y_offset, x_size, y_size)
        
    elif rank == size - 1:
        # to process boundaries get one more row of data from left neighbor
        y_offset = rank*proc_rows - 1
        y_size = rows - proc_rows*(size-1) + 1
        output_data = calculate_operations(band, px, py, y_offset, x_size, y_size)

    elif rank == 0:
        # to process boundaries, get one more row of data from right neighbor
        y_offset = 0
        y_size = proc_rows + 1
        output_data = calculate_operations(band, px, py, y_offset, x_size, y_size)

    # last worker gets get remainder of rows
    elif rank == size - 1:
        y_offset = rank * proc_rows - 1
        y_size = rows - proc_rows * (size-1) + 1

    # all other workers get 2 extra rows
    else:
        y_offset = rank * proc_rows - 1
        y_size = proc_rows + 2
        output_data = calculate_operations(band, px, py, y_offset, x_size, y_size)
    comm.Barrier()
    
    # close input data
    dataset = None


    # write output to file
    # root proc create output file and writes iis output to file 
    if rank == 0:
        t2 = time.time()
        output_dataset = create_raster(cols, rows, output, 
            input_driver_name, geotransform, proj)
        write_raster(output_dataset, output_data, 1, 1, nodata)


    for proc in range(1, size):
        # worker proc send output matrix size to root proc 
        if rank == proc:
            comm.send(output_data.shape, dest=0, tag=proc)
        elif rank == 0:
            proc_output_dim = comm.recv(source=proc, tag=proc)
        comm.Barrier()
        # worker proc send output data to root proc
        if rank == proc:
            comm.Send(output_data, dest=0, tag=proc)
            logging.debug('process %s finishes sending data', str(proc))
        elif rank == 0:            
            buffered_output = np.zeros(proc_output_dim)
            comm.Recv(buffered_output, source=proc, tag=proc)
            # root proc write output to file
            write_raster(output_dataset, buffered_output, 1, proc*proc_rows,
                         nodata)
        comm.Barrier()

    # close output file 
    output_dataset = None
    
    if rank == 0:
        t_end = time.time()
        logging.debug("write time: %f ", t_end-t2)
        logging.debug("total time: %f ", t_end-t1)
