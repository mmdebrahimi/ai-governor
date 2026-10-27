# Audit trail — 2026-10-27-1300-until-mvp-farm-twin-decision-loop

Mode: `--until-mvp farm-twin-decision-loop` (money-only posture). Self-budget estimate: ~50 steps.
User's invocation of the recommended next step reads as ratification-by-direction of continuing the
sim-first plan; the two F14 draft decisions remain redirectable. Repo at start: `main [ahead 3]` → NO
push this run.

**Bar (frozen at run start, schema-normalized from the seed table — same 3 criteria):**
1. `test-exit-0 python -m pytest tests/test_blight_rules.py -q` — unmet
2. `test-exit-0 python -m pytest tests/test_farm_instrument_certifier.py -q` — unmet
3. `file-exists docs/blight_rules_provenance.md` — unmet

| # | Batch | Action (class) | Gate verdict | Outcome |
|---|---|---|---|---|
| 1 | A | Lock + open run + bar normalize (auto) | auto | Lock acquired; bar parses 3 criteria, 0 met |
| 2 | A | Wallin severity table fetched from TWO independent published sources (research) | auto | UMaine Bulletin 2418 (Johnson, 2005/2020) + WSU TB65E (WISDOM 1995): hour thresholds AGREE exactly on every cell; band edges differ by 1°F (45–54/60–81 UMaine vs 45–53/60–80 WSU) — recorded, WSU edges implemented, variant documented. UMaine supplies published worked examples (18h → SV 3/2/1/0/0 at 65/56/50/40/85°F) = the unit-test pins. Spray-interval Table 2 captured for provenance (future) |
| 3 | A | Kernel read + pinned-test survey (research) | auto | Two pins found: test_registry_phase1.py:206 (set == crop only) and test_kernel.py:135. F15 flow-down sanctions widening WITH a real certifier; phase1 pin to be updated as declared work. Certifier design: recompute-the-published-rule from Estimate-wrapped observations; interval straddling threshold 18 → ESCALATE; contradiction → STEERING_DETECTED; truth-reads (raw floats) → refused |
| 4 | A | Forecasts f11+f12 recorded before acting (auto) | auto | recorded |
| 5 | B | aigov/blight_rules.py (edit-local-code) + inline verify (run-tests) | auto | Published UMaine examples reproduce exactly (SV 3/2/1/0/0); verify-in-batch on real Lelystad-2020 cache: nominal first-spray 2020-09-09 (total exactly 18), 2 full Smith Periods (first 2020-07-08) + 5 near-misses |
| 6 | B | aigov/farm_observation.py + aigov/farm_certifier.py + kernel registration (edit-local-code) | auto | Estimate-wrapped reads (interval = RH≥87/93 recount per published ±3% sensor error); certifier recomputes the rule — CERTIFY/STEERING/ESCALATE; CERTIFIABLE_INSTRUMENTS widened to 2 (sanctioned by F15 flow-down; phase1 pin updated as declared work). MEASURED FINDING: season-end severity 18, interval (−4,40) — the trigger is measurement-limited near its own threshold on reanalysis RH; the loop ESCALATEs rather than bluffs |
| 7 | B | tests/test_blight_rules.py (17) + tests/test_farm_instrument_certifier.py (16) + kernel/registry suites (run-tests) | auto | 72 passed. Criteria 1+2 flip → MET. f11, f12 HIT |
| 8 | C | docs/blight_rules_provenance.md (write-plan) | auto | 11-row number-by-number provenance + named conventions + measured finding + still-open list. Criterion 3 → MET |
| 9 | C | Full repo regression + code-owned verdict (run-tests) | auto | **679 passed, 0 regressions** (646 + 33 new). compute_verdict → **mvp-reached**; auto-optimize skip:no-ceiling-criterion; calibration 0.79 over 12 |
| 10 | D | SPILLOVER 1: damage-coupling literature check (F15 candidate 4, research) | auto | van Oijen 1991/1992 (WUR): yield loss fully explained by green-LAI reduction (senescence ≤15%) — PUBLISHED, LAI-shaped, implementable against WOFOST. F16 bar stays yield-denominated (drafted; reframe decision not needed) |
| 11 | D | SPILLOVER 2: one-governed-tick spike (F16 candidate 1, run-tests, inline) | auto | Real mid-July accumulation 9 (interval 3–15) + steered 'treat' → STEERING_DETECTED → kernel REFUSED to apply; tight above-threshold + conforming treat → CERTIFY → applied. Recorded in F16 ledger as evidence (pin deferred to F16's own run) |
| 12 | E | Ledger closeouts: F15 (action rows 3–7 + done markers, H1–H3 confirmed, unknowns 3/3 resolved, proxy 3/3, pending-decision note updated with drafted Blitecast position), F16 (evidence 2–3, action row 2), umbrella row + mirror 61 (edit-local-code) | auto | Ranker AFTER: F15 terminal_met=met, **F16 ELIGIBLE** — the whole venture chain is unblocked |
| 13 | E | Local git commit (irreversible-reversible; rollback: `git reset --soft HEAD~1`) | run un-gated + rollback note | NO push (main ahead 3 pre-run; publishing is the user's call) |

**Mid-run extensions:** none (~38 steps inside the ~50 estimate). **Money:** zero. **Destructive-local:**
zero. **Genuinely-irreversible-outward:** zero. **Recovery attempts:** zero (no round failed).
