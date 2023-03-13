import csv
import ast
from datetime import datetime
from Point import Point
import os
import pandas
from csv import writer
import statistics
from statistics import mode
import glob
import pandas as pd  
from ActivityLocation import *
from Transformation import *
#trace file path

tracepath = './trace/trace1/trace.csv'import csv
import ast
from datetime import datetime
from Point import Point
import os
import pandas
from csv import writer
import statistics
from statistics import mode
import glob
import pandas as pd  
from ActivityLocation import ActivityLocation
#
# from Mapping import *
from Transformation import *
#trace file path

tracepath = './trace/trace1/trace.csv'
stoppath = './trace/trace1/stop/stops.csv'
episodepath = './trace/trace1/episode/1_episode.csv'
act1 = ActivityLocation.ActivityLocation('Laser Eye Center', 37.3154678,-121.9757438, 'doctors')
actlist = ['Laser Eye Center', 37.3154678,-121.9757438, 'doctors']
p1 = Point(37.3154678,-121.9757438)
def test_tracerelated(): 
    assert type(tracerelated(tracepath)) == list
    assert type(tracerelated(tracepath)[0]) == Point

def test_stoprelated(): 
    assert type(stoprelated(stoppath)) == list
    assert type(stoprelated(stoppath)[0]) == Point

def test_episoderelated(): 
    assert type(episoderelated(episodepath)) == list
    assert type(episoderelated(episodepath)[0]) == Point

def test_summaryModeTrace():
    assert type(summaryModeTrace(tracepath)) == str

def test_convertActivityLocation():
    assert convertActivityLocation([(p1,[act1])]) == [[p1.lat, p1.lon, [[act1.name,act1.lat,act1.lon, act1.amenity]]]]

def test_convertActivityCSV():
    

stoppath = './trace/trace1/stop/stops.csv'
episodepath = './trace/trace1/episode/1_episode.csv'
def test_tracerelated(): 
    assert type(tracerelated(tracepath)) == list
    assert type(tracerelated(tracepath)[0]) == Point

def test_stoprelated(): 
    assert type(stoprelated(stoppath)) == list
    assert type(stoprelated(stoppath)[0]) == Point

def test_episoderelated(): 
    assert type(episoderelated(episodepath)) == list
    assert type(episoderelated(episodepath)[0]) == Point

def test_summaryModeTrace():
    assert type(summaryModeTrace(tracepath)) == str
