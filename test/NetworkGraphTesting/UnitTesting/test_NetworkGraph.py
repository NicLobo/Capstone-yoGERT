## @file test_NetworkGraph.py
#  @title Testing NetworkGraph
#  @author Abeer Alyasiri 400198787
#  @date March 4 2023

import pytest 
from NetworkGraph import *
import osmnx as ox
import h3
import networkx as nx
from CustomExceptions import *
from Point import *
from Transformation import *

traceFilePath = "./trace1.csv"
GPSCoord = (43.60902479751416, -79.69011484642793)
OutGPSCoord = (43.59937567752286, -79.67924717546673)
incorrectMode = "stop"
episodeFilePath = "./1_episode.csv"
emptyFilePath = ""

# Test 6.2.1.1
def test_CreateNetworkGraphFromTrace():
    NG = NetworkGraph(traceFilePath, "drive", False)
    assert type(NG.graph) == nx.classes.multidigraph.MultiDiGraph

# Test 6.2.1.2
def test_CreateNetworkGraphFromEpisode():
    NG = NetworkGraph(episodeFilePath)
    assert type(NG.graph) == nx.classes.multidigraph.MultiDiGraph

# Test 6.2.1.3
def test_GetNearestNode():
    NG = NetworkGraph(traceFilePath, "drive", False)
    nearestNode = NG.getNearestNode(GPSCoord)
    assert nearestNode in NG.graph

# Test 6.2.1.4
def test_GetGraphMode():
    NG = NG = NetworkGraph(traceFilePath, "drive", False)
    mode = NG.getMode()
    assert mode == "drive"

# Test 6.2.1.5
def test_GetNearestNodeBoundsException(capsys):
    NG = NetworkGraph(traceFilePath, "drive", False)
    NG.getNearestNode(OutGPSCoord)
    captured = capsys.readouterr()
    assert "OutOfBoundsCoordException" in captured.out

# Test 6.2.1.6
def test_CreateNetworGraphModeException(capsys):
    NetworkGraph(traceFilePath, incorrectMode, False)
    captured = capsys.readouterr()
    assert "InvalidModeException" in captured.out

# Test 6.2.1.7
def test_CreateNetworGraphFileException(capsys):
    NetworkGraph(emptyFilePath, "drive", False)
    captured = capsys.readouterr()
    assert "EmptyFilePathException" in captured.out
