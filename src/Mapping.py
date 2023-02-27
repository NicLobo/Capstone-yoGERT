## @file Mapping.py
#  @title Mapping
#  @author Abeer Alyasiri 400198787
#  @date January 31 2023

import osmnx as ox
import networkx as nx
import h3
import NetworkGraph
from ShortestRouteEpisode import *
from ShortestRouteTrace import *
from ActivityLocation import *
from IPython.display import IFrame
import folium
from Point import * 

## @brief This function maps a route and saves it as an interactive file.
#  @param networkGraph NetworkGraph object that represents the base streats, roads, and walkways for the map.
#  @param route ShortestRoute object that has information of the route and details of how it was created.
#  @param savePath string of where the interactive map will be saved. 
def MapRoute(networkGraph, route, savePath):
    if networkGraph.getMode() == "drive" or networkGraph.getMode() == "mode.DRIVE":
        colorR = '#00FF00'
    elif networkGraph.getMode() == "walk" or networkGraph.getMode() == "mode.WALK":
        colorR = '#0000FF'
    elif networkGraph.getMode() == "bike" or networkGraph.getMode() == "mode.BIKE":
        colorR = '#800080'
    else:
        colorR = '#FF00FF'
    # plot the points used 
    print(type(route))
    if isinstance(route, ShortestRouteEpisode):
        usedPoints = route.sampledData
    else: 
        usedPoints = route.inputData
    base = folium.Map(location=[usedPoints[0].lat, usedPoints[0].lon], zoom_start=10)
    for point in usedPoints:
        tooltip = "ID:" + str(point.episodeID) + ", T:" + point.time
        if point.mode == "mode.DRIVE":
            color = "green"
            icon="car-side"
        elif point.mode == "mode.WALK":
            color = "blue"
            icon="person-walking"
        else:
            color = "red"
            icon="circle-stop"
        base.add_child(folium.Marker([point.lat,point.lon], 
                                     tooltip=tooltip, icon=folium.Icon(color=color, icon=icon, prefix="fa")))
    # plot the routes on top of it 
    routes = route.routes
    route_map = ox.plot_route_folium(networkGraph.graph, routes[0], route_map=base, color=colorR, opacity=0.7)
    for i in range(1,len(routes)):
        route_map = ox.plot_route_folium(networkGraph.graph, routes[i], route_map=route_map, color=colorR, opacity=0.5)
    # place the legend
    filepath = savePath
    route_map.save(filepath)
    IFrame(filepath, width=600, height=500)

## @brief This function plots activity locations as markers on a map and saves it as an interactive file.
#  @param activityLocations list of ActivityLocation type of the GPS coordinates and description for the identified activity locations. 
#  @param stopPoints list of Point type of the GPS coordinates used to find the identified stop points from the episode generation.
#  @param savePath string of where the interactive will be saved. 
def MapActivityLocation(activityLocations, stopPoints, savePath):
    base = folium.Map(location=[stopPoints[0].lat, stopPoints[0].lon], zoom_start=10)
    tooltip = "Activity Location"
    for point in stopPoints:
        base.add_child(folium.Marker([point.lat,point.lon], 
                        tooltip="Episode"+str(point.episodeID), icon=folium.Icon(color="red", icon="stop", prefix="fa")))
    if (len(activityLocations) > 0):
        for ACL in activityLocations:
            base.add_child(folium.Marker([ACL.lat,ACL.lon], popup="Name:" + ACL.name + ", Amenity:" + ACL.amenity, 
                        tooltip=tooltip, icon=folium.Icon(color="orange", icon="info-sign")))
    #place legend
    filepath = savePath
    base.save(filepath)
    IFrame(filepath, width=600, height=500)

## @brief This function plots episode GPS coordinates as markers on a map and saves it as an interactive file.
#  @param GPSCoords list of Point type of the GPS coordinates. 
#  @param savePath string of where the interactive will be saved. 
def MapEpisodePoints(GPSCoords, savePath):
    base = folium.Map(location=[GPSCoords[0].lat, GPSCoords[0].lon], zoom_start=10)
    for point in GPSCoords:
        tooltip = "EpisodeID: " + str(point.episodeID) + ", T: " + point.time
        if point.mode == "drive" or point.mode == "mode.DRIVE":
            color = "green"
            icon="car-side"
        elif point.mode == "walk" or point.mode == "mode.WALK":
            color = "blue"
            icon="person-walking"
        else:
            color = "red"
            icon="circle-stop"
        base.add_child(folium.Marker([point.lat,point.lon], 
                        tooltip=tooltip, icon=folium.Icon(color=color, icon=icon, prefix="fa")))
    #place legend
    base.save(savePath)
    IFrame(savePath, width=600, height=500)

# # example for activity locations
# stoppoints = [(-23.546498,-46.691141),(-23.558094,-46.660205),(-23.635039,-46.641239),
#                 (-23.645996,-46.641027),(-23.625882,-46.640936),(-23.618245,-46.639139),
#                 (-23.6130583,-46.637918),(-23.598541,-46.636634),(-23.589342,-46.634677),
#                 (-23.567615,-46.649027),(-23.56357,-46.653893),(-23.581203,-46.638489),
#                 (-23.5754,-46.6407),(-23.568521,-46.63990),(-23.561435,-46.638534)]
# activitypoints = [(-23.546498,-46.691141),(-23.558094,-46.660205),(-23.635039,-46.641239)]
# activitydescription = ["mall", "park", "school"]
# MapActivityLocation(activitypoints,activitydescription,stoppoints,"C:/Users/sweet/anaconda3/envs/capstone/data/activity_test_graph.html")

# #example for episode
# stoppoints = [(-23.546498,-46.691141),(-23.558094,-46.660205),(-23.635039,-46.641239)]
# timestamps = ["17:10:05", "17:10:05", "17:10:05"]
# mode = ["drive", "stop", "stop"]
# MapEpisodePoints(stoppoints, timestamps, mode, "C:/Users/sweet/anaconda3/envs/capstone/data/episodeagain_test_graph.html")


# inputTwoStops = [Point(43.651605, -79.386759,"17:22:02", "mode.DRIVE"), 
#             Point(43.655093, -79.385935,"17:22:08", "mode.STOP"), Point(43.655388, -79.385236,"17:22:11", "mode.DRIVE")]
# activitypoints = [ActivityLocation("Lemon Bar", 43.651504, -79.386657, "Juice"), 
#             ActivityLocation("Starbucks", 43.655191, -79.385935, "Coffe Shop"), 
#             ActivityLocation("High Hills", 43.655388, -79.385222, "Park, Picnic")]
# MapActivityLocation(activitypoints,inputTwoStops,"C:/Users/sweet/anaconda3/envs/capstone/data/activity_test_graph2.html")
