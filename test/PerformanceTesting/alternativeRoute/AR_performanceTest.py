import main
import NetworkGraph
import AlternativeRoute

import timeit

# Tested data
# traceFilePath = "./trace1.csv"
traceFilePath = "/Users/tommylw/Desktop/University/SE_4G06/Capstone-yoGERT/src/1_episode.csv"

# Test case
def performanceGAR():
    correctTime = 0
    startTime = timeit.default_timer()
    for i in range(10):
        generatedAlternativeRoute = main.generateAlternativeRoute(traceFilePath)
        if (type(generatedAlternativeRoute) == AlternativeRoute.AlternativeRoute):
            correctTime += 1
        
        print("Complete One Time")
        i += 1
    endTime = timeit.default_timer()

    totalRunTime = endTime - startTime
    averageRunTime = totalRunTime/10

    # Report Result
    print("10 cases run, " + str(correctTime) + "/10 cases passes.\nTotal runtime: " + str(totalRunTime) + " seconds.\nAverage runtime for 1 case: " + str(averageRunTime) + " seconds.")


# Automated Driver Code
performanceGAR()