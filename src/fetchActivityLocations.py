import overpy
import pandas as pd
import json
import requests

def fetchActivityLocations(longitude, latitude):
    tolerance = 25 #tolerance of the surrounding areas in meters
    long_lat_tol_query_str = str(tolerance)+''',''' + str(longitude) +''','''+ str(latitude)
    built_query = '''
    [out:json][timeout:25];
    // gather results
    (
    // query part for: “amenity”
    node["amenity"](around:'''+ long_lat_tol_query_str + ''');
    way["amenity"](around:'''+ long_lat_tol_query_str+ ''');
    relation["amenity"](around:'''+ long_lat_tol_query_str+ ''');
    );
    // print results
    out body;
    >;
    out skel qt; 
    '''
    api = overpy.Overpass()                       # creating a overpass API instance 
    result = api.query(built_query)               # get result from API by sending the query to overpass servers


    list_of_node_tags = []                        # initializing empty list , we'll use it to form a dataframe .
    for node in result.nodes:                     # from each node , get the all tags information
        node.tags['latitude'] =  node.lat
        node.tags['longitude'] = node.lon
        node.tags['id'] = node.id
        list_of_node_tags.append(node.tags)
    data_frame = pd.DataFrame(list_of_node_tags)  # forming a pandas dataframe using list of dictionaries

    for column_name in data_frame:
        print(column_name)
        if "name" not in column_name:
            data_frame.drop(column_name, axis=1, inplace=True)
    print(data_frame)                              # return data frame if you want to use it further in main function.



fetchActivityLocations(43.645914,-79.392435)
