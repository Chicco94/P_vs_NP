from __future__ import annotations

from typing import Any, Iterable

from pipeline.agents.base_agent import BaseAgent
from pipeline.collectors.scholar_collector import collect_results


class BibliographicAgent(BaseAgent):
    name = "bibliographic-agent"
    description = "Collects literature references relevant to TSP and complexity research."

    def run(self, payload: Iterable[str] | str | None = None) -> list[dict[str, Any]]:
        if payload is None:
            queries = [
                "traveling salesman problem NP-hard",
                "Held-Karp TSP exact",
                "Euclidean TSP PTAS",
                "metric TSP approximation",
            ]
        elif isinstance(payload, str):
            queries = [payload]
        else:
            queries = list(payload)

        return collect_results(queries, max_results_per_query=5)
