
## @file Transformation.py
#  @title Transformation module
#  @author Niyatha Rangarajan
#  @date Mar 14, 2023


#imports
import csv
import ast
from datetime import datetime
from Point import Point
import os
import pandas
from csv import writer
import statistics
from statistics import mode
import glob
import pandas as pd  
import ActivityLocation

## @brief A class representing a file exception
#  @details Will be used as a file exception class for all functions in Tranformation.py
class FilePathException(Exception):
    "File path passed is not the correct path"
    pass

## @brief A class representing a list exception
#  @details Will be used as a list exception class for all functions in Tranformation.py
class WrongList(Exception):
    "List passed is incorrect"
    pass



## @brief This function to convert the given csv to a list of Point objects.
#  @param tracepath, The file path to the trace file
#  @return List of Point objects representing the given trace
def tracerelated(tracepath): 
    try:
        data = csv.reader(open(tracepath))

        li = []
    
        c=0
        
        for line in data:
            
            if c>0: 
                dt = datetime.strptime(line[2], '%Y-%m-%d %H:%M:%S.%f')
                li.append(Point(float(line[0]),float(line[1]),dt, None,float(line[3])))

            
            c = c+1

        return li
    except:
        print("File path passed is not the correct path")
        raise FilePathException from None

## @brief This function to convert the given csv to a list of Point objects.
#  @param stopfilepath, The file path to the stop file
#  @return List of Point objects representing the given stop csv
def stoprelated(stopfilepath): 
    try:
        data = csv.reader(open(stopfilepath))

        li = []
    
        c=0
        
        for line in data:
            
            if c>0: 
                dt = datetime.strptime(line[4], '%Y-%m-%d %H:%M:%S.%f')
                tracepath = os.path.dirname(os.path.dirname(stopfilepath))
                coord = pandas.read_csv(tracepath+'/trace.csv')
                print(float(line[9]))
                lat = float(coord.iloc[int(float(line[9])):int(float(line[9]))+1,0])
                long = float(coord.iloc[int(float(line[9])):int(float(line[9]))+1,1])
                print(lat,long)
                li.append(Point(lat,long,dt, line[8],float(line[9])))

            
            c = c+1

        return li
    except:
        print("File path passed is not the correct path")
        raise FilePathException from None

## @brief This function to convert the given csv to a list of Point objects.
#  @param episodepath, The file path to the episode file
#  @return List of Point objects representing the given episode
def episoderelated(episodepath): 
    try:
        data = csv.reader(open(episodepath))

        li = []
        filename = os.path.basename(episodepath)
        idname = os.path.splitext(filename)[0]

        c=0
        
        for line in data:
            
            if c>0:
                dt = datetime.strptime(line[2], '%Y-%m-%d %H:%M:%S.%f')
                li.append(Point(float(line[0]),float(line[1]),dt,line[4],float(idname[0])))

            
            c = c+1

        return li
    except:
        print("File path passed is not the correct path")
        raise FilePathException from None


## @brief Converts a list of stop point and activity location objects tuples into a list with their class attributes
#  @param ActvityLoactionList, a list of stop point and activity location objects tuples of 
# form [(Point stop, [activitylocation object1,activitylocation object2]), (Point stop2, [activitylocation object1,activitylocation object2])]
#  @return a list of stop point lat, stop point long and activity location objects attributes in tuple form
# of form [(stop.lat, stop.lon, [[activitylocation.name,activitylocation.lat,activitylocation.lon,activitylocation.amenity],
# [activitylocation2.name,activitylocation2.lat,activitylocation2.lon,activitylocation2.amenity]])....]
def convertActivityLocation(ActvityLoactionList):
    if(len(ActvityLoactionList) == 0):
        
        print("List is not correct")
        raise WrongList from None
    
    if(len(ActvityLoactionList[0]) != 2):
        print("List is not correct")
        raise WrongList from None
    
    convertedList = []
    for i in ActvityLoactionList:
        if i is not None:
            activityList = []
            for j in i[1]: # The list with all nearby locations
                activityList.append([j.name, float(j.lat), float(j.lon), j.amenity])
            # Append to final list
            convertedList.append([i[0].lat, i[0].lon, activityList])
    return convertedList

## @brief Converts a csv file into a list of activity location objects
#  @param userFile, output file of fetchactivitylocation
#  @return list of activity location objects
def convertActivityCSV(userFile):
    try:
        convertedList = []
        with open(userFile, 'r') as inputFile:
            fileReader = csv.reader(inputFile)
            next(fileReader) # Skip Header
            for row in fileReader:
                nearbyList = ast.literal_eval(row[2])
                for activiyList in nearbyList:
                    convertedList.append(convertListToActivityLocationObject(activiyList))
        return convertedList
    except:
        print("File path passed is not the correct path")
        raise FilePathException from None

## @brief Converts a list of activity location attributes into an activity location object
#  @param activityLocationList, an activity location attribute list of form [activitylocation.name,
# activitylocation.lat,activitylocation.lon,activitylocation.amenity] 
#  @return an activity location object
def convertListToActivityLocationObject(activityLocationList):
    if(len(activityLocationList) == 0):
        print("List is not correct")
        raise WrongList from None
    
    if(len(activityLocationList) != 4):
        print("List is not correct")
        raise WrongList from None
    newActivityLocation = ActivityLocation.ActivityLocation(activityLocationList[0],float(activityLocationList[1]),float(activityLocationList[2]), activityLocationList[3])
    return newActivityLocation


## @brief Gives the most used mode for a given trace file
#  @param tracefilepath, File path to the trace file
#  @return string value of most frequently used mode

def summaryModeTrace(tracefilepath):
    try:
        summarymodefilepath = os.path.dirname(tracefilepath)+'/summarymode.csv'
        c=0
        data = csv.reader(open(summarymodefilepath))
        li=""
        for line in data:
            
            if c>0: 
                
                li += line[0]

            
            c = c+1

        return li
    except:
        print("File path passed is not the correct path")
        raise FilePathException from None

