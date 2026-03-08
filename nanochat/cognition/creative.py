"""Creative workspace for generating multiple candidate responses."""

from __future__ import annotations

from .backend import BackendAdapter


class CreativeWorkspace:
    """Generate a small, inspectable set of candidate responses."""

    def __init__(self, backend: BackendAdapter) -> None:
        self.backend = backend

    def generate_candidates(self, query: str, limit: int = 3) -> list[str]:
        candidates: list[str] = []
        for idx in range(max(limit, 1)):
            prompt = f"{query}\n\nDraft option {idx + 1}:"
            text = self.backend.run(prompt).strip()
            if text and text not in candidates:
                candidates.append(text)
        return candidates
