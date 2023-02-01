## @file ALternativeRoute.py
#  @title AlternativeRoute
#  @author Abeer Alyasiri 400198787
#  @date January 31 2023

import osmnx as ox
import networkx as nx
import h3
from NetworkGraph import *
from ShortestRoute import * 
from CustomExceptions import * 

## @brief A class representing an object that represents the alternative route for a travel epsiode. 
#  @details This representation of the alternative route will include the epsiode's important stop points 
#  from the start point to end point. 
class AlternativeRoute:
    ## @brief Constructor for AlternativeRoute
    #  @details Contructor accepts 2 parameters for list of stop GPS coordinates, and weight type.
    #  @param listOfStops list of tuples consisting of the stop points GPS coordinates. 
    #  @param optimizer string for the weight type on the graph's edges.  
    #  @throws InvalidWeightException Raised when the inputted optimizer is not a subset of {time, length}
    def __init__(self, listOfStops, optimizer = "length"):
        try:
            if optimizer not in ["time", "length"]:
                raise InvalidWeightException
            else:
                self.network = NetworkGraph(listOfStops[0], listOfStops[len(listOfStops)-1], listOfStops, "bike")
                self.path = ShortestRoute(self.network, listOfStops, optimizer)
        except InvalidWeightException:
            print("InvalidWeightException: Invalid input for weight type! Enter either time or length.")
    

# alternativeOne = AlternativeRoute(inputOne)
# MapRoute(alternativeOne.network.graph, alternativeOne.path.routes, "C:/Users/sweet/anaconda3/envs/capstone/data/Alterroute_test_graph.html")
        
