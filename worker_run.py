import gdal
import time
import numpy as np
from worker_util import *
from mpi4py import MPI
from gdalconst import *

# write output to file
def write_to_file(data, x_size, y_size, output_file_name, input_driver_name):
	driver = gdal.GetDriverByName(input_driver_name)	
        output_dataset = driver.Create(output_file_name, x_size, y_size, 5, gdal.GDT_Float32)
        for i in range(data.shape[0]):
                output_dataset.GetRasterBand(i+1).WriteArray(data[i],1,1)
        output_dataset = None

# this function assign roughly equally devided data to each process
# then each process do the computation independently.
def run_mpi_jobs (file, p, output):
	comm = MPI.COMM_WORLD
	rank = comm.Get_rank()
	size = comm.Get_size()

        # output is in geo tiff format
	dataset = gdal.Open(file, GA_ReadOnly)
        input_driver_name = dataset.GetDriver().ShortName
	band = dataset.GetRasterBand(1)
	geotransform = dataset.GetGeoTransform()
        # if using default pixel size, get pixel size from data 
	if p == 0:
		p = geotransform[1] 
	cols = dataset.RasterXSize
        # number of columns for each process
	proc_cols = cols/size
        # each process is assigned with same number of columns as original data
	y_size = dataset.RasterYSize
	
        # the process with highest rank get the last chunk of data 
	if rank == size-1 :
                # in order to process boundaries get one more column of data from left neighbor 
		x_offset = rank*proc_cols-1
		proc_cols = cols - proc_cols * (size-1)
		x_size = proc_cols + 1
                output_data = process_bands(band, p, x_offset, x_size, y_size)

        # process with lowest rank get the first chunk of data
	elif rank == 0:
                # in order to process boundaries, get one more column of data from right neighbor 
		x_offset = 0
		x_size = proc_cols + 1		
		output_data = process_bands(band, p, x_offset, x_size, y_size)
	else:
                # get two more columns of data from neighbors to process boundaries
		x_offset = rank*proc_cols-1
		x_size = proc_cols+2		
		output_data = process_bands(band, p, x_offset, x_size, y_size)
                
        # wait for all processes finish processing
	comm.Barrier()
        # close input dataset
        dataset = None
        # rank 0 gathers all processed data
	data = comm.gather(output_data, root=0)
	if rank == 0:
                # output processed data
		data = np.concatenate(data, axis=2)
                write_to_file(data, cols, y_size, output, input_driver_name)
	
        
