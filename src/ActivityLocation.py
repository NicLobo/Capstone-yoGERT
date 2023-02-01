#Activity Location object
# name: string
# lat: float
# long: float
class ActivityLocation:
    def __init__(self, name, lat, lon):
        self.name = name
        self.lat = lat
        self.lon = lon