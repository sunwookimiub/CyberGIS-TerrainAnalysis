import gdal
from gdalconst import *
import numpy

filename = "output_be.tif"
dataset = gdal.Open(filename, GA_ReadOnly)

cols = dataset.RasterXSize
rows = dataset.RasterYSize
bands = dataset.RasterCount
driver = dataset.GetDriver().LongName

geotransform = dataset.GetGeoTransform()
originX = geotransform[0] # top left x
originY = geotransform[3] # top left y
pixelWidth = geotransform[1]
pixelHeight= geotransform[5]

band = dataset.GetRasterBand(1)
data = band.ReadAsArray(0,0,cols,rows).astype(numpy.float)
#rows = len(data) and cols = len(data[0])

# Bounds for x: 0 to rows - 1
# Bounds for y: 0 to cols - 1

#Helper Function for seeing if a point is valid:
#Function: To find out if a neighboring point on the grid is valid
#Parameters: x= x Coordinate, y= y Coordinate, n= the direction on the grid
def check(x,y,n):
	#Create boolean values checking the left,right,up,down validity of coordinates
	hasLeft = (x-1) > 0
	hasRight = (x+1) < (rows-1)
	hasUp = (y-1) > 0
	hasDown = (y+1) < (cols-1)

	#Check the bounds respective to the n value
	if n == 1:
		if (hasUp and hasLeft):
			return True
		else:
			return False
	elif n == 2:
		if (hasUp):
			return True
		else:
			return False
	elif n == 3:
		if (hasUp and hasRight):
			return True
		else:
			return False
	elif n == 4:
		if (hasLeft):
			return True
		else:
			return False
	elif n == 5:
		return True
	elif n == 6:
		if (hasRight):
			return True
		else:
			return False
	elif n == 7:
		if(hasDown and hasLeft):
			return True
		else:
			return False
	elif n == 8:
		if(hasDown):
			return True
		else:
			return False
	elif n == 9:
		if(hasDown and hasRight):
			return True
		else:
			return False
	else:
		return False

