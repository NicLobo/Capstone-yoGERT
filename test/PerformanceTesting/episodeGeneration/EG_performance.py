import main
import csv
import os
import shutil
import timeit

# Tested data
csvFilePath = "./exampleDataset/trace_3.csv"
traceDirPath = "./trace"
stopFilePath = "./trace/stop/stops.csv"

def performanceEG():
    startTime = timeit.default_timer()
    main.generateEpisodes(csvFilePath, "trace")
    endTime = timeit.default_timer()

    totalRuntime = endTime - startTime
    print("Total runtime: " + str(totalRuntime) + " seconds.")

    # Test if the generated file is correct
    isCorrect = False
    with open(stopFilePath) as readFile:
        reader = csv.reader(readFile)
        lineCount = 0
        for line in reader:
            lineCount += 1
        if (lineCount == 13):
            isCorrect = True
    
    shutil.rmtree(traceDirPath)
    return isCorrect, totalRuntime


# Automated Driver code
totalCorrectNum = 0
totalRuntime = 0
for i in range(10):
    isThisCorrect, thisRuntime = performanceEG()

    if (isThisCorrect):
        totalCorrectNum += 1
    totalRuntime += thisRuntime
averageRuntime = totalRuntime / 10
print(" ")
print("10 cases run. " + str(totalCorrectNum) + "/10 cases pass.\nTotal runtime: " + str(totalRuntime) + " seconds.\nAverage runtime: " + str(averageRuntime) + " seconds.")

