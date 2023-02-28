## @file PreProcessing.py
#  @title PreProcessing
#  @author Moksha Srinivasan 400181518
#  @date Feb 1st, 2023

import csv
import pandas as pd
from CustomExceptions import *
import re

#@brief this function confirms that CSV is valid and updates to correct column names, removing invalid data
#@param csvpath - a full path to the input CSV file
#@return Bool - if the data is valid -> true, if valid, the data is processed and written to a new file with the name of the original file concatenated with _processed
def ValidateCSV(csvpath):
    df = pd.read_csv(csvpath)
    try: 
        #check to see if it has fields latitude, longitude, and time in column titles
        counter = 0
        for col in df.columns:
            print("The column name is:"+ col + "and counter value is" + str(counter))
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
            #remove unused columns
            df = df[['lat', 'long', 'time']]
            df = df.dropna(subset=['lat', 'long', 'time'])

            dmslat = re.compile('/^[\+-]?(([1-8]?\d)\D+([1-5]?\d|60)\D+([1-5]?\d|60)(\.\d+)?|90\D+0\D+0)\D+[NSns]?$/')
            dmslong = re.compile('/^[\+-]?([1-7]?\d{1,2}\D+([1-5]?\d|60)\D+([1-5]?\d|60)(\.\d+)?|180\D+0\D+0)\D+[EWew]?$/')
            #convert to DD from DMS if DMS format detected
            if dmslat.match(df.iloc[0]['lat']):
                df['lat'] = df['lat'].apply(DMStoDD)
            if dmslong.match(df.iloc[0]['long']):
                df['long'] = df['long'].apply(DMStoDD)

            #Invalid Latitude: max/min 90.0000000 to -90.0000000
            #Invalid Longitude: max/min 180.0000000 to -180.0000000
            df = df[(df['lat'] >= -90.0) & (df['lat'] <= 90.0)]
            df = df[(df['long'] >= -180.0) & (df['long'] <= 180.0)]
            
            newFilename = csvpath.split('.csv')
            filenameFinal = newFilename[0]+"_processed"+".csv"
            df.to_csv(filenameFinal)
            return True 
            
        raise InvalidInputDataException

    except InvalidInputDataException: 
        raise Exception("InvalidInputDataException: invalid input, you do not have all required columns (latitude, longitude, time)") 


def DMStoDD(dmsstring):
    deg, minutes, seconds, direction =  re.split('[°\'"]', dmsstring)
    return (float(deg) + float(minutes)/60 + float(seconds)/(60*60)) * (-1 if direction in ['W', 'S'] else 1)


#ValidateCSV("/home/moksha/4G06/Capstone-yoGERT/src/exampleDataset.csv")

#print(DMStoDD('78°55\'44.29458\"N'))
#print(DMStoDD('124° 4\' 58\" W'))