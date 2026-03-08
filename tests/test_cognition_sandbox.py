from nanochat.cognition.memory import EpisodicMemory
from nanochat.cognition.sandbox import LightweightSandbox


def test_sandbox_explores_multiple_branches_and_scores() -> None:
    sandbox = LightweightSandbox()

    outcomes = sandbox.explore(
        "plan rollback safe deploy",
        branches=[
            "quick deploy now",
            "stepwise plan with rollback and monitor",
            "document lessons learned",
        ],
    )

    assert len(outcomes) == 3
    assert [item.score for item in outcomes] == sorted([item.score for item in outcomes], reverse=True)
    assert outcomes[0].branch_id.startswith("branch-")
    assert outcomes[0].outcome.startswith("Simulated")


def test_sandbox_writes_ranked_results_to_episodic_memory() -> None:
    sandbox = LightweightSandbox()
    memory = EpisodicMemory()

    outcomes = sandbox.explore(
        "verify migration plan",
        branches=["maybe do it", "step plan verify rollback"],
        episodic_memory=memory,
    )

    episodes = memory.recent(limit=10)
    assert len(episodes) == len(outcomes)
    assert all("sandbox" in episode.tags for episode in episodes)
    recorded_scores = sorted(
        [float(episode.metadata["score"]) for episode in episodes], reverse=True
    )
    expected_scores = sorted([item.score for item in outcomes], reverse=True)
    assert recorded_scores == expected_scores
