import test.PerformanceTesting.main as main
import ShortestRouteStop

import timeit

# Tested data
traceFilePath = "/Users/tommylw/Desktop/University/SE_4G06/Capstone-yoGERT/src/trace/trace.csv"
stopFilePath = "/Users/tommylw/Desktop/University/SE_4G06/Capstone-yoGERT/src/trace/stop/stops.csv"
traceMode = "drive"
episodeAnalysis = False

# Test Case
def performanceGSSR():
    correctTime = 0
    startTime = timeit.default_timer()
    for i in range(10):
        generatedShortestStopRoute = main.generateShortestStopRoute(traceFilePath, traceMode, stopFilePath)
        if (type(generatedShortestStopRoute) == ShortestRouteStop.ShortestRouteStop):
            correctTime +=1
        
        print("Complete One Time.")
        i += 1
    endTime = timeit.default_timer()

    totalRunTime = endTime - startTime
    averageRunTime = totalRunTime/10

    # Report Result
    print("10 cases run, " + str(correctTime) + "/10 cases passes.\nTotal runtime: " + str(totalRunTime) + " seconds.\nAverage runtime for 1 case: " + str(averageRunTime) + " seconds.")
        
# Automated Driver Code
performanceGSSR()

