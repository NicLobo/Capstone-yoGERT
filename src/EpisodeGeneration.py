## @file Episode Generation.py
#  @title Episode Generation
#  @author Nicholas Lobo 400179304
#  @date March 18, 2023

import csv
import os
from csv import writer
import geopy as gp
import pandas as pd
import glob
import statistics
from CustomExceptions import *
import geopy.distance
path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path) 


from enum import Enum
class mode(Enum):
    STOP = 0
    WALK = 2
    DRIVE = 12
    MOVING = 99


## @brief Assigns a unique ID to each GPS ping point of the inputted trace file and creates a new CSV file, called trace.csv, for the trace’s geo-data in the inputted directory path. 
#  @param a full path to the input CSV file.
#  @param a directory path where the new CSV file will be created.
def createTrace(csv_path, tracefolder_fullpath):
    try:
        try: 
            os.mkdir(tracefolder_fullpath)
            print("Trace folder created ") 

        except FileExistsError:
            print("Trace folder already exists")


        df = pd.read_csv(csv_path)
        df = df[["lat","long","time"]]
        df['time']= pd.to_datetime(df['time'])
        starttime = pd.to_datetime(df['time'].iloc[0])
        endtime = pd.to_datetime(df['time'].iloc[-1])
        totaltime = pd.Timedelta(endtime - starttime).seconds 

        if(totaltime == 0):
            stepsize = 1
        else:
            stepsize = (round(len(df)/totaltime)) 

        if(stepsize != 0):
            df = df.drop(df[df.index%stepsize !=0].index)
            df = df.reset_index()
            df = df[["lat","long","time"]]
        
        df.reset_index()
        df['id'] = df.index
        df.to_csv(os.path.join(tracefolder_fullpath,"trace.csv"), index=False)
        print("Trace.csv created") 
    except:
        print("FileException: File passed is not valid")
        raise FileException from None

## @brief Finds segments of the trace.csv file and creates a CSV file for segment information, called segments.csv, in the inputted directory path. 
#  @param  a directory path that contains trace.csv and where the new CSV file will be created.
def createSegments(tracefolder_fullpath):
    try:
        df = pd.read_csv(os.path.join(tracefolder_fullpath,"trace.csv"))
        df2= df.iloc[:-1 , :]
        df1 = df.tail(-1)
        df1 = df1.reset_index()

        velocities = pd.DataFrame(columns= ["start_lat","start_long","end_lat","end_long","start_time","end_time","total_time","total_distance","velocity","start_index","end_index"])
        velocities["start_lat"] = df1["lat"]
        velocities["start_long"] = df1["long"]
        velocities["end_lat"] = df2["lat"]
        velocities["end_long"] = df2["long"]
        velocities["start_time"] = pd.to_datetime(df1['time'])
        velocities["end_time"] =  pd.to_datetime(df2['time'])
        velocities["total_time"] = (velocities["end_time"] - velocities["start_time"]).dt.total_seconds().abs()
        velocities['total_distance'] = velocities.apply(lambda x: gp.distance.distance((x[0], x[1]), (x[2], x[3])).m, axis=1)
        velocities["start_index"] = df2['id']
        velocities["end_index"] =  df1['id']
        velocities['velocity'] = velocities['total_distance'] / (velocities['total_time'])

        velocities.to_csv(os.path.join(tracefolder_fullpath,"segments.csv"), index=False)
        print("Segments csv created") 
    except:
        print("FileException: File passed is not valid")
        raise FileException from None

## @brief Analyzes segments in segments.csv file and creates a CSV file for stop points, called stops.csv, in a newly created directory, called stop, within the input directory path. 
#  @param  a directory path that contains trace.csv and where the new CSV file will be created.
def findStops(tracefolder_fullpath):
    try:
        df = pd.read_csv(os.path.join(tracefolder_fullpath,"segments.csv"))
        episode= pd.DataFrame(columns= ["start_lat","start_long","end_lat","end_long","start_time","end_time","start_index","end_index","mode"])
        startVel = df['velocity'].iloc[0] 
        startIndex = 0
        currMode = mode.STOP
        #moving mode used to isolate for stop episodes 
        if( startVel < mode.WALK.value):
            currMode = mode.STOP
        else:
            currMode = mode.MOVING

        for index in range(1,len(df)):

            endIndex = index - 1
            endVel =  df['velocity'].iloc[endIndex]

            if( endVel < mode.WALK.value):
                endMode = mode.STOP
            else:
                endMode = mode.MOVING

            if(currMode != endMode):
        
                new_row = [df['start_lat'].iloc[startIndex] ,
                    df['start_long'].iloc[startIndex] ,
                    df['end_lat'].iloc[endIndex] ,
                    df['end_long'].iloc[endIndex] ,
                    df['start_time'].iloc[startIndex],
                    df['end_time'].iloc[endIndex],
                    df['start_index'].iloc[startIndex],
                    df['end_index'].iloc[endIndex],
                    currMode]    
                episode.loc[len(episode)] = new_row
                currMode = endMode
                startIndex =index

        episode = episode.loc[(episode['mode'] == mode.STOP)]
        episode['middle_point'] = (episode['start_index'] + episode['end_index'])/2
        stopfolder = os.path.join(tracefolder_fullpath,"stop")

        try: 
                os.mkdir(stopfolder)
                print("Stop folder created ") 

        except FileExistsError:
                print("Stop folder already exists")

        episode.to_csv(os.path.join(stopfolder,"stops.csv"), index=False)
        print("Stops.csv created") 
    except:
        print("FileException: File passed is not valid")
        raise FileException from None



## @brief Updates stops.csv file at the stop directory within the inputted directory path with the inputted filtering parameters. It removes any stop points that don’t satisfy the filtering tolerances. 
#  @param  a directory path that contains the  directory called stop that has stops.csv.
#  @param  a value to filter stops based on distance
#  @param  a value to filter stops based on time
def cleanStops(tracefolder_fullpath, timetol, distol):
    try:
        stopfolder = os.path.join(tracefolder_fullpath,"stop")
        stops= pd.read_csv(os.path.join(stopfolder,"stops.csv")) 
        droplist = []

        for index in range(len(stops)):
            starttime = pd.to_datetime(stops['start_time'].iloc[index]) 
            endtime = pd.to_datetime(stops['end_time'].iloc[index])
            timePassed = pd.Timedelta(endtime - starttime).seconds 
            distance =  gp.distance.distance((stops['start_lat'].iloc[index], stops['start_long'].iloc[index]), (stops['end_lat'].iloc[index], stops['end_long'].iloc[index])).m
            if(timePassed > timetol and index < len(stops)-1 and distol < distance):
                droplist.append(index)
            
        stops = stops.drop(droplist)
        stops.to_csv(os.path.join(stopfolder,"stops.csv"), index=False)
        print("Stops csv filtered with distance tolerance of " +str(distol)+" time tolerance of"+ str(timetol)) 
    except:
        print("FileException: File passed is not valid")
        raise FileException from None



## @brief Analyzes segments in segments.csv file and creates a CSV file for stop points, called stops.csv, in a newly created directory, called stop, within the input directory path. 
#  @param  a directory path that contains the  directory called stop that has stops.csv.
def createEpisodes(tracefolder_fullpath):
    try:
        stopfolder = os.path.join(tracefolder_fullpath,"stop")
        stops= pd.read_csv(os.path.join(stopfolder,"stops.csv")) 
        trace= pd.read_csv(os.path.join(tracefolder_fullpath,"trace.csv")) 
        segments = pd.read_csv(os.path.join(tracefolder_fullpath,"segments.csv"))  
        startindex = 0
        endindex = 0
        eid = 0

        try: 
                os.mkdir(os.path.join(tracefolder_fullpath,"episode"))
                print("Episode folder created ") 

        except FileExistsError:
                print("Episode folder already exists")

        for index, row in stops.iterrows():
            endindex = row['start_index']

            #special case if first episode is a stop episode 
            if (row['start_index'] == 0):
                
                newepisode = trace.loc[row['start_index']:row['end_index']].copy()
                newepisode["mode"] = mode.STOP
                newepisode.to_csv(os.path.join(tracefolder_fullpath,"episode",str(eid)+"_episode.csv"), index=False)
                eid+=1
                startindex = row['end_index'] + 1

            else:
                newepisode = trace.loc[startindex:endindex-1].copy()
                medvelocity = segments.loc[(segments["start_index"] > startindex) & (segments["start_index"] < endindex),['velocity']].copy()
                medvelocity = medvelocity["velocity"].median()
        
                if( medvelocity < mode.DRIVE.value):
                    finalmode = mode.WALK
                else:
                    finalmode = mode.DRIVE

                newepisode["mode"] = finalmode
                newepisode.to_csv(os.path.join(tracefolder_fullpath,"episode",str(eid)+"_episode.csv"), index=False)
                startindex = row['end_index'] + 1
                eid+=1

                newepisode = trace.loc[ row['start_index']: row['end_index']].copy()
                newepisode["mode"] = mode.STOP
                newepisode.to_csv(os.path.join(tracefolder_fullpath,"episode",str(eid)+"_episode.csv"), index=False)
                eid+=1
        
        #special case if there are no stop episodes 
        if (startindex == endindex == 1):
            endindex = len(trace)
            newepisode = trace.loc[startindex:endindex]
            medvelocity = segments.loc[(segments["start_index"] > startindex) & (segments["start_index"] < endindex),['velocity']]
            medvelocity = medvelocity["velocity"].median()

            if( medvelocity < mode.DRIVE.value):
                finalmode = mode.WALK
            else:
                finalmode = mode.DRIVE

            newepisode["mode"] = finalmode
            newepisode.to_csv(os.path.join(tracefolder_fullpath,"episode",str(eid)+"_episode.csv"), index=False)
            startindex = row['end_index'] + 1   
            eid+=1    
        #special case if last episode is a stop episode 
        elif(endindex != len(trace)):
            endindex = len(trace)
            newepisode = trace.loc[startindex:endindex]
            medvelocity = segments.loc[(segments["start_index"] > startindex) & (segments["start_index"] < endindex),['velocity']]
            medvelocity = medvelocity["velocity"].median()

            if( medvelocity < mode.DRIVE.value):
                finalmode = mode.WALK
            else:
                finalmode = mode.DRIVE

            newepisode["mode"] = finalmode
            newepisode.to_csv(os.path.join(tracefolder_fullpath,"episode",str(eid)+"_episode.csv"), index=False)
            startindex = row['end_index'] + 1   
            eid+=1         
    except:
        print("File path passed is not the correct path")
        raise FileException from None
          


## @brief Generates episodes for the inputted geo-data and creates new directories and CSV files to store information on segments, stops, and episodes for the inputted trace information. 
#  @param  a file path for the trace’s geo-data.
#  @param  a directory path that contains the user’s geo-data.
#  @param  a directory name where all the trace’s information should be stored.
#  @param  a time tolerance for the stops default value at 60 seconds.
#  @param  a distance tolerence for stops defaykt value of 60 meters.
def episodeGenerator(csv_path,tracefolder_path,title,disttol = 60, timetol = 60):
    try:
        tracefolder_fullpath = os.path.join(tracefolder_path,title)
        createTrace(csv_path,tracefolder_fullpath)
        createSegments(tracefolder_fullpath)
        findStops(tracefolder_fullpath)
        cleanStops(tracefolder_fullpath,disttol,timetol)
        createEpisodes(tracefolder_fullpath)
        summarymode(tracefolder_fullpath)
        print("Episodes generated successfully")
    except:
        print("File path passed is not the correct path")
        raise FileException from None
   
## @brief Finds the most used travel mode for the inputted trace.csv file and creates a new CSV file containing the summary mode.  
#  @param  a file path that contains trace.csv and where the new CSV file will be created.
def summarymode(tracefilepath):
    try:
        modes = []
        files = glob.glob(os.path.join(tracefilepath,'episode','*.csv'))

        
        for f in files:
            data = csv.reader(open(f))
            c = 0
            
            for line in data:
                
                if c>0 and line[4] != "mode.STOP": 
                    
                    modes.append(line[4])
                    print(line[4])
                    break
                
                c = c+1

        stats=os.path.join(tracefilepath,'summary_mode.csv')
        with open(stats, 'w') as f1:
            writer_object = writer(f1)
            writer_object.writerow(['Summary Mode'])
            writer_object.writerow([str(statistics.mode(modes))])
        print("Summarymodes.csv created successfully")
    except:
        print("File path passed is not the correct path")
        raise FileException from None


## @brief Analyzes the trace’s information and creates a new CSV file, called stats.csv, of ping frequency.
#  @param   a directory path that contains trace.csv and where the new CSV file will be created.
def ping_frequency(trace): 
    try:
        if (os.path.exists(os.path.join(trace,'stats.csv'))):
            os.remove(os.path.join(trace,'stats.csv'))
        
        filepath = os.path.join(trace,'episode')
        files = glob.glob( os.path.join(filepath,"*.csv"))
    
        for f in files:

            df = pd.read_csv(f)
            df['time']= pd.to_datetime(df['time'])
            starttime = pd.to_datetime(df['time'].iloc[0])
            endtime = pd.to_datetime(df['time'].iloc[-1])
            totaltime = pd.Timedelta(endtime - starttime).seconds 
            stepsize1 = 1

            if(totaltime == 0):
                stepsize1 = 1
            else:
                stepsize1 = (round(len(df)/totaltime)) 

            with open( os.path.join(trace,'stats.csv'), 'w') as f1:
                writer_object = writer(f1)
                writer_object.writerow(['Ping Frequency'])
                writer_object.writerow([str(stepsize1) ])
    except:
        print("File path passed is not the correct path")
        raise FileException from None

## @brief Analyzes the trace’s information and creates a new CSV file, called stats.csv of mode change count.
#  @param a directory path that contains trace.csv and where the new CSV file will be created.
def mode_change(trace): 
    try:
        modes = []
        changec = 0
        filepath =  os.path.join(trace,'episodes')
        files = glob.glob( os.path.join(filepath,"*.csv"))
        filecount = 0

        for f in files:
            data = csv.reader(open(f))
            c = 0   
            for line in data:
                if c>0: 
                    modes.append(line[4])
                    filecount+=1
                    if filecount >=2:
                        if modes[-1]!=modes[-2]:
                            changec +=1                  
                        print(changec)
                    break    
                c = c+1
        stats= os.path.join(trace,'stats.csv')
        t = pd.read_csv(stats)  
        t.insert(1, column = "Mode Change", value = str(changec))  
        t.to_csv( os.path.join(trace,"stats.csv"), index=False)
    except:
        print("File path passed is not the correct path")
        raise FileException from None

## @brief Analyzes the trace’s information and creates a new CSV file, called stats.csv, of number of trips
#  @param   a directory path that contains trace.csv and where the new CSV file will be created.
def numberoftrips(trace): 
    try:
        count = 0
        dir_path = trace
        for path in os.scandir(dir_path):
            if path.is_file():
                count += 1
        t = pd.read_csv(os.path.join(trace,"stats.csv"))  
        t.insert(1, column = "Number of trips", value = str(count))  
        t.to_csv( os.path.join(trace,"stats.csv"), index=False)
    except:
        print("File path passed is not the correct path")
        raise FileException from None

## @brief Analyzes the trace’s information and creates a new CSV file, called stats.csv, of ping frequency, mode change count, number of trips, and trace period in the input directory path.
#  @param   a directory path that contains trace.csv and where the new CSV file will be created.
def createStats(fullpath):
    try:
        ping_frequency(fullpath)
        numberoftrips(fullpath)
        mode_change(fullpath)
        print("Stats.csv created successfully")
    except:
        print("FileException: File passed is not valid")
        raise FileException from None
    


