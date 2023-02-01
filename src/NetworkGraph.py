## @file NetworkGraph.py
#  @title NetworkGraph
#  @author Abeer Alyasiri 400198787
#  @date January 31 2023

import osmnx as ox
import h3
from CustomExceptions import *

# exported constants 
DISTANCETOL = 200
EARTHRADIUS = 6371000 

## @brief Object represents a mapping network of streets, walkways, and roads.
# @details The network is a represents by a graph of nodes and edges. 
# Each nodes corresponds to one or more GPS coordinate. Each edge corresponds to a connecting street, road, or walkway. 
class NetworkGraph:
    ## @brief Constructor for NetworkGraph
    #  @details Contructor accepts 4 parameters for start and end GPS coordinates, list of stop GPS coordinates, and mode of transportation.
    #  @param startCoord (lat, long) tuple for the latitude and longitude of the start GPS coordinate. 
    #  @param endCoord (lat, long) tuple for the latitude and longitude of the end GPS coordinate.
    #  @param stops list of tuples consisting of the stop points GPS coordinates. 
    #  @param networkMode string for the object's mode of transportations for ex: drive or walk.  
    #  @throws InvalidModeException Raised when the input value is not a subset of {drive, walk}
    def __init__(self, startCoord, endCoord, stops, networkMode):
        # check inputs
        try: 
            if networkMode not in ["drive", "walk", "bike"]:
                raise InvalidModeException
            else:
                self.dist = self.findDistance(startCoord, endCoord, stops)
                self.stcoord = startCoord
                self.graph = ox.graph_from_point(startCoord, dist=self.dist, network_type=networkMode, simplify=False)
                self.mode = networkMode
        except InvalidModeException:
            print("InvalidModeException: Invalid network mode! Enter either drive or walk for mode.")
        
    ## @brief Returns the nearest graph node to a GPS coordinate
    #  @param coord (lat, long) tuple for the latitude and longitude of the GPS coordinate of interest. 
    #  @return an integer of the node number. 
    #  @throws OutOfBoundsCoordException Raised when the input coordinate is not within the graph data
    def getNearestNode(self, coord):
        #check inputs
        try: 
            if (self.findDistance(self.stcoord, coord, []) > self.dist):
                raise OutOfBoundsCoordException
            else:
                return ox.nearest_nodes(self.graph, coord[1], coord[0])
        except OutOfBoundsCoordException:
            print("OutOfBoundsCoordException: Out of bounds input coordinate.")
    
    ## @brief This function finds the longest distance from the start GPS coordinate to any GPS coordinate within the travel episode.
    #  @details The function uses haversince formula to find the distance between two coordinates. The distance represents the radius from the start point for the extracted graph data.  
    #  @param startCoord (lat, long) tuple for the latitude and longitude of the start GPS coordinate. 
    #  @param endCoord (lat, long) tuple for the latitude and longitude of the end GPS coordinate.
    #  @param stops list of tuples consisting of the stop points GPS coordinates. 
    #  @return a float of the longest distance.
    def findDistance(self, startCoord, endCoord, stops):
        distance = h3.point_dist(startCoord, endCoord, unit='m') # findhdistance
        for i in range(1,len(stops)-1):
            testDis = h3.point_dist(startCoord, stops[i], unit='m')
            if (testDis > distance):
                distance = testDis
        distance = distance + DISTANCETOL
        return distance
        
    ## @brief This function returns the graph's transportation mode
    #  @return a string of the transportation mode
    def getMode(self):
        return self.mode


# inputOne = [(-23.546498,-46.691141),(-23.558094,-46.660205),(-23.635039,-46.641239),
#                 (-23.645996,-46.641027),(-23.625882,-46.640936),(-23.618245,-46.639139),
#                 (-23.6130583,-46.637918),(-23.598541,-46.636634),(-23.589342,-46.634677),
#                 (-23.567615,-46.649027),(-23.56357,-46.653893),(-23.581203,-46.638489),
#                 (-23.5754,-46.6407),(-23.568521,-46.63990),(-23.561435,-46.638534)]
# NetworkGraph1 = NetworkGraph(inputOne[0], (-23.561435,-46.638534), inputOne, "drive")
# NetworkGraph1.getNearestNode(inputOne[0])
# NetworkGraph1.getNearestNode((-23.561435,-46.638534))
