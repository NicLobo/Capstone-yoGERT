## @file test_AlternativeRoute.py
#  @title Testing AlternativeRoute
#  @author Abeer Alyasiri 400198787
#  @date March 4 2023

import pytest 
from NetworkGraph import *
from ShortestRouteTrace import *
from AlternativeRoute import *
import osmnx as ox
import h3
import networkx as nx
from CustomExceptions import *
from Point import *
from Transformation import *

traceFilePath = "./data/trace1.csv"
emptyFilePath = ""

# Test 6.2.4.1
def test_CreatingAlternativeRoute():
    AR = AlternativeRoute(traceFilePath)
    assert type(AR) == AlternativeRoute and len(AR.path.routes) <= len(AR.path.inputData) - 1

# Test 6.2.3.2
def test_CreatingAlternativeRouteOptimizerException(capsys):
    AlternativeRoute(traceFilePath, "distance")
    captured = capsys.readouterr()
    assert "InvalidWeightException" in captured.out

# Test 6.2.3.2
def test_CreatingAlternativeRouteOptimizerException(capsys):
    AlternativeRoute(emptyFilePath)
    captured = capsys.readouterr()
    assert "EmptyFilePathException" in captured.out