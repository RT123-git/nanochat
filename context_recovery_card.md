# Codex context-recovery card

Use this when Codex starts drifting, repeating itself, or forgetting repo constraints.

## Read order
1. `documentation.md`
2. `plans.md`
3. `implement.md`
4. `docs/architecture.md`
5. `docs/evals.md`
6. relevant existing repo files for the active milestone
7. any existing `nanochat/cognition/` files

## What Codex must reconstruct
- current milestone
- completed milestones
- remaining acceptance criteria
- repo constraints that cannot be violated
- latest design decisions
- validation status
- next smallest coding step

## Hard rules
- trust repository files over chat memory
- do not assume unfinished work is complete
- do not widen scope
- do not restructure the repo
- do not disturb training / speedrun code unless explicitly required
- update `documentation.md` after every real change

## Minimal recovery prompt
```text
Recover project state from repository files only.
Read documentation.md, plans.md, implement.md, docs/architecture.md, docs/evals.md, and the relevant current repo files.
Tell me the active milestone, remaining acceptance criteria, repo constraints, and the next smallest coding step.
Then implement only that step, run targeted validation, update documentation.md, and stop.
```
