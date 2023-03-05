import csv
import ast
from datetime import datetime
from Point import Point
import os

def tracerelated(filepath): 
    data = csv.reader(open(filepath))

    li = []
 
    c=0
    
    for line in data:
        
        if c>0: 
            dt = datetime.strptime(line[6], '%y/%m/%d %H:%M:%S')
            li.append(Point(float(line[1]),float(line[0]),dt, None,float(line[2])))

        
        c = c+1

    return li
    
def stoprelated(filepath): 
    data = csv.reader(open(filepath))

    li = []
 
    c=0
    
    for line in data:
        
        if c>0: 
            dt = datetime.strptime(line[5], '%y/%m/%d %H:%M:%S')
            li.append(Point(float(line[2]),float(line[3]),dt, line[8],float(line[9])))

        
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
            dt = datetime.strptime(line[2], '%y/%m/%d %H:%M:%S')
            li.append(Point(float(line[0]),float(line[1]),dt,line[4],float(idname[0])))

        
        c = c+1

    return li

def convertActivityLocation(ActvityLoactionList):
    convertedList = []
    for i in ActvityLoactionList:
        if i != None:
            activityList = []
            for j in i[1]: # The list with all nearby locations
                if j != None:
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

print(stoprelated("trace/stop/stops.csv"))
