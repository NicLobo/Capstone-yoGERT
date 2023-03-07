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
from ActivityLocation import *
from IPython.display import IFrame
import folium
from Point import * 
from branca.element import Template, MacroElement
from Mapping import *

traceFilePath = "trace1.csv"
episodeFilePath = "1_episode.csv"
NGT = NetworkGraph(traceFilePath, "drive", False)
NGE = NetworkGraph(episodeFilePath)
SRT = ShortestRouteTrace(NGT, traceFilePath)
SRE = ShortestRouteEpisode(NGE, episodeFilePath)
AR = AlternativeRoute(traceFilePath) 
activityFilePath = "trace-activityLocation.csv"
stopFilePath = "stops.csv"

MapRoute(NGT, SRT, "test_TraceRouteMap.html")
MapRoute(NGE, SRE, "test_EpisodeRouteMap.html")
MapRoute(AR.network, AR.path, "test_AlternativeRouteMap.html")
MapActivityLocation(activityFilePath, stopFilePath, "test_ActivityLocationMap.html")
MapEpisodePoints(episodeFilePath, "test_EpisodeMap")