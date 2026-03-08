"""Creative workspace for divergent candidate generation."""

from __future__ import annotations

from .schemas import Hypothesis


class CreativeWorkspace:
    """Generate multiple inspectable candidate hypotheses.

    The implementation is intentionally lightweight and deterministic so it is
    easy to test and reason about in Milestone 4.
    """

    _FRAMINGS = (
        "Direct answer",
        "Stepwise plan",
        "Alternative framing",
        "Risk-aware framing",
        "Counterexample check",
    )

    def generate_candidates(
        self,
        query: str,
        *,
        count: int = 3,
        seed_context: list[str] | None = None,
    ) -> list[Hypothesis]:
        prompt = query.strip()
        if not prompt:
            return []

        context_note = ""
        if seed_context:
            joined = "; ".join(seed_context[:2])
            context_note = f" Context hints: {joined}."

        target_count = max(1, count)
        candidates: list[Hypothesis] = []
        for idx in range(target_count):
            framing = self._FRAMINGS[idx % len(self._FRAMINGS)]
            statement = f"{framing}: {prompt}.{context_note}".strip()
            candidates.append(
                Hypothesis(
                    hypothesis_id=f"cand-{idx + 1}",
                    statement=statement,
                    confidence=max(0.2, 0.7 - (idx * 0.1)),
                    metadata={"framing": framing.lower().replace(" ", "_")},
                )
            )

        return candidates
