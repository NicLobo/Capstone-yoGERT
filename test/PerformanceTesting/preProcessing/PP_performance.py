import main

import shutil
import timeit

# Test data
testCSVPath = "./exampleDataset/trace_2.csv"
processedOutputPath = "./precessedCSV"

def performancePP():
    correctTime = 0
    startTime = timeit.default_timer()
    for i in range(10):
        processedFile, isInputValid = main.generatePreProcessingCSV(testCSVPath, processedOutputPath)
        if (isInputValid):
            correctTime += 1
            
            shutil.rmtree(processedOutputPath,ignore_errors=True)
        
        i+= 1
    endTime = timeit.default_timer()

    totalRunTime = endTime - startTime
    averageRunTime = totalRunTime/10

    # Report Result
    print("10 cases run, " + str(correctTime) + "/10 cases passes.\nTotal runtime: " + str(totalRunTime) + " seconds.\nAverage runtime for 1 case: " + str(averageRunTime) + " seconds.")


# Automated Driver Code
performancePP()
