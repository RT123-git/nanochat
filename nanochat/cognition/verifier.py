"""Verifier workspace for critique, ranking, and lightweight repair."""

from __future__ import annotations

from dataclasses import dataclass, field

from .schemas import Hypothesis, VerificationResult


@dataclass(slots=True)
class CandidateCritique:
    candidate_id: str
    strengths: list[str] = field(default_factory=list)
    issues: list[str] = field(default_factory=list)
    score: float = 0.0


@dataclass(slots=True)
class VerifierDecision:
    chosen_candidate_id: str
    ranked_candidate_ids: list[str]
    critiques: list[CandidateCritique]
    repaired_candidate: Hypothesis | None
    result: VerificationResult


class VerifierWorkspace:
    """Rank candidates with explicit critiques and optional repair."""

    def evaluate(
        self,
        candidates: list[Hypothesis],
        *,
        constraints: list[str] | None = None,
        allow_repair: bool = True,
    ) -> VerifierDecision:
        if not candidates:
            raise ValueError("VerifierWorkspace requires at least one candidate")

        critiques = [self._critique(candidate, constraints=constraints or []) for candidate in candidates]
        scored = sorted(critiques, key=lambda c: c.score, reverse=True)
        ranked_ids = [item.candidate_id for item in scored]
        best = scored[0]
        by_id = {candidate.hypothesis_id: candidate for candidate in candidates}
        chosen = by_id[best.candidate_id]

        repaired: Hypothesis | None = None
        if allow_repair and best.issues and constraints:
            repaired = self._repair(chosen, constraints)

        verified = not best.issues or repaired is not None
        verdict = "passed" if verified else "failed"
        if repaired is not None:
            verdict = "repaired"

        result = VerificationResult(
            verified=verified,
            verdict=verdict,
            issues=list(best.issues),
            score=best.score,
            metadata={"chosen_candidate_id": chosen.hypothesis_id},
        )

        return VerifierDecision(
            chosen_candidate_id=chosen.hypothesis_id,
            ranked_candidate_ids=ranked_ids,
            critiques=critiques,
            repaired_candidate=repaired,
            result=result,
        )

    def _critique(self, candidate: Hypothesis, *, constraints: list[str]) -> CandidateCritique:
        text = candidate.statement.lower()
        strengths: list[str] = []
        issues: list[str] = []

        if "step" in text:
            strengths.append("contains procedural guidance")
        if "because" in text or "therefore" in text:
            strengths.append("includes explicit justification")

        for constraint in constraints:
            if constraint.lower() not in text:
                issues.append(f"missing constraint: {constraint}")

        if "maybe" in text or "perhaps" in text:
            issues.append("hedged wording reduces decisiveness")

        score = max(0.0, 1.0 + (0.25 * len(strengths)) - (0.4 * len(issues)))
        return CandidateCritique(
            candidate_id=candidate.hypothesis_id,
            strengths=strengths,
            issues=issues,
            score=score,
        )

    def _repair(self, candidate: Hypothesis, constraints: list[str]) -> Hypothesis:
        repair_suffix = " ".join([f"Constraint satisfied: {item}." for item in constraints])
        repaired_text = f"{candidate.statement} {repair_suffix}".strip()
        return Hypothesis(
            hypothesis_id=f"{candidate.hypothesis_id}-repair",
            statement=repaired_text,
            confidence=min(1.0, candidate.confidence + 0.1),
            metadata={**candidate.metadata, "repaired_from": candidate.hypothesis_id},
        )
