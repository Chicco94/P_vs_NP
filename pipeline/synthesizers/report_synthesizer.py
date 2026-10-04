from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def build_markdown_report(records: list[dict[str, Any]]) -> str:
    lines: list[str] = [
        "# TSP research report",
        "",
        "## Summary",
        "",
        f"Total papers reviewed: {len(records)}",
        "",
    ]

    for record in records:
        lines.extend([
            "## " + record.get("title", "Untitled"),
            "",
            f"- Classification: {record.get('classification', 'UNKNOWN')}",
            f"- Problem: {record.get('problem', 'General TSP')}",
            f"- Complexity: {record.get('complexity', 'Unspecified')}",
            f"- Approach: {record.get('approach', 'Unspecified')}",
            f"- Assumptions: {', '.join(record.get('assumptions', ['Unspecified']))}",
            f"- Notes: {record.get('notes', 'No extra notes')}",
            "",
        ])

    return "\n".join(lines)


def save_report(records: list[dict[str, Any]], output_dir: Path) -> Path:
    output_dir.mkdir(exist_ok=True, parents=True)
    json_path = output_dir / "tsp_pipeline_report.json"
    md_path = output_dir / "tsp_pipeline_report.md"

    json_path.write_text(json.dumps({"papers": records}, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(build_markdown_report(records), encoding="utf-8")
    return json_path
