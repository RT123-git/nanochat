from nanochat.cognition.creative import CreativeWorkspace
from nanochat.cognition.schemas import Hypothesis, Trace
from nanochat.cognition.verifier import VerifierWorkspace


def test_creative_workspace_generates_multiple_candidates_with_context() -> None:
    workspace = CreativeWorkspace()

    candidates = workspace.generate_candidates(
        "Design a robust rollout plan",
        count=4,
        seed_context=["must be reversible", "include monitoring"],
    )

    assert len(candidates) == 4
    assert [c.hypothesis_id for c in candidates] == ["cand-1", "cand-2", "cand-3", "cand-4"]
    assert all("Design a robust rollout plan" in c.statement for c in candidates)
    assert all("Context hints:" in c.statement for c in candidates)


def test_verifier_critiques_ranks_and_repairs_when_constraints_missing() -> None:
    verifier = VerifierWorkspace()
    candidates = [
        Hypothesis(hypothesis_id="cand-1", statement="Direct answer: do the migration maybe quickly."),
        Hypothesis(hypothesis_id="cand-2", statement="Stepwise plan: rollout in phases because rollback is required."),
    ]

    decision = verifier.evaluate(candidates, constraints=["monitoring", "rollback"], allow_repair=True)

    assert decision.chosen_candidate_id in {"cand-1", "cand-2"}
    assert decision.ranked_candidate_ids[0] == decision.chosen_candidate_id
    assert len(decision.critiques) == 2
    assert decision.result.verdict in {"repaired", "failed", "passed"}
    assert decision.repaired_candidate is not None
    assert "Constraint satisfied: monitoring." in decision.repaired_candidate.statement


def test_verifier_without_repair_reports_failed_if_issues_remain() -> None:
    verifier = VerifierWorkspace()
    candidates = [
        Hypothesis(hypothesis_id="cand-1", statement="Alternative framing: perhaps try something."),
    ]

    decision = verifier.evaluate(candidates, constraints=["deterministic"], allow_repair=False)

    assert decision.result.verified is False
    assert decision.result.verdict == "failed"
    assert decision.repaired_candidate is None
    assert any("missing constraint" in issue for issue in decision.result.issues)


def test_trace_supports_workspace_details() -> None:
    trace = Trace(
        trace_id="t-creative-1",
        query="How should we proceed?",
        decision="creative_explore",
        rationale="Need option breadth before narrowing",
        generated_candidates=["cand-1", "cand-2"],
        verifier_critiques=["cand-1 missing rollback", "cand-2 better justification"],
        ranking=["cand-2", "cand-1"],
        selected_candidate="cand-2",
        repairs=["cand-2-repair"],
    )

    assert trace.generated_candidates == ["cand-1", "cand-2"]
    assert trace.ranking[0] == "cand-2"
    assert trace.selected_candidate == "cand-2"
