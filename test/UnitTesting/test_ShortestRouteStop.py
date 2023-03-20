## @file test_ShortestRouteStop.py
#  @title Testing ShortestRouteStop
#  @author Abeer Alyasiri 400198787
#  @date March 18 2023

import pytest 
from NetworkGraph import *
from ShortestRouteStop import *
import osmnx as ox
import h3
import networkx as nx
from CustomExceptions import *
from Point import *
from Transformation import *

traceFilePath = "./trace1/trace.csv"
stopFilePath = "./trace1/stop/stops.csv"
emptyFilePath = ""
NG = NetworkGraph(traceFilePath, "drive", False)

# Test 6.2.12.1
def test_CreatingShortestRouteStop():
    SRT = ShortestRouteStop(NG, stopFilePath)
    assert type(SRT) == ShortestRouteStop and len(SRT.routes) <= len(SRT.inputData) - 1

# Test 6.2.12.2
def test_CreatingShortestRouteStopOptimizerException(capsys):
    ShortestRouteStop(NG, stopFilePath, "distance")
    captured = capsys.readouterr()
    assert "InvalidWeightException" in captured.out

# Test 6.2.12.3
def test_CreatingShortestRouteStopFileException(capsys):
    ShortestRouteStop(NG, emptyFilePath)
    captured = capsys.readouterr()
    assert "EmptyFilePathException" in captured.out