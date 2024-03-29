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
from ShortestRouteStop import *
from AlternativeRoute import *
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
    <li><i class="fa-solid fa-circle-stop" style="font-size:20px;color:red;"></i> Stop</li>
    <li><i class="fa-solid fa-car-side" style="font-size:20px;color:green;"></i> Drive</li>
    <li><i class="fa-solid fa-person-walking" style="font-size:20px;color:blue;"></i> Walk</li>
    <li><i class="fa-solid fa-map-pin" style="font-size:20px;color:gray;"></i> Ping</li>
    <li><i class="fa-solid fa-circle-info" style="font-size:20px;color:orange;"></i> Activity Location</li>
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
#  @return a boolean to indicate if the mapping file was successfully created. 
#  @throws InvalidRouteTypeException Raised when the input route type is not ShortestRouteTrace or ShortestRouteEpisode
#  @throws EmptyFilePathException Raised when input file path is empty
#  @throws InvalidMappingFilePathException Raised when the input file path does not have the file name.html
def MapRoute(networkGraph, route, savePath):
    try:
        if not (isinstance(route, ShortestRouteTrace) or isinstance(route, ShortestRouteEpisode) or isinstance(route, ShortestRouteStop)):
            raise InvalidRouteTypeException
        elif savePath == "":
            raise EmptyFilePathException
        elif ".html" not in savePath:
            raise InvalidMappingFilePathException
        elif networkGraph.getMode() == "drive" or networkGraph.getMode() == "mode.DRIVE":
            colorR = '#00FF00'
        elif networkGraph.getMode() == "walk" or networkGraph.getMode() == "mode.WALK":
            colorR = '#0000FF'
        elif networkGraph.getMode() == "bike" or networkGraph.getMode() == "mode.BIKE":
            colorR = '#800080'
        else:
            colorR = '#FF00FF'
        # plot the points used 
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
            elif isinstance(route, ShortestRouteTrace):
                color = "gray"
                icon="map-pin"
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
        print("Route was mapped successfully and saved at " + savePath)
        return True
    except InvalidRouteTypeException:
        print("InvalidRouteTypeException: invalid route input type. Please input with ShortestRouteTrace or ShortestRouteEpisode")
    except EmptyFilePathException:
        print("EmptyFilePathException: Input file path is empty. Please enter a file path where the map should be save.")
    except InvalidMappingFilePathException:
        print("InvalidMappingFilePathException: Input file path does not include the file name .html. Please include the name, for example: ./dir/dir/fileName.html")

## @brief This function plots activity locations as markers on a map and saves it as an interactive file.
#  @param activityLocationsFile string of path to the csv file containitng the output of ActivityLocation module. 
#  @param stopPointsFile string of path to the csv file of the GPS coordinates used to find the identified stop points from the episode generation.
#  @param savePath string of where the interactive will be saved. 
#  @return a boolean to indicate if the mapping file was successfully created. 
#  @throws EmptyFilePathException Raised when input file path is empty
#  @throws InvalidMappingFilePathException Raised when the input file path does not have the file name.html
def MapActivityLocation(activityLocationsFile, stopPointsFile, savePath):
    try:
        if activityLocationsFile == "" or savePath == "": 
            raise EmptyFilePathException
        elif ".html" not in savePath:
            raise InvalidMappingFilePathException 
        activityLocations = convertActivityCSV(activityLocationsFile)
        stopPoints = stoprelated(stopPointsFile)
        base = folium.Map(location=[stopPoints[0].lat, stopPoints[0].lon], zoom_start=10)
        tooltip = "Activity Location"
        for point in stopPoints:
            base.add_child(folium.Marker([point.lat,point.lon], 
                            tooltip="TraceID:"+str(point.episodeID), icon=folium.Icon(color="red", icon="stop", prefix="fa")))
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
        print("Activity locations was mapped successfully and saved at " + savePath)
        return True
    except EmptyFilePathException:
        print("EmptyFilePathException: Input file path is empty. Please enter a file path for the activity location data or for where the map should be save.")
    except InvalidMappingFilePathException:
        print("InvalidMappingFilePathException: Input file path does not include the file name .html. Please include the name, for example: ./dir/dir/fileName.html")

## @brief This function plots episode GPS coordinates as markers on a map and saves it as an interactive file.
#  @param GPSCoords string of the path to the csv file consisting of GPS coordinates for an episode. 
#  @param savePath string of where the interactive will be saved. 
#  @return a boolean to indicate if the mapping file was successfully created. 
#  @throws EmptyFilePathException Raised when input file path is empty
#  @throws InvalidMappingFilePathException Raised when the input file path does not have the file name.html
def MapEpisodePoints(GPSCoordsFile, savePath):
    try:
        if GPSCoordsFile == "" or savePath == "": 
            raise EmptyFilePathException
        elif ".html" not in savePath:
            raise InvalidMappingFilePathException 
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
        print("Episodes were mapped successfully and saved at " + savePath)
        return True
    except EmptyFilePathException:
        print("EmptyFilePathException: Input file path is empty. Please enter a file path for the episode data or for where the map should be save.")
    except InvalidMappingFilePathException:
        print("InvalidMappingFilePathException: Input file path does not include the file name .html. Please include the name, for example: ./dir/dir/fileName.html")


