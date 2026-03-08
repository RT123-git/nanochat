# AGENTS.md

## Mission
Add a **developmental cognition layer** to the existing nanochat repository.

The goal is not to rebuild nanochat from scratch. The goal is to extend the current repo with an isolated experimental subsystem that can improve capability through:
- episodic memory
- semantic memory
- routing
- creative exploration
- verification / planning
- lightweight sandbox experimentation
- consolidation of repeated wins into reusable skills

## Repo reality
This repository already exists and already works.
Treat these as established constraints:
- the codebase uses a root package layout, not `src/`
- there is already a `nanochat/` package
- there are already `scripts/`, `tasks/`, and `tests/`
- there is already a `pyproject.toml`
- there is already a chat path and evaluation path
- the repo's training and speedrun workflow is important and must not be disturbed casually

## Non-negotiable engineering rules
1. Do not restructure the repository.
2. Do not migrate to `src/` layout.
3. Keep new work isolated unless explicit integration is required by the active milestone.
4. Prefer placing new implementation under `nanochat/cognition/` unless a better repo-native location is clearly justified.
5. Do not modify `runs/`, `scripts/base_train.py`, the speedrun path, or core pretraining flow unless the milestone explicitly requires it.
6. Wrap existing nanochat components instead of replacing them whenever possible.
7. Preserve compatibility with Python 3.10+.
8. Keep tests CPU-friendly, fast, and runnable without downloading real checkpoints.
9. Prefer fake or mocked backends in tests for cognition modules.
10. Any new dependency must be justified in `documentation.md`.
11. Avoid repo-wide lint/type migration unless explicitly requested.
12. Keep diffs small, reviewable, and milestone-scoped.

## Integration principle
The developmental system should be treated as an optional layer around existing nanochat components.

Prefer this pattern:
- existing model + tokenizer + `Engine`
- cognition adapter / controller around them
- optional demo script or evaluation harness for the new subsystem

Avoid this pattern:
- rewriting existing training, inference, or chat code without strong reason

## Quality bar
A milestone is only done when:
- the acceptance criteria in `plans.md` are met
- relevant tests pass
- docs are updated
- `documentation.md` records what changed, what was validated, and what remains

## Documentation discipline
Keep these files current:
- `plans.md` = milestone source of truth
- `implement.md` = execution rules
- `documentation.md` = running log and recovery memory
- `docs/architecture.md` = architecture intent and integration model
- `docs/evals.md` = evaluation approach

## Prompt discipline
Whenever asked to continue:
1. Read `README.md`, `pyproject.toml`, `AGENTS.md`, `plans.md`, `implement.md`, and `documentation.md` first.
2. Inspect relevant repo files for the active milestone before changing code.
3. Restate the active milestone and acceptance criteria.
4. Name the exact files you plan to modify.
5. Implement the smallest clean slice.
6. Run targeted validation first, then broader validation if needed.
7. Update `documentation.md`.
8. Summarize exactly what remains.
