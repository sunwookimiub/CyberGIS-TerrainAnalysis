import gdal
from gdalconst import *
import numpy as np

def band_to_array(filename):
	dataset = gdal.Open(filename, GA_ReadOnly)
	cols = dataset.RasterXSize
	rows = dataset.RasterYSize
	geotransform = dataset.GetGeoTransform()
	pixel = geotransform[1] # this is width. check if height is different...
	band = dataset.GetRasterBand(1)
	data = band.ReadAsArray(0,0,cols,rows).astype(np.float)
	return data

# array_to_band
