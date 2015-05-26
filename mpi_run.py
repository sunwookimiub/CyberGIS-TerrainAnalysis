from mpi_util import *
from mpi4py import MPI
import numpy as np

def run_mpi_jobs (data):
	comm = MPI.COMM_WORLD
	rank = comm.Get_rank()
	size = comm.Get_size()

	vfunc = np.vectorize(test)
	arrayOfBlocks = vfunc(data[:])
	print arrayOfBlocks	
	#some numpy function to check bounds
	#some numpy function to get blocks 
	# have these blocks in an array to have shared memory
	#send to individual mpi process
	#gather
	#return the tif file
	
