# implement.md

## Source of truth
Follow `plans.md` milestone by milestone. Do not jump ahead unless explicitly told to.

## First read before any coding
Before changing code, always read:
1. `README.md`
2. `pyproject.toml`
3. `AGENTS.md`
4. `plans.md`
5. `documentation.md`
6. relevant existing repo files for the active milestone

For example:
- for integration: inspect `scripts/chat_cli.py`, `scripts/chat_web.py`, `nanochat/engine.py`, and checkpoint loading flow
- for evaluation: inspect `scripts/chat_eval.py`, `tasks/`, and report utilities
- for testing style: inspect `tests/`

## Work cycle
For each milestone:
1. Restate the active milestone and acceptance criteria.
2. Name the exact files you plan to touch.
3. Inspect the existing repo files that relate to those changes.
4. Implement the smallest clean slice that satisfies the milestone.
5. Run targeted validation first.
6. Fix failures before broadening scope.
7. Update `documentation.md`.
8. Mark milestone status accurately.

## Scope control
- Do not refactor unrelated modules.
- Do not introduce repo-wide tooling churn early.
- Do not replace existing chat or training paths when a wrapper will do.
- Avoid heavyweight infrastructure in v1.

## Validation guidance
Prefer the lightest relevant validation first.

Typical order:
- syntax sanity for touched files
- targeted unit tests for new cognition modules
- targeted integration test for the new subsystem
- optional broader `pytest` run if the milestone touches shared code

Use the repo's current setup before inventing new setup.
Prefer commands like:
- `python -m pytest -q tests/test_cognition_*.py`
- `python -m pytest -q tests/test_cognition_agent.py`
- `python -m scripts.cognition_demo`

Only add or require tools like `ruff` or `mypy` if:
- they already exist in the repo, or
- the milestone explicitly introduces them and documents why

## Coding standards
- Maintain Python 3.10+ compatibility.
- Use simple dataclasses and plain Python first unless another choice is clearly justified.
- Keep interfaces explicit and swappable.
- Prefer composition over inheritance.
- Add docstrings to public modules, classes, and functions.
- Keep observability built in through trace objects and structured outputs.

## Integration rules
- Treat the cognition subsystem as an optional layer around nanochat, not a replacement for nanochat.
- Prefer an adapter that can call existing model + tokenizer + `Engine`.
- Preserve existing CLI and eval entrypoints unless explicitly asked to integrate more deeply.
- Avoid changing `runs/` and speedrun-critical code.

## Documentation update format
Every real change must update `documentation.md` with:
- active milestone
- repo files inspected
- files changed
- decisions made
- commands run
- results
- known issues
- next step

## Done definition
Only mark a milestone done when:
- acceptance criteria are met
- relevant validation passed
- docs were updated
- the repo state is recoverable from `documentation.md`
