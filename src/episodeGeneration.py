# @file createEpisode.ipynb
# @author Team GIS Gang
# @brief This notebook aims to generate Trip Episodes based on the given datasets of points

import pandas as pd
import os
import subprocess
import geopandas as gpd
import time
import datetime
from os.path import join
import numpy as np
import h3
import geopy.distance
import geopy as gp

#os.chdir("../src/")
path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)

#INPUT TRACE.CSV
#OUTPUT POINTS.CSV

# @param csv_path:
# @param title:
# @return an .csv file that consists of points
def createSegments(csv_path, title):

     # Create Segment Directory

    try: 
        os.mkdir(str(title))
        print("Directory Segment Created ") 

    except FileExistsError:
        print("Directory Segment already exists")

    #Reads csv and store in data frame
    df = pd.read_csv(csv_path)
    df = df[["lat","long","fid","time"]]
    df['time']= pd.to_datetime(df['time'])
    df['index_column'] = df.index

    segments = df['fid'].unique()

    for i in segments: 
        newdf = df.loc[df['fid'] == i]
        newdf = newdf.reset_index()
        #Calculate stepsize using start and end time of dataset
        starttime = pd.to_datetime(newdf['time'].iloc[0])
        endtime = pd.to_datetime(newdf['time'].iloc[-1])
        totaltime = pd.Timedelta(endtime - starttime).seconds 

        if(totaltime == 0):
            stepsize = 1
        else:
            stepsize = (round(len(newdf)/totaltime)) 

        #Trim points based on step size
        if(stepsize != 0):
            newdf = newdf.drop(newdf[newdf.index_column%stepsize !=0].index)
            newdf = newdf.reset_index()
        newdf = newdf[["lat","long","fid","time"]]




        #Create trace directory in segment directory
        try: 
            path = "./"+str(title)+"/segment-"+str(i)
            os.mkdir(path)
            print("Directory " , path ,  " Created ") 
        except FileExistsError:
            print("Directory " , path ,  " already exists")


        #Saves trip points to csv file 
        newdf.to_csv(path+"/points.csv", index=False)
        createVelocities(path)

#INPUT POINTS.CSV
#OUTPUT VELOCITIES.CSV
def createVelocities(csv_path):
    
    #Join the points cvs file by index n and n+1
    df = pd.read_csv(csv_path+"/points.csv")
    df2= df.iloc[:-1 , :]
    df1 = df.tail(-1)
    df1 = df1.reset_index()


    velocities = pd.DataFrame(columns= ["start_lat","start_long","end_lat","end_long","start_time","end_time","total_time","total_distance","velocity"])
    velocities["start_lat"] = df1["lat"]
    velocities["start_long"] = df1["long"]
    velocities["end_lat"] = df2["lat"]
    velocities["end_long"] = df2["long"]
    velocities["start_time"] = pd.to_datetime(df1['time'])
    velocities["end_time"] =  pd.to_datetime(df2['time'])
    velocities["total_time"] = (velocities["end_time"] - velocities["start_time"]).dt.total_seconds().abs()
    velocities['total_distance'] = velocities.apply(lambda x: gp.distance.distance((x[0], x[1]), (x[2], x[3])).m, axis=1)
    velocities['velocity'] = velocities['total_distance'] / (velocities['total_time'])

    #Saves trip segement to csv file
    velocities.to_csv(csv_path+"/velocities.csv", index=False)
    generateEpisodes(csv_path)


from enum import Enum
class mode(Enum):
    STOP = 0
    WALK = 1
    DRIVE = 10


#INPUT VELOCITY.CSV
#OUTPUT EPISODE.CSV
def generateEpisodes(csv_path):

    df = pd.read_csv(csv_path+"/velocities.csv") 
    episode= pd.DataFrame(columns= ["start_lat","start_long","end_lat","end_long","start_time","end_time","mode"])

    startVel = df['velocity'].iloc[0] 
    startIndex = 0
    currMode = mode.STOP
    endIndex = 0

    if( startVel >= mode.WALK.value and startVel < mode.DRIVE.value):
        currMode = mode.WALK
    
    elif(startVel >= mode.DRIVE.value):
        currMode = mode.DRIVE

    for index in range(1,len(df)):

        prevIndex = index - 1
        endVel =  df['velocity'].iloc[index]
        endMode = currMode
        noChange = True
        
        starttime = pd.to_datetime(df['start_time'].iloc[startIndex])
        endtime = pd.to_datetime(df['end_time'].iloc[index])
        totaltime = pd.Timedelta(endtime - starttime).seconds 

        if( endVel >= mode.WALK.value and endVel < mode.DRIVE.value):
            endMode = mode.WALK
        elif(endVel >= mode.DRIVE.value):
            endMode = mode.DRIVE
        else: 
            endMode = mode.STOP

        if(currMode != endMode):

            new_row = [df['start_lat'].iloc[startIndex] ,
                df['start_long'].iloc[startIndex] ,
                df['end_lat'].iloc[index] ,
                df['end_long'].iloc[index] ,
                df['start_time'].iloc[startIndex],
                df['end_time'].iloc[index],
                currMode]    

            episode.loc[len(episode)] = new_row
            currMode = endMode
            startIndex = prevIndex


        if( index == len(df)-1 and noChange):
            new_row = [df['start_lat'].iloc[startIndex] ,
                df['start_long'].iloc[startIndex] ,
                df['end_lat'].iloc[index] ,
                df['end_long'].iloc[index] ,
                df['start_time'].iloc[startIndex],
                df['end_time'].iloc[index],
                currMode]    

            episode.loc[len(episode)] = new_row
            currMode = endMode
            startIndex = prevIndex


    episode.to_csv(csv_path+"/episode.csv", index=False)
    cleanEpisode(csv_path)

def cleanEpisode(csv_path):
    episode = pd.read_csv(csv_path+"/episode.csv") 
    droplist = []


    for index in range(len(episode)):
        starttime = pd.to_datetime(episode['start_time'].iloc[index]) 
        endtime = pd.to_datetime(episode['end_time'].iloc[index])
        timePassed = pd.Timedelta(endtime - starttime).seconds 

        if(episode['mode'].iloc[index] == 'mode.STOP' and timePassed < 60 and index <len(episode)-1):
            droplist.append(index)
            episode['start_time'].iloc[index+1] =  starttime



    episode = episode.drop(droplist)
    episode = episode.reset_index(drop=True)

    
    lenwalk = len(episode.loc[episode['mode'] == 'mode.DRIVE'])
    lendrive = len(episode.loc[episode['mode'] == 'mode.WALK '])

    if(lenwalk <= lendrive):
        summaryepisode = episode.loc[episode['mode'] == 'mode.DRIVE']
        summaryepisode = summaryepisode.loc[:,'mode']
        summaryepisode = summaryepisode.head(1)
        summaryepisode.to_csv(csv_path+"/summary_episode.csv", index=False)

    else: 
        summaryepisode = episode.loc[episode['mode'] == 'mode.WALK']
        summaryepisode = summaryepisode.loc[:,'mode']
        summaryepisode = summaryepisode.head(1)
        summaryepisode.to_csv(csv_path+"/summary_episode.csv", index=False)

    stopepisode = episode.loc[episode['mode'] == 'mode.STOP']
    episode.to_csv(csv_path+"/episode.csv", index=False)
    stopepisode.to_csv(csv_path+"/stop_episode.csv", index=False)
    
createSegments("../src/exampleDataset/data1.csv","data1")
# createVelocities("./Segment/trace1")
# generateEpisodes("./Segment/trace1")
# cleanEpisode("./Segment/trace1")

# createSegments("../src/exampleDataset/trace_2.csv","trace2")
# createVelocities("./Segment/trace2")
# generateEpisodes("./Segment/trace2")
# cleanEpisode("./Segment/trace2")

# createSegments("../src/exampleDataset/trace_3.csv","trace3")
# createSegments("./exampleDataset/trace_3.csv","trace3") 
# createVelocities("./Segment/trace3")
# generateEpisodes("./Segment/trace3")
# cleanEpisode("./Segment/trace3")