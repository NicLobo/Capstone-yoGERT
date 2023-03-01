## @file fetchActiviyLocations.py
#  @title Fetch Activiy Locations
#  @author Smita Singh 400173853
#  @date Feb 28 2022

#imports
import overpy
import pandas as pd
import ActivityLocation
import Point



## @brief This function takes latitude and longitude values of a stop point and a tolerance 
#  @param latitude float the latitude of the stop point
#  @param longitude float the latitude of the stop point
#  @param tol int tolerance for the radius of nearby activity locations
#  @return a tuple containing the stop point object and a list of ActivityLocation objects
def fetchALForIndividualPoint(latitude, longitude, tol):
    newStop = Point.Point(latitude, longitude)
    tolerance = tol #tolerance of the surrounding areas in meters

    # initializing empty list, we'll use it to append ActivityLocation objects
    activityLocationList = []
    activityLocationIndex = []

    #Query to be sent to the api to fetch activity location
    long_lat_tol_query_str = str(tolerance)+''',''' + str(latitude) +''','''+ str(longitude)
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
    
    # creating a overpass API instance 
    api = overpy.Overpass()                      


    #check if the api is available
    serverFree = 1
    try:
        # get result from API by sending the query to overpass servers
        result = api.query(built_query)               
    except overpy.exception.OverpassGatewayTimeout:
        serverFree = 0
        print("Overpass server is at capacity! Please try again later")
    except overpy.exception.OverpassTooManyRequests:
        serverFree = 0
        print("Overpass server is at capacity! Please try again later")

    if (serverFree == 1):
        # initializing empty list , we'll use it to form a dataframe.
        list_of_node_tags = []   
        # from each node , get the all tags information                     
        for node in result.nodes:                     
            node.tags['latitude'] =  node.lat
            node.tags['longitude'] = node.lon
            node.tags['id'] = node.id
            list_of_node_tags.append(node.tags)

        # forming a pandas dataframe using list of dictionaries
        data_frame = pd.DataFrame(list_of_node_tags)  

        #drop unnecessary columns in dataframe for efficency in iterations
        for column_name in data_frame:
             # check to see if any column names dont contain "name", "longitude", latitude
            if not any(x in column_name for x in ("name", "longitude", "latitude", "amenity")):
                # drop the columns if above is true
                data_frame.drop(column_name, axis=1, inplace=True) 
       
        #first checks if theres a name column 
        #then iterates through each row in data table to see if there a name for the activity location
        #then creates a new activity location object
        if "name" in data_frame.columns:
            for row in data_frame.itertuples():
                if str(row.name) != "nan":
                    #creates new activity location object containging name and latitude, longitude information
                    newActivityLocation = ActivityLocation.ActivityLocation(str(row.name), row.latitude, row.longitude, row.amenity)
                    # Add activity location object to list of activity locations
                    activityLocationList.append(newActivityLocation) 
                    # add index of row to indexList to ensure there are not any duplicates
                    activityLocationIndex.append(row.Index)
                    #DROP COLUMN WITH COLUMN NAME NAME
                    data_frame.drop(row.Index, inplace=True) 
            return (newStop, activityLocationList)
    else:
        return None

    

## @brief This function takes a list of Stop Points and tolerance and calls local helper function 
# to create a list of tuples(Stop Point, List of ActivityLocation)
#  @param list_of_stops list of stops
#  @param tol int tolerance for the radius of nearby activity locations
#  @return a list of tuples consisting of Point object and a list of ActivityLocation objects)
def fetchActivityLocations(list_of_stops, tol=25):
    # initializing empty list, we'll use it to append stop Point object and list of ActivityLocation objects
    list_of_stops_AL = []
    for i in list_of_stops:
        stopALTupple= fetchALForIndividualPoint(i[0],i[1], tol)
        list_of_stops_AL.append(stopALTupple)

    if not list_of_stops_AL:
        return []
    else:
        for i in list_of_stops_AL:
            if(i != None):
                print("############",i[0].lat,i[0].lon)
                for x in i[1]:
                    print(x.name, x.lat, x.lon, x.amenity)
        return list_of_stops_AL


listStops = [(43.645914,-79.392435), (43.6531750, -79.3757559), (43.65021, -79.38047),(43.66017343856208, -79.3864813628639,(43.76448579392273, -79.74858754763592))]
# listStops = [(43.76448579392273, -79.74858754763592)]

fetchActivityLocations(listStops)
