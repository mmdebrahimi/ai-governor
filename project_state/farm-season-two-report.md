# Farm Season Two — Report + Real-Plot Go/No-Go (F19)

<!-- project-schema: 0.1 -->

> Initialized 2026-10-27 (Soraya self-init, season-two decompose per the ratified anchor
> `docs/idea-anchor-prompt-farm-season-two-2026-10-27.md`). Project ID: farm-season-two-report.
> Originating goal (verbatim): "Freeze season two's scoring contract BEFORE the season starts, then
> score the completed virtual-shadow season on three metrics — escalation rate at real sensor
> precision vs the ERA5 baseline, sensor-vs-reanalysis divergence, and sim-twin parallel-run drift —
> evaluate the ratified kill condition, and draft the real-plot go/no-go for season three (the
> DECISION is the user's)".

> **PRIVACY — STANDING.** Public repo. No family composition, amounts, holdings or specific locations.
> The report scores data from "the sensor locale" (SHAPE); the cap is reported as breached/not-breached
> only, never as a number.

## Project Context
- **Project ID:** farm-season-two-report
- **Project root:** C:\Users\Farshad\PythonProjects\Skill_Development\AI_Governor
- **Captured:** 2026-10-27
- **Originating goal:** (verbatim above)
- **Refined goal (3c top candidate):** A scoring contract authored and FROZEN before any live data
  exists (same authored-first discipline as F14's validation contract), a scoring implementation
  proven on fixture data long before season end, and a season-two report (v2) that applies the frozen
  contract to F18's decision record, evaluates the kill condition, and ends in a DRAFTED real-plot
  go/no-go for the user to decide.
- **Horizon (months):** 12
- **Relationship to portfolio:** Gate C of season two — the venture gate holder, same shape F16 was
  for season one. Depends on F18 (the decision record). Its scoring-contract work is CROSS-CUTTING and
  runs in parallel with F17 (needs no hardware, no live data). Also hosts the van Oijen v2 arm
  (yield-denominated comparison) when the paywall constraint lifts (R9 register:
  `van-oijen-coupling-paywall`).

## Empirical Concerns
- **Verdict:** N-A
- **Check status:** not-applicable
- **Provisional:** NO
- **Findings:** (no new factual-shape claims; the three metrics are DEFINITIONS this family authors,
  and the season-one quantities they extend — escalation rate, ±3% RH interval, ERA5 baseline — are
  in-repo measured results as of 2026-10-27.)

## Project vs Research-Program
- **Verdict:** PASS
- **Provisional:** NO
- **Classification:** project
- **Rationale:** Bounded: contract frozen (file), scorer tested (fixtures), one report with one
  go/no-go draft. Terminal by construction — the season ends and the report closes it.

## Refinement Candidates
- **Verdict:** PASS
- **Provisional:** NO
- **Refined-from:** originating-goal
- **Candidates:**
  1. (TOP — adopted) Contract-first: freeze metrics + thresholds now, scorer on fixtures now, report
     at season end; kill condition evaluated against the frozen wording.
  2. Score-at-end-only (write the scorer when the data exists). Rejected: post-hoc metric choice is
     the exact bar-drift the authored-first discipline exists to prevent.
  3. Rolling mid-season reports (monthly). Deferred, not rejected: cheap once the scorer exists; adopt
     if the dry-run shows value — never a substitute for the frozen end-of-season contract.

## Goal Hierarchy

### Long-term (venture tier)
The venture's honesty organ for season two: the season is judged by rules written before the data
existed, and the step onto real land is a user decision made against those numbers.

### Mid-term (3-12 months)
| # | Milestone | Success Criterion | Horizon |
|---|---|---|---|
| 1 | Scoring contract FROZEN | docs/farm_season_two_scoring_contract.md: 3 metric definitions, denominators, thresholds, kill-condition wording — before any live data | 1 month |
| 2 | Scorer proven on fixtures | scoring implementation green on synthetic decision records (incl. outage-degraded ones) | 2-3 months |
| 3 | Dry-run scored | F18's winter dry-run report scored as a rehearsal (non-binding) | 3-5 months |
| 4 | Season report v2 + go/no-go draft | frozen contract applied to the real season; kill condition evaluated; real-plot go/no-go DRAFTED for the user | Oct 2027 |

### Short-term (≤1 month)
| # | Action | Class | Owner | Horizon |
|---|---|---|---|---|
| 1 | Author the scoring contract (3 metrics: definitions, denominators, data requirements, thresholds) | write-plan | claude | 1-2 weeks |
| 2 | Freeze the kill-condition wording (unscoreable season / cap breach → pause + re-plan) | write-plan | claude | days |
| 3 | Scorer skeleton + fixture decision records + tests | edit-local-code | claude | 2-4 weeks |

## MVP Criteria
<!-- attempt-budget: 3 -->
- file-exists docs/farm_season_two_scoring_contract.md
- test-exit-0 python -m pytest tests/test_farm_season_two_scoring.py -q
- file-exists docs/farm_season_report_v2.md
<!-- project-state:end:mvp-criteria -->

(Criteria 1-2 are reachable now at $0; criterion 3 — the report itself — lands at season end
(~Oct 2027), so this family's full bar is calendar-gated by construction. The contract MUST exist
before F18's live season starts; that ordering is the discipline, not a dependency accident.)

## State Snapshot

### Assumptions
- Season-one report machinery (SeasonReport/ArmResult shapes) extends to live-season scoring — confidence: high
- The three metrics are computable from F18's decision record + F17's divergence log alone — confidence: medium (the contract-writing step verifies data requirements against what the spine actually logs)
- The kill condition's "recovery budget" number comes from F17's derived budget, referenced not re-defined — confidence: high

### Evidence
| # | Claim | Source | Confidence | Captured |
|---|---|---|---|---|
| 1 | Season-one precedent: frozen-contract-then-measure held (bands authored first, results landed inside, bands not widened) | docs/farm_twin_world_spec.md §5 + validation tests | high | 2026-10-27 |
| 2 | Escalation-rate baseline exists: 61 ambiguous days / 1 ESCALATE at reanalysis precision (governed-precision arm, Fontane@Lelystad 2020) | docs/farm_season_report_v1.md | high | 2026-10-27 |
<!-- project-state:end:evidence -->

### Unknowns
- Threshold choice for "the sensor materially narrowed the interval" (to be DERIVED in the contract from the ±3% RH recount methodology, not asserted)
- Whether sim-twin drift needs its own fixture generator or falls out of F18's parallel-run log
- ~~Exact functional form of the van Oijen LAI damage coupling~~ RESOLVED 2026-10-27: full thesis obtained (open-access WUR eDepot, doi 10.18174/206318); form extraction is now ordinary arm work

### Hypotheses (Active)
| ID | Statement | Status | Last-tested |
|---|---|---|---|
| H1 | The frozen 3-metric contract is computable without any data source beyond F17 logs + F18 decision record | open | — |
<!-- project-state:end:hypotheses -->

### Decisions Made
| Decision | Date | Notes |
|---|---|---|
| Contract-first scoring (candidate 1); rolling reports deferred as optional addition | 2026-10-27 | Authored-first discipline inherited from F14 §5 |
| Real-plot go/no-go is DRAFTED by the report, DECIDED by the user | 2026-10-27 | Same authority shape as the season-two GO gate |
<!-- project-state:end:decisions-made -->

### Pending Decisions
| Decision | Proposer | Blocker | Notes |
|---|---|---|---|
| Real-plot go/no-go (season three) | claude (drafted in report v2) | season end ~Oct 2027 | USER decision |
<!-- project-state:end:pending-decisions -->

## Bellman-Inspired Decision Frame

### Current state (one-line summary)
Seeded from the season-two decompose; season-one report + measured baselines exist; no contract, no
scorer, no live data.

### Target state / terminal condition
Frozen contract + green scorer now; at season end, report v2 with the three scores, the kill-condition
verdict, and a drafted real-plot go/no-go awaiting the user.

### Progress proxy
MVP criteria met: 0 / 3 (seeded 2026-10-27)

### Candidate next actions
| # | Action | Class | Expected progress | Expected info gain | Uncertainty | Cost |
|---|---|---|---|---|---|---|
| 1 | Author + freeze the scoring contract | write-plan | high | high | low | med |
| 2 | Freeze kill-condition wording | write-plan | med | med | low | small |
| 3 | Scorer + fixtures + tests | edit-local-code | high | med | med | med |
<!-- project-state:end:candidate-actions -->

### Re-evaluation trigger
- **Default:** re-run `/project-state` after any action class fires
- **Manual override:** user invokes `/project-state farm-season-two-report` at any time

## Allowed Action Classes (v0.2 placeholder — not enforced in v0.1)
- `propose` — auto
- `research` — auto
- `write-plan` — auto
- `edit-local-code` — REQUIRES per-action human approval
- `run-tests` — auto if local + sandboxed
- `ask-user` — auto
- `stop` — auto

## Action Log
| # | Date | Action class | Description | Outcome |
|---|---|---|---|---|
| 1 | 2026-10-27 | propose | /project-init executed (Soraya self-init by hand, season-two decompose) | ledger created |
| 2 | 2026-10-27 | research | `van-oijen-coupling-paywall` LIFTED: full van Oijen 1991 PhD thesis (108pp, contains the 1991 light-use + leaf-area-dynamics papers and the 1992 simulation paper as Ch.1/3/6) obtained OPEN-ACCESS from Wageningen eDepot (doi 10.18174/206318); constraint registered+resolved in soraya_runs/constraint-expiry.json with evidence; full text stays OFF-REPO (copyright) at a local path named in the store | The planned arm `van Oijen dynamic LAI damage coupling` (criterion: season-report-v2 yield-denominated comparison) is now UNBLOCKED — runnable in a future Soraya run |
<!-- project-state:end:action-log -->

## Open Questions for User
- None blocking now. The go/no-go decision arrives with report v2 (~Oct 2027).

## Last Evaluation (v0.2 placeholder — not enforced in v0.1)
- **Date:** 2026-10-27
- **Progress signal:** (none yet — init only)
