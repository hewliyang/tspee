from queue import PriorityQueue
from networkx.algorithms.matching import max_weight_matching
from networkx.algorithms.euler import eulerian_circuit

def distance(a,b):
    return ((a[0] - b[0])**2 + (a[1] - b[1])**2 )**(0.5)

class Christofides:
    
    def __init__(self, cities):
        self.cities = cities
        self.length = len(cities)
        self.graph = []
        for i in range(self.length):
            for j in range(i):
                self.graph.append((distance(cities[i], cities[j]), (i, j)))
    
    def minkey(self, key, counted, parent):
        edges = PriorityQueue()
        
        for i in range(self.length):
            if counted[i]:
                for edge in self.graph:
                    if counted[i] in edge[1]:
                        edges.put(edge)
        
        while edges.empty() == False:
            distedge = edges.get()
            edge = distedge[1]
            if counted[edge[0]] and counted[edge[1]]:
                continue
            elif counted[edge[0]]:
                u = edge[1]
                parent[u] = edge[0]
            else:
                u = edge[0]
                parent[u] = edge[1]
            
        return u, parent
    
    
    def primMST(self):         
        key = [float('inf') for _ in range(self.length)]
        key[0] = 0
        parent = [None for _ in range(self.length)]
        counted = [False for _ in range(self.length)]
        counted[0] = True
        
        while False in counted:
            u, parent = self.minkey(key, counted, parent)
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
        
        for key, value in degree:
            if value%2 == 1:
                odd.append(key)
        
        return odd
                
        
    def tsp(self):
        mst = self.primMST()
        
        odd = self.oddVertices(mst)
        
        weighted = []
        ixodd = np.ix_(odd, odd)
        G = nx.graph()
        for i in ixodd:
            for j in self.graph:
                if (j[1][0] == i[0] and j[1][1] == i[1]) or (j[1][0] == i[1] and j[1][1] == i[0]):
                    weighted.append((i[0], i[1], -1*j[0]))
        G.add_weighted_edges_from(weighted)
        nxgraphmatching = nx.max_weight_matching(G, maxcardinality=True)
        
        multigraph = nx.MultiGraph()
        for index in range(self.length):
            for j in self.graph:
                if (j[1][0] == index and j[1][1] == mst[index]) or (j[1][0] == mst[index] and j[1][1] == index):
                    multigraph.add_edge(index, mst[index], weight=j[0])
                    break
        for oddedge in nxgraphmatching:
            for j in self.graph:
                if (j[1][0] == odd[oddedge[0]] and j[1][1] == odd[oddedge[1]]) or (j[1][0] == odd[oddedge[1]] and j[1][1] == odd[oddedge[0]]):
                    multigraph.add_edge(odd[oddedge[0]], odd[oddedge[1]], weight=j[0])
                    break
                                                 
        euler_tour = list(eulerian_circuit(multigraph, source=0))
        path = [u for u, v in euler_tour]
        path = list(dict.fromkeys(path).keys())
        path.append(0)
        
        dist = 0                                                          
        for i in range(len(path)):
            dist += distance(path[i], path[i+1])
                                                                  
        return path, dist
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        