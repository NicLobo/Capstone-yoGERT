## @file Point.py
#  @title Point
#  @author Smita Singh, Abeer Al-yasiri
#  @date Feb 28 2022

## @brief A class representing an Point object
#  @details Will be used as a return type to various modules
class Point:
    ## @brief Constructor for Point
    #  @details Contructor accepts 5 parameters for latitude, longitude, time, mode, and ID
    #  @param lat float the latitude of the point
    #  @param lon float the longitude of the point
    #  @param time string with format "%Y-%m-%d %H:%M:%S.%f"
    #  @param mode Enum to represent different modes of transportation
    #  @param ID integer identifier for traces
  def __init__(self, lat, lon, time=None, mode=None, ID=None):
    self.episodeID = ID
    self.lat = lat
    self.lon = lon
    self.time = time
    self.mode = mode
