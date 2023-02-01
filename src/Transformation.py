import csv
from datetime import datetime

def convert_to_floats(arr):
    result = map(float, arr)
    return list(result)

def GenALInput(filepath): 
    data = csv.reader(open(filepath))

    li = []
    c=0
    
    for line in data:
        
        if c>0: 
            li.append(tuple(convert_to_floats(line[2:4])))
        
        c = c+1

    return li
    
def GenALInputT(filepath): 
    data = csv.reader(open(filepath))

    li = []
    lt = []
    c=0
    
    for line in data:
        
        if c>0: 
            li.append(tuple(convert_to_floats(line[2:4])))
            lt.append(line[5])

        
        c = c+1

    return li,lt
    

l = GenALInput('./episode.csv')
l2,ltime = GenALInputT('./episode.csv')
print(l)
print(l2)
print(ltime)
