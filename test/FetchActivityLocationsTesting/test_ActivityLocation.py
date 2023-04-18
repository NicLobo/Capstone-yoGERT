from ActivityLocation import *

newActivityLocation = ActivityLocation("Lemon Bar", 43.651504, -79.386657, "Juice")

def test_creatingActivityLocationObject():
    assert isinstance(newActivityLocation, ActivityLocation)

def test_getActivityName():
    assert newActivityLocation.name == "Lemon Bar"

def test_getActivityLocationLat():
    assert newActivityLocation.lat == 43.651504

def test_getActivityLocationLon():
    assert newActivityLocation.lon == -79.386657

def test_getActivityName():
    assert newActivityLocation.amenity == "Juice"
    
    
def test_creatingActivityLocationObjectWithoutCertainParameters():
    localActivityLocation = ActivityLocation("Lemon Bar", 43.651504, -79.386657)
    assert isinstance(localActivityLocation, ActivityLocation)
    assert localActivityLocation.name == "Lemon Bar"
    assert localActivityLocation.lat == 43.651504
    assert localActivityLocation.lon == -79.386657
    assert localActivityLocation.amenity == "None"
    