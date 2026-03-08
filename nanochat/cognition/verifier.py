"""Verifier workspace for ranking and selecting candidate responses."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RankedCandidate:
    candidate: str
    score: float
    rationale: str


class VerifierWorkspace:
    """Rank candidates with transparent keyword-overlap heuristics."""

    def rank(self, query: str, candidates: list[str]) -> list[RankedCandidate]:
        terms = _terms(query)
        ranked: list[RankedCandidate] = []
        for candidate in candidates:
            content_terms = _terms(candidate)
            if not content_terms:
                ranked.append(RankedCandidate(candidate=candidate, score=0.0, rationale="empty candidate"))
                continue
            overlap = sum(1 for term in terms if term in candidate.lower())
            score = overlap / max(len(terms), 1)
            ranked.append(
                RankedCandidate(
                    candidate=candidate,
                    score=score,
                    rationale=f"term_overlap={overlap}/{max(len(terms), 1)}",
                )
            )
        ranked.sort(key=lambda x: x.score, reverse=True)
        return ranked

    def choose(self, query: str, candidates: list[str]) -> RankedCandidate:
        ranked = self.rank(query=query, candidates=candidates)
        if not ranked:
            return RankedCandidate(candidate="", score=0.0, rationale="no candidates")
        return ranked[0]


def _terms(text: str) -> list[str]:
    return [token for token in text.lower().split() if token]
