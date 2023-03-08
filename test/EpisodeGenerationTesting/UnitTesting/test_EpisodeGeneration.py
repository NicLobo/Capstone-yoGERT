## @file test_episodeGeneration.py
#  @title Testing episodeGeneration
#  @author Nicholas Lobo 400179304
#  @date March 8 2023
 
import pytest  
import geopandas as pd
from episodeGeneration import *
from pandas.testing import *

EG = EpisodeGeneration()


csv_path = "../src/test/EpisodeGenerationTesting/UnitTesting/test_csv/trace_1.csv"
full_path= "../src/test/EpisodeGenerationTesting/UnitTesting/test_trace/trace"


correct_trace = "../src/test/EpisodeGenerationTesting/UnitTesting/correct_trace/trace.csv"
correct_segment = "../src/test/EpisodeGenerationTesting/UnitTesting/correct_trace/segments.csv"
correct_uncleanstop = "../src/test/EpisodeGenerationTesting/UnitTesting/correct_trace/unclean_stops.csv"
correct_stop = "../src/test/EpisodeGenerationTesting/UnitTesting/correct_trace/stops.csv"
correct_episodes="../src/test/EpisodeGenerationTesting/UnitTesting/correct_trace/episode"
distol = 500
timetol = 60

distol2 = 60
timetol2 = 500
# Test 6.2.6.1
def test_CreateTrace(csv_path,full_path):
    EG.createTrace(csv_path,full_path)
    dfc = pd.read_csv(full_path+"/trace.csv")
    dft = pd.read_csv(correct_trace) 
    assert_frame_equal(dfc, dft)   

# Test 6.2.6.2
def test_CreateSegment(full_path):
    EG.createSegments(full_path)
    dfc = pd.read_csv(full_path+"/segment.csv")
    dft = pd.read_csv(correct_trace) 
    assert_frame_equal(dfc, dft)   

# Test 6.2.6.3
def test_FindStops(full_path):
    EG.findStops(full_path)
    dfc = pd.read_csv(full_path+"/unclean_stops.csv")
    dft = pd.read_csv(correct_trace) 
    assert_frame_equal(dfc, dft)   

# Test 6.2.6.4
def test_CleanStops(full_path,timetol,distol):
    EG.cleanStops(full_path,timetol,distol)
    dfc = pd.read_csv(full_path+"/stops.csv")
    dft = pd.read_csv(correct_trace) 
    assert_frame_equal(dfc, dft)   


# Test 6.2.6.5
def test_CleanStops(full_path,timetol2,distol2):
    EG.cleanStops(full_path,timetol2,distol2)
    dfc = pd.read_csv(full_path+"/stops.csv")
    dft = pd.read_csv(correct_trace) 
    assert_frame_equal(dfc, dft)   

# Test 6.2.6.6
def test_createEpisodes(full_path):
    episode_len = len([name for name in os.listdir('../src/test/EpisodeGenerationTesting/UnitTesting/test_trace/episode') if os.path.isfile(name)])
    assert episode_len == 6

