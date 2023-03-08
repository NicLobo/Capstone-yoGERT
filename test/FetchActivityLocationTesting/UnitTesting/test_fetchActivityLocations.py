import os
import logging
import pytest

from fetchActivityLocations import *

def test_outputFileIsGenerated():
  outputPath = "trace/trace1/activitylocations/trace-activityLocation.csv"
  if os.path.exists(outputPath):
      print("removed")
      os.remove(outputPath)
  if not os.path.exists(outputPath):
      print("deleted")

  fetchActivityLocations("trace/stop/stops.csv",outputPath, 500)
  if os.path.exists(outputPath):
      print("worked")
  assert os.path.exists(outputPath)

def test_exceptionNotRaisedWhenInputIsValid(capsys):
    outputPath = "trace/trace1/activitylocations/trace-activityLocation.csv"
    fetchActivityLocations("trace/stop/stops.csv",outputPath, 500)
    captured = capsys.readouterr()
    assert "Input file is invalid" not in captured.out

def test_exceptionRaisedWhenInputIsInvalid(capsys):
    outputPath = "trace/trace1/activitylocations/trace-activityLocation.csv"
    fetchActivityLocations("",outputPath, 500)
    captured = capsys.readouterr()
    assert "Input file is invalid" in captured.out
  
def test_exceptionNotRaisedWhenOutputIsValid(capsys):
    fetchActivityLocations("","trace/trace1/activitylocations/trace-activityLocation.csv", 500)
    captured = capsys.readouterr()
    assert "Error writing to output file" not in captured.out

def test_exceptionRaisedWhenOutputIsInvalid(capsys):
    fetchActivityLocations("trace/stop/stops.csv","", 500)
    captured = capsys.readouterr()
    assert "Error writing to output file" in captured.out

# def test_isApiErrorLogged(mocker,capsys):
#     mock_exception = overpy.exception.OverpassGatewayTimeout
#     mock_exception2 = overpy.exception.OverpassGatewayTimeout
#     mocker.patch("fetchActivityLocations.getResult",side_effect=overpy.exception.OverpassGatewayTimeout)
#     fetchActivityLocations("trace/stop/stops.csv","trace/trace1/activitylocations/trace-activityLocation.csv", 500)
#     captured = capsys.readouterr()
#     assert "Error writing to output file" in captured.out

def test_listOfActivityLocationsCorrect():
  outputPath = "trace/trace1/activitylocations/trace-activityLocation.csv"
  testOutputFile = "../test/csvdata/activityLocationOutputTest.csv"
  if os.path.exists(outputPath):
      print("removed")
      os.remove(outputPath)
  fetchActivityLocations("trace/stop/stops.csv",outputPath, 500)
  with open(outputPath,'r') as f1, open(testOutputFile, 'r') as f2:
      if f1.read() == f2.read():
        assert True
      else:
        assert False



#test if input file given is incorrect in content
#tests if output file syntax is correct
#test with different radiuss
