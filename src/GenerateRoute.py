import osmnx as ox
import networkx as nx
import h3
import NetworkGraph
import ShortestRoute
import AlternativeRoute

def GenerateGraph(stopPoints, detectedMode):
    return NetworkGraph(stopPoints[0], stopPoints[len(stopPoints)-1], stopPoints, detectedMode)

def GenerateShortestPath(graphNetwork, stopPoints, optimizer):
    return ShortestRoute(graphNetwork, stopPoints, optimizer)

def GenerateAlternativePath(stopPoints, optimizer):
    return AlternativeRoute(stopPoints, optimizer)
