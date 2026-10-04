from __future__ import annotations

import re
from html import unescape
from typing import Any, Iterable
from urllib.parse import quote_plus
from urllib.request import Request, urlopen

from pipeline.config import USER_AGENT

try:
    import requests  # type: ignore
except ModuleNotFoundError:  # pragma: no cover
    requests = None  # type: ignore

try:
    from bs4 import BeautifulSoup  # type: ignore
except ModuleNotFoundError:  # pragma: no cover
    BeautifulSoup = None  # type: ignore


def search_google_scholar(query: str, max_results: int = 5) -> list[dict[str, Any]]:
    """Recupera risultati da Google Scholar in modo generico e senza dipendenze aggiuntive."""
    url = f"https://scholar.google.com/scholar?q={quote_plus(query)}&hl=it&num={max_results}"
    headers = {"User-Agent": USER_AGENT}

    try:
        if requests is not None:
            response = requests.get(url, headers=headers, timeout=20)
            response.raise_for_status()
            html = response.text
        else:
            req = Request(url, headers=headers)
            with urlopen(req, timeout=20) as response:
                html = response.read().decode("utf-8", errors="ignore")
    except Exception as exc:
        return [{
            "title": f"Fallback result for query: {query}",
            "authors": ["Manual review required"],
            "year": None,
            "source": "Fallback",
            "url": "",
            "abstract": f"Google Scholar fetch failed: {exc}",
            "query": query,
        }]

    if BeautifulSoup is not None:
        soup = BeautifulSoup(html, "html.parser")
        items = soup.select("div.gs_ri")[:max_results]
        results: list[dict[str, Any]] = []
        for index, item in enumerate(items, start=1):
            title_tag = item.select_one("h3 a")
            title = title_tag.get_text(" ", strip=True) if title_tag else f"Paper {index}"
            citation_tag = item.select_one("div.gs_a")
            citation = citation_tag.get_text(" ", strip=True) if citation_tag else ""
            snippet_tag = item.select_one("div.gs_rs")
            snippet = snippet_tag.get_text(" ", strip=True) if snippet_tag else ""

            results.append({
                "title": title,
                "authors": [part.strip() for part in citation.split("-")[:1] if part.strip()] or ["Unknown author"],
                "year": _extract_year(citation),
                "source": citation,
                "url": title_tag.get("href", "") if title_tag else "",
                "abstract": snippet,
                "query": query,
            })
        return results

    return _fallback_parse_html(html, query, max_results)


def _fallback_parse_html(html: str, query: str, max_results: int) -> list[dict[str, Any]]:
    patterns = re.findall(r"<a[^>]*href=\"([^\"]+)\"[^>]*>(.*?)</a>", html, flags=re.IGNORECASE | re.DOTALL)
    results: list[dict[str, Any]] = []
    seen: set[str] = set()

    for href, content in patterns[:max_results * 10]:
        title = re.sub(r"<.*?>", "", content)
        title = unescape(title).strip()
        if not title or title in seen:
            continue
        seen.add(title)
        results.append({
            "title": title,
            "authors": ["Unknown author"],
            "year": None,
            "source": "Fallback parser",
            "url": href,
            "abstract": f"Fallback extraction for query: {query}",
            "query": query,
        })
        if len(results) >= max_results:
            break

    if not results:
        return [{
            "title": f"No direct Scholar result for: {query}",
            "authors": ["Manual check required"],
            "year": None,
            "source": "Scholar parse fallback",
            "url": "",
            "abstract": "The remote fetch succeeded but no structured result could be extracted.",
            "query": query,
        }]

    return results


def _extract_year(raw: str) -> int | None:
    match = re.search(r"\b(19|20)\d{2}\b", raw)
    if not match:
        return None
    return int(match.group(0))


def collect_results(queries: Iterable[str], max_results_per_query: int = 5) -> list[dict[str, Any]]:
    collected: list[dict[str, Any]] = []
    for query in queries:
        for result in search_google_scholar(query, max_results=max_results_per_query):
            collected.append(result)
    return collected
