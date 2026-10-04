from __future__ import annotations

from typing import Any

from pipeline.agents.base_agent import BaseAgent


class ValidationAgent(BaseAgent):
    name = "validation-agent"
    description = "Validates whether the evidence set is consistent with the TSP literature categories."

    def run(self, payload: list[dict[str, Any]]) -> dict[str, Any]:
        summary = {
            "total_papers": len(payload),
            "exact_general": 0,
            "exact_special": 0,
            "approx": 0,
            "ptas": 0,
            "hardness": 0,
            "empirical": 0,
            "unknown": 0,
        }

        for item in payload:
            category = (item.get("classification") or "UNKNOWN").upper()
            if category == "EXACT_GENERAL":
                summary["exact_general"] += 1
            elif category == "EXACT_SPECIAL":
                summary["exact_special"] += 1
            elif category == "APPROX":
                summary["approx"] += 1
            elif category == "PTAS":
                summary["ptas"] += 1
            elif category == "HARDNESS":
                summary["hardness"] += 1
            elif category == "EMPIRICAL":
                summary["empirical"] += 1
            else:
                summary["unknown"] += 1

        return summary
