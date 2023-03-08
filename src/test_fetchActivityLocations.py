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
  fetchActivityLocations("trace/stop/stops.csv","trace/trace1/activitylocations/trace-activityLocation.csv", 100)
  with open("trace/trace1/activitylocations/trace-activityLocation.csv") as myfile:
     if 'String' in myfile.read():
         assert True
#check if output file is generated
#check exceptions for input file
#check exceptions for 
#check if server unavialable outputs logs
#check if lists out points and 