import osmnx as ox
import networkx as nx
import h3
import NetworkGraph
# from IPython.display import IFrame


class ShortestRoute:
    def __init__(self, networkGraph, listOfStops, optimizer = "time"):
        self.graph = networkGraph
        self.nodes = self.findNodes(listOfStops, networkGraph)
        self.wt = optimizer
        self.routes = self.shortestPath(networkGraph, self.nodes, optimizer)
        
    def findNodes(self, listOfStops, graphInput):
        listOfNodes = []
        for stop in listOfStops:
            listOfNodes.append(graphInput.getNearestNode(stop))
        return listOfNodes
    
    def shortestPath(self, graphInput, nodesInput, weightType):
        listOfRoutes = []
        for i in range(0,len(self.nodes)-1):
            listOfRoutes.append(nx.shortest_path(graphInput.graph,nodesInput[i], nodesInput[i+1], weight=weightType))
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