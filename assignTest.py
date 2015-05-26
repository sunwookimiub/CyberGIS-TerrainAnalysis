import gdal
import numpy as np
from gdalconst import *
import matplotlib.pyplot as plt
import matplotlib as ml
import matplotlib.cm as cm
from mpi4py import MPI

def isOutOfBound(x, y, row_size, col_size):
    if x !=0 and x != row_size - 1 and y != 0 and y != col_size - 1:
        return False
    else:
        return True

def plot(data):
    fig = plt.figure()
    plt.imshow(data)
    plt.colorbar(orientation='vertical')
    plt.show()

def getG(bar, p):
	off = 1
	return( (bar[3-off]+bar[6-off]+bar[9-off] \
			- bar[1-off]-bar[4-off]-bar[7-off]) \
			/(6*p) )

#H: First Derivative in y direction
def getH(bar, p):
	off = 1
	return( (bar[1-off]+bar[2-off]+bar[3-off] \
			- bar[7-off]-bar[8-off]-bar[9-off] ) \
			/(6*p) )

#D: Second Derivative in x direction
def getD(bar, p):
	off = 1
	return( (bar[1-off]+bar[3-off]+bar[4-off] \
			- bar[6-off]-bar[7-off]-bar[9-off] \
			- 2*(bar[2-off]+bar[5-off]+bar[8-off]) ) \
			/(3*p*p) )

#E: Second Derivative in x direction
def getE(bar, p):
	off = 1
	return( (bar[1-off]+bar[2-off]+bar[3-off] \
			- bar[7-off]-bar[8-off]-bar[9-off] \
			- 2*(bar[4-off]+bar[5-off]+bar[6-off]) ) \
			/(3*p*p) )

#F: Second derivative along diagonals
def getF(bar, p):
	off = 1
	return( (bar[3-off]+bar[7-off] \
			- bar[1-off]-bar[9-off] ) \
			/(4*p*p) )

# Not necessary if outer bounds are excluded
def check_bounds(x,y,data):
	if( x-1<0 or y-1<0 or x+1> data.shape[0]-1 or y+1 > data.shape[1]-1 ):
		return False
	else:
		return True

def get_block(x,y,data):
	block_array = np.zeros(9)
	block_array[0] = data[x-1,y-1]
	block_array[1] = data[x  ,y-1]
	block_array[2] = data[x+1,y-1]
	block_array[3] = data[x-1,y  ]
	block_array[4] = data[x  ,y  ]
	block_array[5] = data[x+1,y  ]
	block_array[6] = data[x-1,y+1]
	block_array[7] = data[x  ,y+1]
	block_array[8] = data[x+1,y+1]
	return block_array


dataset = gdal.Open("output.tif", GA_ReadOnly)
band = dataset.GetRasterBand(1)
geotransform = dataset.GetGeoTransform()
originX = geotransform[0]
originY = geotransform[3]
pixelWidth = geotransform[1]
pixelHeight = geotransform[5]

cols = dataset.RasterXSize
rows = dataset.RasterYSize
p = pixelWidth
data = band.ReadAsArray(0,0, cols, rows)
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
process_cols = cols/size
process_rows = rows
process_start = process_cols*rank
if(rank == size - 1):
    x_offset = rank*process_cols - 1
    process_cols = cols - process_cols * (size - 1)    
    x_size = process_cols + 1
    y_size = process_rows
    process_data = band.ReadAsArray(x_offset, 0, x_size, y_size)
    # print np.sum(data[:, x_offset:].reshape(x_size * y_size) - process_data.reshape(x_size * y_size))
    G = np.zeros((process_rows, process_cols))
    for i in xrange(1,y_size-2):
        for j in xrange(1, x_size-2):
            bar = get_block(i,j,process_data)
            G[i,j] = getG(bar, p)
    plot(G)
    
elif(rank == 0):
    x_offset = 0
    x_size = process_cols + 1
    y_size = process_rows
    process_data = band.ReadAsArray(x_offset, 0, x_size, y_size)
    # print np.sum(data[:, 0:x_offset+x_size].reshape(x_size * y_size) - process_data.reshape(x_size * y_size)) 
    G = np.zeros((process_rows, process_cols))
    for i in xrange(1,y_size-2):
        for j in xrange(1, x_size-2):
            bar = get_block(i,j,process_data)
            G[i,j] = getG(bar, p)
    plot(G)
else:
    x_offset = rank*process_cols-1
    x_size = process_cols+2
    y_size = process_rows
    process_data = band.ReadAsArray(x_offset, 0, process_cols+2, y_size)
    # print np.sum(data[:, x_offset: x_offset + x_size].reshape(x_size * y_size) - process_data.reshape(x_size * y_size)) 
    G = np.zeros((process_rows, process_cols))
    for i in xrange(1,y_size-2):
        for j in xrange(1, x_size-2):
            bar = get_block(i,j,process_data)
            G[i,j] = getG(bar, p)
    plot(G)
