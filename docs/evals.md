# Evaluation plan for the nanochat cognition layer

## Objective
Show that the cognition subsystem improves practical behavior over a simpler baseline while fitting naturally into the existing nanochat repo.

## Evaluation philosophy
The first evaluation pass should be cheap, controlled, and easy to interpret.
Avoid building a giant benchmark harness before the basic subsystem works.

## Baselines
1. Existing nanochat-style direct generation loop
2. Nanochat plus memory only
3. Full cognition subsystem

## Evaluation families

### A. Memory usefulness
Goal:
Show that retrieval improves behavior on tasks that benefit from prior episodes or distilled knowledge.

Possible measures:
- retrieval relevance
- retrieval usefulness
- improvement versus no retrieval
- reduced repeated rediscovery

### B. Repeated-task improvement
Goal:
Show that repeated related tasks get easier after consolidation and reuse.

Possible measures:
- success rate over repeated trials
- retries before success
- skill reuse count
- improvement after a skill artifact is formed

### C. Candidate generation and selection
Goal:
Show that creative generation plus verification produces better final choices than direct one-shot answering on suitable tasks.

Possible measures:
- candidate diversity
- verifier ranking quality
- final-task success
- repair count

### D. Sandbox benefit
Goal:
Show that lightweight branch-and-score experimentation can improve final choice quality on tasks where trying alternatives helps.

Possible measures:
- score before sandbox vs after sandbox
- branch efficiency
- final win rate

### E. Trace quality
Goal:
Show that the system is inspectable enough to explain why it improved or failed.

Possible measures:
- presence of structured route rationale
- readable trace artifacts
- ability to identify why a choice was made

## How to align with the existing repo
Use existing repo patterns where sensible.
For example:
- existing script-style entrypoints in `scripts/`
- existing tests in `tests/`
- existing report or artifact conventions if practical

The first cognition eval does not need to reuse every current evaluation mechanism, but it should not fight the repo's style.

## Minimal first deliverables
- one lightweight evaluation entrypoint or script
- one baseline vs cognition-enhanced comparison
- machine-readable result artifact if practical
- markdown notes on setup, commands, and limitations

## Success criteria
A promising result is not just a better answer once.
A promising result shows some combination of:
- better use of prior experience
- lower rediscovery cost
- improved repeated-task performance
- evidence of reuse through skill artifacts
- clearer explanation of why the system made a choice
