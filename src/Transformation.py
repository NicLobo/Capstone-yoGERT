import csv
import ast
from datetime import datetime
from Point import Point
import os
import pandas

def tracerelated(filepath): 
    data = csv.reader(open(filepath))

    li = []
 
    c=0
    
    for line in data:
        
        if c>0: 
            dt = datetime.strptime(line[2], '%Y-%m-%d %H:%M:%S.%f')
            li.append(Point(float(line[0]),float(line[1]),dt, None,float(line[3])))

        
        c = c+1

    return li
    
def stoprelated(filepath1,filepath2): 
    data = csv.reader(open(filepath1))

    li = []
 
    c=0
    
    for line in data:
        
        if c>0: 
            dt = datetime.strptime(line[4], '%Y-%m-%d %H:%M:%S.%f')
            coord = pandas.read_csv(filepath2)
            lat = float(coord.iloc[float(line[9]),0])
            long = float(coord.iloc[float(line[9]),1])
            li.append(Point(lat,long,dt, line[8],float(line[9])))

        
        c = c+1

    return li

def episoderelated(filepath): 
    data = csv.reader(open(filepath))

    li = []
    filename = os.path.basename(filepath)
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
        activityList = []
        for j in i[1]: # The list with all nearby locations
            activityList.append([j.name, float(j.lat), float(j.lon)])
        # Append to final list
        convertedList.append([i[0].lat, i[0].lon, activityList])
    return convertedList

# Convert CSV file(i.e. fetchOutput.csv) into a nested list for mapping
def convertActivityCSV(userFile):
    convertedList = []
    with open(userFile, 'r') as inputFile:
        fileReader = csv.reader(inputFile)
        next(fileReader) # Skip Header
        for row in fileReader:
            nearbyList = ast.literal_eval(row[2])
            convertedList.append([float(row[0]),float(row[1]),nearbyList])
    #print(convertedList)
    return convertedList
            
def summarymode(filepath):
    data = csv.reader(open(filepath))
    li = ""
    for line in data:
        
        if c>0: 
            li+=str(line[0])

        
        c = c+1

    return li

#episoderelated('./trace/episode/0_episode.csv')
