## @file ShortestRouteEpisode.py
#  @title ShortestRouteEpisode
#  @author Abeer Alyasiri 400198787
#  @date January 31 2023

import osmnx as ox
import networkx as nx
import h3
from NetworkGraph  import *
# from IPython.display import IFrame
from CustomExceptions  import *
from Point import *
from Transformation import *

## @brief A class representing an object that represents the shortest route for a travel epsiode of mode type walk or drive. 
#  @details This representation of the shortest route will include the epsiode's sampled GPS pings or the start and end point.
class ShortestRouteEpisode:
    ## @brief Constructor for ShortestRouteEpisode
    #  @details Contructor accepts 5 parameters for map network, GPS coordinates, weight type, sampling condtion, and sampling distance variable.
    #  @param networkGraph NetworkGraph for the map network of street, roads, and walkways. 
    #  @param filePath string of the path to the csv file consisting of GPS Points for one episode. 
    #  @param optimizer string for the weight type on the graph's edges.  
    #  @param sampling boolean to decide when data sampling is needed to make a pings' subset by selecting a ping every specified distance
    #  @param samplingDist integer for the sampling distance variable in m.
    #  @throws InvalidWeightException Raised when the inputted optimizer is not a subset of {time, length}
    #  @throws EmptyFilePathException Raised when input file path is empty
    def __init__(self, networkGraph, filePath, optimizer = "time", sampling = True, samplingDist = 50):
        try:
            if optimizer not in ["time", "length"]:
                raise InvalidWeightException
            elif filePath == "":
                raise EmptyFilePathException
            else:
                self.graph = networkGraph
                self.inputData = episoderelated(filePath) #listOfPoints #this needs to be changed to tranform csvfile to a list of Points 
                if (sampling):
                    self.sampledData = self.findSamples(self.inputData, samplingDist)
                else:
                    self.sampledData = [self.inputData[0], self.inputData[-1]]
                #self.sampledData = self.findSamples(listOfPoints, sampling, samplingDist)
                self.nodes = self.findNodes(self.sampledData, networkGraph)
                self.wt = optimizer
                self.sampling = sampling
                self.samplingDist = samplingDist
                self.routes = self.shortestPath(networkGraph, self.nodes, optimizer)
                print("Shortest Route Episode was successfully created!")
        except InvalidWeightException:
            print("InvalidWeightException: Invalid input for weight type! Enter either time or length.")
        except EmptyFilePathException:
            print("EmptyFilePathException: Input file path is empty. Please enter a file path to a episode.")
    
    ## @brief This function finds sampled data points for a given list of GPS pings. 
    #  @param listOfPoints list of Points consisting of GPS Points with coordinates, time, and mode.
    #  @param distance integer for the sampling distance to select GPS points after certain distance 
    #  @return a list of Points.
    def findSamples(self, listOfPoints, distance):
        listOfSampledPoints = []
        listOfSampledPoints.append(listOfPoints[0])
        selected = listOfPoints[0]
        for i in range(1, len(listOfPoints)-1):
            if (h3.point_dist((selected.lat, selected.lon), (listOfPoints[i].lat,listOfPoints[i].lon), unit='m') > distance):
                listOfSampledPoints.append(listOfPoints[i])
                selected = listOfPoints[i]
        listOfSampledPoints.append(listOfPoints[len(listOfPoints)-1])
        return listOfSampledPoints
    
    ## @brief This function finds nodes on the network graph for the episode's GPS Points. 
    #  @param listOfSampledPoints list of Points consisting of sampled GPS Points with coordinates, time, and mode. 
    #  @param graphInput NetworkGraph for the map network of street, roads, and walkways. 
    #  @return a list of graph nodes.
    def findNodes(self, listOfSampledPoints, graphInput):
        listOfNodes = []
        for point in listOfSampledPoints:
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

