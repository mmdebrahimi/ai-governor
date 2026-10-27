# Result — 2026-10-27-1500-until-mvp-farm-governed-season

**Verdict (code-owned): `mvp-reached`** — all 3 F16 criteria live-MET. With F14 and F15 already met,
**every gate of the farm-season-twin venture's season-one scope is now at its recorded bar.** No
spillover: the remaining moves are the user's (sign-off; season-two go/no-go) or external (the van
Oijen paywall constraint).

| | |
|---|---|
| planned / executed steps | ~60 / ~50 (no extensions) |
| gates hit | none (zero money / destructive / genuinely-irreversible across the whole venture) |
| tests | **693 passed, 0 regressions** (14 new) |
| forecasts | f13, f14, f15 all HIT; calibration 0.83 over 15 |
| recovery attempts | 3 (deepcopy-breaks, terminated-probe ordering, Smith/ambiguity counters — all fixed in-batch) |
| budget verdict | done (bar met inside estimate) |

## Delivered

| | |
|---|---|
| Governed season | `aigov/farm_season.py` — 125-day deterministic replay, on-change cadence, two governed arms, every application through the UNCHANGED kernel; **zero ungated applications** (H1 confirmed) |
| Kernel | farm-twin constraint binding (`Governor(farm_twin=…)` + `FarmTwin.probe_next_tick()`); unbound world fails closed |
| Adversarial extension | 8 named attacks (self-ratification, withheld/premature-spray steering, ambiguity bluff, truth-read injection, no-observation, key mismatch, unbound-world) — ALL end in detection/escalation/refusal |
| Season report | `docs/farm_season_report_v1.md` — measured arm table (precision: 0 sprays/1 ESCALATE; nominal: 1 spray on the published trigger date vs calendar's 18), honesty labels, **kill condition NOT TRIPPED, $0 spent** |
| Registered future | v2 yield-denominated arm (van Oijen coupling) behind constraint `van-oijen-coupling-paywall` — cannot evaporate (R6+R9) |

## Wall classification
**External + authority (both cheap to name, neither code-closable):** (a) USER sign-off on
season-one completion; (b) USER season-two go/no-go (the report's sharpest input: sensor quality is
what converts escalations into certified decisions); (c) the paywalled van Oijen full text (library
access lifts it). Nothing in season-one scope remains for code.

---
single-session; not resumable — bounded attempts per active session only; a re-run after the lock
clears is a NEW session with a fresh budget; repeated re-runs are not globally bounded.
