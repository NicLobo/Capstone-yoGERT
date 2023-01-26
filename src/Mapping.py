import osmnx as ox
import networkx as nx
import h3
import NetworkGraph
from IPython.display import IFrame
import folium

def MapRoute(graph, routes, savePath):
    route_map = ox.plot_route_folium(graph, routes[0], route_color='#ff0000', opacity=0.5)
    for i in range(1,len(routes)):
        route_map = ox.plot_route_folium(graph, routes[i], route_map=route_map, route_color='#0000ff', opacity=0.5)
    filepath = savePath
    route_map.save(filepath)
    IFrame(filepath, width=600, height=500)

def MapActivityLocation(activityLocations, activityLocationsDescription, savePath):
    base = folium.Map(location=[activityLocations[0][0], activityLocations[0][1]], zoom_start=10)
    tooltip = "Activity Location"
    for i in range(0, len(activityLocations)):
        base.add_child(folium.Marker([activityLocations[i][0],activityLocations[i][1]], popup=activityLocationsDescription[i], 
                        tooltip=tooltip, icon=folium.Icon(color="green", icon="info-sign")))
    filepath = savePath
    base.save(filepath)
    IFrame(filepath, width=600, height=500)

def MapEpisodePoints(GPSCoords, savePath):
    base = folium.Map(location=[GPSCoords[0][0], GPSCoords[0][1]], zoom_start=10)
    tooltip = "Episode Stop"
    for point in GPSCoords:
        base.add_child(folium.Marker([point[0], point[1]], tooltip=tooltip))
    base.save(savePath)
    IFrame(savePath, width=600, height=500)
