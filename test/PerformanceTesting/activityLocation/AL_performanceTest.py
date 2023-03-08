import main
import os

import timeit

# Tested data
stopFile = "./trace/stop/stops.csv"
exportFilePath = "./trace/stop/activityLocation.csv"
tolerance = 500

# Test case
def performanceAL():
    startTime = timeit.default_timer()
    main.findActivityLocations(stopFile,exportFilePath,tolerance)
    endTime = timeit.default_timer()
    totalRuntime = endTime - startTime
    print("Runtime: " + str(totalRuntime) + " seconds.")

    # print result
    isCorrect = False
    with open(exportFilePath) as readFile:
        reader = csv.reader(readFile)
        lineCount = 0
        for line in reader:
            lineCount +=1
        if (lineCount == 3):
            isCorrect = True
        
        os.remove(exportFilePath)
        return isCorrect, totalRuntime

# Automated Driver Code
totalCorrectNum = 0
totalRuntime = 0
for i in range(10):
    isThisCorrect, thisRuntime = performanceAL()

    if (isThisCorrect):
        totalCorrectNum += 1
    totalRuntime += thisRuntime
averageRuntime = totalRuntime / 10
print(" ")
print("10 cases run. " + str(totalCorrectNum) + "/10 cases pass.\nTotal runtime: " + str(totalRuntime) + " seconds.\nAverage runtime: " + str(averageRuntime) + " seconds.")


