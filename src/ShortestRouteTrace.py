## @file ShortestRouteTrace.py
#  @title ShortestRouteTrace
#  @author Abeer Alyasiri 400198787
#  @date Feburary 25 2023

import osmnx as ox
import networkx as nx
import h3
from NetworkGraph  import *
# from IPython.display import IFrame
from CustomExceptions  import *
from Point import *
from Transformation import *

## @brief A class representing an object that represents the shortest route for a trace. 
#  @details This representation of the shortest route will include the trace's points 
#  from the start point to end point. 
class ShortestRouteTrace:
    ## @brief Constructor for ShortestRouteTrace
    #  @details Contructor accepts 3 parameters for map network, GPS coordinates, and weight type.
    #  @param networkGraph NetworkGraph for the map network of street, roads, and walkways for the entire trace. 
    #  @param filePath string for the path to the csv file consisting of GPS Points representing of the trace.
    #  @param optimizer string for the weight type on the graph's edges.  
    #  @throws InvalidWeightException Raised when the inputted optimizer is not a subset of {time, length}
    #  @throws EmptyFilePathException Raised when input file path is empty
    def __init__(self, networkGraph, filePath, optimizer = "time"):
        try:
            if optimizer not in ["time", "length"]:
                raise InvalidWeightException
            elif filePath == "":
                raise EmptyFilePathException
            else:
                self.graph = networkGraph
                # self.inputData = episoderelated(filePath) #listOfPoints #this needs to be changed to tranform csvfile to a list of Points 
                self.inputData = tracerelated(filePath)
                self.nodes = self.findNodes(self.inputData, networkGraph)
                self.wt = optimizer
                self.routes = self.shortestPath(networkGraph, self.nodes, optimizer)
                print("Shortest Route Trace was created successfully")
        except InvalidWeightException:
            print("InvalidWeightException: Invalid input for weight type! Enter either time or length.")
        except EmptyFilePathException:
            print("EmptyFilePathException: Input file path is empty. Please enter a file path to a trace.")
    ## @brief This function finds nodes on the network graph for the episode's GPS Points. 
    #  @param listOfStopPoints list of Points consisting of stop points representation for the entire trace. 
    #  @param graphInput NetworkGraph for the map network of street, roads, and walkways. 
    #  @return a list of graph nodes.
    def findNodes(self, listOfStopPoints, graphInput):
        listOfNodes = []
        for point in listOfStopPoints:
            examine = graphInput.getNearestNode((point.lat, point.lon))
            if (len(listOfNodes) > 0 and examine != listOfNodes[-1]):
                listOfNodes.append(examine)
            elif (len(listOfNodes) == 0):
                listOfNodes.append(examine)
        return listOfNodes
    ## @brief Function that finds the shortest path for a list of must hit nodes.
    #  @details The function uses Dijkstra's algorithm with weighted edges. 
    #  @param graphInput NetworkGraph for the map network of street, roads, and walkways. 
    #  @param nodesInput list of integers representing the must hit nodes for the route.
    #  @param weightType string for the graph's edges weight.  
    #  @return list of list nodes for the shorestest path.
    def shortestPath(self, graphInput, nodesInput, weightType):
        listOfRoutes = []
        for i in range(0,len(self.nodes)-1):
            try:
                listOfRoutes.append(nx.shortest_path(graphInput.graph,nodesInput[i], nodesInput[i+1], weight=weightType))
            except nx.exception.NetworkXNoPath:
                print("NetworkXNoPath: No Path Here:(")
        return listOfRoutes
