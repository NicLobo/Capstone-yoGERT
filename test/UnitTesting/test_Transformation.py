## @file test_Transformation.py
#  @title Testing Transfomration
#  @author Niyatha Rangarajan
#  @date March 14 2023

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
from Transformation import *


#Initializing paths and global variables

LOGGER = logging.getLogger(__name__)
tracepath = './trace/trace1/trace.csv'
stoppath = './trace/trace1/stop/stops.csv'
episodepath = './trace/trace1/episode/1_episode.csv'
traceact = './trace/trace-activityLocation.csv'
act1 = ActivityLocation.ActivityLocation('Laser Eye Center', 37.3154678,-121.9757438, 'doctors')
actlist = ['Laser Eye Center', 37.3154678,-121.9757438, 'doctors']
p1 = Point(37.3154678,-121.9757438)

actlist2 = ['Laser Eye Center', 37.3154678,-121.9757438]

## @brief This function tests trace related. It checks if the list produced are valid Point objects.
def test_tracerelated(): 
    assert type(tracerelated(tracepath)) == list
    assert type(tracerelated(tracepath)[0]) == Point

## @brief This function tests stop related. It checks if the list produced are valid Point objects.
def test_stoprelated(): 
    assert type(stoprelated(stoppath)) == list
    assert type(stoprelated(stoppath)[0]) == Point

## @brief This function tests episode related. It checks if the list produced are valid Point objects.
def test_episoderelated(): 
    assert type(episoderelated(episodepath)) == list
    assert type(episoderelated(episodepath)[0]) == Point

## @brief This function tests trace summary mode. It checks if the mode returned is of the right type and value.
def test_summaryModeTrace():
    assert type(summaryModeTrace(tracepath)) == str
    assert (summaryModeTrace(tracepath)) in ['mode.DRIVE','mode.WALK','mode.STOP','mode.MOVING']

## @brief tests if the convertActivityLocation converts activity locations 
# related to a stop point object into a list of their attributes.
def test_convertActivityLocation():
    assert convertActivityLocation([(p1,[act1])]) == [[p1.lat, p1.lon, [[act1.name,act1.lat,act1.lon, act1.amenity]]]]

## @brief tests if the csv given is converted to activity location objects
def test_convertActivityCSV():
    assert ((convertActivityCSV(traceact))[0]).lat == act1.lat
    assert ((convertActivityCSV(traceact))[0]).lon == act1.lon
    assert ((convertActivityCSV(traceact))[0]).name == act1.name
    assert ((convertActivityCSV(traceact))[0]).amenity == act1.amenity

## @brief tests if the list given is converted to an activity location object
def test_convertListToActivityLocationObject():
    assert (convertListToActivityLocationObject(actlist)).lat == act1.lat
    assert (convertListToActivityLocationObject(actlist)).lon == act1.lon
    assert (convertListToActivityLocationObject(actlist)).name == act1.name
    assert (convertListToActivityLocationObject(actlist)).amenity == act1.amenity

## @brief tests if the a wrong file path given to tracerelated() is handled
def test_Fileexception(capsys):
    try:
        tracerelated("")
    except:
        captured = capsys.readouterr()
        assert "FileException: File passed is not valid\n" in captured.out


## @brief tests if the a wrong file path given to stoprelated() is handled
def test_Fileexception2(capsys):
    try:
        stoprelated("")
    except:
        captured = capsys.readouterr()
        assert "FileException: File passed is not valid\n" in captured.out


## @brief tests if the a wrong file path given to episoderelated() is handled
def test_Fileexception3(capsys):
    try:
        episoderelated("")
    except:
        captured = capsys.readouterr()
        assert "FileException: File passed is not valid\n" in captured.out


## @brief tests if the a wrong file path given to summaryModeTrace() is handled
def test_Fileexception4(capsys):
    try:
        summaryModeTrace("")
    except:
        captured = capsys.readouterr()
        assert "FileException: File passed is not valid\n" in captured.out


## @brief tests if the a wrong file path given to  convertActivityCSV() is handled
def test_Fileexception5(capsys):
    try:
        convertActivityCSV("")
    except:
        captured = capsys.readouterr()
        assert "FileException: File passed is not valid\n" in captured.out

## @brief tests if the a wrong file path given to  convertActivityCSV() is handled
def test_FileException6(capsys):
    try:
        convertActivityCSV(actlist2)
    except:
        captured = capsys.readouterr()
        assert "FileException: File passed is not valid\n" in captured.out

## @brief tests if the a wrong list  given to  convertActivityLocation() is handled
def test_ListException1(capsys):
    try:
        convertActivityLocation([([act1])])
    except:
        captured = capsys.readouterr()
        assert "List is not correct" in captured.out


## @brief tests if the a wrong list  given to  convertListToActivityLocationObject() is handled
def test_ListException2(capsys):
    try:
        convertListToActivityLocationObject(actlist2)
    except:
        captured = capsys.readouterr()
        assert "List is not correct" in captured.out
