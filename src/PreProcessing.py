## @file PreProcessing.py
#  @title PreProcessing
#  @author Moksha Srinivasan 400181518
#  @date Feb 1st, 2023

import csv
import pandas as pd
from CustomExceptions import *

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

        #Invalid Latitude: max/min 90.0000000 to -90.0000000
        #Invalid Longitude: max/min 180.0000000 to -180.0000000
        #Invalid Time: this depends on the time format, will be updated for Rev1
        if counter == 3:
            df = df[(df['lat'] >= -90.0) & (df['lat'] <= 90.0)]
            df = df[(df['long'] >= -180.0) & (df['long'] <= 180.0)]
            df = df.dropna(subset=['lat', 'long', 'time'])
            newFilename = csvpath.split('.csv')
            filenameFinal = newFilename[0]+"_processed"+".csv"
            df.to_csv(filenameFinal)
            return True 
        raise InvalidInputDataException

    except InvalidInputDataException: 
        raise Exception("InvalidInputDataException: invalid input, you do not have all required columns (latitude, longitude, time)") 

    
#ValidateCSV("/home/moksha/4G06/Capstone-yoGERT/src/exampleDataset.csv")