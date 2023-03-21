## @file test_PreProcessing.py
#  @title Testing PreProcessing
#  @author Moksha Srinivasan 
#  @date March 6 2023

import pytest
from os import * 
from PreProcessing import *
import shutil 
from CustomExceptions import *

#TC: 6.2.9.1
def test_ExpectedInput():
    inputs = ["./exampleDataset/trace_1.csv","./test_ExpectedInput"]
    Validate_CSV(inputs[0], inputs[1])
    fileoutput = (os.listdir(os.path.join(os.getcwd(),"test_ExpectedInput")))
    assert(fileoutput[0] == 'trace1.csv' and fileoutput[1] == 'trace0.csv')
    shutil.rmtree((os.path.join(os.getcwd(),"test_ExpectedInput")))

#need to update regular expression, not parsing correctly
#TC: 6.2.9.2
#def test_DMSInput():
    # inputs = ["./exampleDataset/trace_1DMS.csv","test_DMSInput"]
    # ValidateCSV(inputs[0], inputs[1])
    # df_original = pd.read_csv("./exampleDataset/trace_1DMS.csv")
    # df_processed = pd.read_csv((os.path.join(os.getcwd(),"test_DMSInput","trace0.csv")))

    # assert str(df_original['lat'].iloc[0]) != str(df_processed['lat'].iloc[0])
    # assert str(df_original['long'].iloc[0]) != str(df_processed['long'].iloc[0])

    # shutil.rmtree((os.path.join(os.getcwd(),"test_DMSInput")))

#TC: 6.2.9.3
def test_RemoveInvalidLatLong():
    inputs = ["./exampleDataset/trace1_InvalidLatLong.csv","test_InvalidLatLongInput"]
    Validate_CSV(inputs[0], inputs[1])
    df_original = pd.read_csv("./exampleDataset/trace1_InvalidLatLong.csv")
    df_processed = pd.read_csv((os.path.join(os.getcwd(),"test_InvalidLatLongInput","trace0.csv")))

    assert (len(df_original) > len(df_processed))
    shutil.rmtree((os.path.join(os.getcwd(),"test_InvalidLatLongInput")))

#TC: 6.2.9.4
def test_DMStoDD():
    inputarray = ['78°55\'44.29458"N', '124°4\'58"W']
    outputarray = [78.92897071666667, -124.08277777777778]
    assert(dms_to_dd(inputarray[0], re.compile(r'^(-?\d{1,2}(?:\.\d+)?)[°\s](\d{1,2}(?:\.\d+)?)[\'\s](\d{1,2}(?:\.\d+)?)["\s]?([NSns])?$')) == outputarray[0])
    assert(dms_to_dd(inputarray[1], re.compile(r'^(-?\d{1,3}(?:\.\d+)?)[°\s](\d{1,2}(?:\.\d+)?)[\'\s](\d{1,2}(?:\.\d+)?)["\s]?([EWew])?$')) == outputarray[1])
#TC: 6.2.9.5
def test_InvalidInputDataException(capsys):
    inputs = ["./exampleDataset/trace_1wrongcolumns.csv","test_ExpectedInput"]
    with pytest.raises(Exception) as exc:
        Validate_CSV(inputs[0], inputs[1])
    assert "invalid input" in str(exc.value)

    
        
    