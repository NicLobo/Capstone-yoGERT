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

#trace file path
def tracerelated(tracepath): 
    data = csv.reader(open(tracepath))

    li = []
 
    c=0
    
    for line in data:
        
        if c>0: 
            dt = datetime.strptime(line[2], '%Y-%m-%d %H:%M:%S.%f')
            li.append(Point(float(line[0]),float(line[1]),dt, None,float(line[3])))

        
        c = c+1

    return li

#stop file path
def stoprelated(stopfilepath): 
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

#episode path
def episoderelated(episodepath): 
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

def convertActivityLocation(ActvityLoactionList):
    convertedList = []
    for i in ActvityLoactionList:
        if i is not None:
            activityList = []
            for j in i[1]: # The list with all nearby locations
                activityList.append([j.name, float(j.lat), float(j.lon), j.amenity])
            # Append to final list
            convertedList.append([i[0].lat, i[0].lon, activityList])
    return convertedList

# Convert CSV file(i.e. fetchOutput.csv) into a list of activity location objects
def convertActivityCSV(userFile):
    convertedList = []
    with open(userFile, 'r') as inputFile:
        fileReader = csv.reader(inputFile)
        next(fileReader) # Skip Header
        for row in fileReader:
            nearbyList = ast.literal_eval(row[2])
            for activiyList in nearbyList:
                convertedList.append(convertListToActivityLocationObject(activiyList))
    return convertedList

def convertListToActivityLocationObject(activityLocationList):
    newActivityLocation = ActivityLocation.ActivityLocation(activityLocationList[0],float(activityLocationList[1]),float(activityLocationList[2]), activityLocationList[3])
    return newActivityLocation


#Summary mode which takes in filepath and gives mode string
def summaryModeTrace(tracefilepath):
    summarymodefilepath = os.path.dirname(tracefilepath)+'/summarymode.csv'
    c=0
    data = csv.reader(open(summarymodefilepath))
    li=""
    for line in data:
        
        if c>0: 
            
            li += line[0]

        
        c = c+1

    return li
