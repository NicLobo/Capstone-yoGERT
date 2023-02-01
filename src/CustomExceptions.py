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
