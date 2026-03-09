#!/usr/bin/env python3
"""Evaluate baseline vs cognition behavior with lightweight deterministic cases."""

from __future__ import annotations

import argparse

from nanochat.cognition.eval import DEFAULT_CASES, run_eval, write_eval_artifact


class EvalDemoBackend:
    """Simple deterministic backend for local cognition evals."""

    def generate(self, prompt: str, **_: object) -> str:
        first_line = prompt.splitlines()[0]
        return f"baseline response: {first_line}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Run cognition baseline-vs-enhanced eval")
    parser.add_argument(
        "--output",
        default="artifacts/cognition_eval.json",
        help="Path to JSON artifact for eval results",
    )
    args = parser.parse_args()

    summary = run_eval(DEFAULT_CASES, backend=EvalDemoBackend())
    artifact_path = write_eval_artifact(summary, args.output)

    print("Cognition eval summary")
    print(f"- baseline_mean: {summary.baseline_mean:.3f}")
    print(f"- cognition_mean: {summary.cognition_mean:.3f}")
    print(f"- delta: {summary.delta:.3f}")
    print(f"- route_counts: {summary.route_counts}")
    print(f"- artifact: {artifact_path}")


if __name__ == "__main__":
    main()
