import overpy
import pandas as pd
import json
import requests
import ActivityLocation
import StopPoint


def fetchActivityLocations(latitude, longitude):
    newStop = StopPoint.StopPoint(latitude, longitude)
    tolerance = 25 #tolerance of the surrounding areas in meters
    long_lat_tol_query_str = str(tolerance)+''',''' + str(latitude) +''','''+ str(longitude)
    activityLocationList = []
    activityLocationIndex = []
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
    # print(data_frame)
    for column_name in data_frame:
        # print(column_name)
        if not any(x in column_name for x in ("name", "longitude", "latitude")): # check to see if any column names dont contain "name", "longitude", latitude
            data_frame.drop(column_name, axis=1, inplace=True) # drop the columns if above is true
    # print(data_frame)
    #first checks name column if there is one and stores in a list of activity locations and then removes both the column and the rows for optimation purposes 
    if "name" in data_frame.columns:
        for row in data_frame.itertuples():
            # print(row)
            if str(row.name) != "nan":
                #creates new activity locaiton object containging name and latitude, longitude information
                newActivityLocation = ActivityLocation.ActivityLocation(str(row.name), row.latitude, row.longitude)
                # activityLocationList.append(str(row.name))
                activityLocationList.append(newActivityLocation) # Add activity location object to list of activity locations
                activityLocationIndex.append(row.Index) # add index of row to indexList to ensure there are not any duplicates
                data_frame.drop(row.Index, inplace=True) #DROP COLUMN WITH COLUMN NAME NAME
        data_frame.drop("name", axis=1, inplace=True)

    # print(activityLocationList)
    return (newStop, activityLocationList) #returns a tuple containting the stop point and a list of activity locaitons near stop point
    # print(data_frame)                              # return data frame if you want to use it further in main function.


def fetchStopAL(list_of_stops):
    list_of_stops_AL = []
    for i in list_of_stops:
        stopALTupple= fetchActivityLocations(i[0],i[1])
        list_of_stops_AL.append(stopALTupple)
    for i in list_of_stops_AL:
        print(i[0].lat,i[0].lon )
        for x in i[1]:
            print(x.name, x.lat, x.lon)
    return list_of_stops_AL

    


    
listStops = [(43.645914,-79.392435), (43.645914,-79.392435), (43.645914,-79.392435)]
fetchStopAL(listStops)
