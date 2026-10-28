# Farm Season Two — Virtual-Shadow Season Loop (F18)

<!-- project-schema: 0.1 -->

> Initialized 2026-10-27 (Soraya self-init, season-two decompose per the ratified anchor
> `docs/idea-anchor-prompt-farm-season-two-2026-10-27.md`). Project ID: farm-virtual-shadow-season.
> Originating goal (verbatim): "Run the governed loop LIVE for one season in virtual-shadow mode: the
> validated twin grows a virtual potato crop on real local weather one tick per real day; the governed
> loop (same rules, certifier, kernel as season one) decides daily on the real station/free-source
> observations in shadow mode (recommend-and-log; nothing is planted, nothing actuates); a parallel
> twin tick accumulates calibration data; the season's decision record survives outages within the
> declared recovery budget".

> **PRIVACY — STANDING.** Public repo. No family composition, amounts, holdings or specific locations.
> The virtual crop's weather locale comes from F17's off-repo site config; in-repo artifacts carry
> SHAPE only ("the sensor locale").

## Project Context
- **Project ID:** farm-virtual-shadow-season
- **Project root:** C:\Users\Farshad\PythonProjects\Skill_Development\AI_Governor
- **Captured:** 2026-10-27
- **Originating goal:** (verbatim above)
- **Refined goal (3c top candidate):** A live daily loop — tick(real day) → ingest (F17 spine) →
  governed decision (propose/ratify/certify, shadow: recommend-and-log) → decision-record append —
  whose machinery is fully testable NOW on simulated "today"s, dry-run for ≥7 real days this winter,
  and run for the full live season Apr–Sep 2027 (northern-hemisphere potato calendar), with the
  governed-precision/nominal arms and the ERA5-baseline arm running side by side for F19's scoring.
- **Horizon (months):** 12
- **Relationship to portfolio:** Gate B of season two (see `docs/farm-season-two-decompose-2026-10-27.md`).
  Depends on F17 (spine). Reuses F14 world + F15 instrument + F16 season-runner patterns UNCHANGED
  where possible (anchor fork 5: maximum transfer). Feeds F19.

## Empirical Concerns
- **Verdict:** N-A
- **Check status:** not-applicable
- **Provisional:** NO
- **Findings:** (no factual-shape claims beyond those already primary-source-pinned in season one —
  rules provenance, twin validation contract — all in-repo and green as of 2026-10-27. The one
  schedule-shaped fact, the Apr–Sep northern-hemisphere potato season, is encoded in the milestones
  rather than flagged: it is a calendar constraint, not a factual error in the goal.)

## Project vs Research-Program
- **Verdict:** PASS
- **Provisional:** NO
- **Classification:** project
- **Rationale:** ONE season, bounded: machinery tests green, a dated dry-run report, one live-season
  decision record. "Operate forever" is explicitly NOT this family — the season ends and F19 scores it.
  The live season's wall-clock length (~150 days) is calendar time, not open-ended scope.

## Refinement Candidates
- **Verdict:** PASS
- **Provisional:** NO
- **Refined-from:** originating-goal
- **Candidates:**
  1. (TOP — adopted) Build-now/dry-run-winter/live-season-2027: machinery + tests now on simulated
     days, ≥7-real-day dry-run on the free spine, full season Apr–Sep 2027.
  2. Southern-hemisphere virtual season starting now (e.g. a public SH potato locale). Rejected: the
     sensor site is the family's real locale — a SH season would decouple the virtual crop from the
     real station the venture is buying; kept as a named fallback ONLY if the user wants results
     before spring.
  3. Replay-live hybrid (replay 2026's weather as if live). Rejected: season one already proved replay;
     season two's point is reality's clock and reality's sensor.

## Goal Hierarchy

### Long-term (venture tier)
The governed brain survives contact with reality's clock: one real decision per real day, all season,
every recommendation gated, logged and scoreable — the evidence base for ever letting it actuate.

### Mid-term (3-12 months)
| # | Milestone | Success Criterion | Horizon |
|---|---|---|---|
| 1 | Loop machinery green | daily tick (ingest → govern → record) passes tests on simulated days incl. outage days | 1-2 months |
| 2 | Winter dry-run | ≥7 consecutive real days on the free spine; dry-run report written (gaps, latencies, decisions) | 2-4 months |
| 3 | Live season start | virtual planting on the real calendar (±station data if approved); arms running: governed-precision, governed-nominal, ERA5-baseline | Apr 2027 |
| 4 | Season complete | decision record covers the season within the recovery budget; handed to F19 | Sep-Oct 2027 |

### Short-term (≤1 month)
| # | Action | Class | Owner | Horizon |
|---|---|---|---|---|
| 1 | Design the live-day state store (what persists between real days; restart-safe) | write-plan | claude | days |
| 2 | Build the daily-tick runner over F17's spine (simulated-today test seam) | edit-local-code | claude | 2-3 weeks |
| 3 | Outage-day behavior per the F17 recovery budget (skip/flag/escalate — never fabricate weather) | edit-local-code | claude | 1 week |
| 4 | Protocol doc: planting rule, arms, cadence, dry-run plan, season calendar | write-plan | claude | 1 week |

## MVP Criteria
<!-- attempt-budget: 3 -->
- test-exit-0 python -m pytest tests/test_farm_shadow_loop.py -q
- file-exists docs/farm_shadow_season_protocol.md
- file-exists docs/farm_shadow_dryrun_report.md
<!-- project-state:end:mvp-criteria -->

(The MVP bar = machinery green + protocol authored + the ≥7-real-day dry-run REPORTED. The full live
season is milestone 3-4 — it takes the 2027 calendar and is F19's scoring subject, not this bar. The
dry-run report requires ≥7 real days to elapse, so this family's MVP is not single-session-reachable
by construction; that is honest, not a defect.)

## State Snapshot

### Assumptions
- Season-one components (twin, rules, certifier, kernel) need interface-level reuse only, no redesign — confidence: high (F16's runner already composes them)
- A real-time daily cadence fits the existing on-change proposal cadence — confidence: medium (restarts + missed days are the new cases)
- The virtual planting date can follow a PUBLIC agronomic rule for the locale's climate zone without leaking the locale — confidence: high (rule in-repo, parameters off-repo)

### Evidence
| # | Claim | Source | Confidence | Captured |
|---|---|---|---|---|
| 1 | Governed season loop works end-to-end on replayed history (0 ungated applications, deterministic) | tests/test_farm_governed_season.py (green 2026-10-27) | high | 2026-10-27 |
| 2 | Northern-hemisphere potato season ≈ Apr-Sep (ten Den trials: Apr planting, Sep-Oct harvest) | docs/farm_twin_world_spec.md (Table 5 dates) | high | 2026-10-27 |
<!-- project-state:end:evidence -->

### Unknowns
- ~~Restart-safety shape~~ RESOLVED 2026-10-27: recompute, no checkpoint — rules recompute severity from the cache each tick; the record file (`local/shadow_season/records.jsonl`, idempotent by date) is the only state; the live-season twin re-simulates from planting each tick (H1 watches the runtime)
- Dry-run window: which 7+ winter days (user-paced; any stretch works on the free spine — needs `local/farm_site.json` filled first, a one-minute user step)
- Whether the station lands before planting (money-gate timing) — determines which arms have real-sensor data from day 1

### Hypotheses (Active)
| ID | Statement | Status | Last-tested |
|---|---|---|---|
| H1 | Re-simulating the season from day 1 on each daily tick stays fast enough all season (~11s at day 125 in season one) | open | — |
| H2 | The governed loop's escalation rate on REAL sensor data is materially lower than the season-one reanalysis-precision rate | open | — |
<!-- project-state:end:hypotheses -->

### Decisions Made
| Decision | Date | Notes |
|---|---|---|
| Build-now / dry-run-winter / live-season-2027 (candidate 1) | 2026-10-27 | SH-season fallback named, not taken; replay-hybrid rejected (season one owns replay) |
| Outage days are flagged/escalated, never gap-filled with fabricated weather | 2026-10-27 | Honesty rail flow-down — the loop ESCALATES under missing data exactly as under ambiguity |
<!-- project-state:end:decisions-made -->

### Pending Decisions
| Decision | Proposer | Blocker | Notes |
|---|---|---|---|
| Dry-run start date | claude | F17 stage-1 spine green | User-paced; any ≥7-day winter stretch |
<!-- project-state:end:pending-decisions -->

## Bellman-Inspired Decision Frame

### Current state (one-line summary)
Seeded from the season-two decompose; all season-one components green; no live-loop code exists;
blocked on F17's free-source spine for anything live.

### Target state / terminal condition
Machinery green on simulated days, protocol authored, ≥7-real-day dry-run reported (MVP); then one
complete live season Apr-Sep 2027 whose decision record F19 can score.

### Progress proxy
MVP criteria met: 2 / 3 (measured 2026-10-27, run `2026-10-27-2339-advance-season-two-spine`: shadow-loop tests 6/6 green + protocol doc; the dry-run report is CALENDAR-GATED — ≥7 real days of live ticks, needs the off-repo site config filled first)

### Candidate next actions
| # | Action | Class | Expected progress | Expected info gain | Uncertainty | Cost |
|---|---|---|---|---|---|---|
| 1 | Live-day state-store design note (restart-safe; resolve the re-simulate-vs-checkpoint unknown) | write-plan | med | high | low | small |
| 2 | Daily-tick runner + simulated-today tests | edit-local-code | high | high | med | med |
| 3 | Outage-day behavior + tests | edit-local-code | med | med | low | small |
| 4 | Season protocol doc | write-plan | med | low | low | small |
<!-- project-state:end:candidate-actions -->

### Re-evaluation trigger
- **Default:** re-run `/project-state` after any action class fires
- **Manual override:** user invokes `/project-state farm-virtual-shadow-season` at any time

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
| 2 | 2026-10-27 | edit-local-code | Daily-tick runner built: aigov/farm_shadow_season.py — decide-yesterday cadence, F17 spine refresh, Estimate-based severity, nominal proposal gated through the REAL farm_fail_safe_gate, TickRecord append (idempotent by date), season_summary aggregates; tests/test_farm_shadow_loop.py 6/6 green via the refresh=False seam (clean-certify, straddle-escalate, degraded, absent-day-escalate, idempotency, pre-season refusal) | MVP criterion 1 MET; full suite 520, 0 regressions [done:state-store+runner+outage rows] |
| 3 | 2026-10-27 | write-plan | Season protocol frozen: docs/farm_shadow_season_protocol.md — cadence, outage behavior (inherits derived budget), dry-run definition, live-season arms (governed-precision / governed-nominal / ERA5-baseline), virtual-planting rule shape, restart-by-recomputation | MVP criterion 2 MET. Named fidelity question recorded: Wallin integer-°F band GAPS (53.6°F scores 0) — an F19 contract question against the primary sources, NOT silently changed here |
| 4 | 2026-10-27 | ask-user | Dry-run start is now a one-minute user step: fill local/farm_site.json (write_example() scaffolds it) — then `python -m aigov.farm_shadow_season <start-date>` daily (or scheduled) for ≥7 days → dry-run report → MVP criterion 3 | PARKED: user-paced (coordinates are the user's to supply; off-repo by privacy rail) |
<!-- project-state:end:action-log -->

## Open Questions for User
- None blocking now. The dry-run start date and the live-season commitment (Apr 2027) will be surfaced
  when F17's spine is green.

## Last Evaluation (v0.2 placeholder — not enforced in v0.1)
- **Date:** 2026-10-27
- **Progress signal:** (none yet — init only)
