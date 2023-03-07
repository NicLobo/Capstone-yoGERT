## @file test_ShortestRouteEpisode.py
#  @title Testing ShortestRouteEpisode
#  @author Abeer Alyasiri 400198787
#  @date March 4 2023

import pytest 
from NetworkGraph import *
from ShortestRouteEpisode import *
import osmnx as ox
import h3
import networkx as nx
from CustomExceptions import *
from Point import *
from Transformation import *

episodeFilePath = "1_episode.csv"
emptyFilePath = ""
NG = NetworkGraph(episodeFilePath, "drive")
samplingDistance = 25

# Test 6.2.2.1
def test_CreatingShortestRouteEpisode():
    SRE = ShortestRouteEpisode(NG, episodeFilePath)
    assert type(SRE) == ShortestRouteEpisode and len(SRE.routes) == len(SRE.sampledData) - 1

# Test 6.2.2.2
def test_CreatingShortestRouteEpisodeCustomized():
    SRE = ShortestRouteEpisode(NG, episodeFilePath, "time", True, samplingDistance)
    assert type(SRE) == ShortestRouteEpisode and len(SRE.routes) == len(SRE.sampledData) - 1

# Test 6.2.2.3
def test_CreatingShortestRouteEpisodeNoSampling():
    SRE = ShortestRouteEpisode(NG, episodeFilePath, "time", False)
    assert type(SRE) == ShortestRouteEpisode and len(SRE.routes) == len(SRE.sampledData) - 1

# Test 6.2.2.4
def test_CreatingShortestRouteEpisodeOptimizerException(capsys):
    ShortestRouteEpisode(NG, episodeFilePath, "distance")
    captured = capsys.readouterr()
    assert "InvalidWeightException" in captured.out
