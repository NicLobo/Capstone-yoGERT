import main
import NetworkGraph
import ShortestRouteEpisode

import timeit

# Tested data
# episodeFilePath = "./1_episode.csv"
# episodeFilePath = "./trace/episode/1_episode.csv"
episodeFilePath = "/Users/tommylw/Desktop/University/SE_4G06/Capstone-yoGERT/src/1_episode.csv"

# Test case
def performanceGSER():
    correctTime = 0
    startTime = timeit.default_timer()
    for i in range(10):
        generatedShortestEpisodeNetworkGraph, generatedShortestEpisodeRoute = main.generateShortestEpisodeRoute(episodeFilePath)
        if (type(generatedShortestEpisodeNetworkGraph) == NetworkGraph.NetworkGraph and type(generatedShortestEpisodeRoute) == ShortestRouteEpisode.ShortestRouteEpisode):
            correctTime += 1
        print("Complete one time.")
        
        i += 1
    endTime = timeit.default_timer()

    totalRunTime = endTime - startTime
    averageRunTime = totalRunTime/10

    # Report Result
    print("10 cases run, " + str(correctTime) + "/10 cases passes.\nTotal runtime: " + str(totalRunTime) + " seconds.\nAverage runtime for 1 case: " + str(averageRunTime) + " seconds.")


# Automated Driver Code
performanceGSER()