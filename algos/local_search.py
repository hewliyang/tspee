"""
Local search post-processing for tour improvements

1) 2-opt
2) 3-opt (omitted since 2-opt already takes so long to run)
3) simmulated_annealing

Code adapted from the C++ implementation at:
https://github.com/forsythe/travelling-salesman/blob/master/main.cpp

"""

import numpy as np
import random
from copy import deepcopy

def get_cost(tour: list, dist_matrix: np.ndarray):
    """
    returns the total cost of the tour
    assumes that there are N + 1 nodes in the `tour` list, including the last node -> first node edge at the end!
    """
    cost = np.sum(dist_matrix[tour[:-1], tour[1:]])
    return cost

def two_opt(tour:list, dist_matrix: np.ndarray, verbose: bool = False) -> list:
    """
    Args:
    @tour - the list of nodes id's traversed in the tour from any algorithm
    @dist_matrix - the N x N distance matrix

    Return:
    - two-opt optimal tour
    """
    N = dist_matrix.shape[0]
    current_tour = deepcopy(tour)
    improvement_made = True
    swaps = 0
    iters = 0

    while improvement_made:
        improvement_made = False
        print(iters)
        for i in range(N - 2):
            for j in range(i+2, N):
                new_tour = deepcopy(current_tour)
                new_tour[i+1:j+1] = reversed(new_tour[i+1:j+1])
                new_distance = get_cost(new_tour, dist_matrix)
                current_distance = get_cost(current_tour, dist_matrix)
                if new_distance < current_distance:
                    current_tour = new_tour
                    improvement_made = True
                    swaps += 1
                    if verbose: print(f"Better tour found: {new_distance}")
        iters += 1

    if verbose:
        print("swaps: ", swaps)
        print("outer loop iters: ", iters)

    return current_tour

def faster_two_opt(tour:list, dist_matrix: np.ndarray, verbose: bool = False):
    """
    A much faster version of the above, but modifies the array in place.
    """
    N = len(tour)
    improvement_made = True
    swaps = 0

    while improvement_made:
        improvement_made = False
        for i in range(N):
            for j in range(i+1, N):
                # get the 2 current edges
                cur1 = (tour[i], tour[i+1])
                cur2 = (tour[j], tour[(j+1)%N])
                cur_length = dist_matrix[cur1] + dist_matrix[cur2]

                # get the two new edges
                new1 = (tour[i], tour[j])
                new2 = (tour[i+1], tour[(j+1)%N])
                new_length = dist_matrix[new1] + dist_matrix[new2]

                if new_length < cur_length:
                    tour[i+1:j+1] = tour[i+1:j+1][::-1]
                    improvement_made = True
                    swaps += 1
    if verbose: print("Swaps: ", swaps)
    return tour


def sim_ann(
        initial_tour: list,
        dist_matrix: np.ndarray,
        initial_temperature: int = 1000,
        cooling_rate : float = 0.995,
        stopping_temperature: float = 1e-8,
        max_iterations: int = 100,
        verbose: bool = False
) -> list:
    """
    Improves an initial tour using simmulated annealing with 2-opt
    """
    N = len(initial_tour) - 1
    current_tour = initial_tour
    best_tour = current_tour
    best_cost = get_cost(current_tour, dist_matrix)
    temperature = initial_temperature
    iter = 0

    while temperature > stopping_temperature and iter < max_iterations:

        # Choose two random vertices to swap
        i, j = sorted(random.sample(range(N), k=2))

        # Generate the new tour by swapping edges
        new_tour = current_tour[:i] + current_tour[i:j+1][::-1] + current_tour[j+1:]

        # Calculate cost difference
        delta = get_cost(new_tour, dist_matrix) - get_cost(current_tour, dist_matrix)

        # Accept tour conditionally
        if delta < 0 or random.uniform(0, 1) < np.exp(-delta / temperature):
            current_tour = new_tour
        
        # Update state
        cur_cost = get_cost(current_tour, dist_matrix)
        if cur_cost < best_cost:
            best_tour = current_tour
            best_cost = cur_cost
            if verbose: print(f"Better Tour Found: {best_cost}")
        
        # Decrease temperature
        temperature *= cooling_rate
        iter += 1
    
    return best_tour

