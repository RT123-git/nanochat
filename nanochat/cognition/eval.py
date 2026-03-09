"""Lightweight evaluation harness for baseline vs cognition comparisons."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import json
from typing import Protocol

from .agent import CognitionAgent
from .backend import BackendAdapter


class PromptBackend(Protocol):
    """Protocol for simple prompt-to-text evaluators."""

    def generate(self, prompt: str, **kwargs: object) -> str:
        """Return one response for the provided prompt."""


@dataclass(slots=True)
class EvalCase:
    """Single benchmark-style prompt with expected keywords."""

    case_id: str
    prompt: str
    expected_keywords: list[str]


@dataclass(slots=True)
class EvalRow:
    """Result row for one eval case."""

    case_id: str
    baseline_response: str
    cognition_response: str
    baseline_score: float
    cognition_score: float
    cognition_decision: str


@dataclass(slots=True)
class EvalSummary:
    """Aggregate summary of baseline vs cognition runs."""

    baseline_mean: float
    cognition_mean: float
    delta: float
    route_counts: dict[str, int]
    rows: list[EvalRow]


DEFAULT_CASES: list[EvalCase] = [
    EvalCase(
        case_id="memory_recall",
        prompt="Can you recall previous summarization guidance?",
        expected_keywords=["summarization", "guidance", "memory"],
    ),
    EvalCase(
        case_id="creative_ideation",
        prompt="Brainstorm three ideas for improving routing quality",
        expected_keywords=["ideas", "routing", "improving"],
    ),
    EvalCase(
        case_id="verification",
        prompt="Please verify this plan and provide the strongest option",
        expected_keywords=["verify", "plan", "option"],
    ),
    EvalCase(
        case_id="sandbox_branching",
        prompt="Try two approaches and pick the best branch",
        expected_keywords=["best", "branch", "approach"],
    ),
]


def score_keywords(response: str, expected_keywords: list[str]) -> float:
    """Return simple keyword recall score in [0, 1]."""
    if not expected_keywords:
        return 0.0
    response_text = response.lower()
    hits = sum(1 for keyword in expected_keywords if keyword.lower() in response_text)
    return hits / len(expected_keywords)


def run_eval(cases: list[EvalCase], backend: PromptBackend) -> EvalSummary:
    """Evaluate direct baseline generation against cognition-enhanced generation."""
    adapter = BackendAdapter(backend=backend)
    agent = CognitionAgent(backend=adapter)

    route_counts: dict[str, int] = {}
    rows: list[EvalRow] = []

    for case in cases:
        baseline_response = adapter.run(case.prompt)
        cognition_result = agent.run(case.prompt)

        baseline_score = score_keywords(baseline_response, case.expected_keywords)
        cognition_score = score_keywords(cognition_result.response, case.expected_keywords)
        route_counts[cognition_result.decision] = route_counts.get(cognition_result.decision, 0) + 1

        rows.append(
            EvalRow(
                case_id=case.case_id,
                baseline_response=baseline_response,
                cognition_response=cognition_result.response,
                baseline_score=baseline_score,
                cognition_score=cognition_score,
                cognition_decision=cognition_result.decision,
            )
        )

    baseline_mean = sum(row.baseline_score for row in rows) / len(rows)
    cognition_mean = sum(row.cognition_score for row in rows) / len(rows)
    return EvalSummary(
        baseline_mean=baseline_mean,
        cognition_mean=cognition_mean,
        delta=cognition_mean - baseline_mean,
        route_counts=route_counts,
        rows=rows,
    )


def write_eval_artifact(summary: EvalSummary, output_path: str) -> Path:
    """Persist machine-readable eval artifact to JSON."""
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "baseline_mean": summary.baseline_mean,
        "cognition_mean": summary.cognition_mean,
        "delta": summary.delta,
        "route_counts": summary.route_counts,
        "rows": [asdict(row) for row in summary.rows],
    }
    output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return output
