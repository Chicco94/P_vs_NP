from __future__ import annotations

from math import hypot
from typing import Any

from pipeline.algorithms.base_solver import BaseSolver


class RestrictedTSPSolver(BaseSolver):
    """Heuristic solver for structured Euclidean TSP instances.

    This prototype is intentionally restricted to a Euclidean setting and uses a
    nearest-neighbor route plus 2-opt improvement. It is designed as a paper-ready
    algorithmic component, not as a universal polynomial-time solver for the
    general TSP.
    """

    def __init__(self, instance: list[tuple[float, float]]):
        super().__init__(instance)
        self.points = [tuple(map(float, point)) for point in self.instance]
        self.cost_history: list[float] = []

    def solve(self) -> list[int]:
        if len(self.points) < 2:
            return list(range(len(self.points)))

        route = self._nearest_neighbor_route()
        route = self._two_opt(route)
        self.cost_history.append(self._tour_length(route))
        return route

    def metrics(self) -> dict[str, Any]:
        route = self.solve()
        return {
            "tour": route,
            "tour_length": self._tour_length(route),
            "n_points": len(self.points),
            "method": "restricted_euclidean_heuristic",
            "assumptions": [
                "Euclidean coordinates",
                "complete graph of pairwise distances",
                "structured geometric instances"
            ],
            "classification": "EXACT_SPECIAL_OR_APPROX",
        }

    def _distance(self, a: tuple[float, float], b: tuple[float, float]) -> float:
        return hypot(a[0] - b[0], a[1] - b[1])

    def _nearest_neighbor_route(self) -> list[int]:
        n = len(self.points)
        if n == 0:
            return []

        start = 0
        unvisited = set(range(1, n))
        route = [start]
        current = start

        while unvisited:
            next_index = min(unvisited, key=lambda idx: self._distance(self.points[current], self.points[idx]))
            route.append(next_index)
            unvisited.remove(next_index)
            current = next_index

        return route

    def _two_opt(self, route: list[int]) -> list[int]:
        improved = True
        best_route = route[:]

        while improved:
            improved = False
            best_length = self._tour_length(best_route)

            for i in range(1, len(best_route) - 1):
                for j in range(i + 1, len(best_route)):
                    if j - i == 1:
                        continue
                    candidate = best_route[:]
                    candidate[i:j] = reversed(candidate[i:j])
                    candidate_length = self._tour_length(candidate)
                    if candidate_length < best_length:
                        best_route = candidate
                        best_length = candidate_length
                        improved = True

        return best_route

    def _tour_length(self, route: list[int]) -> float:
        if len(route) < 2:
            return 0.0

        total = 0.0
        for i in range(len(route) - 1):
            a = self.points[route[i]]
            b = self.points[route[i + 1]]
            total += self._distance(a, b)

        first = self.points[route[0]]
        last = self.points[route[-1]]
        total += self._distance(first, last)
        return total
