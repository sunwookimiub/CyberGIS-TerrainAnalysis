import gdal
from gdalconst import *
import numpy as np

def process_bands(band, p, x_offset, x_size, y_size):
    """Read and analysis elevation data.
    
    Keyword arguments:
    band     -- input data band
    p        -- pixel size
    x_offset -- starting point in x axis for partitioned data chunk
    x_size   -- number of column in partitioned data chunk
    y_size   -- number of row in partitioned data chunk
    Return:
    A 3 dimensional numpy array in following format:
    [G, H, D, E, F, SLOPE, ASPECT, PLANC, PROFC, MEANC]
    Exception:
    Ignoring divide by zero warning and set their value to NaN
    """
    # Set how RuntimeWarning: invalid value encountered in divide
    # error is handled. This error derives from division by Nan
    np.seterr(divide='ignore', invalid='ignore')
    # The assigned block of image data to be processed
    proc_data = band.ReadAsArray(x_offset,0,x_size,y_size)
    # Create a numpy array of offsetted size
    output_data = np.zeros((10, y_size-2, x_size-2))

    # Implementation of Terrain Gradients Evans-Young method
    # G first derivative in x direction
    output_data[0] = G =getG(proc_data, p)
    # H first derivative in y direction
    output_data[1] = H = getH(proc_data, p)
    # D second derivative in x direction
    output_data[2] = D = getD(proc_data, p)
    # E second derivative in y direction
    output_data[3] = E = getE(proc_data,p)
    # F second derivative along diagonals
    output_data[4] = F = getF(proc_data, p)

    # Implemented Morphometrkic Parameters
    # Commonly used variables
    # G*H*F
    GHF = np.multiply(F, np.multiply(G, H) )
    # G^2 + H^2
    G2H2 = np.power(G, 2) + np.power(H, 2)
    # Slope
    output_data[5] = np.sqrt(G2H2)
    # Aspect
    output_data[6] = np.arctan(H/G)
    # Planc
    output_data[7] = - ( ( np.multiply(np.power(H,2),D)  \
        - 2 * GHF + np.multiply(np.power(G, 2), E) ) / np.power(G2H2, 1.5) )
    # Profc
    output_data[8] = - ( (np.multiply(np.power(G, 2), D) + 2 * GHF \
        + np.multiply(np.power(H,2), E) ) \
        / (np.multiply(G2H2, np.power(1+G2H2,1.5) ) ) )
    # Meanc
    output_data[9] = - ( (np.multiply(1 + np.power(H,2), D) - 2 * GHF \
        + np.multiply(np.power(G,2), E) ) / (2 * np.power(1 + G2H2, 1.5) ) )

    return output_data

def getG(data, p):
    # Return G, first derivative in x direction
    bar  = get_block(data)
    return( (bar[2]+bar[5]+bar[8]-bar[0]-bar[3]-bar[6]) / (6*p) )

def getH(data, p):
    # Return H, first derivative in y direction
    bar = get_block(data)
    return( (bar[0]+bar[1]+bar[2]-bar[6]-bar[7]-bar[8] ) / (6*p) )

def getD(data, p):
    # Return D, second derivative in x direction.
    bar = get_block(data)
    return( (bar[0]+bar[2]+bar[3]-bar[5]-bar[6]-bar[8] \
                -2*(bar[1]+bar[4]+bar[7]) ) /(3*p*p) )

def getE(data, p):
    # Return E, second derivative in x direction.
    bar = get_block(data)
    return( (bar[0]+bar[1]+bar[2]-bar[6]-bar[7]-bar[8] \
            - 2*(bar[4]+bar[5]+bar[6]) ) / (3*p*p) )

def getF(data, p):
    # Return F, second derivative along diagonals.
    bar = get_block(data)
    return( (bar[2]+bar[6]-bar[0]-bar[8] ) / (4*p*p) )

def get_block(data):
    """return array with different slices to ease access to nearest neighbors

       Returns a 9 element array to make it easier to access nearest
       neighbors using slices without making copies of the data. The
       array element is organized in the following pattern:
          0 1 2
          3 4 5
          6 7 8

       The slices are smaller than the original data array because the
       boundary cells are excluded. This allows vector operations to work
       correctly.
    """
    return [
        data[ :-2,  :-2], data[ :-2, 1:-1], data[ :-2, 2:  ],
        data[1:-1,  :-2], data[1:-1, 1:-1], data[1:-1, 2:  ],
        data[2:  ,  :-2], data[2:  , 1:-1], data[2:  , 2:  ],
    ]
