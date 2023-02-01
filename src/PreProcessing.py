import csv
import pandas as pd
import re

#an alternative, and possibly more robust method
def validateCSV(csvpath):
    df = pd.read_csv(csvpath)

    #check to see if it has fields latitude, longitude, and time in column titles
    counter = 0
    for col in df.columns:
        if col == 'lat' or col == 'latitude' or col == "Latitude":
            counter+=1
        elif col == 'long' or col == 'longitude' or col == 'Longitude':
            counter+=1
        elif col == 'time' or col == "Time":
            counter+=1

    if counter == 3:
        return True

    raise Exception("invalid input, you do not have all required columns (latitude, longitude, time)")  

