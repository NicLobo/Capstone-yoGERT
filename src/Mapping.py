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
from branca.element import Template, MacroElement

# Global variables 
template = """
{% macro html(this, kwargs) %}

<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.0/css/all.css"></link>

  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
  
  <script>
  $( function() {
    $( "#maplegend" ).draggable({
                    start: function (event, ui) {
                        $(this).css({
                            right: "auto",
                            top: "auto",
                            bottom: "auto"
                        });
                    }
                });
});

  </script>
</head>
<body>

 
<div id='maplegend' class='maplegend' 
    style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
     border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'>
     
<div class='legend-title'>Legend</div>
<div class='legend-scale'>
  <ul class='legend-labels'>
    <li><i class="fa-solid fa-circle-stop" style="font-size:20px;color:red;"></i>Stop</li>
    <li><i class="fa-solid fa-car-side" style="font-size:20px;color:green;"></i>Drive</li>
    <li><i class="fa-solid fa-person-walking" style="font-size:20px;color:blue;"></i>Walk</li>
    <li><i class="fa-solid fa-circle-info" style="font-size:20px;color:orange;"></i>Activity Location</li>
    <li><i class="fa fa-route" style="font-size:20px;color:green;"></i> Drive Route</li>
    <li><i class="fa fa-route" style="font-size:20px;color:blue;"></i> Walk Route</li>
    <li><i class="fa fa-route" style="font-size:20px;color:purple;"></i> Bike Route</li>
  </ul>
</div>
</div>
 
</body>
</html>

<style type='text/css'>
  .maplegend .legend-title {
    text-align: left;
    margin-bottom: 5px;
    font-weight: bold;
    font-size: 90%;
    }
  .maplegend .legend-scale ul {
    margin: 0;
    margin-bottom: 5px;
    padding: 0;
    float: left;
    list-style: none;
    }
  .maplegend .legend-scale ul li {
    font-size: 80%;
    list-style: none;
    margin-left: 0;
    line-height: 18px;
    margin-bottom: 2px;
    }
  .maplegend ul.legend-labels li span {
    display: block;
    float: left;
    height: 16px;
    width: 30px;
    margin-right: 5px;
    margin-left: 0;
    border: 1px solid #999;
    }
  .maplegend .legend-source {
    font-size: 80%;
    color: #777;
    clear: both;
    }
  .maplegend a {
    color: #777;
    }
</style>
{% endmacro %}"""

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
        tooltip = "ID:" + str(point.episodeID) + ", T:" + str(point.time)
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
    macro = MacroElement()
    macro._template = Template(template)
    route_map.get_root().add_child(macro)
    filepath = savePath
    route_map.save(filepath)
    IFrame(filepath, width=600, height=500)
    return 0

## @brief This function plots activity locations as markers on a map and saves it as an interactive file.
#  @param activityLocationsFile string of path to the csv file containitng the output of ActivityLocation module. 
#  @param stopPointsFile string of path to the csv file of the GPS coordinates used to find the identified stop points from the episode generation.
#  @param savePath string of where the interactive will be saved. 
def MapActivityLocation(activityLocationsFile, stopPointsFile, savePath):
    activityLocations = convertActivityCSV(activityLocationsFile)
    stopPoints = stoprelated(stopPointsFile)
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
    macro = MacroElement()
    macro._template = Template(template)
    base.get_root().add_child(macro)
    filepath = savePath
    base.save(filepath)
    IFrame(filepath, width=600, height=500)
    return 0

## @brief This function plots episode GPS coordinates as markers on a map and saves it as an interactive file.
#  @param GPSCoords string of the path to the csv file consisting of GPS coordinates for an episode. 
#  @param savePath string of where the interactive will be saved. 
def MapEpisodePoints(GPSCoordsFile, savePath):
    GPSCoords = episoderelated(GPSCoordsFile)
    base = folium.Map(location=[GPSCoords[0].lat, GPSCoords[0].lon], zoom_start=10)
    for point in GPSCoords:
        tooltip = "EpisodeID: " + str(point.episodeID) + ", T: " + str(point.time)
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
    macro = MacroElement()
    macro._template = Template(template)
    base.get_root().add_child(macro)
    base.save(savePath)
    IFrame(savePath, width=600, height=500)
    return 0

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
