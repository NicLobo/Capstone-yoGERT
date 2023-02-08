import ast
import csv
import os
import osmnx

import PreProcessing
import Mapping
import fetchActivityLocations
import Transformation
import GenerateRoute
import episodeGeneration

import tkinter
from tkinter import filedialog
tkinter.Tk().withdraw()

def generateEpisode(userFile):
    # if (PreProcessing.ValidateCSV(userFile)):
    #     print("File Checking OK:)")
    #     print("-------------------------------------------------------")
    #     episodeGeneration.createSegments(userFile, "trace")
    episodeGeneration.createSegments(userFile, "trace")
    
    print("Complete. You can generate information using other modules.")

def findActivityLocations(traceNum):
    listActivities = []

    dirName = os.path.dirname(os.path.abspath(__file__))
    tracePath = os.path.join(dirName, 'trace')
    os.makedirs('activityLists', exist_ok=True)
    outputPath = os.path.join(dirName,'activityLists')


    for i in range(traceNum):
        # Notify User
        print("Tracking: trace-" + str(i))

        stopEpiDir = tracePath+"/trace-"+str(i)
        stopEpiPath = os.path.join(stopEpiDir, 'stop_episode.csv')


        # Read stops
        listStops = []
        with open(stopEpiPath,'r') as inputFile:
            fileReader = csv.reader(inputFile)
            # Skip Header
            next(fileReader)
            # Import list of stops
            for row in fileReader:
                iniStop = (float(row[0]),float(row[1]))
                listStops.append(iniStop)
                lastStop = (float(row[2]),float(row[3]))
                listStops.append(lastStop)
        
        # Call functions
        result = Transformation.convertActivityLocation(fetchActivityLocations.fetchStopAL(listStops))
        listActivities.append(result)

        # Write result to a csv file
        outputFileName = 'trace-'+str(i)+'.csv'
        outputFilePath = os.path.join(outputPath, outputFileName)
        with open(outputFilePath, 'w', newline='') as outputFile:
            fileWriter = csv.writer(outputFile)
            # Create Header
            fileWriter.writerow(['Latitude', 'Longitude', 'Nearby Activity Locations'])

            # Write each rows
            for i in result:
                fileWriter.writerow([i[0],i[1],i[2]])

    print("Complete. The path of the generated file is: \n" + outputPath)
    return listActivities


# def findActivityLocations(userFile):
#     #First, do input processing.

#     listStops = []
#     with open(userFile,'r') as inputFile:
#         fileReader = csv.reader(inputFile)
#         # Skip Header
#         next(fileReader)
#         # Import list of stops
#         for row in fileReader:
#             stop = (float(row[0]),float(row[1]))
#             listStops.append(stop)
    
#     #Call fetchActivityLocations
#     result = fetchActivityLocations.fetchStopAL(listStops)
#     convertedResult = Transformation.convertActivityLocation(result) # convert to nested list
    
#     # Write Result to a csv file.
#     dirName = os.path.dirname(os.path.abspath(__file__))
#     outFile = os.path.join(dirName, 'fetchOutput.csv')
#     with open(outFile, 'w', newline='') as outputFile:
#         fileWriter = csv.writer(outputFile)
#         # Creater Header
#         fileWriter.writerow(['Latitude', 'Longitude', 'Nearby Activity Locations'])

#         # Write each rows
#         for i in convertedResult:
#             fileWriter.writerow([i[0],i[1],i[2]])

#     print("Complete. The path of the generated file is: \n" + dirName)

#     return convertedResult

def generateShortestPath(stopFile, summaryFile, optimizer):
    inputPoints = []
    mode = ''
    with open(stopFile,'r') as inputFile:
        fileReader = csv.reader(inputFile)
        # Skip Header
        next(fileReader)
        # Import points
        for row in fileReader:
            point = (float(row[0]),float(row[1]))
            inputPoints.append(point)
    
    with open(summaryFile,'r') as modeFile:
        modeReader = csv.reader(modeFile)
        for row in modeReader:
            mode = row[0]
    if (mode == 'mode.WALK'):
        mode = 'walk'
    if (mode == 'mode.DRIVE'):
        mode = 'drive'
    if (mode == 'mode.BIKE'):
        mode = 'bike'
    # Generate NetworkGraph
    networkGraph = GenerateRoute.GenerateGraph(inputPoints, mode)
    # Generate ShortestPath
    shortestRoute = GenerateRoute.GenerateShortestPath(networkGraph, inputPoints, optimizer)
    
    print("Complete, now you can do the mapping.")
    return networkGraph, shortestRoute



# def generateShortestPath(userFile, motion, optimizer):

#     inputPoints = []
#     with open(userFile,'r') as inputFile:
#         fileReader = csv.reader(inputFile)
#         # Skip Header
#         next(fileReader)
#         # Import points
#         for row in fileReader:
#             point = (float(row[0]),float(row[1]))
#             inputPoints.append(point)

#     # Generate NetworkGraph
#     networkGraph = GenerateRoute.GenerateGraph(inputPoints, motion)
#     # Generate ShortestPath
#     shortestRoute = GenerateRoute.GenerateShortestPath(networkGraph, inputPoints, optimizer)
    
#     print("Complete, now you can do the mapping.")
#     return networkGraph, shortestRoute

def generateAlternativePath(stopFile, optimizer):
    inputPoints = []
    with open(stopFile,'r') as inputFile:
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


def mapEpisodes(episodeFile):
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

def mapActivityLocations(activityList, fileName):
    listStops = []
    listActivities = []
    listActDescription = [] #List of activity location description

    for i in activityList:
        for j in i:
            listStops.append((j[0],j[1]))
            for k in j[2]:
                listActivities.append((k[1],k[2]))
                listActDescription.append(k[0])
    
    # Generate Map
    dirName = os.path.dirname(os.path.abspath(__file__))
    outFile = os.path.join(dirName, fileName)
    Mapping.MapActivityLocation(listActivities,listActDescription,listStops,outFile)
    print("Complete. The name of the file is" + fileName)
    print("The path of the generated file is: \n" + dirName)


def mapSRoute(userNetworkGraph,summaryFile, userRoute):
    # Read Mode
    mode = ''
    with open(summaryFile,'r') as modeFile:
        modeReader = csv.reader(modeFile)
        for row in modeReader:
            mode = row[0]
    if (mode == 'mode.WALK'):
        mode = 'walk'
    if (mode == 'mode.DRIVE'):
        mode = 'drive'
    if (mode == 'mode.BIKE'):
        mode = 'bike'

    dirName = os.path.dirname(os.path.abspath(__file__))
    outFile = os.path.join(dirName, 'shortest_path.html')

    # Mapping
    Mapping.MapRoute(userNetworkGraph.graph, mode, userRoute.routes, outFile)
    print("Complete.\n The name of the file is shortest_path.html.\n The path of the generated file is: \n" + dirName)


def mapARoute(summaryFile, userRoute):
    # Read Mode
    mode = ''
    with open(summaryFile,'r') as modeFile:
        modeReader = csv.reader(modeFile)
        for row in modeReader:
            mode = row[0]
    if (mode == 'mode.WALK'):
        mode = 'walk'
    if (mode == 'mode.DRIVE'):
        mode = 'drive'
    if (mode == 'mode.BIKE'):
        mode = 'bike'


    dirName = os.path.dirname(os.path.abspath(__file__))
    outFile = os.path.join(dirName, 'alternative_path.html')

    # Mapping
    Mapping.MapRoute(userRoute.network.graph, mode, userRoute.path.routes, outFile)
    print("Complete.\n The name of the file is alternative_path.html.\n The path of the generated file is: \n" + dirName)




# Driver code
if __name__ == '__main__':
    #Local Variables
    isEpisodeGenerated = False
    traceNum = 0 # Count number of traces generated from the episode
    activityList = []
    dirName = os.path.dirname(os.path.abspath(__file__))
    

    # Testing
    # inputFile = filedialog.askopenfilename()
    # inputMotion = input("Please insert the motion of the episode: ")
    # inputOptimizer = input("Please type in the optimizer[time/length]: ")
    # shortestNetworkGraph, shortestRoute =  generateShortestPath(inputFile, inputMotion, inputOptimizer)


    
    while True:
        moduleSelect = int(input("Please select the module you want to go over: "))

        # Determine modules
        if (moduleSelect == 2): # Module 2: Generate Episode
            print("Please select the csv file you want to process: ")
            userFile = filedialog.askopenfilename()
            #Call function
            generateEpisode(userFile)
            
            isEpisodeGenerated = True
            
            path = os.path.join(dirName, 'trace')
            traceNum = len(next(os.walk(path))[1])
        else:
            if not isEpisodeGenerated: #First Check if the episodes are generated
                print("You have to generate the Episode first!")
                continue
            else:
                if (moduleSelect == 3): # Module 3: find activity locations
                    activityList = findActivityLocations(traceNum)
                elif(moduleSelect == 5): # Module 5: Generate Shortest Route
                    selectTraceNum = input(str(traceNum) + " traces detected, which trace do you want to map?: ")
                    
                    selectedTraceName = 'trace-'+selectTraceNum
                    selectedTracePath = os.path.join(os.path.join(dirName, 'trace'),selectedTraceName)
                    
                    stopFile = os.path.join(selectedTracePath, 'stop_episode.csv')
                    summaryFile = os.path.join(selectedTracePath, 'summary_episode.csv')
                    optimizer = input("Please type in the optimizer[time/length]: ")

                    sRNetworkGraph, sRShortestRoute = generateShortestPath(stopFile,summaryFile,optimizer)
                    
                elif(moduleSelect == 6): # Module 6: Generate Alternative Routes
                    selectTraceNum = input(str(traceNum) + " traces detected, which trace do you want to map?: ")
                    
                    selectedTraceName = 'trace-'+selectTraceNum
                    selectedTracePath = os.path.join(os.path.join(dirName, 'trace'),selectedTraceName)
                    
                    stopFile = os.path.join(selectedTracePath, 'stop_episode.csv')
                    summaryFile = os.path.join(selectedTracePath, 'summary_episode.csv')
                    optimizer = input("Please type in the optimizer[time/length]: ")

                    alternativeRoute = generateAlternativePath(stopFile, optimizer)
                
                elif (moduleSelect == 7): # Module 7: Mapping Episodes
                    selectTraceNum = input(str(traceNum) + " traces detected, which trace do you want to map?: ")

                    selectedTraceName = 'trace-'+selectTraceNum
                    selectedTracePath = os.path.join(os.path.join(dirName, 'trace'),selectedTraceName)

                    episodeFile = os.path.join(selectedFilePath, 'episode.csv')
                    mapEpisodes(episodeFile)

                
                elif (moduleSelect == 8): # Module 8: Mapping ActivityLocations
                    if (len(activityList) != 0):
                        useExistingData = input(("Existing analyzed Activity Location found. Do you want to use these data?[y/n]: "))
                        # Use Existing Data
                        if (useExistingData == 'y'):
                            mapActivityLocations(activityList, 'activityLocation.html')
                            continue

                    selectTraceNum = input(str(traceNum) + " traces detected, which trace do you want to map?: ")
                    selectedFileName = 'trace-'+selectTraceNum+'.csv'
                    selectedFilePath = os.path.join(os.path.join(dirName, 'activityList'),selectedFileName)
                    activityList.append(Transformation.convertActivityCSV(selectedFilePath))
                    mapFileName = 'activityLocation.html'+selectedFileName
                    mapActivityLocations(activityList,mapFileName)



                elif(moduleSelect == 9): # Module 9: Mapping shortest route
                    mapSRoute(sRNetworkGraph, summaryFile,sRShortestRoute)

                elif(moduleSelect == 10):
                    mapARoute(summaryFile,alternativeRoute)
                
                elif (moduleSelect == 0): # Exit the program
                    print("Thank you for using the system.")
                    break
                else:
                    print("Not acceptable value, please try again.")
                    continue





# if __name__ == '__main__':
#     print("Please select the csv file you want to process: ")
#     inputFile = filedialog.askopenfilename()

#     # Should keep
#     ActivityList = []


#     while True:
#         moduleSelect = int(input("Please select the module you want to go over: "))
#         if(moduleSelect == 2): # Generate Episodes
#             generateEpisode(inputFile)
#         elif(moduleSelect == 3): # Find Activity Locations
#             ActivityList = findActivityLocations(inputFile)
#         elif(moduleSelect == 5): # Generate Shortest Path
#             inputMotion = input("Please insert the motion of the episode: ")
#             inputOptimizer = input("Please type in the optimizer[time/length]: ")
#             shortestNetworkGraph, shortestRoute =  generateShortestPath(inputFile, inputMotion, inputOptimizer)
#         elif(moduleSelect == 6): # Generate Alternative Path
#             inputOptimizer = input("Please type in the optimizer[time/length]: ")
#             alternativeRoute = generateAlternativePath(inputFile, inputOptimizer)
#         elif(moduleSelect == 7): # Mapping Episodes
#             mapEpisodes(inputFile)
#         elif(moduleSelect == 8): # Mapping Activity Locations
#             if (len(ActivityList) != 0):
#                 print("Dected pre-stored data in the system. Displaying the data: ")
#                 print(ActivityList)
#                 choice = input("Do you want to use this data to continue?[y/n]: ")
#                 if (choice == 'y'):
#                     mapActivityLocations(ActivityList)
#                 else:
#                     print("Please select the csv to continue: ")
#                     inputFile = filedialog.askopenfilename()
#                     ActivityList = Transformation.convertActivityCSV(inputFile)
#                     mapActivityLocations(ActivityList)
#             else:
#                 print("No pre-stored data detected.\n Please select the csv file to continue: ")
#                 inputFile = filedialog.askopenfilename()
#                 ActivityList = Transformation.convertActivityCSV(inputFile)
#                 mapActivityLocations(ActivityList)
#             # print("Please select the csv file you want to process: ")
#             # inputFile = filedialog.askopenfilename()
#             # mapActivityLocations(inputFile)
#         elif(moduleSelect == 9): # Mapping Shortest Route
#             sRouteMotion = input("Please insert the motion of the episode: ")
#             mapSRoute(shortestNetworkGraph, sRouteMotion, shortestRoute)
#         elif (moduleSelect == 10): # Mapping Alternative Route
#             inputMotion = input("Please insert the mode of the points: ")
#             mapARoute(inputMotion, alternativeRoute)
#         elif (moduleSelect == 0):
#             print("Thank you for using the system.")
#             break
#         else:
#             print("Error. You choose the wrong number.")
#             continue