#Activity Location object
# name: string
# lat: float
# long: float
class ActivityLocation:
    def __init__(self, name, lat, lon, amenity = "None"):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.amenity = amenity