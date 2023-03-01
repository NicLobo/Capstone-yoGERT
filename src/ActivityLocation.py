## @file ActivityLocation.py
#  @title ActivityLocation
#  @author Smita Singh 400173853
#  @date Feb 28 2022

## @brief A class representing an activity location object
#  @details Will be used as a return type to fetchActivityLocation module
class ActivityLocation:
    ## @brief Constructor for ActivityLocation
    #  @details Contructor accepts 4 parameters for name, latitude, longitude, and amenity
    #  @param name String describing the name of the location
    #  @param lat float the latitude of the activity location
    #  @param lon float the longitude of the activity location
    #  @param amenity String describing the type of the activity location
    def __init__(self, name, lat, lon, amenity = "None"):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.amenity = amenity