# Collection of TSP Algorithms in Python

Put algos (`.py` files) under `./algos`

Run in the `ipynb` by importing, eg:

```python
import numpy as np
from scipy.spatial.distance import cdist
from algos.greedy import solver_greedy
from algos.nn import solver_nearest_neighbours

cities = np.load("cities.npy", allow_pickle = True)
dist_matrix = cdist(cities, cities)

print(solver_greedy(dist_matrix, random=False))
print(solver_nearest_neighbours(dist_matrix, random=False))
```
