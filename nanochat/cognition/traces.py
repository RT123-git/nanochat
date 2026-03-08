"""Trace assembly helpers for cognition loop inspection."""

from __future__ import annotations

from .schemas import Trace


class TraceRecorder:
    def __init__(self) -> None:
        self._counter = 0

    def build(self, query: str, decision: str, rationale: str, steps: list[str], metadata: dict[str, object] | None = None) -> Trace:
        self._counter += 1
        return Trace(
            trace_id=f"trace-{self._counter}",
            query=query,
            decision=decision,
            rationale=rationale,
            steps=steps,
            metadata=metadata or {},
        )
