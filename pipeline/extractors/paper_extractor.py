from __future__ import annotations

import re
from typing import Any


def normalize_paper(raw: dict[str, Any]) -> dict[str, Any]:
    title = (raw.get("title") or "Unknown title").strip()
    abstract = (raw.get("abstract") or "").strip()
    authors = raw.get("authors") or ["Unknown author"]
    if isinstance(authors, str):
        authors = [authors]

    problem = infer_problem(title, abstract)
    assumptions = infer_assumptions(title, abstract)
    complexity = infer_complexity(title, abstract)
    approach = infer_approach(title, abstract)

    return {
        "title": title,
        "authors": authors,
        "year": raw.get("year"),
        "source": raw.get("source", ""),
        "url": raw.get("url", ""),
        "abstract": abstract,
        "problem": problem,
        "assumptions": assumptions,
        "complexity": complexity,
        "approach": approach,
    }


def infer_problem(title: str, abstract: str) -> str:
    text = f"{title} {abstract}".lower()
    if "euclidean" in text:
        return "Euclidean TSP"
    if "metric" in text:
        return "Metric TSP"
    if "planar" in text:
        return "Planar TSP"
    if "np-hard" in text or "np hard" in text:
        return "General TSP / NP-hardness"
    if "held-karp" in text:
        return "Exact dynamic-programming TSP"
    return "General TSP"


def infer_assumptions(title: str, abstract: str) -> list[str]:
    text = f"{title} {abstract}".lower()
    assumptions: list[str] = []
    if "euclidean" in text:
        assumptions.append("Euclidean metric")
    if "metric" in text:
        assumptions.append("Metric distances")
    if "planar" in text:
        assumptions.append("Planar graph or geometric embedding")
    if "complete graph" in text:
        assumptions.append("Complete graph")
    if "asymmetric" in text:
        assumptions.append("Asymmetric TSP")
    if not assumptions:
        assumptions.append("General graph or unspecified metric")
    return assumptions


def infer_complexity(title: str, abstract: str) -> str:
    text = f"{title} {abstract}".lower()
    if "ptas" in text:
        return "PTAS or approximation scheme"
    if "np-hard" in text or "np hard" in text:
        return "NP-hardness / lower bound"
    if "dynamic programming" in text or "held-karp" in text:
        return "O(n^2 2^n) or exponential exact DP"
    if "approximation" in text:
        return "Approximation guarantee"
    return "Unspecified complexity in abstract"


def infer_approach(title: str, abstract: str) -> str:
    text = f"{title} {abstract}".lower()
    if "dynamic programming" in text or "held-karp" in text:
        return "Exact dynamic programming"
    if "ptas" in text or "approximation scheme" in text:
        return "Approximation scheme"
    if "heuristic" in text:
        return "Heuristic / empirical optimization"
    if "np-hard" in text or "hardness" in text:
        return "Complexity reduction / hardness result"
    return "General literature review or theoretical analysis"


def extract_keywords_for_notes(title: str, abstract: str) -> dict[str, Any]:
    cleaned = re.sub(r"[^a-zA-Z0-9 ]+", " ", f"{title} {abstract}").lower()
    tokens = [token for token in cleaned.split() if len(token) > 3]
    return {"keywords": sorted(set(tokens))[:20]}
