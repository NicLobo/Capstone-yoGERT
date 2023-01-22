import osmnx as ox
import h3

# exported constants 
DISTANCETOL = 200
EARTHRADIUS = 6371000 

class NetworkGraph:
    def __init__(self, startCoord, endCoord, stops, networkMode):
        self.dist = self.findDistance(startCoord, endCoord, stops)
        self.graph = ox.graph_from_point(startCoord, dist=self.dist, network_type=networkMode, simplify=False)
    
    def getNearestNode(self, coord):
        return ox.nearest_nodes(self.graph, coord[1], coord[0])
    
    def findDistance(self, startCoord, endCoord, stops):
        distance = h3.point_dist(startCoord, endCoord, unit='m') # findhdistance
        for i in range(1,len(stops)-1):
            testDis = h3.point_dist(startCoord, stops[i], unit='m')
            if (testDis > distance):
                distance = testDis
        distance = distance + DISTANCETOL
        return distance

# inputOne = [(-23.546498,-46.691141),(-23.558094,-46.660205),(-23.635039,-46.641239),
#                 (-23.645996,-46.641027),(-23.625882,-46.640936),(-23.618245,-46.639139),
#                 (-23.6130583,-46.637918),(-23.598541,-46.636634),(-23.589342,-46.634677),
#                 (-23.567615,-46.649027),(-23.56357,-46.653893),(-23.581203,-46.638489),
#                 (-23.5754,-46.6407),(-23.568521,-46.63990),(-23.561435,-46.638534)]
# NetworkGraph1 = NetworkGraph(inputOne[0], (-23.561435,-46.638534), inputOne, "drive")
# NetworkGraph1.getNearestNode(inputOne[0])
# NetworkGraph1.getNearestNode((-23.561435,-46.638534))
