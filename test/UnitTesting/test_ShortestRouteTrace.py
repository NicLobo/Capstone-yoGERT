## @file test_ShortestRouteTrace.py
#  @title Testing ShortestRouteTrace
#  @author Abeer Alyasiri 400198787
#  @date March 4 2023

import pytest 
from NetworkGraph import *
from ShortestRouteTrace import *
import osmnx as ox
import h3
import networkx as nx
from CustomExceptions import *
from Point import *
from Transformation import *

traceFilePath = "./data/trace1.csv"
emptyFilePath = ""
NG = NetworkGraph(traceFilePath, "drive", False)
samplingDistance = 25

# Test 6.2.3.1
def test_CreatingShortestRouteTrace():
    SRT = ShortestRouteTrace(NG, traceFilePath)
    assert type(SRT) == ShortestRouteTrace and len(SRT.routes) <= len(SRT.inputData) - 1

# Test 6.2.3.2
def test_CreatingShortestRouteTraceOptimizerException(capsys):
    ShortestRouteTrace(NG, traceFilePath, "distance")
    captured = capsys.readouterr()
    assert "InvalidWeightException" in captured.out

# Test 6.2.3.3
def test_CreatingShortestRouteTraceFileException(capsys):
    ShortestRouteTrace(NG, emptyFilePath)
    captured = capsys.readouterr()
    assert "EmptyFilePathException" in captured.out