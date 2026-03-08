# Nanochat Codex Pack v2

This pack is rewritten specifically for the existing `RT123-git/nanochat` repository.

It assumes the repo already has:
- a root `nanochat/` package
- `scripts/`, `tasks/`, and `tests/`
- `pyproject.toml`
- working chat and evaluation entrypoints

The pack is designed to help Codex add a **developmental cognition layer** to the repo without breaking the current nanochat training and speedrun workflow.

## Files to upload
Place these files into the existing repo with this structure:

- `AGENTS.md`
- `plans.md`
- `implement.md`
- `documentation.md`
- `codex_prompt_pack.md`
- `context_recovery_card.md`
- `docs/architecture.md`
- `docs/evals.md`

## Intent
These files tell Codex to:
- preserve the current repo layout
- avoid repo-wide restructuring
- avoid intrusive edits to training and speedrun code unless explicitly required
- implement new work as an isolated subsystem, preferably under `nanochat/cognition/`
- use targeted, cheap tests first
- stay compatible with the repo's current Python floor

## Recommended use
1. Upload these files to the repo root and `docs/` folder.
2. Start Codex with the bootstrap prompt in `codex_prompt_pack.md`.
3. Let Codex work milestone by milestone.
4. Use `documentation.md` as the project memory.
5. Use `context_recovery_card.md` whenever Codex starts drifting.
