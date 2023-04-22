from queue import PriorityQueue
from networkx.algorithms.matching import max_weight_matching
from networkx.algorithms.euler import eulerian_circuit
import numpy as np
import networkx as nx

def get_cost(tour: list, dist_matrix: np.ndarray):
    """
    returns the total cost of the tour
    assumes that there are N + 1 nodes in the `tour` list, including the last node -> first node edge at the end!
    """
    cost = np.sum(dist_matrix[tour[:-1], tour[1:]])
    return cost
def distance(a,b):
    return ((a[0] - b[0])**2 + (a[1] - b[1])**2 )**(0.5)

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
class Christofides:
    
    def __init__(self, cities):
        self.cities = cities
        self.length = len(cities)
        self.graph = np.zeros((self.length,self.length))
        for i in range(self.length):
            for j in range(self.length):
                self.graph[i][j] = distance(cities[i], cities[j])
    
    def minkey(self, counted, parent):
        edges = PriorityQueue()
        
        for k, v in counted.items():
            if v == True:
                for i in range(self.length):
                    if counted[i] == False:
                        edges.put((self.graph[k][i], (k, i)))
        
        while edges.empty() == False:
            distedge = edges.get()
            edge = distedge[1]
            if counted[edge[0]] == True and counted[edge[1]] == True:
                continue
            elif counted[edge[0]] == True:
                u = edge[1]
                parent[u] = edge[0]
                break
            else:
                u = edge[0]
                parent[u] = edge[1]
                break
            
        return u, parent
    
    
    def primMST(self):
        parent = {}
        counted = {}
        
        for i in range(self.length):
            parent[i] = None
            counted[i] = False
        
        counted[0] = True
        parent[0] = -1
        
        while False in counted.values():
            u, parent = self.minkey(counted, parent)
            counted[u] = True
        
        return parent
            
            
    def oddVertices(self, mst):
        degree = {}
        odd = []
        for i in range(self.length):
            if i not in degree:
                degree[i] = 0
            if mst[i] not in degree:
                degree[mst[i]] = 0
                
            degree[i] += 1
            degree[mst[i]] += 1
        
        degree[0] -= 1
        degree.pop(-1)
        
        for key, value in degree.items():
            if value%2 == 1:
                odd.append(key)
        
        return odd
                
        
    def tsp(self):
        mst = self.primMST()
        
        odd = self.oddVertices(mst)
        
        ixodd = np.ix_(odd, odd)
        G = nx.from_numpy_array(-1 * self.graph[ixodd])
        nxgraphmatching = nx.max_weight_matching(G, maxcardinality=True)
        
        multigraph = nx.MultiGraph()
        for i in range(1, self.length):
            multigraph.add_edge(i, mst[i], weight=self.graph[i][mst[i]])
        for oddedge in nxgraphmatching:
            multigraph.add_edge(odd[oddedge[0]], odd[oddedge[1]], weight=self.graph[odd[oddedge[0]]][odd[oddedge[1]]])
                                                 
        euler_tour = list(eulerian_circuit(multigraph, source=0))
        path = [u for u, v in euler_tour]
        path = list(dict.fromkeys(path).keys())
        path.append(0)
        
        dist = 0                                                          
        for i in range(len(path) - 1):
            dist += distance(self.cities[path[i]], self.cities[path[i+1]])
                                                                  
        return path, dist