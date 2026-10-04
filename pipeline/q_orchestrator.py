from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
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
    summary_path: Path = field(
        default_factory=lambda: Path(__file__).resolve().parents[1] / "docs" / "restricted_tsp_summary.tex"
    )
    pdf_path: Path = field(
        default_factory=lambda: Path(__file__).resolve().parents[1] / "docs" / "restricted_tsp_summary.pdf"
    )

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

    def objective_reached(self, summary: dict[str, Any]) -> bool:
        return bool(summary.get("has_required_evidence")) and summary.get("coverage_score", 0.0) >= 0.65

    def refine_proof(self, summary: dict[str, Any]) -> str:
        if self.objective_reached(summary):
            return (
                "The evidence collected in this cycle is sufficient to justify a more precise scientific claim: "
                "the unrestricted case remains outside the scope of a proven polynomial-time exact solver, while the "
                "specialized literature provides structured exact and approximation results that are relevant to the problem class."
            )
        return (
            "The evidence is still incomplete: the current cycle identifies special-case and approximation literature, "
            "but it has not yet reached the threshold needed to state a definitive general conclusion. Further retrieval is required."
        )

    def update_summary_document(self, summary: dict[str, Any], proof_text: str) -> bool:
        tex_path = Path(self.summary_path)
        if not tex_path.exists():
            return False

        text = tex_path.read_text(encoding="utf-8")
        marker = "\\section{Evidence-driven literature refinement}"
        replacement = (
            "\\section{Evidence-driven literature refinement}\n\n"
            "The orchestrator refreshed the corpus and analyzed the new evidence. The latest run reports "
            f"{summary.get('total_records', 0)} records with a coverage score of {summary.get('coverage_score', 0.0)}. "
            f"The status is {'objective reached' if self.objective_reached(summary) else 'continuing the search'} and the evidence gate is "
            f"{'satisfied' if summary.get('has_required_evidence') else 'not yet satisfied'}.\n\n"
            f"{proof_text}\n"
        )

        if marker in text:
            start = text.index(marker)
            end = text.index("\\section{Conclusion}", start) if "\\section{Conclusion}" in text[start:] else len(text)
            text = text[:start] + replacement + text[end:]
        else:
            before_conclusion = text.rfind("\\section{Conclusion}")
            if before_conclusion >= 0:
                text = text[:before_conclusion] + replacement + "\n" + text[before_conclusion:]
            else:
                text = text.rstrip() + "\n\n" + replacement + "\n"

        tex_path.write_text(text, encoding="utf-8")
        return True

    def compile_pdf(self, tex_path: str | Path) -> bool:
        path = Path(tex_path)
        if not path.exists():
            return False

        candidates: list[Path] = [
            Path(r"C:\Users\enric\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe"),
            Path("pdflatex"),
        ]
        compiler = None
        for candidate in candidates:
            if candidate.exists():
                compiler = candidate
                break
            if shutil.which(str(candidate)):
                compiler = candidate
                break
            if candidate.name == "pdflatex":
                compiler = candidate

        if compiler is None:
            return False

        try:
            subprocess.run(
                [str(compiler), "-interaction=nonstopmode", str(path.name)],
                cwd=str(path.parent),
                check=True,
                capture_output=True,
                text=True,
            )
            return True
        except subprocess.CalledProcessError:
            return False

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
            proof = self.refine_proof(summary)
            self.update_summary_document(summary, proof)
            self.compile_pdf(self.summary_path)

            if self.objective_reached(summary):
                return {
                    "status": "completed",
                    "iterations": iteration + 1,
                    "queries_seen": len(seen_queries),
                    "summary": summary,
                    "proof": proof,
                    "records": all_records,
                }

            if not self.should_continue(summary):
                return {
                    "status": "done",
                    "iterations": iteration + 1,
                    "queries_seen": len(seen_queries),
                    "summary": summary,
                    "proof": proof,
                    "records": all_records,
                }

            if iteration < self.max_iterations - 1:
                queryset = [
                    "Karp 1972 TSP NP-hardness",
                    "Held Karp dynamic programming TSP exact",
                    "Euclidean TSP PTAS Arora",
                    "TSP special cases polynomial time exact",
                ]

        final_summary = self.evaluate_records(all_records)
        final_proof = self.refine_proof(final_summary)
        self.update_summary_document(final_summary, final_proof)
        self.compile_pdf(self.summary_path)
        return {
            "status": "max_iterations_reached",
            "iterations": self.max_iterations,
            "queries_seen": len(seen_queries),
            "summary": final_summary,
            "proof": final_proof,
            "records": all_records,
        }


def main() -> None:
    parser = argparse.ArgumentParser(description="Evidence-driven TSP literature orchestrator")
    parser.add_argument("--queries", nargs="*", default=None, help="Target queries to run in sequence")
    parser.add_argument("--target", default=None, help="Single target query to evaluate")
    parser.add_argument("--max-results", type=int, default=3, help="Maximum results per query")
    parser.add_argument("--iterations", type=int, default=4, help="Maximum search iterations")
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent / "output" / "q_orchestrator_report.json", help="JSON report path")
    args = parser.parse_args()

    orchestrator = QOrchestrator(
        base_queries=args.queries or QOrchestrator().base_queries,
        max_iterations=args.iterations,
        max_results_per_query=args.max_results,
    )
    result = orchestrator.run(target=args.target)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({"status": result["status"], "summary": result["summary"], "report": str(args.output)}, indent=2))


if __name__ == "__main__":
    main()
