from __future__ import annotations

from pathlib import Path
from typing import Any

from pipeline.agents.base_agent import BaseAgent


class SynthesisAgent(BaseAgent):
    name = "synthesis-agent"
    description = "Creates a summary report from classified paper records."

    def run(self, payload: list[dict[str, Any]], output_dir: str | Path | None = None) -> dict[str, Any]:
        report = {
            "paper_count": len(payload),
            "categories": {},
            "titles": [item.get("title", "Untitled") for item in payload],
        }

        for item in payload:
            category = item.get("classification", "UNKNOWN")
            report["categories"][category] = report["categories"].get(category, 0) + 1

        if output_dir is not None:
            out_dir = Path(output_dir)
            out_dir.mkdir(exist_ok=True, parents=True)
            summary_path = out_dir / "agent_summary.json"
            summary_path.write_text(str(report).replace("'", '"'), encoding="utf-8")
            report["summary_path"] = str(summary_path)

        return report
