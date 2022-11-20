"""! @brief Converts CSVs to point SHPs."""

"""@package src

This module will process an incoming travel episode CSVs 
with fields Latitude, Longitude, and Time
and convert them to point SHP files
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os
from os.path import join


def readDir(inputpath):
    files = os.listdir(inputpath)
    return files


def convertCSVtoSHP(filenames):
    curDir =  os.getcwd()
    targetPath = os.path.join(curDir, "/SHPfiles/")
    os.mkdir(targetPath)
    for csvfile in range(len(filenames)):
        data = pd.read_csv(csvfile)
        dataGDF = gpd.GeoDataFrame(data, geometry = gpd.points_from_xy(data['longitude'], data['latitude']))
        ESRI_WKT = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]]'
        shpfilename = 'travelepisode' + csvfile + ".shp"
        dataGDF.to_file(filename=shpfilename, driver = 'ESRI Shapefile', crs_wkt='ESRI_WKT')

    return targetPath

