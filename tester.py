import gdal
import numpy as np
from gdalconst import *
import matplotlib.pyplot as plt
import matplotlib as ml
import matplotlib.cm as cm
import time

dataset = gdal.Open("pitremoved.tif", GA_ReadOnly)
band = dataset.GetRasterBand(1)
geotransform = dataset.GetGeoTransform()
originX = geotransform[0]
originY = geotransform[3]
pixelWidth = geotransform[1]
pixelHeight = geotransform[5]
input_driver_name = dataset.GetDriver().ShortName
cols = dataset.RasterXSize
rows = dataset.RasterYSize
p = pixelWidth
data = band.ReadAsArray(0,0, cols, rows)
output_file_name = "single.tif"

def write_to_file(data, x_size, y_size, output_file_name, input_driver_name):
	tic = time.clock()
	driver = gdal.GetDriverByName(input_driver_name)	
	output_dataset = driver.Create(output_file_name, x_size, y_size, 5, gdal.GDT_Float32)
	for i in range(5):
		output_dataset.GetRasterBand(i+1).WriteArray(data[i])
	output_dataset = None

def check_diff():
	sin_dataset = gdal.Open("single.tif", GA_ReadOnly)
	mpi_dataset = gdal.Open("mpiResult3.tif", GA_ReadOnly)

	for i in range(5):
		sin_band = sin_dataset.GetRasterBand(i+1)
		sin_cols = sin_dataset.RasterXSize
		sin_rows = sin_dataset.RasterYSize
		sin_data = sin_band.ReadAsArray(0,0, sin_cols, sin_rows)
		
		mpi_band = mpi_dataset.GetRasterBand(i+1)
		mpi_cols = mpi_dataset.RasterXSize
		mpi_rows = mpi_dataset.RasterYSize
		mpi_data = sin_band.ReadAsArray(0,0, mpi_cols, mpi_rows)

		error = 0
		for i in range(1, mpi_rows - 1):
			for j in range(1, mpi_cols - 1):
				if (sin_data[i][j] != mpi_data[i][j]):
					print 'at ',i,j
					print sin_data[i][j], mpi_data[i][j]
					error = error + 1
		print error
#		print np.sum(sin_data.reshape(1,-1) - mpi_data.reshape(1,-1))

def isOutOfBound(x,y):
    if x !=0 and x != rows - 1 and y != 0 and y != cols - 1:
        return False
    else:
        return True
    
def getG(x,y):
    if(isOutOfBound(x,y)):
        return 0
    else:
        z3 = data[x+1, y-1]
        z6 = data[x+1, y]
        z9 = data[x+1, y+1]
        z1 = data[x-1, y-1]
        z4 = data[x-1, y]
        z7 = data[x-1, y+1]
        return (z3 + z6 + z9 - z1 - z4 - z7)/(6*p)
    
def getH(x,y):
    if (isOutOfBound(x,y)):
        return 0
    else:
        z3 = data[x+1, y-1]
        z6 = data[x+1, y]
        z9 = data[x+1, y+1]
        z1 = data[x-1, y-1]
        z4 = data[x-1, y]
        z7 = data[x-1, y+1]
        z2 = data[x, y-1]
        z8 = data[x, y+1]
        return(z1 + z2 + z3 - z7 - z8 -z9)/(6*p)
def getD(x,y):
    if(isOutOfBound(x,y)):
        return 0
    else:
        z3 = data[x+1, y-1]
        z6 = data[x+1, y]
        z9 = data[x+1, y+1]
        z1 = data[x-1, y-1]
        z4 = data[x-1, y]
        z7 = data[x-1, y+1]
        z2 = data[x, y-1]
        z5 = data[x,y]
        z8 = data[x, y+1]
        return (z1 + z3 + z4 - z6 - z7 - z9 - 2*(z2 + z5 + z8))/float(3*p**2)

def getE(x,y):
    if(isOutOfBound(x,y)):
        return 0
    else:
        z3 = data[x+1, y-1]
        z6 = data[x+1, y]
        z9 = data[x+1, y+1]
        z1 = data[x-1, y-1]
        z4 = data[x-1, y]
        z7 = data[x-1, y+1]
        z2 = data[x, y-1]
        z5 = data[x,y]
        z8 = data[x, y+1]
        return (z1 + z3 + z4 - z6 - z7 - z9 -2 * (z4 + z5 + z6))/float(3*p**2)
def getF(x,y):
    if (isOutOfBound(x,y)):
        return 0
    else:
        z3 = data[x+1, y-1]
        z6 = data[x+1, y]
        z9 = data[x+1, y+1]
        z1 = data[x-1, y-1]
        z4 = data[x-1, y]
        z7 = data[x-1, y+1]
        z2 = data[x, y-1]
        z5 = data[x,y]
        z8 = data[x, y+1]
        return (z3 + z7 -z1 -z9)/(4*p**2)

def plot(data):
    fig = plt.figure()
    plt.imshow(data)
    plt.colorbar(orientation='vertical')
    plt.show()


def main():
	G = H = D = E = F = np.zeros((rows, cols))
	allFive = np.zeros((5,rows,cols))
	for i in range(data.shape[0]):
		for j in range(data.shape[1]):
			G[i,j] = getG(i,j)
			H[i,j] = getH(i,j)
			D[i,j] = getD(i,j)
			E[i,j] = getE(i,j)	
			F[i,j] = getF(i,j)

	allFive[0] = G
	allFive[1] = H
	allFive[2] = D
	allFive[3] = E
	allFive[4] = F
	
	write_to_file(allFive, cols, rows, output_file_name, input_driver_name)

#main()
check_diff()
