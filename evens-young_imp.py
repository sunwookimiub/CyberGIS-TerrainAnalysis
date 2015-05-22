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

#-----------Terrain Gradients Evens-Young Method---------------

def isOutOfBounds(x,y,rows,cols):
	if( (x-1 < 0) or (x+1 > rows-1) or (y-1 < 0) or (y+1 > cols-1)):
		return True
	else:
		return False

def Z(x,y,n):
	if n == 1:
		return data[x-1,y-1]
	elif n == 2:
		return data[x,y-1]
	elif n == 3:
		return data[x+1,y-1]
	elif n == 4:
		return data[x-1,y]
	elif n == 5:
		return data[x,y]
	elif n == 6:
		return data[x+1,y]
	elif n == 7:
		return data[x-1, y+1]
	elif n == 8:
		return data[x, y+1]
	elif n == 9:
		return data[x+1,y+1]

#G: First Derivative in x direction
def G(x,y,p):
		return ( Z(x,y,3) + Z(x,y,6) + Z(x,y,9) - Z(x,y,1) - Z(x,y,4) - Z(x,y,7)) / (6 * p)

#H: First Derivative in y direction
def H(x,y,p):	
		return ( Z(x,y,1) + Z(x,y,2) + Z(x,y,3) - Z(x,y,7) - Z(x,y,8) - Z(x,y,9)) / (6 * p)

#D: Second Derivative in x direction
def D(x,y,p):
	return ( Z(x,y,1) + Z(x,y,3) + Z(x,y,4) - Z(x,y,6) - Z(x,y,7) - Z(x,y,9) - 2*(Z(x,y,2) + Z(x,y,5) + Z(x,y,8)) ) / (3 * p*p) 

#E: Second Derivative in y direction
def E(x,y,p):
	return ( Z(x,y,1) + Z(x,y,2) + Z(x,y,3) - Z(x,y,7) - Z(x,y,8) - Z(x,y,9) - 2*(Z(x,y,4) + Z(x,y,5) + Z(x,y,6)) ) / (3 * p*p)

#F: Second derivative along diagonals
def F(x,y,p):
	return ( Z(x,y,3) + Z(x,y,7) - Z(x,y,1) - Z(x,y,9) ) / (4 * p*p)
	
def main():
	p = pixelWidth
	for i in range(cols):
		for j in range(rows):
			if (not isOutOfBounds(i,j,rows,cols)):
				D(i,j,p) # Do stuff			
				#Currently testing the validity of the functions

main()
