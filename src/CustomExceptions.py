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

class InvalidRouteTypeException(Exception):
    "Raised when the input route type is not ShortestRouteTrace or ShortestRouteEpisode"
    pass

class InvalidMappingFilePathException(Exception):
    "Raised when the input file path does not have the file name.html"
    pass

## @brief A class representing a file exception
#  @details Will be used as a file exception class for all functions in Tranformation.py
class FileException(Exception):
    "File path passed is not valid"
    pass

## @brief A class representing a list exception
#  @details Will be used as a list exception class for all functions in Tranformation.py
class WrongList(Exception):
    "List passed is incorrect"
    pass
