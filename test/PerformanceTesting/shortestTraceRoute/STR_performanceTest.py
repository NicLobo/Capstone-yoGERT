import main
import NetworkGraph
import ShortestRouteTrace

import timeit

# Tested data
# traceFilePath = "./trace1.csv"
traceFilePath = "/Users/tommylw/Desktop/University/SE_4G06/Capstone-yoGERT/src/trace.csv"
traceMode = "drive"
episodeAnalysis = False

# Test case
def performanceGSTR():
    correctTime = 0
    startTime = timeit.default_timer()
    for i in range(10):
        generatedShortestTraceNetworkGraph, generatedShortestTraceRoute = main.generateShortestTraceRoute(traceFilePath,traceMode,episodeAnalysis)
        if (type(generatedShortestTraceNetworkGraph) == NetworkGraph.NetworkGraph and type(generatedShortestTraceRoute) == ShortestRouteTrace.ShortestRouteTrace):
            correctTime += 1
        
        print("Complete One Time")
        i += 1
    endTime = timeit.default_timer()

    totalRunTime = endTime - startTime
    averageRunTime = totalRunTime/10

    # Report Result
    print("10 cases run, " + str(correctTime) + "/10 cases passes.\nTotal runtime: " + str(totalRunTime) + " seconds.\nAverage runtime for 1 case: " + str(averageRunTime) + " seconds.")


# Automated Driver Code
performanceGSTR()