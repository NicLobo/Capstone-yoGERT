import csv
import ast
from datetime import datetime
from Point import Point

def convert_to_floats(arr):
    result = map(float, arr)
    return list(result)

def GenALInput(filepath): 
    data = csv.reader(open(filepath))

    li = []
    c=0
    
    for line in data:
        
        if c>0:
            lp = convert_to_floats(line[2:4])
            li.append(Point(lp[0],lp[1]))
        
        c = c+1

    return li
    
def GenALInputT(filepath): 
    data = csv.reader(open(filepath))

    li = []
    lt = []
    c=0
    
    for line in data:
        
        if c>0: 
            lp = convert_to_floats(line[2:4])
            li.append(Point(lp[0],lp[1],line[6]))

        
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
