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

## @brief A class representing an object that represents the shortest route for a travel epsiode. 
#  @details This representation of the shortest route will include the epsiode's important stop points 
#  from the start point to end point. 
class ShortestRoute:
    ## @brief Constructor for ShortestRoute
    #  @details Contructor accepts 3 parameters for map network, list of stop GPS coordinates, and weight type.
    #  @param networkGraph NetworkGraph for the map network of street, roads, and walkways. 
    #  @param listOfStops list of tuples consisting of the stop points GPS coordinates. 
    #  @param optimizer string for the weight type on the graph's edges.  
    #  @throws InvalidWeightException Raised when the inputted optimizer is not a subset of {time, length}
    def __init__(self, networkGraph, listOfStops, optimizer = "time"):
        try:
            if optimizer not in ["time", "length"]:
                raise InvalidWeightException
            else:
                self.graph = networkGraph
                self.nodes = self.findNodes(listOfStops, networkGraph)
                self.wt = optimizer
                self.routes = self.shortestPath(networkGraph, self.nodes, optimizer)
        except InvalidWeightException:
            print("InvalidWeightException: Invalid input for weight type! Enter either time or length.")
        
    ## @brief This function finds nodes on the network graph for the episode's stop points. 
    #  @param listOfStops list of tuples consisting of the stop points GPS coordinates. 
    #  @param graphInput NetworkGraph for the map network of street, roads, and walkways. 
    #  @return a list of graph nodes.
    def findNodes(self, listOfStops, graphInput):
        listOfNodes = []
        for stop in listOfStops:
            listOfNodes.append(graphInput.getNearestNode(stop))
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

# inputOne = [(-23.546498,-46.691141),(-23.558094,-46.660205),(-23.635039,-46.641239),
#                 (-23.645996,-46.641027),(-23.625882,-46.640936),(-23.618245,-46.639139),
#                 (-23.6130583,-46.637918),(-23.598541,-46.636634),(-23.589342,-46.634677),
#                 (-23.567615,-46.649027),(-23.56357,-46.653893),(-23.581203,-46.638489),
#                 (-23.5754,-46.6407),(-23.568521,-46.63990),(-23.561435,-46.638534)]
# NetworkGraph1 = NetworkGraph(inputOne[0], (-23.561435,-46.638534), inputOne, "drive")
# shortestrouteone = ShortestRoute(NetworkGraph1, inputOne)
# route_map = ox.plot_route_folium(NetworkGraph1.graph, shortestrouteone.routes[0], route_color='#ff0000', opacity=0.5)
# for i in range(1,len(shortestrouteone.routes)):
#      route_map = ox.plot_route_folium(NetworkGraph1.graph, shortestrouteone.routes[i], route_map=route_map, route_color='#0000ff', opacity=0.5)
# filepath = "C:/Users/sweet/anaconda3/envs/capstone/data/route_test_graph.html"
# route_map.save(filepath)
# IFrame(filepath, width=600, height=500)
