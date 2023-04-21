import numpy as np
import networkx as nx

def get_cost(tour: list, dist_matrix: np.ndarray):
    """
    returns the total cost of the tour
    assumes that there are N + 1 nodes in the `tour` list, including the last node -> first node edge at the end!
    """
    cost = np.sum(dist_matrix[tour[:-1], tour[1:]])
    return cost

def solver_christofides(dist_matrix: np.ndarray):
    """
    Christofides TSP algorithm implemented in NetworkX

    Args:
    - dist_matrix: The N x N distance matrix for the graph
    Return:
    - tour: list: The id's of the nodes visited in sequence for the tour
    - cost: float: The total cost of the tour
    """

    N = dist_matrix.shape[0]

    # Construct the graph and MST
    G = nx.from_numpy_array(dist_matrix)
    T = nx.minimum_spanning_tree(G, weight="weight")

    # Get odd-degree nodes
    odd_degree_nodes = [ i for i in T.nodes if T.degree(i) % 2 ]

    # Min-Weight Perfect Matching
    matching = nx.min_weight_matching( G.subgraph(odd_degree_nodes) )

    # Construct MultiGraph
    M = nx.MultiGraph()
    M.add_nodes_from(range(N))
    M.add_edges_from(T.edges())
    M.add_edges_from(matching)

    # Construct Eulerian Tour
    initial_tour = list( nx.eulerian_circuit(M, source=0) )

    # Construct TSP Tour (starting from node 0)
    tour = [0]
    for (i, j) in initial_tour:
        if j not in tour:
            tour.append(j)

    # Return back to start
    tour.append(tour[0])

    assert len(tour) == N + 1

    return tour, get_cost(tour, dist_matrix)
