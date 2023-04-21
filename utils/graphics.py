import matplotlib.pyplot as plt
import numpy as np

def draw_tour(cities: np.ndarray, tour: list, title="TSP Nodes"):
    route = np.asarray([ [cities[pos][0], cities[pos][1]] for pos in tour ])
    plt.scatter(cities[:,0], cities[:,1], alpha=0.7, label="Cities (Nodes)")
    plt.plot(route[:,0], route[:,1], alpha=1, color="red", linewidth=1, label="Connections (Edges)")
    plt.legend()
    plt.title(label=title)
    plt.xlabel("$x$")
    plt.ylabel("$y$")