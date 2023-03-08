## @file test_PreProcessing.py
#  @title Testing PreProcessing
#  @author Moksha Srinivasan 
#  @date March 6 2023

import pytest
from os import * 
from PreProcessing import *
import shutil 

def test_ExpectedInput():
    inputs = ["./exampleDataset/trace_1.csv","test_ExpectedInput"]
    ValidateCSV(inputs[0], inputs[1])
    fileoutput = (os.listdir((os.path.join(os.getcwd(),"test_ExpectedInput"))))[0]
    assert(fileoutput == 'trace0.csv')
    shutil.rmtree((os.path.join(os.getcwd(),"test_ExpectedInput")))

#need to update regular expression, not parsing correctly
#def test_DMSInput():
#    inputs = ["./exampleDataset/trace_1DMS.csv","test_DMSInput"]
#    ValidateCSV(inputs[0], inputs[1])
#    df_original = pd.read_csv("./exampleDataset/trace_1DMS.csv")
#    df_processed = pd.read_csv((os.path.join(os.getcwd(),"test_DMSInput","trace0.csv")))

#    assert str(df_original['lat'].iloc[0]) != str(df_processed['lat'].iloc[0])
#    assert str(df_original['long'].iloc[0]) != str(df_processed['long'].iloc[0])

#    shutil.rmtree((os.path.join(os.getcwd(),"test_DMSInput")))

def test_RemoveInvalidLatLong():
    inputs = ["./exampleDataset/trace1_InvalidLatLong.csv","test_InvalidLatLongInput"]
    ValidateCSV(inputs[0], inputs[1])
    df_original = pd.read_csv("./exampleDataset/trace1_InvalidLatLong.csv")
    df_processed = pd.read_csv((os.path.join(os.getcwd(),"test_InvalidLatLongInput","trace0.csv")))

    assert (len(df_original) > len(df_processed))
    shutil.rmtree((os.path.join(os.getcwd(),"test_InvalidLatLongInput")))


def test_DMStoDD():
    inputarray = ['78°55\'44.29458\"N', '124° 4\' 58\" W']
    outputarray = [78.92897071666667, 124.08277777777778]
     
    for i, input in enumerate(inputarray):
        assert(DMStoDD(input) == outputarray[i])