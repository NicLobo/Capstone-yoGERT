## @file AlternativeRoute.py
#  @title AlternativeRoute
#  @author Abeer Alyasiri 400198787
#  @date January 31 2023

import osmnx as ox
import networkx as nx
import h3
from NetworkGraph import *
from ShortestRouteTrace import * 
from CustomExceptions import * 
from Point import * 

## @brief A class representing an object that represents the alternative route for an entity's trace. 
#  @details This representation of the alternative route will include the epsiode's important stop points 
#  from the start point to end point. 
class AlternativeRoute:
    ## @brief Constructor for AlternativeRoute
    #  @details Contructor accepts 2 parameters for list of stop GPS coordinates, and weight type.
    #  @param filePath list of Point type consisting of the GPS coordinates for the trace. 
    #  @param optimizer string for the weight type on the graph's edges.  
    #  @throws InvalidWeightException Raised when the inputted optimizer is not a subset of {time, length}
    def __init__(self, filePath, optimizer = "length"):
        try:
            if optimizer not in ["time", "length"]:
                raise InvalidWeightException
            else:
                self.network = NetworkGraph(filePath, "bike", False, True)
                self.path = ShortestRouteTrace(self.network, filePath, optimizer)
        except InvalidWeightException:
            print("InvalidWeightException: Invalid input for weight type! Enter either time or length.")
    

# alternativeOne = AlternativeRoute(inputTwoStops)
# MapRoute(alternativeOne.network, alternativeOne.path, "C:/Users/sweet/anaconda3/envs/capstone/data/Alterroute_test_graph.html")
# alternativeOne = AlternativeRoute("C:/Users/sweet/anaconda3/envs/capstone/data/stops.csv")
