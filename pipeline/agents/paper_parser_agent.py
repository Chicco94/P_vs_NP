from __future__ import annotations

from typing import Any

from pipeline.agents.base_agent import BaseAgent
from pipeline.extractors.paper_extractor import normalize_paper


class PaperParserAgent(BaseAgent):
    name = "paper-parser-agent"
    description = "Normalizes raw paper metadata into a standard schema."

    def run(self, payload: list[dict[str, Any]]) -> list[dict[str, Any]]:
        normalized: list[dict[str, Any]] = []
        for item in payload:
            normalized.append(normalize_paper(item))
        return normalized
