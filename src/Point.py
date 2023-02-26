class Point:
  def __init__(self, lat, lon, time=None, mode=None, ID=None):
    self.episodeID = ID
    self.lat = lat
    self.lon = lon
    self.time = time
    self.mode = mode
