# Plan artifact — decompose & --plan, farm-season-twin (2026-10-27)

**Bar for THIS run (checkable):** F14 MVP criterion 1 — `tests/test_farm_twin_smoke.py` green on this
host (day-steppable potato world on Python 3.14), plus all decompose/registration artifacts in place.
Full F14→F16 completion is NOT this run's bar — it is the families' (horizons 2–4 months).

**Budget:** ~100-step self-budget; estimate for this run ≈ 30 steps. No money steps planned; one
dep-install (reversible; rollback: `pip uninstall pcse`); one local git commit (reversible); NO push
(pre-existing unpushed commit on main — publishing it is not this run's call).

## Ordered batches

| Batch | Steps | Gate class | Depends on |
|---|---|---|---|
| A. Decompose + register | research (4 web lookups) · decompose doc · 3 ledgers · account ×3 · umbrella rows · flow-down rows · F13 supersession row · mirrors | auto | — |
| B. Ranker verification | `advance_ranker.rank(aigov.md)` — F14 must parse ELIGIBLE; F15/F16 blocked:predecessor (fail-closed, expected) | auto | A |
| C. World-model install + smoke | `pip install pcse` (irreversible-reversible: run + rollback note) · exploratory smoke script (API discovery 5.x/6.x) · day-step potato run with mid-run state reads | auto | B |
| D. Formalize | `tests/test_farm_twin_smoke.py` pinned from the working API · full suite regression run (430 must stay green) | auto | C |
| E. Record + close | F14 action rows · forecast scores · audit trail · recommendation/result · local commit · release lock | auto (commit reversible) | D |

**Irreversible-flagged:** pip install (reversible, noted) · git commit (local, reversible). ZERO
genuinely-irreversible-outward steps. Money: none.

## Forecasts (E1, scored at re-check)
| id | Action | Prediction |
|---|---|---|
| f1 | pcse installs on Python 3.14 | predicted_flip: install-ok, expected_progress: high — **medium confidence** (3.9/3.10 target) |
| f2 | potato season steps day-by-day with readable state | predicted_flip: F14-MVP-1, expected_progress: high — high confidence IF f1 hits |
