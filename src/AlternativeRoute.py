## @file AlternativeRoute.py
#  @title AlternativeRoute
#  @author Abeer Alyasiri 400198787
#  @date January 31 2023

import osmnx as ox
import networkx as nx
import h3
from NetworkGraph import *
from ShortestRouteTrace import * 
from ShortestRouteStop import * 
from CustomExceptions import * 
from Point import * 

## @brief A class representing an object that represents the alternative route for an entity's trace. 
#  @details This representation of the alternative route will include the enttire trace or trace's important stop points 
#  from the start point to end point. 
class AlternativeRoute:
    ## @brief Constructor for AlternativeRoute
    #  @details Contructor accepts 2 parameters for list of stop GPS coordinates, and weight type.
    #  @param filePath string for the path to the csv file consisting of Point type consisting of the GPS coordinates for the trace. 
    #  @param optimizer string for the weight type on the graph's edges.  
    #  @param filePathStops string for the path to the csv file consisting of Point type consisting of the GPS coordinates for the stop points  
    #  @throws InvalidWeightException Raised when the inputted optimizer is not a subset of {time, length}
    #  @throws EmptyFilePathException Raised when input file path is empty
    def __init__(self, filePath, optimizer = "length", filePathStops = None):
        try:
            if optimizer not in ["time", "length"]:
                raise InvalidWeightException
            elif filePath == "" or filePathStops == "":
                raise EmptyFilePathException
            else:
                self.network = NetworkGraph(filePath, "bike", False, True)
                if filePathStops != None:
                    self.path = ShortestRouteStop(self.network, filePathStops, optimizer)
                else:
                    self.path = ShortestRouteTrace(self.network, filePath, optimizer)
                print("Alternative Route was successfully created!")
        except InvalidWeightException:
            print("InvalidWeightException: Invalid input for weight type! Enter either time or length.")
        except EmptyFilePathException:
            print("EmptyFilePathException: Input file path is empty. Please enter a file path to a trace.")
    
