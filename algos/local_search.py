"""
Local search post-processing for tour improvements

1) 2-opt
2) 3-opt
3) simmulated_annealing

"""

import numpy as np
from copy import deepcopy

def get_cost(tour: list, dist_matrix: np.ndarray):
    """
    returns the total cost of the tour
    assumes that there are N + 1 nodes in the `tour` list, including the last node -> first node edge at the end!
    """
    cost = np.sum(dist_matrix[tour[:-1], tour[1:]])
    return cost

def two_opt(tour:list, dist_matrix: np.ndarray) -> list:
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

    while improvement_made:
        improvement_made = False
        for i in range(N - 2):
            for j in range(i+2, N):
                new_tour = deepcopy(current_tour)
                new_tour[i+1:j+1] = reversed(new_tour[i+1:j+1])
                new_distance = get_cost(new_tour, dist_matrix)
                current_distance = get_cost(current_tour, dist_matrix)
                if new_distance < current_distance:
                    current_tour = new_tour
                    improvement_made = True
    
    return current_tour
    