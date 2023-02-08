import ast
import csv
import os
import osmnx

import Mapping
import fetchActivityLocations
import Transformation
import GenerateRoute
import episodeGeneration

import tkinter
from tkinter import filedialog
tkinter.Tk().withdraw()

def generateEpisode(userFile):
    episodeGeneration.createSegments(userFile, "trace")
    print("Complete.")

def findActivityLocations(userFile):
    #First, do input processing.

    listStops = []
    with open(userFile,'r') as inputFile:
        fileReader = csv.reader(inputFile)
        # Skip Header
        next(fileReader)
        # Import list of stops
        for row in fileReader:
            stop = (float(row[0]),float(row[1]))
            listStops.append(stop)
    
    #Call fetchActivityLocations
    result = fetchActivityLocations.fetchStopAL(listStops)
    convertedResult = Transformation.convertActivityLocation(result) # convert to nested list
    
    # Write Result to a csv file.
    dirName = os.path.dirname(os.path.abspath(__file__))
    outFile = os.path.join(dirName, 'fetchOutput.csv')
    with open(outFile, 'w', newline='') as outputFile:
        fileWriter = csv.writer(outputFile)
        # Creater Header
        fileWriter.writerow(['Latitude', 'Longitude', 'Nearby Activity Locations'])

        # Write each rows
        for i in convertedResult:
            fileWriter.writerow([i[0],i[1],i[2]])

    print("Complete. The path of the generated file is: \n" + dirName)

    return convertedResult

def generateShortestPath(userFile, motion, optimizer):
    #File Preprocessing

    inputPoints = []
    with open(userFile,'r') as inputFile:
        fileReader = csv.reader(inputFile)
        # Skip Header
        next(fileReader)
        # Import points
        for row in fileReader:
            point = (float(row[0]),float(row[1]))
            inputPoints.append(point)

    # Generate NetworkGraph
    networkGraph = GenerateRoute.GenerateGraph(inputPoints, motion)
    # Generate ShortestPath
    shortestRoute = GenerateRoute.GenerateShortestPath(networkGraph, inputPoints, optimizer)
    
    print("Complete, now you can do the mapping.")
    return networkGraph, shortestRoute

def generateAlternativePath(userFile, optimizer):
    #File Preprocessing

    inputPoints = []
    with open(userFile,'r') as inputFile:
        fileReader = csv.reader(inputFile)
        next(fileReader)
        # Import points
        for row in fileReader:
            point = (float(row[0]),float(row[1]))
            inputPoints.append(point)
    
    # Generate Graph
    alternativeRoute = GenerateRoute.AlternativeRoute(inputPoints, optimizer)
    print("Complete, now you can put the points on the map.")
    return alternativeRoute


def mapEpisodes(userFile):
    listStops = []
    listTime = []
    listMode = []
    
    with open(userFile, 'r') as inputFile:
        fileReader = csv.reader(inputFile)
        # Skip Header
        next(fileReader)
        # Import data
        for row in fileReader:
            listStops.append((float(row[0]),float(row[1])))
            listTime.append(row[4])
            listMode.append(row[6])
        
        # Deal with the last point
        listStops.append((float(row[0]),float(row[1])))
        listTime.append(row[4])
        listMode.append(row[6])


    # Generate Graph 
    dirName = os.path.dirname(os.path.abspath(__file__))
    outFile = os.path.join(dirName, 'episode_path.html')
    Mapping.MapEpisodePoints(listStops,listTime,listMode,outFile)

    print("Complete.\n The name of the file is episode_path.html.\n The path of the generated file is: \n" + dirName)    

def mapActivityLocations(userList):
    listStops = []
    listActivities = []
    listActDescription = [] #List of activity location description

    for i in userList:
        listStops.append((i[0],i[1]))
        for j in i[2]:
            listActivities.append((j[1],j[2]))
            listActDescription.append(j[0])

    # Generate Map
    dirName = os.path.dirname(os.path.abspath(__file__))
    outFile = os.path.join(dirName, 'activity_location.html')
    Mapping.MapActivityLocation(listActivities,listActDescription,listStops,outFile)
    print("Complete. The name of the file is activity_location.html.\n The path of the generated file is: \n" + dirName)


def mapSRoute(userNetworkGraph,userMotion, userRoute):
    dirName = os.path.dirname(os.path.abspath(__file__))
    outFile = os.path.join(dirName, 'shortest_path.html')

    # Mapping
    Mapping.MapRoute(userNetworkGraph.graph,userMotion, userRoute.routes, outFile)
    print("Complete.\n The name of the file is shortest_path.html.\n The path of the generated file is: \n" + dirName)

def mapARoute(userMotion, userRoute):
    dirName = os.path.dirname(os.path.abspath(__file__))
    outFile = os.path.join(dirName, 'alternative_path.html')

    # Mapping
    Mapping.MapRoute(userRoute.network.graph, userMotion, userRoute.path.routes, outFile)
    print("Complete.\n The name of the file is alternative_path.html.\n The path of the generated file is: \n" + dirName)


# Driver code
if __name__ == '__main__':
    print("Please select the csv file you want to process: ")
    inputFile = filedialog.askopenfilename()

    # Should keep
    ActivityList = []


    while True:
        moduleSelect = int(input("Please select the module you want to go over: "))
        if(moduleSelect == 2): # Generate Episodes
            generateEpisode(inputFile)
        elif(moduleSelect == 3): # Find Activity Locations
            ActivityList = findActivityLocations(inputFile)
        elif(moduleSelect == 5): # Generate Shortest Path
            inputMotion = input("Please insert the motion of the episode: ")
            inputOptimizer = input("Please type in the optimizer[time/length]: ")
            shortestNetworkGraph, shortestRoute =  generateShortestPath(inputFile, inputMotion, inputOptimizer)
        elif(moduleSelect == 6): # Generate Alternative Path
            inputOptimizer = input("Please type in the optimizer[time/length]: ")
            alternativeRoute = generateAlternativePath(inputFile, inputOptimizer)
        elif(moduleSelect == 7): # Mapping Episodes
            mapEpisodes(inputFile)
        elif(moduleSelect == 8): # Mapping Activity Locations
            if (len(ActivityList) != 0):
                print("Dected pre-stored data in the system. Displaying the data: ")
                print(ActivityList)
                choice = input("Do you want to use this data to continue?[y/n]: ")
                if (choice == 'y'):
                    mapActivityLocations(ActivityList)
                else:
                    print("Please select the csv to continue: ")
                    inputFile = filedialog.askopenfilename()
                    ActivityList = Transformation.convertActivityCSV(inputFile)
                    mapActivityLocations(ActivityList)
            else:
                print("No pre-stored data detected.\n Please select the csv file to continue: ")
                inputFile = filedialog.askopenfilename()
                ActivityList = Transformation.convertActivityCSV(inputFile)
                mapActivityLocations(ActivityList)
            # print("Please select the csv file you want to process: ")
            # inputFile = filedialog.askopenfilename()
            # mapActivityLocations(inputFile)
        elif(moduleSelect == 9): # Mapping Shortest Route
            sRouteMotion = input("Please insert the motion of the episode: ")
            mapSRoute(shortestNetworkGraph, sRouteMotion, shortestRoute)
        elif (moduleSelect == 10): # Mapping Alternative Route
            inputMotion = input("Please insert the mode of the points: ")
            mapARoute(inputMotion, alternativeRoute)
        elif (moduleSelect == 0):
            print("Thank you for using the system.")
            break
        else:
            print("Error. You choose the wrong number.")
            continue
