import unittest
import os

from fetchActivityLocations import fetchActivityLocations, fetchALForIndividualPoint


class ActivityLocationsTest(unittest.TestCase):
  def test_outputFileIsGenerated(self):
    print("helo")
    print(os.path)
    outputPath = "trace/activitylocations/trace-activityLocation.csv"
    if os.path.exists(outputPath):
        print("removed")
        os.remove(outputPath)
    if not os.path.exists(outputPath):
        print("deleted")

    fetchActivityLocations("trace/stop/stops.csv",outputPath, 500)
    if os.path.exists(outputPath):
        print("worked")
    assert os.path.exists(outputPath)


  if __name__ == '__main__':
    unittest.main()



#check if output file is generated
#check exceptions for input file
#check exceptions for 
#check if server unavialable outputs logs
#check if lists out points and 