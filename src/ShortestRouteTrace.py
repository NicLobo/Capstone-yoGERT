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
    #  @details Contructor accepts 3 parameters for map network, stop GPS coordinates, and weight type.
    #  @param networkGraph NetworkGraph for the map network of street, roads, and walkways for the entire trace. 
    #  @param filePath string for the path to the csv file consisting of GPS Points representing of the trace.
    #  @param optimizer string for the weight type on the graph's edges.  
    #  @throws InvalidWeightException Raised when the inputted optimizer is not a subset of {time, length}
    def __init__(self, networkGraph, filePath, optimizer = "time"):
        try:
            if optimizer not in ["time", "length"]:
                raise InvalidWeightException
            else:
                self.graph = networkGraph
                # self.inputData = episoderelated(filePath) #listOfPoints #this needs to be changed to tranform csvfile to a list of Points 
                self.inputData = tracerelated(filePath)
                self.nodes = self.findNodes(self.inputData, networkGraph)
                self.wt = optimizer
                self.routes = self.shortestPath(networkGraph, self.nodes, optimizer)
        except InvalidWeightException:
            print("InvalidWeightException: Invalid input for weight type! Enter either time or length.")
    ## @brief This function finds nodes on the network graph for the episode's GPS Points. 
    #  @param listOfStopPoints list of Points consisting of stop points representation for the entire trace. 
    #  @param graphInput NetworkGraph for the map network of street, roads, and walkways. 
    #  @return a list of graph nodes.
    def findNodes(self, listOfStopPoints, graphInput):
        listOfNodes = []
        for point in listOfStopPoints:
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
                print("NetworkXNoPath: No Path Here:(")
        return listOfRoutes


# inputTwo = [Point(43.651605, -79.386759,"17:22:02", "mode.DRIVE", 1), Point(43.651484, -79.386665,"17:22:03", "mode.DRIVE", 1), 
#          Point(43.652269, -79.387062,"17:22:04", "mode.DRIVE", 1),Point(43.653047, -79.387406,"17:22:05", "mode.DRIVE", 1),
#          Point(43.653523, -79.385977,"17:22:06", "mode.DRIVE, 1"),Point(43.653915, -79.385434,"17:22:07", "mode.DRIVE, 1"),
#          Point(43.655093, -79.385935,"17:22:08", "mode.STOP, 2"), Point(43.655199, -79.385977,"17:22:09", "mode.DRIVE, 3"), 
#          Point(43.655244, -79.385862,"17:22:10", "mode.DRIVE, 3"), Point(43.655388, -79.385236,"17:22:11", "mode.DRIVE, 3")]
# inputTwoStops = [Point(43.651605, -79.386759,"17:22:02", None),Point(43.655093, -79.385935,"17:22:08", None), 
#                   Point(43.655388, -79.385236,"17:22:11", None)]
# NetworkGraphTwoTrace = NetworkGraph(inputTwoStops, "drive")
# ShortestRouteTraceOne = ShortestRouteTrace(NetworkGraphTwoTrace, inputTwoStops, "time") # ShortestRouteTraceone = ShortestRouteTrace(NetworkGraphTwo, inputTwoTuples)
# baseT = folium.Map(location=[inputTwoStops[0].lat, inputTwoStops[0].lon], zoom_start=10)
# for point in inputTwoStops:
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
#     baseT.add_child(folium.Marker([point.lat,point.lon], 
#                     tooltip=tooltip, icon=folium.Icon(color=color, icon=icon, prefix="fa")))

# route_map2T = ox.plot_route_folium(NetworkGraphTwo.graph, ShortestRouteTraceOne.routes[0], route_map=baseT, color='#005eff', opacity=0.7)
# for i in range(1,len(ShortestRouteTraceOne.routes)):
#      route_map2T = ox.plot_route_folium(NetworkGraphTwo.graph, ShortestRouteTraceOne.routes[i], route_map=route_map2T, color='#005eff', opacity=0.7)
# filepath = "C:/Users/sweet/anaconda3/envs/capstone/data/Ttraceroute_test_graph2withmarkers.html"
# route_map2T.save(filepath)
# IFrame(filepath, width=600, height=500)
