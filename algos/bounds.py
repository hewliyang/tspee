import numpy as np
from scipy.sparse import csgraph

def mst_lower_bound(dist_matrix: np.ndarray):
    return csgraph.minimum_spanning_tree(dist_matrix).sum()