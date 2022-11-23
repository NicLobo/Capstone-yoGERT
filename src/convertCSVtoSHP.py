"""! @brief Converts CSVs to point SHPs."""

"""@package src

This module will process incoming travel episode CSVs 
with fields Latitude, Longitude, and Time
and convert them to point SHP files
"""

import pandas as pd
import geopandas as gpd
import os
from os.path import join


#This function receives a directory and returns an array of all files
#within the directory, full file paths
def readDir(inputpath):
    return [os.path.join(inputpath, file) for file in os.listdir(inputpath)]


#The function receives an array of csv epsiode files and 
#returns a directory filled with the corresponding point shapefiles 
def convertCSVtoSHP(filenames):
    targetPath = os.path.join("../", "SHPfiles/")
    os.mkdir(targetPath)
    print("Here is the list of tiles in the directory: ", filenames)
    print("Print the targetpath: ", targetPath)
    os.chdir(targetPath)
    for csvfile in range(len(filenames)):
        data = pd.read_csv(filenames[csvfile])
        dataGDF = gpd.GeoDataFrame(data, geometry = gpd.points_from_xy(data['Longitude'], data['Latitude']))
        print("We have gotten to this point")
        ESRI_WKT = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]]'
        shpfilename = 'travelepisode' + str(csvfile) + ".shp"
        dataGDF.to_file(filename=shpfilename, driver = 'ESRI Shapefile', crs=ESRI_WKT)
    return targetPath


