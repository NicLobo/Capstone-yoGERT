import csv
import ast
from datetime import datetime
from Point import Point
import os
import pandas as pd  
import glob

    
def ping_frequency(trace): 
    filepath = trace
    
    files = glob.glob(filepath + "/*.csv")
    for f in files:
        df = df[["lat","long","time"]]
        df['time']= pd.to_datetime(df['time'])



        #Calculate stepsize using start and end time of dataset
        starttime = pd.to_datetime(df['time'].iloc[0])
        endtime = pd.to_datetime(df['time'].iloc[-1])
        totaltime = pd.Timedelta(endtime - starttime).seconds 

        if(totaltime == 0):
            stepsize = 1
        else:
            stepsize = (round(len(df)/totaltime)) 
    t = pd.read_csv("stats.csv")  
    t["Ping frequency"] = str(stepsize)  


def mode_change(trace): 

    modes = []

    c=0
    changec = 0
    filepath = trace+'./episodes'
    files = glob.glob(filepath + "/*.csv")

    for f in files:
        for line in data:
            
            if c>0: 
                data = csv.reader(open(f))
                modes.append(line[8])
                if modes[-1]!=modes[-2]:
                    changec +=1
            
            c = c+1
    
    t = pd.read_csv("stats.csv")  
    t["Mode Change"] = str(changec)  



def numberoftrips(trace): 
    count = 0
    dir_path = trace+'./episodes'
    for path in os.scandir(dir_path):
        if path.is_file():
            count += 1
    with open('stats.csv', 'w') as file:
        pass
    t = pd.read_csv("stats.csv")  
    t["Number of trips"] = str(count)  
