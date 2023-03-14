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
from ActivityLocation import ActivityLocation
import logging


#
# from Mapping import *
from Transformation import *
#trace file path

LOGGER = logging.getLogger(__name__)
tracepath = './trace/trace1/trace.csv'
stoppath = './trace/trace1/stop/stops.csv'
episodepath = './trace/trace1/episode/1_episode.csv'
traceact = './trace/trace-activityLocation.csv'
act1 = ActivityLocation.ActivityLocation('Laser Eye Center', 37.3154678,-121.9757438, 'doctors')
actlist = ['Laser Eye Center', 37.3154678,-121.9757438, 'doctors']
p1 = Point(37.3154678,-121.9757438)

actlist2 = ['Laser Eye Center', 37.3154678,-121.9757438]
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
    assert ((convertActivityCSV(traceact))[0]).lat == act1.lat
    assert ((convertActivityCSV(traceact))[0]).lon == act1.lon
    assert ((convertActivityCSV(traceact))[0]).name == act1.name
    assert ((convertActivityCSV(traceact))[0]).amenity == act1.amenity

def test_convertListToActivityLocationObject():
    assert (convertListToActivityLocationObject(actlist)).lat == act1.lat
    assert (convertListToActivityLocationObject(actlist)).lon == act1.lon
    assert (convertListToActivityLocationObject(actlist)).name == act1.name
    assert (convertListToActivityLocationObject(actlist)).amenity == act1.amenity

def test_Fileexception(capsys):
    try:
        tracerelated("")
    except:
        captured = capsys.readouterr()
        assert "File path passed is not the correct path" in captured.out

def test_Fileexception2(capsys):
    try:
        stoprelated("")
    except:
        captured = capsys.readouterr()
        assert "File path passed is not the correct path" in captured.out

def test_Fileexception3(capsys):
    try:
        episoderelated("")
    except:
        captured = capsys.readouterr()
        assert "File path passed is not the correct path" in captured.out

def test_Fileexception4(capsys):
    try:
        summaryModeTrace("")
    except:
        captured = capsys.readouterr()
        assert "File path passed is not the correct path" in captured.out

def test_Fileexception5(capsys):
    try:
        convertActivityCSV("")
    except:
        captured = capsys.readouterr()
        assert "File path passed is not the correct path" in captured.out

def test_FileException6(capsys):
    try:
        convertActivityCSV(actlist2)
    except:
        captured = capsys.readouterr()
        assert "File path passed is not the correct path" in captured.out

def test_ListException1(capsys):
    try:
        convertActivityLocation([([act1])])
    except:
        captured = capsys.readouterr()
        assert "List is not correct" in captured.out

def test_ListException2(capsys):
    try:
        convertListToActivityLocationObject(actlist2)
    except:
        captured = capsys.readouterr()
        assert "List is not correct" in captured.out

