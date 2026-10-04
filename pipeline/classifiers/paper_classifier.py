from __future__ import annotations


def classify_paper(title: str, abstract: str, problem: str) -> tuple[str, float]:
    text = f"{title} {abstract}".lower()

    if "ptas" in text or "polynomial time approximation scheme" in text:
        return "PTAS", 0.94
    if "approximation" in text and "scheme" not in text:
        return "APPROX", 0.88
    if "np-hard" in text or "np hard" in text or "hardness" in text:
        return "HARDNESS", 0.95
    if "dynamic programming" in text or "held-karp" in text or "exact" in text and "approx" not in text:
        if "metric" in text or "euclidean" in text or "planar" in text:
            return "EXACT_SPECIAL", 0.82
        return "EXACT_GENERAL", 0.85
    if "heuristic" in text or "empirical" in text:
        return "EMPIRICAL", 0.75
    if "metric" in text or "euclidean" in text or "planar" in text:
        return "EXACT_SPECIAL", 0.7
    return "UNKNOWN", 0.4
