from terrain_util import *
from gdalrw_util import *
from mpi_run import *

if __name__ == ("__main__") :
	#parseArgs() cn
	file = "output_be.tif"
	dataset = gdalOpen(file, GA_ReadOnly)
	pixel = dataset.GetGeoTransform()[1]
 	data = band_to_array(dataset, xi, yi, xf, yf)
	run_mpi_jobs(data)
#	newdata = run_mpi_jobs(data)
