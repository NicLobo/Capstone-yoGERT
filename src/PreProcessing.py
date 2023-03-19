## @file PreProcessing.py
#  @title PreProcessing
#  @author Moksha Srinivasan 400181518
#  @date March 18th, 2023

import pandas as pd
from CustomExceptions import *
import re
import os
import datetime
from dateutil.parser import parse

#@brief this function confirms that CSV is valid and updates to correct column names, removing invalid data
#@param csvpath - a full path to the input CSV file
#@param directory_name - directory that will be created to store processed traces
#@return fileNameFinal - the full path of the file written to
#@return Bool - if the data is valid -> true, if valid, the data is processed and written to a new file within the specified directory
def Validate_CSV(csv_path, directory_name):
    df = pd.read_csv(csv_path)
    try: 
        #check to see if it has fields latitude, longitude, and time in column titles
        counter = 0
        for col in df.columns:
            if col == 'lat' or col == 'latitude' or col == "Latitude":
                df = df.rename({col: 'lat'}, axis='columns')
                counter+=1
            elif col == 'long' or col == 'longitude' or col == 'Longitude':
                df = df.rename({col: 'long'}, axis='columns')
                counter+=1
            elif col == 'time' or col == "Time":
                df = df.rename({col: 'time'}, axis='columns')
                counter+=1

        if counter == 3:
            try: 
                os.mkdir(directory_name)
            except OSError:
                raise Exception('Failed to create directory') 

            df = df.dropna(subset=['lat', 'long', 'time'])

            #creating regexps to match lat and long, avoids constant recompilation
            lat_regex = re.compile(r'^(-?\d{1,2}(?:\.\d+)?)[°\s](\d{1,2}(?:\.\d+)?)[\'\s](\d{1,2}(?:\.\d+)?)["\s]?([NSns])?$')
            lon_regex = re.compile(r'^(-?\d{1,3}(?:\.\d+)?)[°\s](\d{1,2}(?:\.\d+)?)[\'\s](\d{1,2}(?:\.\d+)?)["\s]?([EWew])?$')

            #convert to DD from DMS if DMS format detected
            if re.match(lat_regex, str(df.iloc[0]['lat'])):
                df['lat'] = df['lat'].apply(dms_to_dd, args=(lat_regex,))
            if re.match(lon_regex, (str(df.iloc[0]['long']))):
                df['long'] = df['long'].apply(dms_to_dd, args=(lon_regex,))

            df = df.astype({'lat':'float'})
            df = df.astype({'long':'float'})

            #Invalid Latitude: max/min 90.0000000 to -90.0000000
            #Invalid Longitude: max/min 180.0000000 to -180.0000000
            df = df[(df['lat'] >= -90.0) & (df['lat'] <= 90.0)]
            df = df[(df['long'] >= -180.0) & (df['long'] <= 180.0)]

            #convert time format to %Y-%m-%d %H:%M:%S.%f           
            df['time'] = df['time'].apply(convert_time_format)

            dfs = []
            #case 1: multiple IDs in a trace
            id_names = ['id','ID','fid','FID']
            for id_name in id_names: 
                if id_name in df:
                    dfs = [group[1] for group in df.groupby(id_name)]
                    for i, each_df in enumerate(dfs):
                        filename_final = os.path.join(os.path.abspath(directory_name), "trace"+str(i)+".csv")
                        df = df[['lat', 'long', 'time']]
                        each_df.to_csv(filename_final)
                        
                    print("Success: Your processed file(s) now reside in: " + str(os.path.join(os.path.abspath(directory_name))))
                    return str(os.path.join(os.path.abspath(directory_name))), True
                else: 
                    pass

            #case 2: one ID in a trace
            df = df[['lat', 'long', 'time']]
            new_filename = os.path.join(os.path.abspath(directory_name), "trace"+str(0)+".csv")
            df.to_csv(new_filename)
            return str(new_filename), True
        else: 
            raise InvalidInputDataException 


    except InvalidInputDataException: 
        raise Exception("InvalidInputDataException: invalid input, you do not have all required columns (latitude, longitude, time)") 

#@brief this function converts DMS format lat/long to DD
#@param dmsstring - a string containing the dms value
#@param regex - the corresponding regex value for the lat or long
#@return float with the correct dd representation
def dms_to_dd(dms_string, regex):
    match = regex.match(dms_string)
    if not match:
        raise ValueError(f"{dms_string} is not a valid DMS string")
        
    degrees = float(match.group(1))
    minutes = float(match.group(2))
    seconds = float(match.group(3))
    hemisphere = match.group(4)
    
    dd = degrees + (minutes / 60) + (seconds / 3600)
    if hemisphere in ['S', 's', 'W', 'w']:
        dd *= -1     
    return dd

#@brief this function converts unknown time formats to accepted format for the toolbox "%Y-%m-%d %H:%M:%S.%f"
#@param time_string - string value to be converted
#@return string with correct formatting
def convert_time_format(time_string):
    dt = parse(time_string)
    return dt.strftime('%Y-%m-%d %H:%M:%S.%f')