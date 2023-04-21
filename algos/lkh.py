"""

Lin-Kernighan Solver by Keld Helsgaun

Solver Version 2.0.9

Python wrapper (elkai) by @fikisipi
https://github.com/fikisipi/elkai/tree/master

http://webhotel4.ruc.dk/~keld/research/LKH/
Licensed for non-commercial use only

"""

import elkai
import numpy as np

def get_cost(tour: list, dist_matrix: np.ndarray):
    """
    returns the total cost of the tour
    assumes that there are N + 1 nodes in the `tour` list, including the last node -> first node edge at the end!
    """
    cost = np.sum(dist_matrix[tour[:-1], tour[1:]])
    return cost

def solver_lkh(dist_matrix: np.ndarray):
    """
    Args:
    - dist_matrix: The N x N distance matrix for the graph
    Return:
    - tour: list: The id's of the nodes visited in sequence for the tour
    - cost: float: The total cost of the tour
    """

    tour = elkai.solve_float_matrix(dist_matrix)

    # append the starting point into the tour to complete it
    tour.append(tour[0])

    return tour, get_cost(tour, dist_matrix)
