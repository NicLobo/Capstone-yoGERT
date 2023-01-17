import osmnx as ox
import networkx as nx
import h3
from IPython.display import IFrame

ox.config(log_console=True, use_cache=True)
# define the start and end locations in latlng
start_latlng = (43.25011, -79.84963) #(37.78497,-122.43327)
mid_latlng_1 = (43.683334, -79.766670)
end_latlng = (43.651070, -79.347015) #(37.78071,-122.41445)
# location where you want to find your route
place     = 'San Francisco, California, United States'
# find shortest route based on the mode of travel
mode      = 'walk'        # 'drive', 'bike', 'walk'
# find shortest path based on distance or time
optimizer = 'time'        # 'length','time'
# create graph from OSM within the boundaries of some 
# geocodable place(s)
#graph = ox.graph_from_place(place, network_type = mode)
distance = h3.point_dist(start_latlng, end_latlng, unit='m')
distance = distance + 200
graph = ox.graph_from_point(start_latlng, dist=distance, network_type=mode, simplify=False) 

# find the nearest node to the start location
#orig_node = ox.get_nearest_node(graph, start_latlng)
orig_node = ox.nearest_nodes(graph, start_latlng[1], start_latlng[0])
#find the neartest node to the stop 1
mid_node1 = ox.nearest_nodes(graph, mid_latlng_1[1], mid_latlng_1[0])
# find the nearest node to the end location
#dest_node = ox.get_nearest_node(graph, end_latlng)
dest_node = ox.nearest_nodes(graph, end_latlng[1], end_latlng[0])
#  find the shortest path
shortest_route = nx.shortest_path(graph,
                                  orig_node,
                                  dest_node,
                                  weight=optimizer)
#find the shorest path with segment stops
shortest_route1 = nx.shortest_path(graph,
                                  orig_node,
                                  mid_node1,
                                  weight=optimizer)
shortest_route2 = nx.shortest_path(graph,
                                  mid_node1,
                                  dest_node,
                                  weight=optimizer)
#plot the shortest route
shortest_route_map = ox.plot_route_folium(graph, shortest_route)
shortest_route_map
# plot shortest route with stops
routes = [shortest_route1,shortest_route2]
#fig, ax = ox.plot_graph_routes(graph, routes, node_size=0)
route_map = ox.plot_route_folium(graph, routes[0], route_color='#ff0000', opacity=0.5)
route_map = ox.plot_route_folium(graph, routes[1], route_map=route_map, route_color='#0000ff', opacity=0.5)
#save the plot
filepath = "C:/Users/sweet/anaconda3/envs/capstone/data/route_graph2.html"
shortest_route_map.save(filepath)
IFrame(filepath, width=600, height=500)
filepath = "C:/Users/sweet/anaconda3/envs/capstone/data/route_stop_graph.html"
route_map.save(filepath)
IFrame(filepath, width=600, height=500)