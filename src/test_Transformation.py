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

tracepath = './trace/trace1/trace.csv'
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
