import gdal
import time
import numpy as np
from mpi_util import *
from mpi4py import MPI
from gdalconst import *

def run_mpi_jobs (file, p):
	comm = MPI.COMM_WORLD
	rank = comm.Get_rank()
	size = comm.Get_size()

	output_file = "myoutput.tif"
	driver = gdal.GetDriverByName("GTiff")	
	dataset = gdal.Open(file, GA_ReadOnly)
	band = dataset.GetRasterBand(1)
	geotransform = dataset.GetGeoTransform()
	if p == 0:
		p = geotransform[1] 
	cols = dataset.RasterXSize
	proc_cols = cols/size
	y_size = dataset.RasterYSize
	
	if rank == size-1 :
		x_offset = rank*proc_cols-1
		proc_cols = cols - proc_cols * (size-1)
		G = np.zeros((y_size, proc_cols))
		x_size = proc_cols + 1

		process_bands(band, p, x_offset, x_size, y_size, G)
	
	elif rank == 0:
		G = np.zeros((y_size, proc_cols))
		tic = time.clock()
		x_offset = 0
		x_size = proc_cols + 1
		
		process_bands(band, p, x_offset, x_size, y_size, G)

	else:
		G = np.zeros((y_size, proc_cols))
		x_offset = rank*proc_cols-1
		x_size = proc_cols+2
		
		process_bands(band, p, x_offset, x_size, y_size, G)

	comm.Barrier()
	data = comm.gather(G, root=0)
	
	if rank == 0:
		data = np.concatenate(data, axis=1)
		toc = time.clock()
		print toc - tic
		
		output_dataset = driver.Create(output_file, cols, y_size, 1, gdal.GDT_Float32)
		output_dataset.SetGeoTransform(geotransform)
		output_dataset.GetRasterBand(1).WriteArray(data)
		output_dataset = None
		dataset = None
