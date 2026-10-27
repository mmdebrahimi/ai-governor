# Result — 2026-10-27-1100-until-mvp-farm-twin-world

**Verdict (code-owned): `mvp-reached`** — all 3 F14 criteria live-MET in one round, re-checked live.
Spillover (default-on) then banked F15's ratification-free research head-start and stopped at the
genuine authority fork (ratification of the two draft-then-ratify decisions + F15's rules-module work
being its own until-mvp run).

| | |
|---|---|
| planned / executed steps | ~40 / ~36 (no extensions) |
| gates hit | none (zero money / destructive / genuinely-irreversible) |
| tests | **646 passed, 0 regressions** (19 new; validation suite fully OFFLINE) |
| forecasts | f9 HIT, f10 HIT; calibration 0.75 over 10 |
| recovery attempts | 1 (harvest-day tripwire defect — diagnosed + fixed in-batch) |
| budget verdict | done (bar met inside estimate) |

## Delivered

| | |
|---|---|
| Reference region-season | ten Den et al. 2022 trial site-seasons (Lelystad + Vredepeel NL, 2019+2020) — field-measured near-potential yields for the EXACT cultivars PCSE ships; PCSE's Fontane verified BY RUNNING to carry the paper's calibration (TSUMEM 255 + REALLOC_*) |
| Frozen contract | `docs/farm_twin_world_spec.md` §5, authored BEFORE the first validation run: Layer-1 repro ±10% vs paper-sim; Layer-2 fidelity ±20% vs observed; 2020 gating / 2019 reported |
| Contract result | ALL 6 gating combos pass BOTH layers: Layer-1 worst +7.6%, Layer-2 worst −7.4%. 2019 reported: within ±4.7% of paper-sim on all 6 |
| Data spine | `data/farm_twin/weather/` — 4 cached files (NASA POWER daily PCSE-CSV + open-meteo hourly RH, both sites, 2019+2020); re-runs offline; missing cache raises |
| Wrapper | `aigov/farm_twin.py` — FarmTwin honoring coverage / observability-enforced reads / per-tick tripwires; `tests/test_farm_twin_disciplines.py` |
| Ranker state | F14 terminal_met=met (proxy 3/3); **F15 ELIGIBLE**; F16 blocked on F15 (correct) |
| Spillover | F15 evidence rows 4–7: Smith definition pinned (primary-adjacent authoritative review), Blitecast threshold-18 + 50%-emergence start, hourly-RH unknown resolved |

## Wall classification
**External (cheap): user ratification** of the two draft-then-ratify decisions recorded in the F14
ledger (reference region-season; contract bands). Everything after them is code-closable (F15: Wallin
1962 severity table → rules module → certifier). No money / hardware / partner walls; $0 cap holding.

---
single-session; not resumable — bounded attempts per active session only; a re-run after the lock
clears is a NEW session with a fresh budget; repeated re-runs are not globally bounded.
