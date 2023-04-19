import numpy as np
from typing import DefaultDict

def solver_nearest_neighbours(tsp: np.ndarray, random: bool = True):
    """
    in:
    -----------
    tsp : np.ndarray: the NxN distance matrix
    random: bool: True -> random starts, False -> start at node 0
    -----------
    out:
    -----------
    tour: list
    cost: float

    1. Choose a starting node, say node 0, and mark it as visited
    2. Initialize a list to store the tour and a variable to keep track of the total cost
    3. While there are unvisited nodes:
        a. Find the nearest unvisited node to the current node (use Euclidean distance)
        b. Add the nearest node to the tour and mark it as visited
        c. Update the total cost by adding the distance between the current node and the nearest node
        d. Set the nearest node as the new current node
    4. Finally, add the starting node to the end of the tour to complete the circuit
    5. Print the tour and the total cost
    """

    N = tsp.shape[0]
    
    # tour will contain the sequential route taken by the agent
    tour = []

    # hashmap for checking visited in O(1)
    visited = DefaultDict(int)

    # initialise starting node according to flag provided
    current_node = 0
    if random:
        current_node = np.random.randint(N)

    # push initial values into state
    tour.append(current_node)
    visited[current_node] = 1

    while len(tour) < N:
        nearest_node = None
        nearest_distance = np.inf
        # find the nearest neighbour to the current node
        for i in range(N):
            if visited[i] == 0:
                distance = tsp[current_node, i]
                if distance < nearest_distance:
                    nearest_node = i
                    nearest_distance = distance
        # update state
        tour.append(nearest_node)
        visited[nearest_node] = 1
        current_node = nearest_node
    
    # complete the circuit
    tour.append(tour[0])
    cost = np.sum(tsp[tour[:-1], tour[1:]])

    return tour, cost