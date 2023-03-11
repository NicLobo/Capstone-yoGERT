## @file fetchActiviyLocations.py
#  @title Fetch Activiy Locations
#  @author Smita Singh 400173853
#  @date Feb 28 2022

#imports
import overpy
import pandas as pd
import ActivityLocation
import Transformation
import csv
import logging
from CustomExceptions import *



def getResult(api, built_query):
    serverFree = 1
    try:
        # get result from API by sending the query to overpass servers
        result = api.query(built_query)               
    except overpy.exception.OverpassGatewayTimeout:
        try:
            raise OverpassGatewayTimeout
        except:
            serverFree = 0
            print("Overpass server is at capacity! Please try again later")
    except overpy.exception.OverpassTooManyRequests:
        try:
            raise OverpassTooManyRequests
        except:
            serverFree = 0
            print("Overpass server is at capacity! Please try again later")
    return result, serverFree

## @brief This function takes latitude and longitude values of a stop point and a tolerance 
#  @param latitude float the latitude of the stop point
#  @param longitude float the latitude of the stop point
#  @param tol int tolerance for the radius of nearby activity locations
#  @return a tuple containing the stop point object and a list of ActivityLocation objects
def fetchALForIndividualPoint(stopPoint, tol):
    tolerance = tol #tolerance of the surrounding areas in meters

    # initializing empty list, we'll use it to append ActivityLocation objects
    activityLocationList = []
    activityLocationIndex = []

    #Query to be sent to the api to fetch activity location
    long_lat_tol_query_str = str(tolerance)+''',''' + str(stopPoint.lat) +''','''+ str(stopPoint.lon)
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

    result, serverFree = getResult(api, built_query)

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
            return (stopPoint, activityLocationList)
    else:
        logging.warning("Stop point: "+ str(stopPoint.lat)+ ", "+ str(stopPoint.lon) + " activity locations not found due to sever being unavailable")
        return None

    

## @brief This function takes a list of Stop Points and tolerance and calls local helper function 
# to create a list of tuples(Stop Point, List of ActivityLocation)
#  @param list_of_stops list of stops
#  @param tol int tolerance for the radius of nearby activity locations
#  @return a list of tuples consisting of Point object and a list of ActivityLocation objects)
def fetchActivityLocations(inPath, outPath,  tol=25):
    # creating a list of points based on csv file path provided
    listStops =[]
    try:
        try:
            listStops = Transformation.stoprelated(inPath)
        except:
           raise InvalidInputFileException
    except:
         print("Input file is invalid")

    # initializing empty list, we'll use it to append stop Point object and list of ActivityLocation objects
    list_of_stops_AL = []
    for i in listStops:
        stopALTupple= fetchALForIndividualPoint(i, tol)
        list_of_stops_AL.append(stopALTupple)


    listActivities =[]
    convertedResult = Transformation.convertActivityLocation(list_of_stops_AL)
    listActivities.append(convertedResult)

    # Write result to a csv file
    try:
        try:
            with open(outPath, 'w', newline='') as outputFile:
                fileWriter = csv.writer(outputFile)
                # Create Header
                fileWriter.writerow(['Latitude', 'Longitude', 'Nearby Activity Locations'])

                # Write each rows
                for i in convertedResult:
                    fileWriter.writerow([i[0],i[1],i[2]])
        except:
            raise WritingFileException
    except:
            print("Error writing to output file")


    return 0
    
# fetchActivityLocations("trace/trace1/stop/stops.csv","trace/trace-activityLocation.csv", 500)
# fetchActivityLocations("../test/csvdata/stops.csv","", 500)


