from terrain_util import *
from gdalrw_util import *
from mpi_run import *

if __name__ == ("__main__") :
	#parseArgs() cn
	file = "output_be.tif"
 	data = band_to_array(file)
	run_mpi_jobs(data)
#	newdata = run_mpi_jobs(data)
