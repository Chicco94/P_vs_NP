from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Any

from pipeline.classifiers.paper_classifier import classify_paper
from pipeline.collectors.scholar_collector import collect_results
from pipeline.extractors.paper_extractor import normalize_paper, extract_keywords_for_notes
from pipeline.models import PaperRecord


@dataclass
class QOrchestrator:
    base_queries: list[str] = field(
        default_factory=lambda: [
            "TSP NP-hardness",
            "Held Karp TSP exact algorithm",
            "Euclidean TSP special case",
            "Metric TSP approximation lower bounds",
        ]
    )
    max_iterations: int = 4
    min_evidence: int = 2
    max_results_per_query: int = 3

    def expand_queries(self, query: str) -> list[str]:
        query = query.strip()
        if not query:
            return []

        expansions: list[str] = [query]
        lower = query.lower()

        if "np-hard" in lower or "hardness" in lower or "hard" in lower:
            expansions.extend([
                f"{query} Karp 1972",
                f"Karp 1972 TSP NP-hardness",
                f"TSP NP-hardness Garey Johnson",
            ])
        if "held" in lower or "dynamic" in lower or "exact" in lower:
            expansions.extend([
                f"{query} Held Karp",
                "Held Karp dynamic programming TSP exact",
                "Exact TSP dynamic programming algorithm",
            ])
        if "euclidean" in lower or "planar" in lower or "special" in lower:
            expansions.extend([
                f"{query} polynomial time",
                "TSP special cases polynomial time exact",
                "Planar TSP polynomial time exact",
            ])
        if "approx" in lower or "metric" in lower:
            expansions.extend([
                f"{query} lower bounds",
                "Metric TSP approximation lower bounds",
                "Euclidean TSP PTAS Arora",
            ])

        canonical = [
            "Karp 1972 TSP NP-hardness",
            "Held Karp dynamic programming TSP exact",
            "Euclidean TSP PTAS Arora",
            "Metric TSP approximation lower bounds",
            "TSP special cases polynomial time exact",
            "Planar TSP polynomial time exact",
        ]
        expansions.extend(canonical)

        unique: list[str] = []
        seen: set[str] = set()
        for item in expansions:
            if item not in seen:
                seen.add(item)
                unique.append(item)
        return unique

    def evaluate_records(self, records: Iterable[dict[str, Any]]) -> dict[str, Any]:
        counts: dict[str, int] = {}
        for record in records:
            label = str(record.get("classification", "UNKNOWN")).upper()
            counts[label] = counts.get(label, 0) + 1

        hardness_count = counts.get("HARDNESS", 0)
        exact_special_count = counts.get("EXACT_SPECIAL", 0)
        exact_general_count = counts.get("EXACT_GENERAL", 0)
        ptas_count = counts.get("PTAS", 0)
        approximation_count = counts.get("APPROX", 0)

        total = sum(counts.values())
        coverage_score = 0.0
        if total:
            coverage_score = (
                hardness_count + exact_special_count + exact_general_count + ptas_count + approximation_count
            ) / total

        has_required_evidence = (
            hardness_count >= 1 and (exact_special_count >= 1 or ptas_count >= 1 or exact_general_count >= 1)
        )

        return {
            "hardness_count": hardness_count,
            "exact_special_count": exact_special_count,
            "exact_general_count": exact_general_count,
            "ptas_count": ptas_count,
            "approximation_count": approximation_count,
            "coverage_score": round(coverage_score, 3),
            "has_required_evidence": has_required_evidence,
            "total_records": total,
            "min_evidence": self.min_evidence,
        }

    def should_continue(self, summary: dict[str, Any]) -> bool:
        if summary.get("has_required_evidence") and summary.get("coverage_score", 0.0) >= 0.5:
            return False
        if summary.get("total_records", 0) >= self.min_evidence:
            return False
        return True

    def run(self, target: str | None = None) -> dict[str, Any]:
        queryset = self.base_queries[:]
        if target:
            queryset = [target]

        all_records: list[dict[str, Any]] = []
        seen_queries: set[str] = set()

        for iteration in range(self.max_iterations):
            candidate_queries: list[str] = []
            for query in queryset:
                candidate_queries.extend(self.expand_queries(query))

            for query in candidate_queries:
                if query in seen_queries:
                    continue
                seen_queries.add(query)
                raw_results = collect_results([query], max_results_per_query=self.max_results_per_query)
                for raw in raw_results:
                    normalized = normalize_paper(raw)
                    classification, confidence = classify_paper(
                        normalized["title"],
                        normalized["abstract"],
                        normalized["problem"],
                    )
                    paper = PaperRecord(
                        id=f"paper-{len(all_records) + 1}",
                        title=normalized["title"],
                        authors=normalized["authors"],
                        year=normalized["year"],
                        source=normalized["source"],
                        url=normalized["url"],
                        abstract=normalized["abstract"],
                        problem=normalized["problem"],
                        assumptions=normalized["assumptions"],
                        complexity=normalized["complexity"],
                        approach=normalized["approach"],
                        classification=classification,
                        confidence=confidence,
                        notes=", ".join(
                            extract_keywords_for_notes(normalized["title"], normalized["abstract"])["keywords"]
                        ),
                        raw=raw,
                    )
                    all_records.append(paper.to_dict())

            summary = self.evaluate_records(all_records)
            if not self.should_continue(summary):
                return {
                    "status": "done",
                    "iterations": iteration + 1,
                    "queries_seen": len(seen_queries),
                    "summary": summary,
                    "records": all_records,
                }

            if iteration < self.max_iterations - 1:
                queryset = [
                    "Karp 1972 TSP NP-hardness",
                    "Held Karp dynamic programming TSP exact",
                    "Euclidean TSP PTAS Arora",
                    "TSP special cases polynomial time exact",
                ]

        return {
            "status": "max_iterations_reached",
            "iterations": self.max_iterations,
            "queries_seen": len(seen_queries),
            "summary": self.evaluate_records(all_records),
            "records": all_records,
        }
