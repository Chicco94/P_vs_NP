from __future__ import annotations

import json
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


def search_crossref(query: str, max_results: int = 5) -> list[dict[str, Any]]:
    """Recupera record da Crossref, una fonte bibliografica canonica e strutturata."""
    url = "https://api.crossref.org/works"
    params = {
        "query.title": query,
        "rows": max_results,
        "select": "title,author,issued,publisher,URL,abstract",
    }
    headers = {"User-Agent": USER_AGENT}

    try:
        if requests is not None:
            response = requests.get(url, params=params, headers=headers, timeout=20)
            response.raise_for_status()
            payload = response.json()
        else:
            query_string = "&".join(f"{key}={quote_plus(str(value))}" for key, value in params.items())
            req = Request(f"{url}?{query_string}", headers=headers)
            with urlopen(req, timeout=20) as response:
                payload = json.loads(response.read().decode("utf-8", errors="ignore"))
    except Exception:
        return []

    items = payload.get("message", {}).get("items", [])
    results: list[dict[str, Any]] = []
    for item in items[:max_results]:
        title = item.get("title", ["Untitled"])[0]
        authors = []
        for author in item.get("author", []) or []:
            given = author.get("given", "").strip()
            family = author.get("family", "").strip()
            if given and family:
                authors.append(f"{given} {family}")
            elif family:
                authors.append(family)
        issued = item.get("issued", {}).get("date-parts", [[None]])[0]
        year = issued[0] if issued and issued[0] else None
        abstract = item.get("abstract", "")
        if isinstance(abstract, str):
            abstract = abstract.replace("\n", " ").strip()
        results.append({
            "title": title,
            "authors": authors or ["Unknown author"],
            "year": year,
            "source": item.get("publisher", "Crossref"),
            "url": item.get("URL", ""),
            "abstract": abstract,
            "query": query,
        })
    return results


def search_openalex(query: str, max_results: int = 5) -> list[dict[str, Any]]:
    """Recupera record da OpenAlex, una fonte aperta e strutturata per lavori scientifici."""
    url = "https://api.openalex.org/works"
    params = {
        "search": query,
        "per-page": max_results,
        "mailto": "research@example.com",
    }
    headers = {"User-Agent": USER_AGENT}

    try:
        if requests is not None:
            response = requests.get(url, params=params, headers=headers, timeout=20)
            response.raise_for_status()
            payload = response.json()
        else:
            query_string = "&".join(f"{key}={quote_plus(str(value))}" for key, value in params.items())
            req = Request(f"{url}?{query_string}", headers=headers)
            with urlopen(req, timeout=20) as response:
                payload = json.loads(response.read().decode("utf-8", errors="ignore"))
    except Exception:
        return []

    results: list[dict[str, Any]] = []
    for item in payload.get("results", [])[:max_results]:
        title = item.get("title", "Untitled")
        authors = [a.get("author", {}).get("display_name", "Unknown author") for a in item.get("authorships", []) or []]
        year = item.get("publication_year")

        host_venue = item.get("host_venue") or {}
        primary_location = item.get("primary_location") or {}
        source_data = primary_location.get("source") or {}
        source = host_venue.get("display_name") or source_data.get("display_name") or "OpenAlex"

        url = item.get("ids", {}).get("doi") or item.get("id") or ""
        if url and not url.startswith("http"):
            if url.startswith("https://doi.org/"):
                pass
            else:
                url = f"https://doi.org/{url}"

        abstract = ""
        results.append({
            "title": title,
            "authors": authors or ["Unknown author"],
            "year": year,
            "source": source,
            "url": url,
            "abstract": abstract,
            "query": query,
        })
    return results


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
    seen_titles: set[str] = set()

    for query in queries:
        source_searchers = [
            search_crossref,
            search_openalex,
            search_google_scholar,
        ]
        for fetcher in source_searchers:
            for result in fetcher(query, max_results=max_results_per_query):
                title = str(result.get("title") or "").strip()
                if not title or title in seen_titles:
                    continue
                seen_titles.add(title)
                collected.append(result)
    return collected
