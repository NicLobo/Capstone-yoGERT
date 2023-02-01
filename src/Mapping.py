## @file Mapping.py
#  @title Mapping
#  @author Abeer Alyasiri 400198787
#  @date January 31 2023

import osmnx as ox
import networkx as nx
import h3
import NetworkGraph
from IPython.display import IFrame
import folium

## @brief This function maps a route and saves it as an interactive file.
#  @param graph NetworkGraph graph that represents the base streats, roads, and walkways for the map.
#  @param mode string of the mode of transportation. 
#  @param routes list of graph nodes to be connected to form a route.
#  @param savePath string of where the interactive will be saved. 
def MapRoute(graph, mode, routes, savePath):
    if mode == "drive":
        color = '#00FF00'
    elif mode == "walk":
        color = '#0000FF'
    else:
        color = '#FF00FF'
    route_map = ox.plot_route_folium(graph, routes[0], color=color, opacity=0.5)
    for i in range(1,len(routes)):
        route_map = ox.plot_route_folium(graph, routes[i], route_map=route_map, color=color, opacity=0.5)
    filepath = savePath
    route_map.save(filepath)
    IFrame(filepath, width=600, height=500)

## @brief This function plots activity locations as markers on a map and saves it as an interactive file.
#  @param activityLocations list of tuples of the GPS coordinates for the identified activity locations. 
#  @param activityLocationsDescription list of string that describes the activity locations.
#  @param savePath string of where the interactive will be saved. 
def MapActivityLocation(activityLocations, activityLocationsDescription, savePath):
    base = folium.Map(location=[activityLocations[0][0], activityLocations[0][1]], zoom_start=10)
    tooltip = "Activity Location"
    for i in range(0, len(activityLocations)):
        base.add_child(folium.Marker([activityLocations[i][0],activityLocations[i][1]], popup=activityLocationsDescription[i], 
                        tooltip=tooltip, icon=folium.Icon(color="green", icon="info-sign")))
    filepath = savePath
    base.save(filepath)
    IFrame(filepath, width=600, height=500)

## @brief This function plots episode GPS coordinates as markers on a map and saves it as an interactive file.
#  @param GPSCoords list of tuples of the GPS coordinates. 
#  @param GPSCoords list of date time stamp for GPS coordinates.
#  @param modes list of string that describes mode of transportation at each GPS coordinate.
#  @param savePath string of where the interactive will be saved. 
def MapEpisodePoints(GPSCoords, timestamps, modes, savePath):
    base = folium.Map(location=[GPSCoords[0][0], GPSCoords[0][1]], zoom_start=10)
    for i in range(0, len(GPSCoords)):
        tooltip = timestamps[i]
        if modes[i] == "drive":
            color = "green"
            icon="car-side"
        elif modes[i] == "walk":
            color = "blue"
            icon="person-walking"
        else:
            color = "red"
            icon="circle-stop"
        base.add_child(folium.Marker([GPSCoords[i][0],GPSCoords[i][1]], 
                        tooltip=tooltip, icon=folium.Icon(color=color, icon=icon, prefix="fa")))
    base.save(savePath)
    IFrame(savePath, width=600, height=500)
