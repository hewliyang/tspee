from typing import DefaultDict
import numpy as np
 
INT_MAX = 2147483647
 
# Function to find the minimum
# cost path for all the paths
def solver_greedy(tsp: np.ndarray, random : bool = True):
    """
    in:
    @ tsp: np.ndarray: the NxN distance matrix
    @ random: bool: True -> random starts, False -> start at node 0
    """

    sum = 0
    counter = 0
    j = 0
    i = 0
    min = INT_MAX
    visitedRouteList = DefaultDict(int)
 
    # Starting from a random node
    N = tsp.shape[0]
    start = np.random.randint(N)

    # city i.e., the first city
    if random: visitedRouteList[start] = 1 
    else: visitedRouteList[0] = 1

    route = [0] * len(tsp)
 
    # Traverse the adjacency
    # matrix tsp[][]
    while i < len(tsp) and j < len(tsp[i]):
 
        # Corner of the Matrix
        if counter >= len(tsp[i]) - 1:
            break
 
        # If this path is unvisited then
        # and if the cost is less then
        # update the cost
        if j != i and (visitedRouteList[j] == 0):
            if tsp[i][j] < min:
                min = tsp[i][j]
                route[counter] = j + 1
 
        j += 1
 
        # Check all paths from the
        # ith indexed city
        if j == len(tsp[i]):
            sum += min
            min = INT_MAX
            visitedRouteList[route[counter] - 1] = 1
            j = 0
            i = route[counter] - 1
            counter += 1
 
    # Update the ending city in array
    # from city which was last visited
    i = route[counter - 1] - 1
 
    for j in range(len(tsp)):
 
        if (i != j) and tsp[i][j] < min:
            min = tsp[i][j]
            route[counter] = j + 1
 
    sum += min
 
    # Started from the node where
    # we finished as well.
    return sum