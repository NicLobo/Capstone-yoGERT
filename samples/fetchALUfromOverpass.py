from OSMPythonTools.overpass import Overpass
overpass = Overpass()
query = '''
area[name="Austin"];
(
relation["type"="boundary"]["name"="Austin"]
);
(._;>;);
out body;
'''

r = overpass.query(query)
r.toJSON()