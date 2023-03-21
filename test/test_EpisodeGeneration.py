## @file test_episodeGeneration.py
#  @title Testing episodeGeneration
#  @author Nicholas Lobo 400179304
#  @date March 8 2023
 
import pandas as pd
import geopandas as gpd
from pandas.testing import *
import os 
import EpisodeGeneration as EG

csv_path = os.path.join("..","src","exampleDataset","trace_1.csv")
full_path = os.path.join("..","src","test_trace")

correct_trace = os.path.join("..","src","correct_trace","trace.csv")
correct_segment = os.path.join("..","src","correct_trace","segments.csv")
correct_unclean_stop = os.path.join("..","src","correct_trace","stop","unclean_stops.csv")
correct_clean_stop_time = os.path.join("..","src","correct_trace","stop","clean_stops_time.csv")
correct_clean_stop_distance = os.path.join("..","src","correct_trace","stop","clean_stops_distance.csv")
correct_episodes= os.path.join("..","src","correct_trace","episode")
correct_stats= os.path.join("..","src","correct_trace","stats.csv")
correct_summarymode= os.path.join("..","src","correct_trace","summary_mode.csv")

distol = 500
timetol = 50
distol2 = 50
timetol2 = 500

# Test 6.2.6.1
def test_CreateTrace(csv_path,full_path):
    EG.createTrace(csv_path,full_path)
    dft = pd.read_csv(os.path.join(full_path,"trace.csv"))
    dfc = pd.read_csv(correct_trace) 
    assert_frame_equal(dfc, dft)   

# Test 6.2.6.2
def test_CreateSegment(full_path):
    EG.createSegments(full_path)
    dft = pd.read_csv(os.path.join(full_path,"segments.csv"))
    dfc = pd.read_csv(correct_segment) 
    assert_frame_equal(dfc, dft)   

# Test 6.2.6.3
def test_FindStops(full_path):
    EG.findStops(full_path)
    dfc = pd.read_csv(os.path.join(full_path,"stop","stops.csv"))
    dft = pd.read_csv(correct_unclean_stop) 
    assert_frame_equal(dfc, dft)   

# Test 6.2.6.4
def test_CleanStopsTime(full_path,timetol,distol):
    EG.cleanStops(full_path,timetol,distol)
    dfc = pd.read_csv(os.path.join(full_path,"stop","stops.csv"))
    dft = pd.read_csv(correct_clean_stop_time ) 
    assert_frame_equal(dfc, dft)   


# Test 6.2.6.5
def test_CleanStopsDistance(full_path,timetol2,distol2):
    EG.cleanStops(full_path,timetol2,distol2)
    dfc = pd.read_csv(os.path.join(full_path,"stop","stops.csv"))
    dft = pd.read_csv(correct_clean_stop_distance) 
    assert_frame_equal(dfc, dft)   

# Test 6.2.6.6
def test_createEpisodes(full_path):
    EG.createEpisodes(full_path)
    episode_len = len(os.listdir(os.path.join(full_path,"episode")))
    print(episode_len)
    assert episode_len == 6

# Test 6.2.6.7
def test_createSummaryMode(full_path):
    EG.summarymode(full_path)
    dfc = pd.read_csv(os.path.join(full_path,"summary_mode.csv"))
    dft = pd.read_csv(correct_summarymode) 
    assert_frame_equal(dfc, dft)

# Test 6.2.6.8
def test_createStats(full_path):
    EG.createStats(full_path)
    dfc = pd.read_csv(os.path.join(full_path,"stats.csv"))
    dft = pd.read_csv(correct_stats) 
    assert_frame_equal(dfc, dft)


