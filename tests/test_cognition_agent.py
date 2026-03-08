from __future__ import annotations

from nanochat.cognition.agent import CognitionAgent
from nanochat.cognition.backend import BackendAdapter
from nanochat.cognition.schemas import Episode


class FakeBackend:
    def generate(self, prompt: str, **kwargs: object) -> str:
        return f"generated::{prompt.splitlines()[0]}"


def test_end_to_end_cognition_loop_produces_trace_and_records_episode() -> None:
    agent = CognitionAgent(backend=BackendAdapter(backend=FakeBackend()))

    result = agent.run("Brainstorm ideas for memory routing")

    assert result.response
    assert result.trace.trace_id
    assert result.trace.decision == "creative_explore"
    assert result.trace.steps
    hits = agent.episodic.retrieve("memory routing", limit=5)
    assert hits


def test_end_to_end_retrieval_and_consolidation_paths() -> None:
    agent = CognitionAgent(backend=BackendAdapter(backend=FakeBackend()), min_skill_repetitions=2)
    agent.episodic.write(
        Episode(
            episode_id="e1",
            prompt="Summarize notes",
            response="extract bullets then condense",
            tags=["summarization"],
            metadata={"success": True, "trigger": "summarization", "strategy": "extract bullets then condense"},
        )
    )
    agent.episodic.write(
        Episode(
            episode_id="e2",
            prompt="Summarize report",
            response="extract bullets then condense",
            tags=["summarization"],
            metadata={"success": True, "trigger": "summarization", "strategy": "extract bullets then condense"},
        )
    )

    consolidated = agent.run("Please consolidate repeated summarization pattern")
    assert consolidated.decision == "consolidate"
    assert "Consolidated skill" in consolidated.response

    reused = agent.run("Can you help with summarization?")
    assert reused.reused_skill_id is not None
    assert reused.response.startswith("[Reused skill:")

    retrieval = agent.run("Can you recall previous summarization guidance?")
    assert retrieval.decision == "retrieve_memory"
    assert retrieval.trace.metadata["confidence"] > 0
