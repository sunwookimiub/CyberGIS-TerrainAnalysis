import gdal
from gdalconst import *
from mpi4py import MPI
from mpi_run import *
import sys
import os

def main():
	file = sys.argv[1]
	p = float(sys.argv[2])
	run_mpi_jobs(file, p)
	
if __name__ == ("__main__") :
	main()
