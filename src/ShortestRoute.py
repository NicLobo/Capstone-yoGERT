## @file ShortestRoute.py
#  @title ShortestRoute
#  @author Abeer Alyasiri 400198787
#  @date January 31 2023

import osmnx as ox
import networkx as nx
import h3
from NetworkGraph  import *
# from IPython.display import IFrame
from CustomExceptions  import *
from Point import *

## @brief A class representing an object that represents the shortest route for a travel epsiode. 
#  @details This representation of the shortest route will include the epsiode's important stop points 
#  from the start point to end point. 
class ShortestRoute:
    ## @brief Constructor for ShortestRoute
    #  @details Contructor accepts 3 parameters for map network, list of stop GPS coordinates, and weight type.
    #  @param networkGraph NetworkGraph for the map network of street, roads, and walkways. 
    #  @param listOfPoints list of Points consisting of GPS Points. --change later to filepath to needed csv
    #  @param optimizer string for the weight type on the graph's edges.  
    #  @param sampling string for what type of data sampling to make a pings' subset (stop, distance) where stop stands for stop points, distance stands for every 50m add a ping to the subset
    #  @param samplingDist integer for the sampling distance variable in m.
    #  @throws InvalidWeightException Raised when the inputted optimizer is not a subset of {time, length}
    #  @throws InvalidSamplingException Raised when the inputted sampling is not a subset of {stop, distance}
    def __init__(self, networkGraph, listOfPoints, optimizer = "time", sampling = "stop", samplingDist = 50):
        try:
            if optimizer not in ["time", "length"]:
                raise InvalidWeightException
            elif sampling not in ["stop", "distance"]:
                raise InvalidSamplingException
            else:
                self.graph = networkGraph
                self.inputData = listOfPoints #this needs to be changed to tranform csvfile to a list of Points 
                self.sampledData = self.findSamples(listOfPoints, sampling, samplingDist)
                self.nodes = self.findNodes(self.sampledData, networkGraph)
                self.wt = optimizer
                self.sampling = sampling
                self.samplingDist = samplingDist
                self.routes = self.shortestPath(networkGraph, self.nodes, optimizer)
        except InvalidWeightException:
            print("InvalidWeightException: Invalid input for weight type! Enter either time or length.")
        except InvalidSamplingException:
            print("InvalidSamplingException: Invalid input for sampling type! Enter either stop or distance.")
    
    ## @brief This function finds sampled data points for a given list of GPS pings. 
    #  @param listOfPoints list of Points consisting of GPS Points with coordinates, time, and mode.
    #  @param type string for type of sampling to be performed on list of points (stop, distance).  
    #  @param distance integer for the sampling distance to select GPS points after certain distance 
    #  @return a list of Points.
    def findSamples(self, listOfPoints, type, distance):
        listOfSampledPoints = []
        if type == "stop":
            for stop in listOfPoints:
                if stop.mode == "mode.STOP":
                    listOfSampledPoints.append(stop)
        if type == "distance":
            listOfSampledPoints.append(listOfPoints[0])
            selected = listOfPoints[0]
            for i in range(1, len(listOfPoints)-1):
                if listOfPoints[i].mode == "mode.STOP":
                    selected = listOfPoints[i]
                    listOfSampledPoints.append(listOfPoints[i])
                elif (h3.point_dist((selected.lat, selected.lon), (listOfPoints[i].lat,listOfPoints[i].lon), unit='m') > distance):
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
            if (len(listOfNodes)>0 and examine != listOfNodes[-1]):
                listOfNodes.append(examine)
            elif (len(listOfNodes)==0):
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
                print("No Path Here:(")
        return listOfRoutes


# inputTwo = [Point(43.651605, -79.386759,"17:22:02", "mode.DRIVE"), Point(43.651484, -79.386665,"17:22:03", "mode.DRIVE"), 
#          Point(43.652269, -79.387062,"17:22:04", "mode.DRIVE"),Point(43.653047, -79.387406,"17:22:05", "mode.DRIVE"),
#          Point(43.653523, -79.385977,"17:22:06", "mode.DRIVE"),Point(43.653915, -79.385434,"17:22:07", "mode.DRIVE"),
#          Point(43.655093, -79.385935,"17:22:08", "mode.STOP"), Point(43.655199, -79.385977,"17:22:09", "mode.DRIVE"), 
#          Point(43.655244, -79.385862,"17:22:10", "mode.DRIVE"), Point(43.655388, -79.385236,"17:22:11", "mode.DRIVE")]
# inputTwoTuples = []
# for point in inputTwo:
#     inputTwoTuples.append((point.lat,point.lon))
# NetworkGraphTwo = NetworkGraph(inputTwoTuples[0], (43.655388, -79.385236), inputTwoTuples, "drive")
# ShortestRouteOne = ShortestRoute(NetworkGraphTwo, inputTwo, "time", "distance", 50) # shortestrouteone = ShortestRoute(NetworkGraphTwo, inputTwoTuples)
# base = folium.Map(location=[inputTwo[0].lat, inputTwo[0].lon], zoom_start=10)
# for point in inputTwo:
#     tooltip = point.time
#     if point.mode == "mode.DRIVE":
#         color = "green"
#         icon="car-side"
#     elif point.mode == "mode.WALK":
#         color = "blue"
#         icon="person-walking"
#     else:
#         color = "red"
#         icon="circle-stop"
#     base.add_child(folium.Marker([point.lat,point.lon], 
#                     tooltip=tooltip, icon=folium.Icon(color=color, icon=icon, prefix="fa")))

# route_map2 = ox.plot_route_folium(NetworkGraphTwo.graph, ShortestRouteOne.routes[0], route_map=base, color='#005eff', opacity=0.7)
# for i in range(1,len(ShortestRouteOne.routes)):
#      route_map2 = ox.plot_route_folium(NetworkGraphTwo.graph, ShortestRouteOne.routes[i], route_map=route_map2, color='#005eff', opacity=0.7)
# filepath = "C:/Users/sweet/anaconda3/envs/capstone/data/route_test_graph2withmarkers.html"
# route_map2.save(filepath)
# IFrame(filepath, width=600, height=500)
