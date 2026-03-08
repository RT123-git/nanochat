"""Lightweight branch-and-score sandbox for candidate experimentation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class SandboxOutcome:
    branch: str
    score: float
    rationale: str


class LightweightSandbox:
    def explore(self, query: str, branches: list[str]) -> list[SandboxOutcome]:
        outcomes: list[SandboxOutcome] = []
        for branch in branches:
            score = _score_branch(query=query, branch=branch)
            outcomes.append(SandboxOutcome(branch=branch, score=score, rationale="keyword_overlap"))
        outcomes.sort(key=lambda x: x.score, reverse=True)
        return outcomes


def _score_branch(query: str, branch: str) -> float:
    terms = [token for token in query.lower().split() if token]
    if not terms:
        return 0.0
    text = branch.lower()
    hits = sum(1 for term in terms if term in text)
    return hits / len(terms)
