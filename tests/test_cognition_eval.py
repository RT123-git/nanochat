from __future__ import annotations

import json

from nanochat.cognition.eval import DEFAULT_CASES, run_eval, write_eval_artifact


class FakeEvalBackend:
    def generate(self, prompt: str, **kwargs: object) -> str:
        return f"baseline::{prompt}"


def test_run_eval_produces_comparison_rows_and_route_counts() -> None:
    summary = run_eval(DEFAULT_CASES, backend=FakeEvalBackend())

    assert len(summary.rows) == len(DEFAULT_CASES)
    assert set(summary.route_counts)
    assert -1.0 <= summary.delta <= 1.0


def test_write_eval_artifact_writes_json_payload(tmp_path) -> None:
    summary = run_eval(DEFAULT_CASES, backend=FakeEvalBackend())

    artifact_path = write_eval_artifact(summary, str(tmp_path / "cognition_eval.json"))

    payload = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert payload["baseline_mean"] == summary.baseline_mean
    assert payload["cognition_mean"] == summary.cognition_mean
    assert len(payload["rows"]) == len(DEFAULT_CASES)
