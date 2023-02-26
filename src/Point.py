class Point:
  def __init__(self, ID, lat, lon, time=None, mode=None):
    self.episodeID = ID
    self.lat = lat
    self.lon = lon
    self.time = time
    self.mode = mode
