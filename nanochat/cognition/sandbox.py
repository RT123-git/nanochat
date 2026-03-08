"""Lightweight sandbox for branch-and-score experimentation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from .memory import EpisodicMemory
from .schemas import Episode


@dataclass(slots=True)
class SandboxOutcome:
    """Result of simulating one candidate branch in the sandbox."""

    branch_id: str
    candidate: str
    outcome: str
    score: float
    metadata: dict[str, object] = field(default_factory=dict)


class LightweightSandbox:
    """Run deterministic, cheap branch-and-score experiments.

    The sandbox intentionally uses heuristic simulation so it remains CPU-friendly
    and does not depend on external infrastructure.
    """

    def __init__(self, *, scorer: Callable[[str, str], float] | None = None) -> None:
        self._scorer = scorer or self._default_score

    def explore(
        self,
        query: str,
        branches: list[str],
        *,
        episodic_memory: EpisodicMemory | None = None,
    ) -> list[SandboxOutcome]:
        """Evaluate branch candidates and optionally persist results to episodes."""
        cleaned = [branch.strip() for branch in branches if branch.strip()]
        outcomes: list[SandboxOutcome] = []

        for index, candidate in enumerate(cleaned, start=1):
            score = self._scorer(query, candidate)
            outcome = self._simulate_outcome(candidate, score)
            outcomes.append(
                SandboxOutcome(
                    branch_id=f"branch-{index}",
                    candidate=candidate,
                    outcome=outcome,
                    score=score,
                )
            )

        outcomes.sort(key=lambda item: item.score, reverse=True)

        if episodic_memory is not None:
            for rank, item in enumerate(outcomes, start=1):
                episodic_memory.write(
                    Episode(
                        episode_id=f"sandbox-{item.branch_id}",
                        prompt=f"sandbox: {query}",
                        response=item.outcome,
                        tags=["sandbox", "branch"],
                        metadata={
                            "branch_id": item.branch_id,
                            "candidate": item.candidate,
                            "score": item.score,
                            "rank": rank,
                        },
                    )
                )

        return outcomes

    def _simulate_outcome(self, candidate: str, score: float) -> str:
        verdict = "promising" if score >= 0.6 else "uncertain"
        return f"Simulated {verdict} outcome for: {candidate}"

    def _default_score(self, query: str, candidate: str) -> float:
        query_terms = {token for token in query.lower().split() if token}
        branch_terms = {token for token in candidate.lower().split() if token}
        if not query_terms or not branch_terms:
            return 0.0

        overlap = len(query_terms & branch_terms) / len(query_terms)
        procedural_bonus = 0.1 if {"step", "steps", "plan"} & branch_terms else 0.0
        risk_bonus = 0.1 if {"verify", "rollback", "monitor"} & branch_terms else 0.0
        return min(1.0, overlap + procedural_bonus + risk_bonus)
