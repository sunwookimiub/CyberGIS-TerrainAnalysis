import sys

from osgeo import gdal
from gdalconst import *
import numpy as np
from pyspark.mllib.clustering import KMeans
from pyspark import SparkContext
from numpy import unravel_index

def tiff_to_array(dataset, weights=[1, 1, 1, 1, 1], cut=True, adjust=False):
    x_size = dataset.RasterXSize
    y_size = dataset.RasterYSize
    if cut: 
        x_size -= 2
        y_size -= 2
        x_offset = 1
        y_offset = 1

    bands = [6, 7, 8, 9, 10]
    if len(weights) != len(bands):
        print "weight vector size should be", len(band)
        sys.exit(-1)
    ret = np.zeros((x_size*y_size, len(bands)))
    
    means = np.zeros(len(bands))
    for i in range(len(bands)):
        band = dataset.GetRasterBand(bands[i])
        ret[:, i] = band.ReadAsArray(x_offset, y_offset, x_size, y_size).reshape(x_size*y_size)
        print "One read done"
        means[i] = abs(ret[:, i]).mean()

    if adjust:
        for i in range(len(bands)):
            weights[i] *= 1.0 / (ret[:, i].max()-ret[:, i].min())
    
    print "Means are:", means
    print "Weights are: ", weights
    for i in range(len(bands)):
        ret[:, i] *= weights[i]

    ret=np.nan_to_num(ret)
    return x_size, y_size, ret

def predict(model, data, x, y):
    ret = np.zeros((len(data), 1))
    for i in range(len(data)):
        ret[i] = model.predict(data[i])
    ret = ret.reshape(x, y)
    return ret

def write_to_tif(output_file_name, x_size, y_size, data, input_driver_name):
    print input_driver_name
    driver = gdal.GetDriverByName(input_driver_name)
    print driver
    output_dataset = driver.Create(output_file_name, x_size,
            y_size, 1, gdal.GDT_Float32)
    data = data.reshape(y_size, x_size)
    print data.shape
    print x_size, y_size
    output_dataset.GetRasterBand(1).WriteArray(data)

weights = [10, 0.02, 50, 50, 50]

def main():
    sc = SparkContext()
    filename = sys.argv[1]
    clusters=int(sys.argv[2])
    outmodelname = sys.argv[3]
    dataset = gdal.Open(filename, GA_ReadOnly)
    driver = dataset.GetDriver().ShortName
    x, y, data = tiff_to_array(dataset, weights)
    print "after change to array"
    clusterdata = sc.parallelize(data)
    print "parallelize done"
    kmeanmodel = KMeans.train(clusterdata, clusters, maxIterations=50, runs=10)
    kmeanmodel.save(sc, outmodelname)
    print kmeanmodel.clusterCenters

if __name__ == '__main__':
    main()
