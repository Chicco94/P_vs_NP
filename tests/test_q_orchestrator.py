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
