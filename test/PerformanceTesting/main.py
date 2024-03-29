## @file main.py
#  @title Main Module
#  @author Longwei Ye 400236382, team GIS GANG
#  @date February 25 2023

import PreProcessing
import EpisodeGeneration
import FetchActivityLocations
import NetworkGraph
import ShortestRouteTrace
import ShortestRouteEpisode
import ShortestRouteStop
import AlternativeRoute
import Mapping

## @brief This function generates Episodes
#  @param inputCSVFilePath the path of the csv file that consists of points that the users may interested in.
#  @param exportFolderTitle the title that the exported folder(includes episodes and stop-points analyzed by the program).
def generateEpisodes(inputCSVFilePath, exportFolderPath, Title):
    EpisodeGeneration.episodeGenerator(inputCSVFilePath,exportFolderPath, Title)

## @brief This function maps the Episodes points generated by the previous generatedEpisodes() function
#  @param inputEpisodeFilePath the path of the Episode Point file that the user wants to map
#  @param exportFilePath the path that user wants to store the mapped .html file
def mapEpisodes(inputEpisodeFilePath, exportFilePath):
    Mapping.MapEpisodePoints(inputEpisodeFilePath, exportFilePath)

## @brief This function fetches the near-by locations based on the stop points that the user interested in
#  @param inputStopsFilePath the path of the file that has all the stop points
#  @param exportCSVFilePath the path that user wants to store the fetched activity-locations .csv file
#  @param tolerance the tolerance of the radius searched for the stop point in integer
def findActivityLocations(inputStopsFilePath, exportCSVFilePath, tolerance):
    FetchActivityLocations.FetchActivityLocations(inputStopsFilePath, exportCSVFilePath, tolerance)

## @brief This function maps the stop points and their nearby possible activity-locations
#  @param activityLocationFilePath the path of the nearby-locations file(i.e. activityLocation.csv) generated
#         by the previous findActivityLocations() function
#  @param stopPointFilePath the path of the stop point file
#  @param exportFilePath the path for the stopPoint-activityLocation map that the user wants to save
def mapActivityLocations(activityLocationFilePath, stopPointFilePath, exportFilePath):
    Mapping.MapActivityLocation(activityLocationFilePath, stopPointFilePath, exportFilePath)

## @brief This function generates a shortestRoute based on an Episode
#  @param inputEpisodePath the path of the Episode file(i.e. id_episode.csv) provided by the user
#  @return shortestEpisodeNetworkGraph a NetworkGraph type object that represents the generated mapping
#          network Episodes and their nearby information(e.g. streets, walkways, roads)
#  @return shortestEpisodeRoute a ShortestRouteEpisode object that records the the shortest route for 
#          the analyzed travel episode
def generateShortestEpisodeRoute(inputEpisodePath):
    shortestEpisodeNetworkGraph = NetworkGraph.NetworkGraph(inputEpisodePath)
    shortestEpisodeRoute = ShortestRouteEpisode.ShortestRouteEpisode(shortestEpisodeNetworkGraph, inputEpisodePath)

    return shortestEpisodeNetworkGraph, shortestEpisodeRoute

## @brief This functions maps a generated Episode's shortest route
#  @param episodeNetworkGraph the NetworkGraph object previously generated by the generateShortestEpisodeRoute() function
#  @param shortestEpisodeRoute the corresponding shortestRouteEpisode object to the previous entity
#         (i.e. episodeNetworkGraph entity)
#  @param exportFilePath the desired storing location for the episode-route map determined by the user
def mapShortestEpisodeRoute(episodeNetworkGraph, episodeRoute, exportFilePath):
    Mapping.MapRoute(episodeNetworkGraph, episodeRoute, exportFilePath)

## @brief This function generates a shortestRoute based on a set of trace points
#  @param inputTracePath the path of the trace file provided by the user
#  @param traceMode the mode of the trace(i.e. drive)
#  @param episodeAnalysis a boolean telling modules to generate a episode-based NetworkGraph. Set to False by default
#  @return shortestTraceNetworkGraph a NetworkGraph type object that represents the generated mapping
#          network Traces and their nearby information(e.g. streets, walkways, roads)
#  @return shortestTraceRoute a ShortestRouteEpisode object that records the the shortest route for 
#          the analyzed trace
def generateShortestTraceRoute(inputTracePath, traceMode, episodeAnalysis = False):
    shortestTraceNetworkGraph = NetworkGraph.NetworkGraph(inputTracePath, traceMode, episodeAnalysis)
    shortestTraceRoute = ShortestRouteTrace.ShortestRouteTrace(shortestTraceNetworkGraph, inputTracePath)

    return shortestTraceNetworkGraph, shortestTraceRoute

## @brief This function maps one trace's shortest route
#  @param shortestTraceNetworkGraph the NetworkGraph object previously generated by the generateShortestTraceRoute() function
#  @param shortestTraceRoute the corresponding shortestRouteTrace object to the previous entity
#         (i.e. shortestTraceNetworkGraph entity)
#  @param exportFilePath
def mapShortestTraceRoute(shortestTraceNetworkGraph, shortestTraceRoute, exportFilePath):
    Mapping.MapRoute(shortestTraceNetworkGraph, shortestTraceRoute, exportFilePath)

## @brief This function generate the alternative route of a set of trace points, under bike mode by default
#  @param inputTracePath the path of the trace file provided by the user
#  @return alternativeRoute the AlternativeRoute object that can be used for mapping.
def generateAlternativeRoute(inputTracePath):
    alternativeRoute = AlternativeRoute.AlternativeRoute(inputTracePath)

    return alternativeRoute

## @brief This function maps the alternative route of a trace
#  @param alternativeRoute the AlternativeRoute object generated by the generateAlternativeRoute() function 
#         called before
#  @param exportFilePath the path of the generated route map that needed to be stored on user's computer
def mapAlternativeRoute(alternativeRoute, exportFilePath):
    Mapping.MapRoute(alternativeRoute.network, alternativeRoute.path, exportFilePath)
    
## @brief This is function generates a ShortestRoute based on stop points
#  @param traceFilePath the file path of the trace data file for analysis
#  @param traceMode the mode of the trace(i.e. walk, drive)
#  @param stopFilePath the file path of the stop points data
#  @return an ShortestRouteStop object
def generateShortestStopRoute(traceFilePath, traceMode, stopFilePath):
    generatedNetworkGraph = NetworkGraph.NetworkGraph(traceFilePath, traceMode, False)
    generatedShortestStopRoute = ShortestRouteStop.ShortestRouteStop(generatedNetworkGraph, stopFilePath)

    return generatedShortestStopRoute

def generatePreProcessingCSV(csvFilePath, dirPath):
    processedFile, isDataValid = PreProcessing.Validate_CSV(csvFilePath, dirPath)
    
    return processedFile, isDataValid

# csvPath = "/Users/tommylw/Desktop/University/SE_4G06/Capstone-yoGERT/src/exampleDataset/trace_1.csv"
# generateEpisodes(csvPath,"trace")
# episodeFilePath = "/Users/tommylw/Desktop/University/SE_4G06/Capstone-yoGERT/src/1_episode.csv"
# generateShortestEpisodeRoute(episodeFilePath)
# traceFilePath = "/Users/tommylw/Desktop/University/SE_4G06/Capstone-yoGERT/src/trace.csv"
# generateShortestTraceRoute(traceFilePath, "drive", False)
# generateAlternativeRoute(traceFilePath)

# tracePath = "/Users/tommylw/Desktop/University/SE_4G06/Capstone-yoGERT/src/trace/trace.csv"
# stopPath = "/Users/tommylw/Desktop/University/SE_4G06/Capstone-yoGERT/src/trace/stop/stops.csv"
# generateShortestStopRoute(tracePath,"drive",stopPath)
