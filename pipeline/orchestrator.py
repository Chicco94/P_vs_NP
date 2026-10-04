from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from pipeline.classifiers.paper_classifier import classify_paper
from pipeline.collectors.scholar_collector import collect_results
from pipeline.config import DEFAULT_QUERIES, OUTPUT_DIR
from pipeline.extractors.paper_extractor import extract_keywords_for_notes, normalize_paper
from pipeline.models import PaperRecord
from pipeline.synthesizers.report_synthesizer import save_report


def run_pipeline(queries: list[str], max_results_per_query: int = 5) -> list[dict]:
    collected = collect_results(queries, max_results_per_query=max_results_per_query)
    records: list[dict] = []

    for index, raw in enumerate(collected, start=1):
        normalized = normalize_paper(raw)
        classification, confidence = classify_paper(
            normalized["title"],
            normalized["abstract"],
            normalized["problem"],
        )

        paper = PaperRecord(
            id=f"paper-{index}",
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
            notes=f"Keywords: {', '.join(extract_keywords_for_notes(normalized['title'], normalized['abstract'])['keywords'])}",
            raw=raw,
        )
        records.append(paper.to_dict())

    return records


def main() -> None:
    parser = argparse.ArgumentParser(description="Raccoglie, classifica e riassume la letteratura sul TSP.")
    parser.add_argument(
        "--queries",
        nargs="*",
        default=DEFAULT_QUERIES,
        help="Query di ricerca per Google Scholar.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=OUTPUT_DIR,
        help="Directory dove salvare il report generato.",
    )
    parser.add_argument("--max-results", type=int, default=5, help="Numero massimo di risultati per query.")
    args = parser.parse_args()

    results = run_pipeline(args.queries, max_results_per_query=args.max_results)
    report_path = save_report(results, args.output_dir)
    print(json.dumps({"status": "ok", "papers_found": len(results), "report": str(report_path)}, indent=2))


if __name__ == "__main__":
    main()
