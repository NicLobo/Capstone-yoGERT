import csv

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
    

l = GenALInput('./episode.csv')
print(l)
