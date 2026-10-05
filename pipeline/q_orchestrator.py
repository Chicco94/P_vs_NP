from __future__ import annotations

import argparse
import json
import logging
import re
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Any

logger = logging.getLogger(__name__)

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
    corpus_path: Path = field(
        default_factory=lambda: Path(__file__).resolve().parent / "output" / "paper_corpus.json"
    )
    algorithm_candidate_path: Path = field(
        default_factory=lambda: Path(__file__).resolve().parent / "output" / "algorithm_candidate.json"
    )

    @staticmethod
    def _record_key(record: dict[str, Any]) -> str:
        title = re.sub(r"[^\w]+", " ", str(record.get("title") or "").casefold()).strip()
        year = record.get("year")
        if title:
            return f"title:{title}:{year or ''}"
        url = str(record.get("url") or "").casefold().rstrip("/")
        return f"url:{url}"

    @classmethod
    def _upsert_record(cls, records: list[dict[str, Any]], record: dict[str, Any]) -> tuple[bool, bool]:
        key = cls._record_key(record)
        existing = next((item for item in records if cls._record_key(item) == key), None)
        if existing is None:
            record["id"] = f"paper-{len(records) + 1}"
            records.append(record)
            return True, True

        changed = False
        existing_confidence = float(existing.get("confidence") or 0.0)
        incoming_confidence = float(record.get("confidence") or 0.0)
        for name, value in record.items():
            if name == "id" or value in (None, "", [], {}):
                continue
            current = existing.get(name)
            if name == "classification":
                if incoming_confidence > existing_confidence and current != value:
                    existing[name] = value
                    changed = True
            elif name == "confidence":
                if incoming_confidence > existing_confidence:
                    existing[name] = value
                    changed = True
            elif isinstance(value, list):
                merged = list(dict.fromkeys([*(current or []), *value]))
                if merged != current:
                    existing[name] = merged
                    changed = True
            elif isinstance(value, dict):
                merged = {**(current or {}), **value}
                if merged != current:
                    existing[name] = merged
                    changed = True
            elif not current or (isinstance(value, str) and len(value) > len(str(current))):
                if current != value:
                    existing[name] = value
                    changed = True
        return False, changed

    def load_corpus(self) -> list[dict[str, Any]]:
        corpus_path = Path(self.corpus_path)
        source_path = corpus_path
        if not source_path.exists():
            legacy_report = corpus_path.parent / "q_orchestrator_report.json"
            if legacy_report.exists() and legacy_report != corpus_path:
                source_path = legacy_report
                logger.info("Importing existing records from legacy report %s", legacy_report)
            else:
                return []

        payload = json.loads(source_path.read_text(encoding="utf-8"))
        raw_records = payload if isinstance(payload, list) else payload.get("records", [])
        records: list[dict[str, Any]] = []
        for record in raw_records:
            if isinstance(record, dict):
                self._upsert_record(records, record.copy())

        if source_path != corpus_path or len(records) != len(raw_records):
            self.save_corpus(records)
        return records

    def save_corpus(self, records: list[dict[str, Any]]) -> None:
        corpus_path = Path(self.corpus_path)
        corpus_path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = corpus_path.with_suffix(corpus_path.suffix + ".tmp")
        temporary_path.write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")
        temporary_path.replace(corpus_path)

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
            "Deterministic polynomial-time exact algorithm for general TSP",
            "Unrestricted traveling salesman problem exact polynomial-time algorithm",
        ]
        expansions.extend(canonical)

        unique: list[str] = []
        seen: set[str] = set()
        for item in expansions:
            if item not in seen:
                seen.add(item)
                unique.append(item)
        return unique

    def evaluate_records(
        self,
        records: Iterable[dict[str, Any]],
        algorithm_candidate: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        record_list = list(records)
        counts: dict[str, int] = {}
        for record in record_list:
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
        candidate_count = int(self._is_synthesized_candidate(algorithm_candidate))
        verified_algorithm_count = int(self._is_verified_synthesized_candidate(algorithm_candidate))

        return {
            "hardness_count": hardness_count,
            "exact_special_count": exact_special_count,
            "exact_general_count": exact_general_count,
            "ptas_count": ptas_count,
            "approximation_count": approximation_count,
            "coverage_score": round(coverage_score, 3),
            "has_required_evidence": has_required_evidence,
            "algorithm_candidate_count": candidate_count,
            "verified_algorithm_count": verified_algorithm_count,
            "total_records": total,
            "min_evidence": self.min_evidence,
        }

    @staticmethod
    def _is_synthesized_candidate(candidate: dict[str, Any] | None) -> bool:
        return bool(
            candidate
            and candidate.get("origin") == "synthesized"
            and str(candidate.get("pseudocode", "")).strip()
        )

    @classmethod
    def _is_verified_synthesized_candidate(cls, candidate: dict[str, Any] | None) -> bool:
        return bool(
            cls._is_synthesized_candidate(candidate)
            and candidate.get("deterministic") is True
            and candidate.get("exact") is True
            and candidate.get("scope") == "general_tsp"
            and candidate.get("polynomial_time") is True
            and str(candidate.get("complexity_analysis", "")).strip()
            and str(candidate.get("correctness_argument", "")).strip()
            and candidate.get("verification_status") == "verified"
            and str(candidate.get("verification_evidence", "")).strip()
        )

    def load_algorithm_candidate(self) -> dict[str, Any] | None:
        candidate_path = Path(self.algorithm_candidate_path)
        if not candidate_path.exists():
            return None
        try:
            candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            logger.warning("Unable to read algorithm candidate %s: %s", candidate_path, error)
            return None
        if not isinstance(candidate, dict):
            logger.warning("Algorithm candidate %s must contain a JSON object", candidate_path)
            return None
        return candidate

    def should_continue(self, summary: dict[str, Any]) -> bool:
        return not self.objective_reached(summary)

    def objective_reached(self, summary: dict[str, Any]) -> bool:
        return summary.get("verified_algorithm_count", 0) >= 1

    def refine_proof(self, summary: dict[str, Any]) -> str:
        if self.objective_reached(summary):
            return (
                "A deterministic polynomial-time exact algorithm for unrestricted TSP is recorded as independently verified. "
                "The algorithm and its proof should remain linked to the verification evidence in the corpus."
            )
        if summary.get("algorithm_candidate_count", 0):
            return (
                "A synthesized algorithm candidate exists, but its exactness, general-case scope, polynomial complexity, "
                "and correctness argument have not all been verified. The research cycle continues."
            )
        return (
            "No synthesized algorithm candidate has been produced yet. Analyze the full text of the collected papers to "
            "derive a new candidate; hardness, exponential exact algorithms, approximation results, and special cases "
            "are source material, not the objective."
        )

    def update_summary_document(self, summary: dict[str, Any], proof_text: str) -> bool:
        tex_path = Path(self.summary_path)
        if not tex_path.exists():
            return False

        text = tex_path.read_text(encoding="utf-8")
        marker = "\\section{Evidence-driven literature refinement}"
        replacement = (
            "\\section{Evidence-driven literature refinement}\n\n"
            "The orchestrator evaluated the accumulated corpus of "
            f"{summary.get('total_records', 0)} records (coverage score: {summary.get('coverage_score', 0.0)}). "
            f"Algorithm claims matching the unrestricted deterministic polynomial-time exact criteria: "
            f"{summary.get('algorithm_candidate_count', 0)}; independently verified: "
            f"{summary.get('verified_algorithm_count', 0)}. "
            f"The algorithm-finding objective is {'reached' if self.objective_reached(summary) else 'not reached'}.\n\n"
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

        logger.info("Starting TSP orchestrator run with base queries=%s target=%s", queryset, target)
        all_records = self.load_corpus()
        logger.info("Loaded %s accumulated records from %s", len(all_records), self.corpus_path)
        seen_queries: set[str] = set()

        for iteration in range(self.max_iterations):
            logger.info("Iteration %s/%s: expanding and collecting evidence", iteration + 1, self.max_iterations)
            candidate_queries: list[str] = []
            for query in queryset:
                expanded = self.expand_queries(query)
                logger.info("Expanded query '%s' into %s candidate queries", query, len(expanded))
                candidate_queries.extend(expanded)

            pending_queries = list(dict.fromkeys(query for query in candidate_queries if query not in seen_queries))
            if not pending_queries:
                algorithm_candidate = self.load_algorithm_candidate()
                summary = self.evaluate_records(all_records, algorithm_candidate)
                proof = self.refine_proof(summary)
                logger.warning("No unseen queries remain; stopping without reaching the algorithm objective")
                self.update_summary_document(summary, proof)
                self.compile_pdf(self.summary_path)
                return {
                    "status": "search_stalled",
                    "iterations": iteration,
                    "queries_seen": len(seen_queries),
                    "summary": summary,
                    "proof": proof,
                    "records": all_records,
                }

            for query in pending_queries:
                seen_queries.add(query)
                logger.info("Querying bibliographic sources for: %s", query)
                raw_results = collect_results([query], max_results_per_query=self.max_results_per_query)
                logger.info("Received %s raw results for query '%s'", len(raw_results), query)

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
                    is_new, changed = self._upsert_record(all_records, paper.to_dict())
                    if changed:
                        self.save_corpus(all_records)
                    if is_new:
                        logger.info("Added paper '%s' to persistent corpus (%s records)", normalized["title"], len(all_records))
                    elif changed:
                        logger.info("Enriched existing paper '%s' in persistent corpus", normalized["title"])
                    else:
                        logger.debug("Paper '%s' already exists in persistent corpus", normalized["title"])

            algorithm_candidate = self.load_algorithm_candidate()
            summary = self.evaluate_records(all_records, algorithm_candidate)
            logger.info("Evaluated current evidence: %s", summary)

            proof = self.refine_proof(summary)
            logger.info("Updating summary document and regenerating PDF for this iteration")
            self.update_summary_document(summary, proof)
            self.compile_pdf(self.summary_path)

            if self.objective_reached(summary):
                logger.info("Objective reached; stopping orchestrator after iteration %s", iteration + 1)
                return {
                    "status": "completed",
                    "iterations": iteration + 1,
                    "queries_seen": len(seen_queries),
                    "summary": summary,
                    "proof": proof,
                    "records": all_records,
                }

            if iteration < self.max_iterations - 1:
                logger.info("Algorithm not verified; continuing search with follow-up queries")
                queryset = [
                    "Karp 1972 TSP NP-hardness",
                    "Held Karp dynamic programming TSP exact",
                    "Euclidean TSP PTAS Arora",
                    "TSP special cases polynomial time exact",
                    "Deterministic polynomial-time exact algorithm for general TSP",
                    "Unrestricted traveling salesman problem exact polynomial-time algorithm",
                ]

        algorithm_candidate = self.load_algorithm_candidate()
        final_summary = self.evaluate_records(all_records, algorithm_candidate)
        final_proof = self.refine_proof(final_summary)
        logger.info(
            "Maximum iterations reached without a verified algorithm; verified_algorithm_count=%s",
            final_summary.get("verified_algorithm_count", 0),
        )
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
    parser.add_argument("--corpus", type=Path, default=QOrchestrator().corpus_path, help="Persistent paper corpus JSON path")
    parser.add_argument("--algorithm-candidate", type=Path, default=QOrchestrator().algorithm_candidate_path, help="Synthesized algorithm candidate JSON path")
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent / "output" / "q_orchestrator_report.json", help="JSON report path")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    orchestrator = QOrchestrator(
        base_queries=args.queries or QOrchestrator().base_queries,
        max_iterations=args.iterations,
        max_results_per_query=args.max_results,
        corpus_path=args.corpus,
        algorithm_candidate_path=args.algorithm_candidate,
    )
    logger.info("Starting orchestrator CLI run")
    result = orchestrator.run(target=args.target)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({"status": result["status"], "summary": result["summary"], "report": str(args.output)}, indent=2))


if __name__ == "__main__":
    main()
