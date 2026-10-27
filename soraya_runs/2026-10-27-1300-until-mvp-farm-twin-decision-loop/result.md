# Result — 2026-10-27-1300-until-mvp-farm-twin-decision-loop

**Verdict (code-owned): `mvp-reached`** — all 3 F15 criteria live-MET in one round. Spillover banked
F16's two cheapest unknowns (damage coupling published; integration spike demonstrated), then stopped:
the next real moves are F16's own until-mvp run and two user ratifications.

| | |
|---|---|
| planned / executed steps | ~50 / ~38 (no extensions) |
| gates hit | none |
| tests | **679 passed, 0 regressions** (33 new) |
| forecasts | f11 HIT, f12 HIT; calibration 0.79 over 12 |
| budget verdict | done (bar met inside estimate) |

## Delivered

| | |
|---|---|
| Rules | `aigov/blight_rules.py` — Wallin table (two concurring published sources, cell-identical; 1°F edge variant named), Blitecast threshold-18 from 50% emergence, Smith Period + near-miss; 17 tests pinned to PUBLISHED worked examples |
| Observation | `aigov/farm_observation.py` — Estimate-wrapped severity with a DERIVED interval (±3% RH sensor error recounted through the 90% threshold); truth-reads refused |
| Certifier | `aigov/farm_certifier.py` + kernel registration — recompute-the-published-rule gate; CERTIFY / STEERING_DETECTED / ESCALATE-on-straddle / ESCALATE-on-no-observation; CERTIFIABLE_INSTRUMENTS = {crop_area_allocation, blight_treatment_trigger} |
| Provenance | `docs/blight_rules_provenance.md` — 11 numbers, each sourced; conventions and limits named |
| Measured finding | Season-scale severity is MEASUREMENT-LIMITED near the 18 trigger on reanalysis RH (interval −4…40): the loop escalates to humans instead of bluffing — the governance behaving as designed |
| Spillover | van Oijen 1991/1992 damage coupling (LAI-shaped, published) → F16 bar stays yield-denominated; one-governed-tick spike: kernel REFUSED a steered spray on real data, applied a conforming one |

## Wall classification
**External (cheap): user ratification** — (a) Blitecast vs Smith as the season-one ratified rule
(drafted: Blitecast primary, Smith diagnostic; they disagree by two months on the replayed season);
(b) the two standing F14 ratifications. Everything else is code-closable: F16's governed-season run
(bind FarmTwin into kernel._constraints_hold, implement the van Oijen coupling, replay the season
governed vs status-quo vs never-treat, adversarial attacks, kill-condition evaluation).

---
single-session; not resumable — bounded attempts per active session only; a re-run after the lock
clears is a NEW session with a fresh budget; repeated re-runs are not globally bounded.
