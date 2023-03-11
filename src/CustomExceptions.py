## @file Exceptions.py
#  @title Exceptions
#  @author Abeer Alyasiri 400198787
#  @date January 31 2023

# This file is for custom exceptions to be handled with messages

class InvalidModeException(Exception):
    "Raised when the input value is not a subset of {drive, walk}"
    pass

class OutOfBoundsCoordException(Exception):
    "Raised when the input coordinate is not within the network mapped area"
    pass

class  InvalidWeightException(Exception):
    "Raised when the input value is not a subset of {time, length}"
    pass

class InvalidInputDataException(Exception):
    "Raised when the inputdata does not have all required columns (lat, long, time)"
    pass

class InvalidSamplingException(Exception):
    "Raised when input value is not a subset of (stop, distance)"
    pass

class EmptyFilePathException(Exception):
    "Raised when input file path is empty"
    pass

class OverpassGatewayTimeout(Exception):
    "Raised when connecting to Overpass server fails because it is at capacity"
    pass
class OverpassTooManyRequests(Exception):
    "Raised when OverPass has too many requests and is over capacity"
    pass
class InvalidInputFileException(Exception):
    "Raised when inputted CSV file is invalid and doesn't have the required columns"
    pass
class WritingFileException(Exception):
    "Raised when the function fails to write to a CSV file"
    pass