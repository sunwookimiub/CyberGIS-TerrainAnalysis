from mpi4py import MPI

import gdal
from gdalconst import *
import numpy as np

FILENAME = "output_be.tif"
BLOCKSIZE= 5

# register all of the GDAL drivers
gdal.AllRegister()

# open the image
dataset = gdal.Open(FILENAME, GA_ReadOnly)
if dataset is None:
	print 'Could not open', FILENAME
	sys.exit(1)

# get image size
cols = dataset.RasterXSize
rows = dataset.RasterYSize
band = dataset.GetRasterBand(1)

count = 0
rows = 13
cols = 11
# loop through the rows
for i in range(0, rows, BLOCKSIZE):
	if i + BLOCKSIZE < rows:
		ySize = BLOCKSIZE
	else:
		ySize = rows - i
	
	# loop through the columns
	for j in range(0, cols, BLOCKSIZE):
		if j + BLOCKSIZE < cols:
			xSize = BLOCKSIZE
		else:
			xSize = cols - j
		
		# read the data and do the calculations
		data = band.ReadAsArray(j, i, xSize, ySize).astype(np.float)
		# some calculation
		count = count + 1
