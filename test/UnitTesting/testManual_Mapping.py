## @file testManual_Mapping.py
#  @title Testing Mapping
#  @author Abeer Alyasiri 400198787
#  @date March 4 2023

import osmnx as ox
import networkx as nx
import h3
import NetworkGraph
from ShortestRouteEpisode import *
from ShortestRouteTrace import *
from AlternativeRoute import *
from src.ActivityLocation import *
from IPython.display import IFrame
import folium
from Point import * 
from branca.element import Template, MacroElement
from Mapping import *

traceFilePath = "./data/trace1.csv"
episodeFilePath = "./data/1_episode.csv"
NGT = NetworkGraph(traceFilePath, "drive", False)
NGE = NetworkGraph(episodeFilePath)
SRT = ShortestRouteTrace(NGT, traceFilePath)
SRE = ShortestRouteEpisode(NGE, episodeFilePath)
AR = AlternativeRoute(traceFilePath) 
activityFilePath = "./data/trace-activityLocation.csv"
stopFilePath = "./data/stops.csv"

# 6.2.5.1
MapRoute(NGT, SRT, "test_TraceRouteMap.html")
# 6.2.5.2
MapRoute(NGE, SRE, "test_EpisodeRouteMap.html")
# 6.2.5.3
MapRoute(AR.network, AR.path, "test_AlternativeRouteMap.html")
# 6.2.5.4
MapActivityLocation(activityFilePath, stopFilePath, "test_ActivityLocationMap.html")
# 6.2.5.5
MapEpisodePoints(episodeFilePath, "test_EpisodeMap.html")

# 6.2.5.6
MapRoute(NGT, AR, "test_AlternativeRouteMap.html")
# 6.2.5.7
MapRoute(NGT, SRT, "")
# 6.2.5.8
MapRoute(NGT, SRT, "testmappingtrace")
# 6.2.5.9
MapActivityLocation("", stopFilePath, "test_ActivityLocationMap.html")
# 6.2.5.10
MapActivityLocation(activityFilePath, stopFilePath, "testmappingactivitylocations")
# 6.2.5.11
MapEpisodePoints("", "test_EpisodeMap.html")
# 6.2.5.12
MapEpisodePoints(episodeFilePath, "testmappingepisode")