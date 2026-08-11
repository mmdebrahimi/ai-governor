# Result - soraya --advance (aigov) run 3, 2026-08-11

## Spillover terminal summary
- **Planned:** ~70 | **Executed:** ~84 | **Extensions:** 1 (two defect-repair cycles)
- **Pivots:** 1 - F4 twin -> F5 kernel (Gate D unblocked mid-run by F4's completion)
- **terminal_reason:** all ACCEPTED families terminal-met + budget
- **budget_verdict:** ~84/100 (model-counted; OT1 - not a code-enforced cap)
- **Hard gates hit:** none

## Bars - 7/7 families MET
foundations 5/5 | constitution 4/4 | dept-contract 6/6 | collective-choice 4/4 |
guideline-intake 3/3 | **twin 3/3 (new)** | **kernel 3/3 (new)**

Tests: root **182** + vendored organ **193** = **375 green**.

## What changed in the world
1. **`aigov/twin.py`** - the world departments act on. Serves all 10 declared StateVars at matching
   observability, ENFORCES the observability field (a LATENT variable cannot be read as a measurement),
   reproduces the vendored per-capita references within 5%, and can FAIL - then refuses to report.
2. **`aigov/kernel.py`** - the runtime. `apply()` raises on 7 of the 8 gate-condition combinations and
   takes no bypass parameter. Binds the REAL vendored anti-steering gate where it is valid and REFUSES
   every other instrument rather than inventing a check.
3. **Gate C cleared; Gate D partially cleared.** The AI Governor now exists as a runnable object.

## Not resumable from here
Run closed. Next: F9 (D15 independent audit) and F10 (adversarial suite), then F11 integration.
