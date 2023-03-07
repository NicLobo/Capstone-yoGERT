## @file NetworkGraph.py
#  @title NetworkGraph
#  @author Abeer Alyasiri 400198787
#  @date January 31 2023

import osmnx as ox
import h3
from CustomExceptions import *
from Point import *
from Transformation import *

# exported constants 
DISTANCETOL = 200

## @brief Object represents a mapping network of streets, walkways, and roads.
# @details The network is a represents by a graph of nodes and edges. 
# Each nodes corresponds to one or more GPS coordinate. Each edge corresponds to a connecting street, road, or walkway. 
class NetworkGraph:
    ## @brief Constructor for NetworkGraph
    #  @details Contructor accepts 4 parameters for start and end GPS coordinates, list of stop GPS coordinates, and mode of transportation.
    #  @param filePath string of the path to the csv file consisting of the GPS pings for an episode or trace. 
    #  @param networkMode string for the entity's mode of transportations for ex: drive or walk.
    #  @param episodeAnalysis boolean to know the type of inputted GPS pings. Defaulted to True
    #  @param alternativeAnalysis boolean to know the type of inputted GPS pings. Defaulted to False
    #  @throws InvalidModeException Raised when the input value is not a subset of {drive, walk}
    #  @throws EmptyFilePathException "Raised when input file path is empty"
    def __init__(self, filePath, networkMode = None, episodeAnalysis = True, alternativeAnalysis = False):
        # check inputs
        try: 
            if networkMode not in ["drive", "walk", "bike", None]:
                raise InvalidModeException
            elif filePath == "":
                raise EmptyFilePathException
            else:
                if episodeAnalysis:
                    points = episoderelated(filePath)
                    tempMode = points[0].mode
                    self.mode = tempMode.split('.')[1].lower()
                elif alternativeAnalysis:
                    points = tracerelated(filePath)
                    self.mode = networkMode
                else:
                    points = tracerelated(filePath)
                    self.mode = summaryModeTrace(filePath).split('.')[1].lower()
                self.stCoord = (points[0].lat, points[0].lon)
                self.endCoord = (points[-1].lat, points[-1].lon)
                self.dist = self.findDistance(self.stCoord, self.endCoord, points)
                self.graph = ox.graph_from_point(self.stCoord, dist=self.dist, network_type=self.mode, simplify=False)
        except InvalidModeException:
            print("InvalidModeException: Invalid network mode! Enter either drive or walk for mode.")
        except EmptyFilePathException:
            print("EmptyFilePathException: Input file path is empty. Please enter a file path to a trace or episode.")
        
    ## @brief Returns the nearest graph node to a GPS coordinate
    #  @param coord (lat, long) tuple for the latitude and longitude of the GPS coordinate of interest. 
    #  @return an integer of the node number. 
    #  @throws OutOfBoundsCoordException Raised when the input coordinate is not within the graph data
    def getNearestNode(self, coord):
        #check inputs
        try: 
            if (self.findDistance(self.stCoord, coord, []) > self.dist):
                raise OutOfBoundsCoordException
            else:
                return ox.nearest_nodes(self.graph, coord[1], coord[0])
        except OutOfBoundsCoordException:
            print("OutOfBoundsCoordException: Out of bounds input coordinate.")
    
    ## @brief This function finds the longest distance from the start GPS coordinate to any GPS coordinate within the travel episode.
    #  @details The function uses haversince formula to find the distance between two coordinates. The distance represents the radius from the start point for the extracted graph data.  
    #  @param startCoord (lat, long) tuple for the latitude and longitude of the start GPS coordinate. 
    #  @param endCoord (lat, long) tuple for the latitude and longitude of the end GPS coordinate.
    #  @param stops list of Point type consisting of the GPS coordinates of an episode or trace. 
    #  @return a float of the longest distance.
    def findDistance(self, startCoord, endCoord, points):
        distance = h3.point_dist(startCoord, endCoord, unit='m') # findhdistance
        for i in range(1,len(points)-1):
            testDis = h3.point_dist(startCoord, (points[i].lat, points[i].lon), unit='m')
            if (testDis > distance):
                distance = testDis
        distance = distance + DISTANCETOL
        return distance
        
    ## @brief This function returns the graph's transportation mode
    #  @return a string of the transportation mode
    def getMode(self):
        return self.mode


# inputTwo = [Point(43.651605, -79.386759,"17:22:02", "mode.DRIVE"), Point(43.651484, -79.386665,"17:22:03", "mode.DRIVE"), 
#          Point(43.652269, -79.387062,"17:22:04", "mode.DRIVE"),Point(43.653047, -79.387406,"17:22:05", "mode.DRIVE"),
#          Point(43.653523, -79.385977,"17:22:06", "mode.DRIVE"),Point(43.653915, -79.385434,"17:22:07", "mode.DRIVE")]
#          ,Point(43.655093, -79.385935,"17:22:08", "mode.STOP"), Point(43.655199, -79.385977,"17:22:09", "mode.DRIVE"), 
#         Point(43.655244, -79.385862,"17:22:10", "mode.DRIVE"), Point(43.655388, -79.385236,"17:22:11", "mode.DRIVE")]
# inputTwoTuples = []
# for point in inputTwo:
#     inputTwoTuples.append((point.lat,point.lon))
# NetworkGraphTwo = NetworkGraph(inputTwo, "drive")
# NG1 = NetworkGraph("C:/Users/sweet/anaconda3/envs/capstone/data/trace1.csv", "drive", False)
