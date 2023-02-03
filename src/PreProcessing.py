import csv
import pandas as pd
import re

#ValidateCSV - confirms that CSV is valid and updates to correct column names, removing invalid data
#Inputs - csvpath is a full path to the input CSV file
#Outputs - Bool if the data is valid, if valid, the data is processed and written to a new file with the name of the original file concatenated with _processed
def ValidateCSV(csvpath):
    df = pd.read_csv(csvpath)

    #check to see if it has fields latitude, longitude, and time in column titles
    counter = 0
    for col in df.columns:
        if col == 'lat' or col == 'latitude' or col == "Latitude":
            df = df.rename({col: 'Latitude'}, axis='columns')
            counter+=1
        elif col == 'long' or col == 'longitude' or col == 'Longitude':
            df = df.rename({col: 'Longitude'}, axis='columns')
            counter+=1
        elif col == 'time' or col == "Time":
            df = df.rename({col: 'Time'}, axis='columns')
            counter+=1

    #Invalid Latitude: max/min 90.0000000 to -90.0000000
    #Invalid Longitude: max/min 180.0000000 to -180.0000000
    #Invalid Time: this depends on the time format
    if counter == 3:
        df = df[float(df.Latitude) >= -90 and float(df.Latitude) <= 90]
        df = df[float(df.Longitude) >= -180 and float(df.Longitude) <= 180]
        df = df.dropna(subset=['Latitude', 'Longitude', 'Time'])
        df.to_csv(csvpath+"_processed")
        return True

    else: 
        raise Exception("invalid input, you do not have all required columns (latitude, longitude, time)") 

    
