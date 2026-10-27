# Farm-Season Twin — Governed Season Integration (F16)

<!-- project-schema: 0.1 -->

> Initialized 2026-10-27 (Soraya self-init, run `2026-10-27-0900-decompose-plan-farm-season-twin`).
> Project ID: farm-governed-season. Originating goal (verbatim): "Run one full replayed historical
> potato season end-to-end under the aigov kernel with every action gated, emit a season report,
> extend the adversarial suite to the new instrument, and evaluate the venture kill condition".

> **PRIVACY — STANDING.** Public repo. Concept-level only.

## Project Context
- **Project ID:** farm-governed-season
- **Project root:** C:\Users\Farshad\PythonProjects\Skill_Development\AI_Governor
- **Captured:** 2026-10-27
- **Originating goal:** (verbatim above)
- **Refined goal (3c top candidate):** One governed replayed season: F14's world ticked day-by-day,
  F15's instrument proposed/ratified/certified/applied through the UNCHANGED kernel, a season report
  comparing governed vs status-quo vs never-treat runs, ≥3 new named adversarial attacks on the farm
  instrument all ending in detection or escalation, and a written kill-condition evaluation.
- **Horizon (months):** 4
- **Relationship to portfolio:** Gate C — the venture terminal. Depends on F14 + F15. The explicit
  NON-GOAL: a permanent farm-operations loop (unbounded operating state — the F13 init carved this
  out and the same carve-out binds here). Season two (dirt/hardware/orchestration over bought
  machines) is a USER decision gated on this family's season report.

## Empirical Concerns
- **Verdict:** FLAG
- **Check status:** inherited
- **Findings:** Inherits F14's composition-fidelity flag and F15's damage-coupling flag. Adds its own:
  a season report whose yield comparison rests on an unverified damage coupling must label those
  numbers model-coherent-only (the Mars twin's own honesty class), never outcome claims.

## Project vs Research-Program
- **Verdict:** FAIL → hybrid
- **Rationale:** BOUNDED: the replayed season, the report, the adversarial extension, the kill
  evaluation. UNBOUNDED: "govern the farm" — explicitly out, recorded as what the project makes
  possible, not what it delivers (same shape as F13's carve-out).

## Goal Hierarchy

### Mid-term (≤4 months)
| # | Milestone | Success Criterion |
|---|---|---|
| 1 | One governed tick | a single sim day flows propose→ratify→certify→apply with zero bypasses |
| 2 | Full governed season | replayed season completes; every applied action carries a RatificationRecord + certification |
| 3 | Season report | governed vs status-quo vs never-treat comparison, honesty-labelled |
| 4 | Adversarial extension | ≥3 named attacks on the farm instrument; all end in detection or escalation |
| 5 | Kill condition evaluated | written verdict against the decompose doc §5 condition, either way |

## MVP Criteria
<!-- attempt-budget: 3 -->
- test-exit-0 python -m pytest tests/test_farm_governed_season.py -q
- file-exists docs/farm_season_report_v1.md
- test-exit-0 python -m pytest tests/test_adversarial_farm_instrument.py -q
<!-- project-state:end:mvp-criteria -->

(Schema-normalized 2026-10-27 from the seed-time table — same three criteria, no redefinition.)

## State Snapshot

### Assumptions
- The kernel's cycle machinery needs no fork to drive a 365-tick season — confidence: **medium**
- Season-scale determinism (seeded) is achievable so the report is reproducible — confidence: **high**

### Evidence
| # | Claim | Source | Confidence | Captured |
|---|---|---|---|---|
| 1 | Running the composed loop finds defects green suites cannot (kernel lost-atmosphere incident; decisions.py 3 defects) | this repo's own record | high | 2026-10-27 |
| 2 | Published LAI-shaped damage coupling exists: potato late-blight yield loss fully explained by reduced green leaf area (lesion coverage; senescence ≤15%) — implementable against WOFOST's own LAI | van Oijen WUR thesis 1991 + model papers 1991a/b, 1992 (Springer BF01998073); found by F15 run 2026-10-27-1300 | medium-high (abstract-level; fetch exact form before implementing) | 2026-10-27 |
| 3 | The governed chain works end-to-end on real replayed data: steered 'treat' at accumulation 9 (interval 3–15) → STEERING_DETECTED → kernel refused; conforming treat over clear-threshold observation → CERTIFY → applied | one-governed-tick spike, F15 run 2026-10-27-1300 (inline, not yet pinned as a test) | high (reproduced live; pin it in this family's first run) | 2026-10-27 |
<!-- project-state:end:evidence -->

### Unknowns
- ~~Cadence~~ RESOLVED 2026-10-27: on-change proposals + one on-the-record escalation at a nominal trigger under ambiguity (design note in aigov/farm_season.py)
- ~~Report denominator~~ RESOLVED 2026-10-27: v1 = risk-coverage + compliance (yield model-coherent-only); yield-denominated = registered v2 arm behind `van-oijen-coupling-paywall` (R9)
- H2's yield half — reopens when the constraint lifts (the v2 arm runs)

### Hypotheses (Active)
| ID | Statement | Status | Last-tested |
|---|---|---|---|
| H1 | The governed season completes with zero ungated applications | confirmed | 2026-10-27 |
| H2 | Governed run beats never-treat and ≈ matches status-quo calendar on the replayed season's risk profile | open | 2026-10-27 |
<!-- project-state:end:hypotheses -->

### Decisions Made
| Decision | Date | Notes |
|---|---|---|
| Venture kill condition + $0 season-one capital cap encoded here (user-ratified "supersede, bounded") | 2026-10-27 | See decompose doc §5; failing it re-instates F13 row 46's hobby decision with an R9 constraint-expiry entry |
| **SEASON-TWO: GO** (user, verbatim: "strong GO!") | 2026-10-27 | USER authority exercised against the season report (milestone 5 complete). Scope of season two is NOT yet decomposed — dirt/hardware/sensors/orchestration planning is a NEW cycle (idea-anchor → decompose), and the $0 season-one cap does NOT carry over automatically: season-two spend limits are a decision for that cycle's anchor. Sensor quality named in the report as the first budget question |
<!-- project-state:end:decisions-made -->

### Pending Decisions
| Decision | Proposer | Blocker | Notes |
|---|---|---|---|
| ~~Season-two go/no-go~~ DECIDED 2026-10-27: **GO** | user | — | See Decisions Made; season-two planning is a new cycle |
<!-- project-state:end:pending-decisions -->

## Bellman-Inspired Decision Frame

### Current state (one-line summary)
**MVP REACHED 2026-10-27** (run `2026-10-27-1500-until-mvp-farm-governed-season`): full governed
replayed season (125 days, deterministic), zero ungated applications (H1 confirmed), 8 named
adversarial attacks all detected/escalated/refused, season report v1 authored with the
kill-condition evaluation — **NOT TRIPPED, $0 spent**. Suite 693 green. Remaining: H2's yield half
(registered v2 arm behind the van Oijen paywall constraint) + the SEASON-TWO GO/NO-GO (user).

### Target state / terminal condition
All five milestones met and the kill condition evaluated in writing. The unbounded operating state is
explicitly NOT the terminal.

### Progress proxy
- MVP criteria met: 3 / 3 (measured 2026-10-27, code-owned verdict mvp-reached); milestones 5/5

### Candidate next actions
| # | Action | Class | Expected progress | Expected info gain | Uncertainty | Cost |
|---|---|---|---|---|---|---|
| 1 | One-governed-tick spike (earliest possible integration) | run-tests | high | highest | medium | 1 day once F14/F15 walk |
| 2 | Season-cadence design note (propose-per-tick vs on-change) | write-plan | medium | medium | low | 2 hrs |
<!-- project-state:end:candidate-actions -->

### Re-evaluation trigger
- after any action; immediately when F14 milestone 1 + F15 milestone 1 both land (unblocks the spike)

## Allowed Action Classes (v0.2 placeholder)
- `propose` / `research` / `write-plan` / `run-tests` / `ask-user` / `stop` — auto
- `edit-local-code` — auto in-cwd

## Action Log
| # | Date | Action class | Description | Outcome |
|---|---|---|---|---|
| 1 | 2026-10-27 | propose | /project-init protocol executed by hand (Soraya self-init, decompose mode) | ledger created |
| 2 | 2026-10-27 | run-tests | Spillover from F15 run: one-governed-tick integration spike executed inline (candidate 1, SPIKE ONLY — not pinned) | Full propose→certify→apply chain demonstrated on real Lelystad-2020 data incl. a kernel REFUSAL of a steered proposal (evidence 3). Named integration gap carried over: kernel._constraints_hold probes the COLONY twin for farm actions — binding the FarmTwin into the constraint probe is this family's work. Bar framing: damage coupling EXISTS published (evidence 2) → the yield-denominated bar stands as drafted; reframe-to-compliance NOT needed |
| 3 | 2026-10-27 | research | van Oijen 1991/1992 exact functional form sought: PAYWALLED (Springer BF01998073; NJPP 97/98). Deferred-and-registered instead of improvised: arm `van Oijen dynamic LAI damage coupling` declared (planned, R6) on "season-report-v2 yield-denominated comparison"; constraint `van-oijen-coupling-paywall` registered with manual expiry (R9) | Season-report v1 yield column stays model-coherent-only; NO agronomy authored in-house (the kill-condition rail held by refusing to improvise) |
| 4 | 2026-10-27 | edit-local-code | Kernel named gap CLOSED: Governor gains `farm_twin` binding; `_constraints_hold` routes the farm instrument to `FarmTwin.probe_next_tick()` (fresh-replica probe — PCSE's VariableKiosk breaks deepcopy, found by running); unbound farm twin FAILS CLOSED | Milestone 1 machinery completed properly (the spike's vacuous colony-probe is gone) |
| 5 | 2026-10-27 | edit-local-code | aigov/farm_season.py: governed-season runner — on-change cadence (resolves ledger unknown 1), scripted conventional-practice ratifier (NAMED simulation seam), two governed arms (precision-honoring / nominal-sensitivity), calendar + never-treat comparison arms. Two defects found by inspection mid-batch: unprotected-Smith counter included near-misses; ambiguity silently swallowed the nominal trigger (now routed through the kernel once → ESCALATE on record) | Deterministic 125-day season in ~11s. Measured: precision arm 0 sprays / 61 ambiguous days / 1 kernel ESCALATE (2020-09-09); nominal arm 1 spray CERTIFIED+applied (2020-09-09, the published trigger date) / 15 protected days; calendar 18 sprays; never-treat 0. Zero ungated applications anywhere |
| 6 | 2026-10-27 | run-tests | tests/test_farm_governed_season.py (6 tests: completion, H1 zero-bypass, both arms' kernel events, bracket arms, determinism) + tests/test_adversarial_farm_instrument.py (8 NAMED attacks A-FARM-1..8, every one ends in detection/escalation/refusal AND apply() raises) | 14 passed. Milestones 1,2,4 MET. Forecasts f13+f14 HIT |
| 7 | 2026-10-27 | write-plan | docs/farm_season_report_v1.md: measured arm table, honesty labels (yield = model-coherent PP ceiling, identical across arms BY CONSTRUCTION), H2 partial verdict (risk-coverage evaluable, yield deferred to v2), registered follow-ons, KILL-CONDITION EVALUATION: **NOT TRIPPED** (contract met first-run inside bands; zero in-house agronomy; $0 spent), season-two decision framed as USER authority with the sensor-quality input | Milestones 3+5 MET. Forecast f15 HIT. MVP criterion 2 MET |
| 8 | 2026-10-27 | run-tests | Full repo regression + code-owned verdict | **693 passed, 0 regressions** (14 new). compute_verdict → **mvp-reached**; auto-optimize skip:no-ceiling-criterion; calibration 0.83 over 15 |
| 9 | 2026-10-27 | ask-user | Season report delivered; user decided | **SEASON-TWO GO** recorded (user verbatim "strong GO!"); push to origin authorized by the user; plain-English season-one summary requested before formal sign-off |
<!-- project-state:end:action-log -->

## Open Questions for User
- Season-two go/no-go is yours, gated on milestone 5 — recorded now so it cannot drift into an autonomous call.

## Last Evaluation
- **Date:** 2026-10-27
- **Progress signal:** (init only)
