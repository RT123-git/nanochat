# documentation.md

## Current status
- Active milestone: Milestones 0-3 completed (scaffold, contracts, memory, explicit router)
- Overall state: cognition subsystem scaffolded and validated in isolation; deeper integration intentionally pending Milestones 4+

## Repo constraints already identified
- Repository already exists and is functioning.
- Root package layout is already in use.
- Existing repo includes `nanochat/`, `scripts/`, `tasks/`, `tests/`, and `pyproject.toml`.
- Existing chat and evaluation flows already exist.
- The training / speedrun path should be treated as high-sensitivity code.
- New work should begin as an isolated subsystem, preferably under `nanochat/cognition/`.
- The repo currently targets Python 3.10+.

## Initial design stance
- Build a developmental cognition layer around the existing nanochat stack.
- Wrap existing model / tokenizer / `Engine` behavior rather than replacing it.
- Start with cheap CPU-friendly tests and fake backends.
- Add a dedicated demo path before considering deeper integration.

## Validation log
- No code changes yet.

## Change log
### Entry template
#### YYYY-MM-DD HH:MM
- Milestone:
- Repo files inspected:
- Files changed:
- Summary:
- Decisions made:
- Commands run:
- Results:
- Known issues:
- Next step:

## Known issues / risks
- It is easy for an agent to overreach and start restructuring the repo.
- It is easy to accidentally disturb speedrun or training-critical paths.
- A cognition layer can become too abstract too early if interfaces are not kept tight.
- Sandbox scope must stay intentionally lightweight in v1.

## How to run
- Populate after Milestone 0.

## Demo notes
- Populate after Milestone 0.

#### 2026-03-08 19:29
- Milestone: Milestone 0 (Task A scaffold)
- Repo files inspected: `documentation.md`, `plans.md`, `implement.md`, `AGENTS.md`, `docs/architecture.md`, `docs/evals.md`, `README.md`, `pyproject.toml`, `scripts/chat_cli.py`, `scripts/chat_eval.py`, `nanochat/engine.py`, `tests/test_engine.py`
- Files changed: `nanochat/cognition/__init__.py`, `tests/test_cognition_smoke.py`
- Summary: Added a minimal cognition package scaffold and a cheap smoke test to confirm import and baseline routing behavior.
- Decisions made: Kept the subsystem isolated under `nanochat/cognition/`; avoided touching training/speedrun/core paths.
- Commands run: `python -m compileall nanochat/cognition tests/test_cognition_smoke.py`; `python -m pytest -q tests/test_cognition_smoke.py`
- Results: Syntax check passed; smoke test passed.
- Known issues: None for Milestone 0 scaffold.
- Next step: Implement Milestone 1 typed schemas and backend contracts with focused tests.

#### 2026-03-08 19:29
- Milestone: Milestone 1 (Task B schemas/backend contracts)
- Repo files inspected: `plans.md`, `implement.md`, `docs/architecture.md`, `docs/evals.md`
- Files changed: `nanochat/cognition/schemas.py`, `nanochat/cognition/backend.py`, `tests/test_cognition_schemas.py`
- Summary: Added explicit dataclass schemas (`Episode`, `MemoryItem`, `Trace`, `RoutingDecision`, `Hypothesis`, `VerificationResult`, `SkillArtifact`) plus a minimal backend protocol and adapter contract.
- Decisions made: Used stdlib dataclasses/protocols only; no new dependencies.
- Commands run: `python -m compileall nanochat/cognition/schemas.py nanochat/cognition/backend.py tests/test_cognition_schemas.py`; `python -m pytest -q tests/test_cognition_schemas.py`
- Results: Syntax check passed; schema/contract tests passed.
- Known issues: Backend adapter remains intentionally minimal and not yet wired to `Engine` in this milestone.
- Next step: Implement Milestone 2 in-memory episodic and semantic memory with ranking tests.

#### 2026-03-08 19:30
- Milestone: Milestone 2 (Task C memory subsystem)
- Repo files inspected: `plans.md`, `docs/architecture.md`, `docs/evals.md`
- Files changed: `nanochat/cognition/memory.py`, `tests/test_cognition_memory.py`
- Summary: Implemented replaceable in-memory `EpisodicMemory` and `SemanticMemory` with write/retrieve helpers and simple relevance+recency ranking.
- Decisions made: Kept persistence out of scope; used transparent scoring and list-backed stores for easy replacement.
- Commands run: `python -m compileall nanochat/cognition/memory.py tests/test_cognition_memory.py`; `python -m pytest -q tests/test_cognition_memory.py`
- Results: Syntax check passed; memory behavior tests passed.
- Known issues: Ranking heuristics are intentionally simple and token-substring based.
- Next step: Implement Milestone 3 explicit router with structured decisions and edge-case tests.

#### 2026-03-08 19:30
- Milestone: Milestone 3 (Task D explicit router)
- Repo files inspected: `plans.md`, `docs/architecture.md`, `docs/evals.md`
- Files changed: `nanochat/cognition/router.py`, `tests/test_cognition_router.py`
- Summary: Added an explicit heuristic router that emits structured `RoutingDecision` values with rationale and confidence for direct/retrieve/creative/verify/sandbox/consolidate actions.
- Decisions made: Prioritized inspectable keyword heuristics over opaque logic to match milestone intent.
- Commands run: `python -m compileall nanochat/cognition/router.py tests/test_cognition_router.py`; `python -m pytest -q tests/test_cognition_router.py`
- Results: Syntax check passed; router scenario tests passed.
- Known issues: Heuristics are intentionally conservative and may need tuning with eval data in later milestones.
- Next step: Milestone 4+ workspace modules and optional cognition adapter integration around existing `Engine`.

#### 2026-03-08 19:31
- Milestone: Milestone 4 (creative + verifier workspaces)
- Repo files inspected: `documentation.md`, `plans.md`, `implement.md`, `AGENTS.md`, `docs/architecture.md`, `docs/evals.md`, `nanochat/cognition/schemas.py`, `nanochat/cognition/router.py`, `tests/test_cognition_schemas.py`
- Files changed: `nanochat/cognition/creative.py`, `nanochat/cognition/verifier.py`, `nanochat/cognition/schemas.py`, `nanochat/cognition/__init__.py`, `tests/test_cognition_creative_verifier.py`
- Summary: Added an isolated creative workspace that generates multiple inspectable candidates, plus a verifier workspace that critiques/ranks candidates and can optionally repair chosen outputs against constraints. Extended trace schema with candidate/verifier fields and added focused tests for generation, narrowing, and repair behavior.
- Decisions made: Kept logic deterministic/heuristic for cheap CPU tests; reused `Hypothesis`/`VerificationResult`; avoided modifying training, speedrun, or core pretraining flows.
- Commands run: `python -m compileall nanochat/cognition/creative.py nanochat/cognition/verifier.py nanochat/cognition/schemas.py tests/test_cognition_creative_verifier.py`; `python -m pytest -q tests/test_cognition_creative_verifier.py tests/test_cognition_schemas.py tests/test_cognition_memory.py tests/test_cognition_router.py`
- Results: Compile checks passed; targeted cognition tests passed (`16 passed`).
- Known issues: Verifier scoring/repair heuristics are intentionally simple (keyword+constraint checks) and should be tuned later with Milestone 8 eval data.
- Next step: Milestone 5 lightweight sandbox module and tests for branch-and-score outcomes written back to episodic memory.

#### 2026-03-08 19:33
- Milestone: Milestone 5 (lightweight sandbox)
- Repo files inspected: `README.md`, `pyproject.toml`, `AGENTS.md`, `plans.md`, `implement.md`, `documentation.md`, `docs/architecture.md`, `docs/evals.md`, `nanochat/cognition/schemas.py`, `nanochat/cognition/memory.py`, `nanochat/cognition/creative.py`, `nanochat/cognition/verifier.py`, `nanochat/cognition/__init__.py`
- Files changed: `nanochat/cognition/sandbox.py`, `nanochat/cognition/__init__.py`, `tests/test_cognition_sandbox.py`, `documentation.md`
- Summary: Added a deterministic lightweight sandbox that explores multiple branches, scores outcomes, and optionally records ranked branch results into episodic memory as sandbox-tagged episodes.
- Decisions made: Kept branch simulation heuristic and offline-only to satisfy CPU-friendly/no-infra goals; integrated by export only (no invasive wiring to existing chat/training flows).
- Commands run: `python -m compileall nanochat/cognition/sandbox.py nanochat/cognition/__init__.py tests/test_cognition_sandbox.py`; `python -m pytest -q tests/test_cognition_sandbox.py tests/test_cognition_creative_verifier.py tests/test_cognition_memory.py tests/test_cognition_router.py tests/test_cognition_schemas.py tests/test_cognition_smoke.py`
- Results: Compile checks passed; cognition-targeted suite passed (`19 passed`).
- Known issues: Sandbox scoring remains intentionally heuristic and should be tuned against Milestone 8 evaluation data.
- Next step: Implement Milestone 6 consolidation + skill reuse with provenance-aware storage and regression tests.
