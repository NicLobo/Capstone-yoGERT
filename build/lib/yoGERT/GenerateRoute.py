## @file GenerateRoute.py
#  @title GenerateRoute
#  @author Abeer Alyasiri 400198787
#  @date January 31 2023

import osmnx as ox
import networkx as nx
import h3
from .NetworkGraph import *
from .ShortestRoute import *
from .AlternativeRoute  import *
from .CustomExceptions import * 

## @brief This function create and returns a network graph object for the travel episode area.
#  @param startCoord (lat, long) tuple for the latitude and longitude of the start GPS coordinate. 
#  @param endCoord (lat, long) tuple for the latitude and longitude of the end GPS coordinate.
#  @param stopPoints list of tuples consisting of the stop points GPS coordinates. 
#  @param detectedMode string representing the episode's travel mode 
#  @return a NetworkGraph object.
def GenerateGraph(stopPoints, detectedMode):
    return NetworkGraph(stopPoints[0], stopPoints[len(stopPoints)-1], stopPoints, detectedMode)

## @brief This function create and returns a shortest route object for the travel episode.
#  @param graphNetwork NetworkGraph for the map network of street, roads, and walkways. 
#  @param stopPoints list of tuples consisting of the stop points GPS coordinates. 
#  @param optimizer string for the weight type on the graph's edges.  
#  @return a ShortestRoute object.
def GenerateShortestPath(graphNetwork, stopPoints, optimizer):
    return ShortestRoute(graphNetwork, stopPoints, optimizer)

## @brief This function create and returns an alternative route object for the travel episode.
#  @param stopPoints list of tuples consisting of the stop points GPS coordinates. 
#  @param optimizer string for the weight type on the graph's edges. 
#  @return a AlternativeRoute object. 
def GenerateAlternativePath(stopPoints, optimizer):
    return AlternativeRoute(stopPoints, optimizer)
