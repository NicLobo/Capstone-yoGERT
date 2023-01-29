import osmnx as ox
import networkx as nx
import h3
import NetworkGraph
import ShortestRoute

class AlternativeRoute:
    def __init__(self, listOfStops, optimizer = "length"):
        self.network = NetworkGraph(listOfStops[0], listOfStops[len(listOfStops)-1], listOfStops, "bike")
        self.path = ShortestRoute(self.network, listOfStops, optimizer)

# alternativeOne = AlternativeRoute(inputOne)
# MapRoute(alternativeOne.network.graph, alternativeOne.path.routes, "C:/Users/sweet/anaconda3/envs/capstone/data/Alterroute_test_graph.html")
        
