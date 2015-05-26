import numpy as np

#G: First Derivative in x direction
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

def test(data):
	return data*2
