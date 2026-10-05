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


def test_collect_results_demotes_generic_fallback_noise(monkeypatch):
    from pipeline.collectors.scholar_collector import collect_results

    def fake_crossref(query, max_results=5):
        return [{
            "title": "Karp 1972: Reducibility Among Combinatorial Problems",
            "authors": ["R. Karp"],
            "year": 1972,
            "source": "Crossref",
            "url": "https://example.org/karp",
            "abstract": "Canonical NP-hardness result for TSP",
            "query": query,
        }]

    def fake_openalex(query, max_results=5):
        return [{
            "title": "Traveling Salesman Decision Problem",
            "authors": ["A. Smith"],
            "year": 1980,
            "source": "OpenAlex",
            "url": "https://example.org/openalex",
            "abstract": "TSP complexity overview",
            "query": query,
        }]

    def fake_google(query, max_results=5):
        return [{
            "title": "Paper 1",
            "authors": ["Unknown"],
            "year": None,
            "source": "Fallback",
            "url": "",
            "abstract": "Generic webpage with no canonical bibliographic signal",
            "query": query,
        }]

    monkeypatch.setattr("pipeline.collectors.scholar_collector.search_crossref", fake_crossref)
    monkeypatch.setattr("pipeline.collectors.scholar_collector.search_openalex", fake_openalex)
    monkeypatch.setattr("pipeline.collectors.scholar_collector.search_google_scholar", fake_google)

    results = collect_results(["TSP NP-hardness"])
    assert results[0]["title"] == "Karp 1972: Reducibility Among Combinatorial Problems"
    assert [item["title"] for item in results].count("Paper 1") == 0


def test_orchestrator_updates_summary_and_compiles_when_objective_is_reached(monkeypatch, tmp_path):
    orchestrator = QOrchestrator(
        base_queries=["TSP NP-hardness"],
        max_iterations=2,
        max_results_per_query=1,
        corpus_path=tmp_path / "paper_corpus.json",
    )

    def fake_collect_results(queries, max_results_per_query=5):
        return [
            {
                "title": "Karp 1972: Reducibility Among Combinatorial Problems",
                "authors": ["R. Karp"],
                "year": 1972,
                "source": "Crossref",
                "url": "https://example.org/karp",
                "abstract": "NP-hardness for combinatorial optimization",
                "query": queries[0],
            },
            {
                "title": "Held-Karp Dynamic Programming for TSP",
                "authors": ["M. Held", "R. Karp"],
                "year": 1962,
                "source": "Crossref",
                "url": "https://example.org/held-karp",
                "abstract": "Exact dynamic-programming algorithm for TSP",
                "query": queries[0],
            },
        ]

    monkeypatch.setattr("pipeline.q_orchestrator.collect_results", fake_collect_results)
    monkeypatch.setattr("pipeline.q_orchestrator.normalize_paper", lambda raw: {
        "title": raw["title"],
        "authors": raw["authors"],
        "year": raw["year"],
        "source": raw["source"],
        "url": raw["url"],
        "abstract": raw["abstract"],
        "problem": "General TSP / NP-hardness" if "Karp" in raw["title"] else "TSP exact dynamic programming",
        "assumptions": ["General graph or unspecified metric"] if "Karp" in raw["title"] else ["Complete graph"],
        "complexity": "NP-hardness / lower bound" if "Karp" in raw["title"] else "Exact dynamic programming",
        "approach": "Complexity reduction / hardness result" if "Karp" in raw["title"] else "Dynamic programming / exact algorithm",
    })
    monkeypatch.setattr("pipeline.q_orchestrator.classify_paper", lambda title, abstract, problem: ("HARDNESS", 0.95) if "1972" in title else ("EXACT_SPECIAL", 0.9))
    monkeypatch.setattr("pipeline.q_orchestrator.extract_keywords_for_notes", lambda title, abstract: {"keywords": ["hardness", "tsp"] if "1972" in title else ["exact", "tsp"]})

    calls = []
    monkeypatch.setattr(orchestrator, "update_summary_document", lambda summary, proof: calls.append(("document", summary["has_required_evidence"], proof)))
    monkeypatch.setattr(orchestrator, "compile_pdf", lambda path: calls.append(("pdf", str(path))))

    result = orchestrator.run(target="TSP NP-hardness")

    assert result["status"] == "completed"
    assert calls[0][0] == "document"
    assert calls[1][0] == "pdf"


def test_update_summary_document_uses_real_newlines_in_latex(tmp_path):
    tex_path = tmp_path / "restricted_tsp_summary.tex"
    tex_path.write_text(
        "\\documentclass{article}\n\\begin{document}\n\\section{Evidence-driven literature refinement}\n"
        "The old text.\\n\\n\\section{Conclusion}\nThe conclusion.\\n\\end{document}\n",
        encoding="utf-8",
    )

    orchestrator = QOrchestrator(base_queries=["TSP NP-hardness"], summary_path=tex_path)
    summary = {"total_records": 3, "coverage_score": 0.8, "has_required_evidence": False}

    orchestrator.update_summary_document(summary, "The new proof text.")

    updated = tex_path.read_text(encoding="utf-8")
    assert "\\n\\n" not in updated
    assert "The new proof text." in updated
    assert "\\section{Evidence-driven literature refinement}" in updated


def test_orchestrator_accumulates_records_across_runs(tmp_path, monkeypatch):
    import json

    report_path = tmp_path / "q_orchestrator_report.json"
    corpus_path = tmp_path / "paper_corpus.json"
    report_path.write_text(
        '{"status": "done", "records": [{"id": "paper-1", "title": "Existing Paper", '
        '"year": 2001, "classification": "UNKNOWN", "confidence": 0.2}]}',
        encoding="utf-8",
    )
    orchestrator = QOrchestrator(
        base_queries=["TSP NP-hardness"],
        max_iterations=1,
        max_results_per_query=1,
        corpus_path=corpus_path,
    )
    collection_number = 0

    def fake_collect_results(queries, max_results_per_query=5):
        nonlocal collection_number
        collection_number += 1
        return [
            {
                "title": f"Collected Paper {collection_number}",
                "authors": ["A. Author"],
                "year": 2024,
                "source": "Crossref",
                "url": f"https://example.org/{collection_number}",
                "abstract": "A TSP paper",
                "query": queries[0],
            },
            {
                "title": "Existing Paper",
                "authors": ["A. Author"],
                "year": 2001,
                "source": "Crossref",
                "url": "https://example.org/existing",
                "abstract": "A richer TSP abstract",
                "query": queries[0],
            },
        ]

    monkeypatch.setattr("pipeline.q_orchestrator.collect_results", fake_collect_results)
    monkeypatch.setattr("pipeline.q_orchestrator.normalize_paper", lambda raw: {
        **raw,
        "problem": "TSP",
        "assumptions": [],
        "complexity": "Unknown",
        "approach": "Unknown",
    })
    monkeypatch.setattr("pipeline.q_orchestrator.classify_paper", lambda *args: ("UNKNOWN", 0.2))
    monkeypatch.setattr("pipeline.q_orchestrator.extract_keywords_for_notes", lambda *args: {"keywords": []})
    monkeypatch.setattr(orchestrator, "update_summary_document", lambda *args: True)
    monkeypatch.setattr(orchestrator, "compile_pdf", lambda *args: True)

    first_run = orchestrator.run()
    first_run_titles = {record["title"] for record in first_run["records"]}
    second_run = orchestrator.run()
    second_run_titles = {record["title"] for record in second_run["records"]}

    assert "Existing Paper" in first_run_titles
    assert first_run_titles < second_run_titles
    assert len(second_run["records"]) == len(second_run_titles)
    existing_paper = next(record for record in second_run["records"] if record["title"] == "Existing Paper")
    assert existing_paper["abstract"] == "A richer TSP abstract"
    assert len(json.loads(corpus_path.read_text(encoding="utf-8"))) == len(second_run_titles)
