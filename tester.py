import gdal
import numpy as np
from gdalconst import *
import matplotlib.pyplot as plt
import matplotlib as ml
import matplotlib.cm as cm
from mpi4py import MPI
import time
import osr


#Global Variables ---------------------------
file = "pitremoved.tif"
dataset = gdal.Open(file, GA_ReadOnly)
band = dataset.GetRasterBand(1)
geotransform = dataset.GetGeoTransform()
p = geotransform[1]
cols = dataset.RasterXSize
rows = dataset.RasterYSize
data = band.ReadAsArray(0,0,cols,rows)
G=H=D=E=F=np.zeros((rows,cols))
output_data = np.zeros((9,rows,cols))
np.seterr(divide='ignore', invalid='ignore')
#---------------------------------------------

def read_and_plot(file_name):
        dataset_check = gdal.Open(file_name, GA_ReadOnly)
        band_check = dataset_check.GetRasterBand(1)    
        cols_check = dataset_check.RasterXSize
        rows_check = dataset_check.RasterYSize
        data_check = band_check.ReadAsArray(0,0, cols_check, rows_check)
        fig = plt.figure()
        plt.imshow(data_check)
        plt.colorbar(orientation='vertical')
        plt.show()

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
def getG(x,y,p):
		return ( Z(x,y,3) + Z(x,y,6) + Z(x,y,9) - Z(x,y,1) - Z(x,y,4) - Z(x,y,7)) / (6 * p)

#H: First Derivative in y direction
def getH(x,y,p):	
		return ( Z(x,y,1) + Z(x,y,2) + Z(x,y,3) - Z(x,y,7) - Z(x,y,8) - Z(x,y,9)) / (6 * p)

#D: Second Derivative in x direction
def getD(x,y,p):
	return ( Z(x,y,1) + Z(x,y,3) + Z(x,y,4) - Z(x,y,6) - Z(x,y,7) - Z(x,y,9) - 2*(Z(x,y,2) + Z(x,y,5) + Z(x,y,8)) ) / (3 * p*p) 

#E: Second Derivative in y direction
def getE(x,y,p):
	return ( Z(x,y,1) + Z(x,y,2) + Z(x,y,3) - Z(x,y,7) - Z(x,y,8) - Z(x,y,9) - 2*(Z(x,y,4) + Z(x,y,5) + Z(x,y,6)) ) / (3 * p*p)

#F: Second derivative along diagonals
def getF(x,y,p):
	return ( Z(x,y,3) + Z(x,y,7) - Z(x,y,1) - Z(x,y,9) ) / (4 * p*p)

def getTif():
	#print "cols=",cols
	#print "rows=",rows
	#print "data.shape[0]",data.shape[0]
	#print "data.shape[1]",data.shape[1]
	#print "G.shape[0]",G.shape[0]
	#print "G.shape[1]",G.shape[1]
	#print "output_data[0].shape[0]",output_data[0].shape[0]
	#print "output_data[0].shape[1]",output_data[0].shape[1]	
	for i in range(data.shape[0]):
		for j in range(data.shape[1]):
			if (not isOutOfBounds(i,j,rows,cols)):
				G[i,j] = getG(i,j,p)
				H[i,j] = getH(i,j,p)
				D[i,j] = getD(i,j,p)
				E[i,j] = getE(i,j,p)
				F[i,j] = getF(i,j,p)
	output_data[0] = G
	output_data[1] = H
	output_data[2] = D
	output_data[3] = E
	output_data[4] = F

	GHF = np.multiply(F, np.multiply(G, H) )
	G2H2 = np.power(G, 2) + np.power(H, 2)
	output_data[5] = np.sqrt(G2H2)
	output_data[6] = np.arctan(H/G)
	output_data[7] = - ( ( np.multiply(np.power(H,2),D) \
	- 2 * GHF + np.multiply(np.power(G, 2), E) ) \
	/ np.power(G2H2, 1.5) )
	output_data[8] = - ( (np.multiply(np.power(G, 2), D) + 2 * GHF \
	+ np.multiply(np.power(H,2), E) ) \
	/ (np.multiply(G2H2, np.power(1+G2H2,1.5) ) ) )
	output_data[9] = - ( (np.multiply(1 + np.power(H,2), D) - 2 * GHF \
	+ np.multiply(np.power(G,2), E) ) \
	/ (2 * np.power(1 + G2H2, 1.5) ) )
	input_driver_name = dataset.GetDriver().ShortName
	driver = gdal.GetDriverByName(input_driver_name)
	outputDS=driver.Create("singleResult.tif",cols,rows,5,gdal.GDT_Float32)
		
	for i in range(output_data.shape[0]):
		outputDS.GetRasterBand(i+1).WriteArray(data[i],1,1)
	outputDS = None

def checkdiff(sinv, mpiv):
	sinds = gdal.Open(sinv, GA_ReadOnly)
	sinband=sinds.GetRasterBand(1)
	sincols = sinds.RasterXSize
	sinrows = sinds.RasterYSize
	sindata = sinband.ReadAsArray(0,0,cols,rows)
	
	mpids = gdal.Open(sinv, GA_ReadOnly)
	mpiband=mpids.GetRasterBand(1)
	mpicols = mpids.RasterXSize
	mpirows = mpids.RasterYSize
	mpidata = mpiband.ReadAsArray(0,0,cols,rows)

	#print np.sum(mpidata.reshape(1,-1) - sindata.reshape(1,-1))

#Global Variables ---------------------------
file = "pitremoved.tif"
dataset = gdal.Open(file, GA_ReadOnly)
band = dataset.GetRasterBand(1)
geotransform = dataset.GetGeoTransform()
p = geotransform[1]
cols = dataset.RasterXSize
rows = dataset.RasterYSize
data = band.ReadAsArray(0,0,cols,rows)
G=H=D=E=F=np.zeros((rows,cols))
output_data = np.zeros((9,rows,cols))
np.seterr(divide='ignore', invalid='ignore')
#---------------------------------------------

def read_and_plot(file_name):
        dataset_check = gdal.Open(file_name, GA_ReadOnly)
        band_check = dataset_check.GetRasterBand(1)    
        cols_check = dataset_check.RasterXSize
        rows_check = dataset_check.RasterYSize
        data_check = band_check.ReadAsArray(0,0, cols_check, rows_check)
if __name__ == "__main__":
	checkdiff("singleResult.tif","mpiResult.tif")
