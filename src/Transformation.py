import csv
# read csv file as a list of lists

def GenInput(filepath):
    data = csv.reader(open(filepath))

    li = []
    c=0
    for line in data:
        
        if c>0: 
            li.append(tuple(line))
        
        c = c+1
    
    return li


