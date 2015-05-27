import gdal
import time
import numpy as np
from mpi_util import *
from mpi4py import MPI
from gdalconst import *

import matplotlib.pyplot as plt
import matplotlib as ml
import matplotlib.cm as cm

# this function assign roughly equally devided data to each process,
# then each process do the computation independently.
def run_mpi_jobs (file, p):
	comm = MPI.COMM_WORLD
	rank = comm.Get_rank()
	size = comm.Get_size()

        # output is in geo tiff format
	output_file = "myoutput.tif"
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
	
        # the process with highest rank get the last chunk of data 
	if rank == size-1 :
                # in order to process boundaries get one more column of data from left neighbor 
		x_offset = rank*proc_cols-1
		proc_cols = cols - proc_cols * (size-1)
		G = np.zeros((y_size, proc_cols))
		x_size = proc_cols + 1

		process_bands(band, p, x_offset, x_size, y_size, G)

        # process with lowest rank get the first chunk of data
	elif rank == 0:
                # in order to process boundaries, get one more column of data from right neighbor 
		G = np.zeros((y_size, proc_cols))
		x_offset = 0
		x_size = proc_cols + 1
		
		process_bands(band, p, x_offset, x_size, y_size, G)
        

	else:
                # get two more columns of data from neighbors to process boundaries
		G = np.zeros((y_size, proc_cols))
		x_offset = rank*proc_cols-1
		x_size = proc_cols+2
		
		process_bands(band, p, x_offset, x_size, y_size, G)
                
        # wait for all processes finish processing
	comm.Barrier()
        # rank 0 gathers all processed data
	data = comm.gather(G, root=0)
	
	if rank == 0:
                # output processed data
		data = np.concatenate(data, axis=1)
                # set boundary data to NULL
                data[[0,-1]] = None
                data[:, [0,-1]] = None
		output_dataset = driver.Create(output_file, cols, y_size, 1, gdal.GDT_Float32)
		output_dataset.SetGeoTransform(geotransform)
		output_dataset.GetRasterBand(1).WriteArray(data)
                output_dataset = None
		dataset = None
                
