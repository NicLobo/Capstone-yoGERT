import csv
import ast
from datetime import datetime
from Point import Point
import os
import pandas as pd  
import glob
from csv import writer

    
def ping_frequency(trace): 
    filepath = trace
    
    files = glob.glob(filepath + "/*e.csv")
    print(files)
    for f in files:
        df = pd.read_csv(f)
        #print(df.head(10))
        
        df['time']= pd.to_datetime(df['time'])



        #Calculate stepsize using start and end time of dataset
        starttime = pd.to_datetime(df['time'].iloc[0])
        endtime = pd.to_datetime(df['time'].iloc[-1])
        #print(starttime,endtime)
        totaltime = pd.Timedelta(endtime - starttime).seconds 
        print(totaltime)
        if(totaltime == 0):
            stepsize = 1
        else:
            stepsize = (round(len(df)/totaltime)) 
    
    with open(trace+'/stats.csv', 'w') as f1:
        writer_object = writer(f1)
        writer_object.writerow(['Ping Frequency'])
        writer_object.writerow([str(stepsize) ])
  

def mode_change(trace): 

    modes = []


    changec = 0
    filepath = trace+'/episode'
    files = glob.glob(filepath + "/*.csv")
    print(files)
    filecount = 0
    for f in files:
        data = csv.reader(open(f))
        c = 0
        
        for line in data:
            
            if c>0: 
                
                modes.append(line[4])
                #print(modes)
                filecount+=1
                if filecount >=2:
                    if modes[-1]!=modes[-2]:
                        changec +=1
                    print(modes)
                    print(changec)
                break
            
            c = c+1
    print(changec)
    stats=trace+'/stats.csv'
    t = pd.read_csv(stats)  
    t.insert(1, column = "Mode Change", value = str(changec))  
    t.to_csv(trace+"/stats.csv", index=False)


def numberoftrips(trace): 
    count = 0
    dir_path = trace+'/episode'
    for path in os.scandir(dir_path):
        if path.is_file():
            count += 1
   
    print(count)
    t = pd.read_csv(trace+"/stats.csv")  
    
    t.insert(1, column = "Number of trips", value = str(count))  
    print(t.head(2))
    t.to_csv(trace+"/stats.csv", index=False)

ping_frequency('./trace')
#numberoftrips('./trace')
mode_change('./trace')
