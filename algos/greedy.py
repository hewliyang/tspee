import numpy as np
 
# Function to find the minimum
# cost path for all the paths
def solver_greedy(graph: np.ndarray):
    """
    in:
    @ tsp: np.ndarray: the NxN distance matrix
    """
    r, c = len(graph), len(graph[0])
    i, j, total, counter = 0, 0, 0, 1
    min_dist = 100 # Can just set an arbritarily large number since max distance between 2 points is just 1.4ish
    visited = {x: 0 for x in range(r)}
    
    # Start from first node
    visited[0] = 1
    route = [0 for x in range(r+1)]
    route[0] = 1
 
    # Traverse the adjacency
    # matrix graph[][]
    while i < r and j < c:
        # Corner of matrix
        if counter > (c-1):
            break
 
        # If this path is unvisited then
        # and if the cost is less then
        # update the cost
        if (j != i) and (visited[j] == 0):
            if graph[i][j] < min_dist:
                min_dist = graph[i][j]
                route[counter] = j + 1
 
        j += 1

        # Check all paths from the
        # ith indexed city
        if j == r:
            total += min_dist
            min_dist = 100
            visited[route[counter] - 1] = 1
            j = 0
            i = route[counter] - 1
            counter += 1
 
    # Update the ending city in array
    # from city which was last visited
    route[counter] = 1
 
    total += graph[route[counter-1] - 1][0]
    
    return total, route
