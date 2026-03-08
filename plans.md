# plans.md

## Project
Nanochat cognition layer for the existing nanochat repository.

## Outcome
A repo-native experimental subsystem that wraps the existing nanochat stack with:
- episodic memory
- semantic memory
- router
- creative workspace
- verifier workspace
- lightweight sandbox
- consolidation / skill reuse
- traceable decision-making

The system should improve capability through structure while preserving nanochat's current minimal, hackable philosophy.

## Global constraints
- Preserve existing repo layout.
- Prefer `nanochat/cognition/` for new implementation.
- Prefer `scripts/cognition_demo.py` for first runnable entrypoint.
- Keep training and speedrun code untouched unless a milestone explicitly says otherwise.
- Keep first tests lightweight and CPU-friendly.
- Remain compatible with Python 3.10+.

## Suggested target file layout
This is a target, not a hard requirement:

```text
nanochat/
  cognition/
    __init__.py
    schemas.py
    backend.py
    memory.py
    router.py
    creative.py
    verifier.py
    sandbox.py
    consolidation.py
    skills.py
    traces.py
    agent.py
scripts/
  cognition_demo.py
  cognition_eval.py            # later milestone if needed
tests/
  test_cognition_schemas.py
  test_cognition_memory.py
  test_cognition_router.py
  test_cognition_agent.py
```

## Milestone 0 - Repo-native scaffold and integration plan
### Goals
- Confirm the existing repo structure and constraints
- Add only the minimum docs / module scaffold needed for the cognition subsystem
- Establish the first isolated entrypoint without disturbing current paths

### Acceptance criteria
- new work follows existing repo layout
- no `src/` migration or broad restructuring
- `nanochat/cognition/` exists with minimal scaffold
- at least one cheap smoke test exists for the new subsystem
- `documentation.md` records repo constraints and first design decisions

## Milestone 1 - Contracts and shared schemas
### Goals
- Define typed interfaces and shared data structures for the cognition subsystem
- Make integration with existing nanochat model / tokenizer / Engine explicit

### Acceptance criteria
- typed schemas exist for episodes, memories, traces, routing decisions, hypotheses, verifications, and skills
- backend interface can wrap existing nanochat generation stack
- focused unit tests validate basic contracts

## Milestone 2 - Memory subsystem
### Goals
- Implement episodic memory and semantic memory for the cognition layer
- Add simple retrieval and write policies

### Acceptance criteria
- memory write and retrieve path works
- relevance + recency strategy exists
- tests cover write -> retrieve -> rank behavior
- design is simple and replaceable

## Milestone 3 - Router
### Goals
- Decide when to answer directly, retrieve memory, explore creatively, verify, sandbox, or consolidate

### Acceptance criteria
- router emits structured decisions with rationale
- common scenarios are tested
- routing stays explicit and inspectable

## Milestone 4 - Creative and verifier workspaces
### Goals
- Add divergent idea generation and convergent critique / ranking
- Keep the first version inspectable rather than fancy

### Acceptance criteria
- creative workspace can produce multiple candidates
- verifier can critique, rank, and optionally repair candidates
- traces show why the final candidate was chosen
- tests validate candidate narrowing behavior

## Milestone 5 - Lightweight sandbox
### Goals
- Add a simple experimentation loop for branching and scoring candidate actions or plans

### Acceptance criteria
- multiple branches can be explored
- outcomes can be scored
- results are written back to episodic memory
- smoke tests prove the loop works without external infrastructure

## Milestone 6 - Consolidation and skill reuse
### Goals
- Distill repeated successful patterns into reusable skills or concepts
- Make future runs able to reuse them

### Acceptance criteria
- repeated wins can produce a skill artifact
- semantic memory and skill registry store provenance and trigger conditions
- later runs can discover and reuse the skill
- regression test proves reuse behavior

## Milestone 7 - End-to-end cognition loop
### Goals
- Connect backend wrapper, memory, router, workspaces, sandbox, and consolidation into a coherent loop
- Deliver a runnable demo path in the existing repo

### Acceptance criteria
- `scripts/cognition_demo.py` or equivalent runs
- end-to-end integration test passes
- output trace is inspectable
- existing nanochat paths remain intact

## Milestone 8 - Evaluation harness
### Goals
- Compare baseline nanochat behavior against cognition-enhanced behavior
- Reuse existing repo evaluation style where sensible

### Acceptance criteria
- at least one evaluation entrypoint exists for cognition experiments
- baseline vs enhanced comparisons are recorded
- evaluation artifacts are documented
- docs explain how to run the evals

## Milestone 9 - Polish and optional deeper integration
### Goals
- Improve docs, examples, config, and graceful failure behavior
- Optionally add carefully scoped integration hooks into chat workflows if justified

### Acceptance criteria
- docs are complete and repo-native
- quickstart for the cognition subsystem works
- optional integration points are documented and justified
