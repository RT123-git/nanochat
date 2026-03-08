#!/usr/bin/env python3
"""Runnable demo entrypoint for the nanochat cognition loop."""

from __future__ import annotations

import argparse

from nanochat.cognition.agent import CognitionAgent
from nanochat.cognition.backend import BackendAdapter


class DemoBackend:
    def generate(self, prompt: str, **_: object) -> str:
        return f"demo-backend response to: {prompt.splitlines()[0][:120]}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Run cognition loop demo")
    parser.add_argument("query", nargs="?", default="Brainstorm ideas for a tiny chatbot")
    args = parser.parse_args()

    agent = CognitionAgent(backend=BackendAdapter(backend=DemoBackend()))
    result = agent.run(args.query)

    print("Decision:", result.decision)
    print("Response:", result.response)
    print("Trace:", result.trace)


if __name__ == "__main__":
    main()
