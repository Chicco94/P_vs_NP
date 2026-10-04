from __future__ import annotations

from typing import Any

from pipeline.agents.base_agent import BaseAgent
from pipeline.classifiers.paper_classifier import classify_paper


class ClassifierAgent(BaseAgent):
    name = "classifier-agent"
    description = "Labels normalized papers using the repository taxonomy."

    def run(self, payload: list[dict[str, Any]]) -> list[dict[str, Any]]:
        classified: list[dict[str, Any]] = []
        for item in payload:
            category, confidence = classify_paper(item.get("title", ""), item.get("abstract", ""), item.get("problem", ""))
            enriched = dict(item)
            enriched["classification"] = category
            enriched["confidence"] = confidence
            classified.append(enriched)
        return classified
