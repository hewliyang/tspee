def distance(a,b):
    return ((a[0] - b[0])**2 + (a[1] - b[1])**2 )**(0.5)

class Graph:
    def __init__(self, cities):
        self.cities = cities
        self.length = len(cities)
        self.graph = []
        for i in range(self.length):
            for j in range(i):
                self.graph.append([i, j, distance(cities[i], cities[j])])
                

    def search(self, parent, i):
        if parent[i] == i:
            return i
        return self.search(parent, parent[i])
 
    def apply_union(self, parent, rank, x, y):
        xroot = self.search(parent, x)
        yroot = self.search(parent, y)
        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1
 
  
    def tsp(self):
        result = []
        counter = 0
        self.graph = sorted(self.graph, key=lambda item: item[2])
        degree = [0 for _ in range(self.length)]
        parent = []
        rank = []
        for node in range(self.length):
            parent.append(node)
            rank.append(0)
        while len(result) < self.length-1:
            u, v, w = self.graph[counter]
            counter += 1
            if (degree[u] > 1) or (degree[v] > 1): 
                continue
            
            x = self.search(parent, u)
            y = self.search(parent, v)
            if x != y:
                result.append([u, v, w])
                self.apply_union(parent, rank, x, y)
                degree[u] += 1
                degree[v] += 1

        counter = 0
        final_edge = []
        for deg in degree:
            if deg == 1:
                final_edge.append(counter)
                if len(final_edge) == 2:
                    break
            counter += 1
        for edge in self.graph:
            if edge[1] == final_edge[0] and edge[0] == final_edge[1]:
                result.append(
                    [edge[1], edge[0], distance( self.cities[edge[1]], self.cities[edge[0]] ) ]
                    )
                
        convert = result.copy()
        start = convert.pop(0)
        proper_route = [start[0]]
        next = start[1]
        while len(convert) != 0:
            proper_route.append(next)
            for edge in convert:
                if edge[0] == next:
                    next = edge[1]
                    convert.remove(edge)
                    break
                if edge[1] == next:
                    next = edge[0]
                    convert.remove(edge)
                    break
        proper_route.append(next)

        return sum([x[2] for x in result]), result, proper_route
 
