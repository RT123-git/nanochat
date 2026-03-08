"""End-to-end cognition controller that wires module interactions."""

from __future__ import annotations

from dataclasses import dataclass

from .backend import BackendAdapter
from .consolidation import Consolidator
from .creative import CreativeWorkspace
from .memory import EpisodicMemory, SemanticMemory
from .router import ExplicitRouter
from .sandbox import LightweightSandbox
from .schemas import Episode, SkillArtifact, Trace
from .skills import SkillRegistry
from .traces import TraceRecorder
from .verifier import VerifierWorkspace


@dataclass(slots=True)
class CognitionResult:
    response: str
    trace: Trace
    decision: str
    reused_skill_id: str | None = None
    consolidated_skill: SkillArtifact | None = None


class CognitionAgent:
    def __init__(self, backend: BackendAdapter, min_skill_repetitions: int = 2) -> None:
        self.backend = backend
        self.episodic = EpisodicMemory()
        self.semantic = SemanticMemory()
        self.router = ExplicitRouter()
        self.registry = SkillRegistry()
        self.creative = CreativeWorkspace(backend=backend)
        self.verifier = VerifierWorkspace()
        self.sandbox = LightweightSandbox()
        self.traces = TraceRecorder()
        self.consolidator = Consolidator(
            semantic_memory=self.semantic,
            skill_registry=self.registry,
            min_repetitions=min_skill_repetitions,
        )

    def run(self, query: str) -> CognitionResult:
        decision = self.router.decide(query)
        steps = [f"route:{decision.action}"]
        reused_skill = self.registry.best_for(query)
        response = ""

        if decision.action == "retrieve_memory":
            episodes = self.episodic.retrieve(query, limit=3)
            steps.append(f"episodic_hits:{len(episodes)}")
            context = "\n".join(f"- {ep.prompt} -> {ep.response}" for ep in episodes)
            prompt = query if not context else f"{query}\n\nRelevant memory:\n{context}"
            response = self.backend.run(prompt)
        elif decision.action in {"creative_explore", "verify", "sandbox"}:
            candidates = self.creative.generate_candidates(query, limit=3)
            steps.append(f"candidates:{len(candidates)}")
            if decision.action == "sandbox":
                outcomes = self.sandbox.explore(query, branches=candidates)
                steps.append(f"sandbox_branches:{len(outcomes)}")
                response = outcomes[0].branch if outcomes else ""
            else:
                best = self.verifier.choose(query=query, candidates=candidates)
                steps.append(f"verifier_score:{best.score:.2f}")
                response = best.candidate
        elif decision.action == "consolidate":
            skill = self.consolidator.consolidate(self.episodic.recent(limit=50))
            if skill is None:
                response = "No repeated successful pattern was found yet."
                steps.append("consolidated:false")
            else:
                response = f"Consolidated skill: {skill.name} ({skill.skill_id})"
                steps.append("consolidated:true")
        else:
            response = self.backend.run(query)

        if reused_skill is not None:
            response = f"[Reused skill: {reused_skill.name}]\n{response}"
            steps.append(f"skill_reused:{reused_skill.skill_id}")

        episode = Episode(
            episode_id=f"ep-{len(self.episodic.recent(limit=10_000)) + 1}",
            prompt=query,
            response=response,
            tags=[decision.action],
            metadata={"success": bool(response.strip()), "decision": decision.action},
        )
        self.episodic.write(episode)

        consolidated_skill = self.consolidator.consolidate(self.episodic.recent(limit=50))
        if consolidated_skill is not None:
            steps.append(f"auto_consolidated:{consolidated_skill.skill_id}")

        trace = self.traces.build(
            query=query,
            decision=decision.action,
            rationale=decision.rationale,
            steps=steps,
            metadata={
                "confidence": decision.confidence,
                "reused_skill_id": reused_skill.skill_id if reused_skill else None,
            },
        )
        return CognitionResult(
            response=response,
            trace=trace,
            decision=decision.action,
            reused_skill_id=reused_skill.skill_id if reused_skill else None,
            consolidated_skill=consolidated_skill,
        )
