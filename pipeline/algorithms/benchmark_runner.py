from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Any

from pipeline.algorithms.restricted_tsp_solver import RestrictedTSPSolver


class BenchmarkRunner:
    """Generates synthetic Euclidean TSP instances and evaluates the solver."""

    def __init__(self, seed: int = 42):
        self.seed = seed
        random.seed(seed)

    def generate_points(self, n: int, low: int = 0, high: int = 100) -> list[tuple[float, float]]:
        return [(random.uniform(low, high), random.uniform(low, high)) for _ in range(n)]

    def run_suite(self, sizes: list[int]) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        for n in sizes:
            points = self.generate_points(n)
            solver = RestrictedTSPSolver(points)
            route = solver.solve()
            metrics = solver.metrics()
            results.append({
                "n": n,
                "route": route,
                "tour_length": metrics["tour_length"],
                "method": metrics["method"],
                "assumptions": metrics["assumptions"],
            })
        return results

    def save_report(self, results: list[dict[str, Any]], path: str | Path) -> Path:
        out_path = Path(path)
        out_path.parent.mkdir(exist_ok=True, parents=True)
        out_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
        return out_path
