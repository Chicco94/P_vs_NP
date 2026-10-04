from pipeline.q_orchestrator import QOrchestrator


def test_query_expansion_includes_canonical_terms():
    orchestrator = QOrchestrator(base_queries=["TSP NP-hardness"])
    expanded = orchestrator.expand_queries("TSP NP-hardness")

    assert len(expanded) >= 3
    assert any("Karp" in query for query in expanded)
    assert any("TSP" in query for query in expanded)


def test_evidence_gate_raises_when_hardness_and_special_case_are_present():
    orchestrator = QOrchestrator(base_queries=["TSP NP-hardness"])
    records = [
        {"classification": "HARDNESS"},
        {"classification": "EXACT_SPECIAL"},
        {"classification": "PTAS"},
    ]

    summary = orchestrator.evaluate_records(records)
    assert summary["has_required_evidence"] is True
    assert summary["coverage_score"] >= 0.5


def test_orchestrator_stops_when_evidence_is_sufficient():
    orchestrator = QOrchestrator(base_queries=["TSP NP-hardness"], min_evidence=2)
    summary = {
        "hardness_count": 1,
        "exact_special_count": 1,
        "ptas_count": 0,
        "coverage_score": 0.8,
        "has_required_evidence": True,
    }

    assert orchestrator.should_continue(summary) is False


def test_collect_results_prioritizes_canonical_sources(monkeypatch):
    from pipeline.collectors.scholar_collector import collect_results

    def fake_crossref(query, max_results=5):
        return [{"title": "Crossref Canonical Paper", "authors": ["A. Author"], "year": 2023, "source": "Crossref", "url": "https://example.org/crossref", "abstract": "Canonical result", "query": query}]

    def fake_openalex(query, max_results=5):
        return [{"title": "OpenAlex Canonical Paper", "authors": ["B. Author"], "year": 2023, "source": "OpenAlex", "url": "https://example.org/openalex", "abstract": "Canonical result", "query": query}]

    def fake_google(query, max_results=5):
        return [{"title": "Google Noise", "authors": ["C. Author"], "year": 2023, "source": "Google", "url": "https://example.org/google", "abstract": "Noisy", "query": query}]

    monkeypatch.setattr("pipeline.collectors.scholar_collector.search_crossref", fake_crossref)
    monkeypatch.setattr("pipeline.collectors.scholar_collector.search_openalex", fake_openalex)
    monkeypatch.setattr("pipeline.collectors.scholar_collector.search_google_scholar", fake_google)

    results = collect_results(["TSP NP-hardness"])
    titles = [item["title"] for item in results]
    assert titles[0] == "Crossref Canonical Paper"
    assert "OpenAlex Canonical Paper" in titles
    assert "Google Noise" in titles
