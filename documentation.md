# documentation.md

## Current status
- Active milestone: NOT STARTED
- Overall state: repo-specific cognition pack prepared; code integration not started

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
