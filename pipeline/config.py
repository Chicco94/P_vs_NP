from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "output"
DEFAULT_QUERIES = [
    "TSP NP-hard general case",
    "Held-Karp TSP dynamic programming exact",
    "Euclidean TSP PTAS approximation",
    "Metric TSP approximation algorithms",
    "traveling salesman problem special cases polynomial time",
]

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0 Safari/537.36"
)
