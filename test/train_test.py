import sys

from osgeo import gdal
from gdalconst import *
import numpy as np
from pyspark.mllib.clustering import KMeans, KMeansModel
from pyspark import SparkContext

import train

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

def main():
    modelname = sys.argv[1]
    tiffname = sys.argv[2]
    outputname = sys.argv[3]
    sc = SparkContext()
    model = KMeansModel.load(sc, modelname)
    dataset = gdal.Open(tiffname, GA_ReadOnly)
    x, y, data = train.tiff_to_array(dataset, train.weights)
    driver = dataset.GetDriver().ShortName
    clusterdata = sc.parallelize(data)
    result = np.array(clusterdata.map(lambda point: model.predict(point)).collect())
    write_to_tif(outputname, x, y, result, driver)


if __name__=="__main__":
    main()
