# Audit trail — 2026-10-27-0900-decompose-plan-farm-season-twin

Gate mode: money-only (default). Self-budget estimate: ~30 steps. Session-board checked: one live
peer session, different tree (non-colliding).

| # | Batch | Action (class) | Gate verdict | Outcome |
|---|---|---|---|---|
| 1 | A | 4 web lookups: PCSE/WOFOST, DSSAT steppability, Blitecast/Smith rules, NASA POWER (research) | auto | All four surfaces verified; PCSE chosen (steppable, EUPL, potato 701–704); DSSAT batch-only; published spray rules EXIST (provenance unlocked) |
| 2 | A | PCSE docs + WOFOST_crop_parameters fetches (research) | auto | Day-step `run()` + `get_variable` mid-run confirmed; potato varieties confirmed |
| 3 | A | Care disk check + repo state (auto) | auto | 62G free; main [ahead 1] — pre-existing unpushed commit noted → NO push this run |
| 4 | A | docs/farm-season-twin-decompose-2026-10-27.md (write-plan) | auto | Decomposition + flow-down + §0 verified surfaces + named fidelity gap (WOFOST has no disease model — composition risk stated) |
| 5 | A | 3 × /project-init protocol executed by hand (propose) | auto | F14 farm-twin-world, F15 farm-twin-decision-loop, F16 farm-governed-season ledgers created; ANNOUNCED |
| 6 | A | self_init account record ×3 (auto) | auto | 12/25 live, audit ALIGNED (12 on disk, all recorded) |
| 7 | A | Umbrella family rows + flow-down rows + F13 supersession decision + mirrors (edit-local-code) | auto | Direct-Edit + mirror rows 58/59 (umbrella), row 47 (F13) per AC9 |
| 8 | B | advance_ranker.rank verification (run-tests) | auto | F14 parses ELIGIBLE (next action = the smoke); F15/F16 blocked:predecessor fail-closed as designed; F13 parse bug did NOT recur. R15 advisory: all candidates tier small. F13 stale-candidate warnings noted as handoff |
| 9 | C | pip install pcse (dep-install, irreversible-reversible) | run un-gated + rollback note (`pip uninstall pcse -y`) | pcse 6.0.13 on Python 3.14 — clean. Forecast f1 HIT |
| 10 | C | Exploratory smokes ×4 (run-tests) | auto | Two real API gotchas found by RUNNING: YAMLCropDataProvider needs model=Wofost81_PP (default branch lacks REALLOC_DVS); site provider requires NAVAILI. Full season: 173 daily ticks, mid-run reads, TWSO 22,315 kg/ha dry (PP ceiling, model-coherent only) |
| 11 | D | tests/test_farm_twin_smoke.py pinned (edit-local-code) + run (run-tests) | auto | 4 passed, 2.4s (offline-cached). Verify-in-batch: output inspected, not just exit code |
| 12 | D | Full repo regression (run-tests) | auto | **627 passed, 0 regressions** (tests/ + aigov/choice/tests/) |
| 13 | E | F14 ledger rows 2–4, current-state refresh, H1→confirmed (edit-local-code) | auto | Mirrors recorded |
| 14 | E | Forecasts f1/f2 recorded + scored (auto) | auto | Both HIT; calibration 0.69 over 8 |
| 15 | E | Local git commit (irreversible-reversible) | run + rollback note (`git reset --soft HEAD~1`) | NO push (pre-existing unpushed commit is not this run's to publish) |

**Mid-run extensions:** none (ran inside the ~30-step estimate).
**Money actions:** zero. **Destructive-local:** zero. **Genuinely-irreversible-outward:** zero.
