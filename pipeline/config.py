from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "output"
DEFAULT_QUERIES = [
    "Karp 1972 TSP NP-hardness",
    "Held Karp dynamic programming TSP exact",
    "Euclidean TSP NP-hardness Garey Johnson",
    "Planar TSP polynomial time special case",
    "Bitonic TSP polynomial time algorithm",
    "Metric TSP approximation lower bounds",
    "Euclidean TSP PTAS Arora",
    "TSP special cases polynomial time exact",
]

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0 Safari/537.36"
)
