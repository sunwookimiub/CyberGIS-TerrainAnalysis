import gdal
import logging
from gdalconst import *
import numpy as np
import math
import time
import sys

_MIN_ZERO_ONE = 1e-5
THRESHOLD = 1e-6
def calculate_operations(band, px, py,  y_offset, x_size, y_size):
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
    t0 = time.time()
    proc_data = band.ReadAsArray(0, y_offset, x_size, y_size)
    nodata = band.GetNoDataValue()
    min_value = np.min(proc_data)
    t1 = time.time()
    output_data = np.zeros((10, y_size-2, x_size-2))
    if nodata:
        nodata_ind = abs(proc_data - nodata)/abs(nodata)<THRESHOLD
        np.place(proc_data, nodata_ind, float('nan')) # Implementation of Terrain Gradients Evans-Young method
    output_data[0] = getG(proc_data, px) 
    output_data[1] = getH(proc_data, py)
    output_data[2] = getD(proc_data, px)
    output_data[3] =  getE(proc_data, py)
    output_data[4] = getF(proc_data, px, py)

    for i in range(5):
        np.place(output_data[i], abs(output_data[i]) < _MIN_ZERO_ONE, 0)
    G = output_data[0]
    H = output_data[1]
    D = output_data[2]
    E = output_data[3]
    F = output_data[4]
    # Implemented Morphometrkic Parameters
    GHF = np.multiply(F, np.multiply(G, H) )
    G2H2 = np.power(G, 2) + np.power(H, 2)
    output_data[5] = np.sqrt(G2H2)
    output_data[6] = np.arctan(H/G)
    output_data[7] = - (np.multiply(np.power(H, 2), D)  \
                            - 2*GHF + np.multiply(np.power(G, 2), E)) \
                            / np.power(G2H2, 1.5)
    output_data[8] = - (np.multiply(np.power(G, 2), D) + 2*GHF \
                            + np.multiply(np.power(H, 2), E)) \
                            / (np.multiply(G2H2, np.power(1+G2H2, 1.5)))
    output_data[9] = - (np.multiply(1+np.power(H, 2), D) - 2*GHF \
                            + np.multiply(np.power(G, 2), E)) / \
                            (2*np.power(1+G2H2, 1.5)) 
    for i in range(5, 10):
        np.place(output_data[i], np.isnan(output_data[i]), 0)
    # For nodata points in input data, change them back to nodata in output
    for i in range(1, 10):
        np.place(output_data[i], nodata_ind[1:-1, 1:-1], nodata)
    t2 = time.time()
    logging.debug("reading time %f", t1 - t0)
    logging.debug("process time %f", t2 - t1)
    return output_data

def getG(data, p):
    """Return G, first derivative in x direction"""
    bar  = get_block(data)
    return (bar[2]+bar[5]+bar[8]-bar[0]-bar[3]-bar[6]) / (6*p)

def getH(data, p):
    """Return H, first derivative in y direction"""
    bar = get_block(data)
    return (bar[0]+bar[1]+bar[2]-bar[6]-bar[7]-bar[8]) / (6*p)

def getD(data, p):
    """Return D, second derivative in x direction"""
    bar = get_block(data)
    return (bar[0]+bar[2]+bar[3]+bar[5]+bar[6]+bar[8] \
            - 2*(bar[1]+bar[4]+bar[7])) / (3*p*p)

def getE(data, p):
    """Return E, second derivative in y direction"""
    bar = get_block(data)
    return (bar[0]+bar[1]+bar[2]+bar[6]+bar[7]+bar[8] \
            - 2*(bar[4]+bar[5]+bar[6])) / (3*p*p)

def getF(data, px, py):
    """Return F, second derivative along diagonals"""
    bar = get_block(data)
    return (bar[2]+bar[6]-bar[0]-bar[8]) / (4*px*py)

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

def get_unit(str):
    pos = str.find("UNIT")
    if -1 == pos:
        print "invalid string"
        sys.exit()
    pos = str.find('"', pos)
    if -1 == pos:
        print "invalid string"
        sys.exit()
    pos2 = str.find('"', pos+1)
    unit = str[pos+1:pos2]
    return unit

def get_distance(lat1, lon1, lat2, lon2):
    R = 6371000
    theta1 = math.radians(lat1)
    theta2 = math.radians(lat2)
    delta = math.radians(lat2-lat1)
    lamda = math.radians(lon2-lon1)
    a = math.sin(delta/2) ** 2 + math.cos(theta1) * math.cos(theta2) *\
            math.sin(lamda/2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R*c
    return d

def get_pixel(projection, geotransform):
    cordx = geotransform[0]
    cordy = geotransform[3]
    xpixel = geotransform[1]
    ypixel = geotransform[5]
    unit = get_unit(projection)
    if unit == "degree":        #for lat/lon unit
        xunit = get_distance(cordy, cordx, cordy, cordx+xpixel)
        yunit = get_distance(cordy, cordx, cordy+ypixel, cordx)
        return xunit, yunit
    elif unit == "metre":       #for meter unit
        return abs(xpixel), abs(ypixel)
    elif unit == "feet" or unit == "Foot_US" or unit == "Degree":
        factor = 0.3048006096012192
        return factor*abs(xpixel), factor*abs(ypixel)
    else:
        print projection
        print unit
        print "Error: invalid unit for the input file"
        sys.exit(-1)
