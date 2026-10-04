# Restricted TSP solver prototype

## Scope

This module implements a paper-ready prototype for a restricted Euclidean TSP setting. It is intentionally not a universal exact solver for the general TSP.

## Assumptions

- Euclidean points in the plane
- complete graph over the input points
- geometric structure is available and exploitable
- objective is to minimize total route length

## Algorithm

The prototype uses:

1. nearest-neighbor construction of an initial tour;
2. 2-opt refinement;
3. final route evaluation with tour length metrics.

## API

```python
from pipeline.algorithms import RestrictedTSPSolver

points = [(0, 0), (1, 2), (3, 1)]
solver = RestrictedTSPSolver(points)
route = solver.solve()
print(route)
print(solver.metrics())
```

## Intended use

This component is appropriate as a baseline for a restricted geometric TSP paper, not as a proof of a polynomial-time exact solver for the unrestricted TSP.
