from Point import *

newPoint = Point(43.651605, -79.386759,"17:22:02", "mode.DRIVE")

def test_creatingPointObject():
    assert isinstance(newPoint, Point)

def test_getPointLat():
    assert newPoint.lat == 43.651605

def test_getPointLon():
    assert newPoint.lon == -79.386759
    
def test_getPointTime():
    assert newPoint.time == "17:22:02"
    
def test_getPointMode():
    assert newPoint.mode == "mode.DRIVE"
    
def test_creatingPointObjectWithoutCertainParameters():
    localPoint = Point(43.651605, -79.386759)
    assert isinstance(localPoint, Point)
    assert localPoint.lat == 43.651605
    assert localPoint.lon == -79.386759
    assert localPoint.time == None
    assert localPoint.mode == None
    
