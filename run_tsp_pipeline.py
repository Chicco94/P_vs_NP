from __future__ import annotations

import argparse
import json
from pathlib import Path

from pipeline.q_orchestrator import QOrchestrator


def main() -> None:
    parser = argparse.ArgumentParser(description="Task runner for the TSP evidence-driven orchestrator")
    parser.add_argument("--queries", nargs="*", default=None, help="List of initial queries to feed into the orchestrator")
    parser.add_argument("--target", default=None, help="Single target query to analyze")
    parser.add_argument("--max-results", type=int, default=3, help="Maximum results to collect per query")
    parser.add_argument("--iterations", type=int, default=4, help="Maximum search-improvement iterations")
    parser.add_argument("--summary-path", type=Path, default=Path(__file__).resolve().parent / "docs" / "restricted_tsp_summary.tex", help="Path to the summary .tex file")
    parser.add_argument("--pdf-path", type=Path, default=Path(__file__).resolve().parent / "docs" / "restricted_tsp_summary.pdf", help="Path to the final compiled PDF")
    args = parser.parse_args()

    base_queries = args.queries or QOrchestrator().base_queries
    orchestrator = QOrchestrator(
        base_queries=base_queries,
        max_iterations=args.iterations,
        max_results_per_query=args.max_results,
        summary_path=args.summary_path,
        pdf_path=args.pdf_path,
    )

    result = orchestrator.run(target=args.target)
    payload = {
        "status": result["status"],
        "iterations": result["iterations"],
        "queries_seen": result["queries_seen"],
        "summary": result["summary"],
        "proof": result.get("proof"),
        "target": args.target,
        "summary_path": str(args.summary_path),
        "pdf_path": str(args.pdf_path),
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
