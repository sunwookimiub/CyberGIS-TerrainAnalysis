import gdal
import time
import numpy as np
from worker_util import *
from mpi4py import MPI
from gdalconst import *

# The function run_mpi_jobs assigns equally divided data to each process
# Each process performs the computation independently
def run_mpi_jobs (file, p, output_file):
	comm = MPI.COMM_WORLD
	rank = comm.Get_rank()
	size = comm.Get_size()

    # Current output format is geoTIFF
	driver = gdal.GetDriverByName("GTiff")	
	dataset = gdal.Open(file, GA_ReadOnly)
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
	
    # The process with highest rank receives the last chunk of data 
	if rank == size-1 :
		# Process the boundaries
        # One more column of data is attained from the neighbor to the left 
		x_offset = rank*proc_cols-1
		proc_cols = cols - proc_cols * (size-1)
		G = np.zeros((y_size, proc_cols))
		x_size = proc_cols + 1

		process_bands(band, p, x_offset, x_size, y_size, G)

        # The process with lowest rank receives the first chunk of data
	elif rank == 0:
		# Again, process the boundaries
		# One more column of data is attained from the neighbor to the right
		G = np.zeros((y_size, proc_cols))
		x_offset = 0
		x_size = proc_cols + 1
		
		process_bands(band, p, x_offset, x_size, y_size, G)
        

	else:
        # Again, process the boundaries
		# Two more columns of data is attained from neighbors 
		G = np.zeros((y_size, proc_cols))
		x_offset = rank*proc_cols-1
		x_size = proc_cols+2
		
		process_bands(band, p, x_offset, x_size, y_size, G)
                
    # Barrier is called to wait for all processes 
	comm.Barrier()
    # The root, rank 0, gathers all processed data
	data = comm.gather(G, root=0)
	
	if rank == 0:
        # output processed data
		data = np.concatenate(data, axis=1)
		output_dataset = driver.Create(output_file, cols, y_size, 1, \
							gdal.GDT_Float32)
		output_dataset.SetGeoTransform(geotransform)
		output_dataset.GetRasterBand(1).WriteArray(data)
		output_dataset = None
		dataset = None
