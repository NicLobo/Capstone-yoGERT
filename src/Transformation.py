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
            li.append(Point(convert_to_floats(line[0:2])))
        
        c = c+1

    return li
    
def GenALInputT(filepath): 
    data = csv.reader(open(filepath))

    li = []
    lt = []
    c=0
    
    for line in data:
        
        if c>0: 
            li.append(Point(convert_to_floats(line[0:2]),line[2]))

        
        c = c+1

    return li,lt

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
            


    

# l = GenALInput('./episode.csv')
# l2,ltime = GenALInputT('./episode.csv')
# print(l)
# print(l2)
# print(ltime)
