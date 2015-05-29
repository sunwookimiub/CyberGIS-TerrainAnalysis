import gdal
from gdalconst import *
import numpy as np

def process_bands(band, p, x_offset, x_size, y_size):	
	proc_data = band.ReadAsArray(x_offset,0,x_size,y_size)
	output_data = np.zeros((10, y_size-2, x_size-2))
    output_data[0] = G =getG(proc_data, p)
	output_data[1] = H = getH(proc_data, p)
    output_data[2] = D = getD(proc_data, p)
	output_data[3] = E = getE(proc_data, p)
	output_data[4] = F = getF(proc_data, p)

	GHF = np.multiply(F, np.multiply(G, H) )

	G2H2 = np.power(G, 2) + np.power(H, 2)

	output_data[5] = np.sqrt(G2H2)

	output_data[6] = np.arctan(H/G)
        
	output_data[7] = - ( ( np.multiply(np.power(H,2),D)  \
    	                    	- 2 * GHF + np.multiply(np.power(G, 2), E) ) \
                             	/ np.power(G2H2, 1.5) )

	output_data[8] = - ( (np.multiply(np.power(G, 2), D) + 2 * GHF \
                              + np.multiply(np.power(H,2), E) ) \
                             / (np.multiply(G2H2, np.power(1+G2H2,1.5) ) ) )
        
	output_data[9]  = - ( (np.multiply(1 + np.power(H,2), D) - 2 * GHF \
                               + np.multiply(np.power(G,2), E) ) \
                              / (2 * np.power(1 + G2H2, 1.5) ) )
        
	return output_data

                

#G: First Derivative in x direction
def getG(data, p):
	off = 1
	bar  = get_block(data)
	return( (bar[3-off]+bar[6-off]+bar[9-off] \
			- bar[1-off]-bar[4-off]-bar[7-off]) \
			/(6*p) )

#H: First Derivative in y direction
def getH(data, p):
	off = 1
	bar = get_block(data)
	return( (bar[1-off]+bar[2-off]+bar[3-off] \
			- bar[7-off]-bar[8-off]-bar[9-off] ) \
			/(6*p) )

#D: Second Derivative in x direction
def getD(data, p):
	off = 1
	bar = get_block(data)
	return( (bar[1-off]+bar[3-off]+bar[4-off] \
			- bar[6-off]-bar[7-off]-bar[9-off] \
			- 2*(bar[2-off]+bar[5-off]+bar[8-off]) ) \
			/(3*p*p) )

#E: Second Derivative in x direction
def getE(data, p):
	off = 1
	bar = get_block(data)
	return( (bar[1-off]+bar[2-off]+bar[3-off] \
			- bar[7-off]-bar[8-off]-bar[9-off] \
			- 2*(bar[4-off]+bar[5-off]+bar[6-off]) ) \
			/(3*p*p) )

#F: Second derivative along diagonals
def getF(data, p):
	off = 1
	bar = get_block(data)
	return( (bar[3-off]+bar[7-off] \
			- bar[1-off]-bar[9-off] ) \
			/(4*p*p) )

# Not necessary if outer bounds are excluded
def check_bounds(x,y,data):
	if( x-1<0 or y-1<0 or x+1> data.shape[0]-1 or y+1 > data.shape[1]-1 ):
		return False
	else:
		return True

def get_block(data):
	#Need to be replaced with views
	block_array = np.zeros((9, data.shape[0]-2, data.shape[1]-2))
	block_array[0] = data[ :-2,  :-2]
	block_array[1] = data[ :-2, 1:-1]
	block_array[2] = data[ :-2, 2:  ]
	block_array[3] = data[1:-1,  :-2]
	block_array[4] = data[1:-1, 1:-1]
	block_array[5] = data[1:-1, 2:  ]
	block_array[6] = data[2:  ,  :-2]
	block_array[7] = data[2:  , 1:-1]
	block_array[8] = data[2:  , 2:  ]
	return block_array
