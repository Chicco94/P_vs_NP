from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class PaperRecord:
    id: str
    title: str
    authors: list[str] = field(default_factory=list)
    year: int | None = None
    source: str = ""
    url: str = ""
    abstract: str = ""
    problem: str = ""
    assumptions: list[str] = field(default_factory=list)
    complexity: str = ""
    approach: str = ""
    classification: str = "UNKNOWN"
    confidence: float = 0.0
    notes: str = ""
    raw: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "authors": self.authors,
            "year": self.year,
            "source": self.source,
            "url": self.url,
            "abstract": self.abstract,
            "problem": self.problem,
            "assumptions": self.assumptions,
            "complexity": self.complexity,
            "approach": self.approach,
            "classification": self.classification,
            "confidence": self.confidence,
            "notes": self.notes,
            "raw": self.raw,
        }
