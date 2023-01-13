import requests
response = requests.get("https://www.openstreetmap.org/api/0.6/map?bbox=-79.954424,43.264522,-79.943202,43.270746")
print(response.content)
#https://www.openstreetmap.org/api/0.6/map?bbox=43.264522,-79.971056,43.272664,-79.943202
#https://www.openstreetmap.org/api/0.6/map?bbox=-79.954424,43.264522,-79.943202,43.270746"
#https://www.openstreetmap.org/api/0.6/map?bbox=-75.569587,42.806358,-75.507789,42.832202