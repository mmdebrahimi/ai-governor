# Farm Season Two — Live Sensor-Data Spine (F17)

<!-- project-schema: 0.1 -->

> Initialized 2026-10-27 (Soraya self-init, season-two decompose per the ratified anchor
> `docs/idea-anchor-prompt-farm-season-two-2026-10-27.md`). Project ID: farm-live-sensor-spine.
> Originating goal (verbatim): "Build season two's live sensor-data spine: select and (after
> money-gate approval) procure one weather/canopy sensor station measuring the Blitecast/Smith inputs
> (hourly RH + temperature) at a reachable sensor site; ingest its live data plus real local
> forecast/reanalysis weather into the season-one cache format so the validated twin and rules consume
> it unchanged; prove the ingestion path end-to-end on a free live source BEFORE any purchase; handle
> gaps and outages within a recovery budget".

> **PRIVACY — STANDING.** Public repo. No family composition, amounts, holdings or specific locations.
> The sensor site is a SHAPE ("a reachable sensor site"), never a location; its coordinates/locale
> NEVER enter this repo — the ingestion code takes site parameters from an OFF-REPO local config
> (gitignored), exactly as the capital-cap number stays off-repo. The season-two capital cap exists;
> only its CATEGORY list (sensors, consumables) is recorded here.

## Project Context
- **Project ID:** farm-live-sensor-spine
- **Project root:** C:\Users\Farshad\PythonProjects\Skill_Development\AI_Governor
- **Captured:** 2026-10-27
- **Originating goal:** (verbatim above)
- **Refined goal (3c top candidate):** A live data spine with TWO stages — stage 1 ($0): daily
  ingestion of a FREE live source (open-meteo forecast + current conditions for the off-repo sensor
  locale) into the season-one cache format (`aigov/farm_weather.py` CSV contract), proven by tests the
  twin + rules pass unchanged; stage 2 (money-gated): a sensor station chosen by a written spec+price
  doc, its live feed replacing/augmenting the free source through the SAME contract, with outage
  handling inside a declared recovery budget.
- **Horizon (months):** 4
- **Relationship to portfolio:** Gate A of season two (see `docs/farm-season-two-decompose-2026-10-27.md`).
  Successor of F14's data spine (same cache contract); feeds F18. Owns season two's ONLY money action
  (the station), which hard-pauses at the money gate with spec+price.

## Empirical Concerns
- **Verdict:** PASS
- **Check status:** attempted
- **Provisional:** NO
- **Findings:** Goal's factual premises checked: (1) Blitecast/Smith inputs = hourly RH + temperature —
  pinned in-repo against primary sources this same day (`docs/blight_rules_provenance.md`; Wallin
  humid-hours table, Smith 10°C/90%RH/11h). (2) Hobby-grade stations measuring RH/temp with optional
  leaf-wetness and cloud logging EXIST (web, 2026-10-27: Davis Vantage line + leaf-wetness sensor;
  Ecowitt WN35 + gateway). (3) Programmatic export (WeatherLink v2 API / Ecowitt local gateway HTTP)
  was NOT confirmed per-model by the search — the spec doc MUST verify the API surface of each
  candidate BEFORE it reaches the money gate. Non-load-bearing for the MVP bar (stage 1 is free-source).

## Project vs Research-Program
- **Verdict:** PASS
- **Provisional:** NO
- **Classification:** project
- **Rationale:** Bounded: free-source spine proven by tests, spec doc written, outage handling tested —
  each checkable; horizon 4 months. The unbounded "operate forever" state lives in F18/F19's season
  scope, not here.

## Refinement Candidates
- **Verdict:** PASS
- **Provisional:** NO
- **Refined-from:** originating-goal
- **Candidates:**
  1. (TOP — adopted as refined goal) Two-stage spine: free-source first at $0, sensor station second
     behind the money gate, both through the unchanged season-one cache contract.
  2. Sensor-first spine: spec+buy immediately, free source only as fallback. Rejected: spends before
     the ingestion path exists; violates the anchor's measured-delta rationale.
  3. Forecast-only season (no sensor at all). Rejected: cannot answer season two's binding question
     (what real sensor precision buys over reanalysis); kept as the fallback if the money gate declines.

## Goal Hierarchy

### Long-term (venture tier)
Reality's weather enters the venture through one honest, contract-stable pipe — cheap first, certified
later — so every downstream decision is scoreable against what was actually measured.

### Mid-term (3-12 months)
| # | Milestone | Success Criterion | Horizon |
|---|---|---|---|
| 1 | Free-source live spine proven | daily open-meteo pull for the off-repo locale lands in the F14 CSV contract; twin + rules consume it unchanged (tests green) | 1 month |
| 2 | Sensor spec+price at the money gate | `docs/farm_sensor_station_spec.md` written: candidates, verified API surface each, precision vs the ±3% RH finding, price — paused for user approval | 1-2 months |
| 3 | Station live (post-approval) | station data flows through the same contract; sensor-vs-free-source divergence logged daily | 2-4 months |
| 4 | Outage handling declared + tested | recovery budget written (max gap before a day is unscoreable); gap-fill/flagging tested | 2 months |

### Short-term (≤1 month)
| # | Action | Class | Owner | Horizon |
|---|---|---|---|---|
| 1 | Off-repo local site config seam (gitignored path + loader honoring the privacy rail) | edit-local-code | claude | days |
| 2 | Free-source live ingestion: open-meteo forecast+current → F14 CSV contract + tests | edit-local-code | claude | 1-2 weeks |
| 3 | Write the recovery-budget note (what gap makes a day unscoreable) BEFORE the loop runs | write-plan | claude | days |
| 4 | Sensor-station spec doc: candidates, per-model API verification, precision, price → money gate | research | claude | 2-4 weeks |

## MVP Criteria
<!-- attempt-budget: 3 -->
- test-exit-0 python -m pytest tests/test_farm_live_spine.py -q
- file-exists docs/farm_sensor_station_spec.md
- file-exists docs/farm_live_spine_recovery_budget.md
<!-- project-state:end:mvp-criteria -->

(The MVP bar is deliberately $0-provable: free-source spine green + spec doc at the money gate +
recovery budget declared. The station PURCHASE and its live feed are milestone 3 — money-gated, so
never an MVP criterion; the fallback if declined is candidate 3's forecast-only season.)

## State Snapshot

### Assumptions
- open-meteo serves forecast + recent actuals for the sensor locale at hourly RH/temp resolution — confidence: high (season one used its ERA5 archive for both NL sites)
- The F14 CSV contract carries live data without schema change (dates forward of today handled) — confidence: medium (forecast rows are a new case; tests decide)
- A hobby-grade station with verifiable API access exists inside the private cap — confidence: medium (hardware confirmed; API surface per-model unverified)

### Evidence
| # | Claim | Source | Confidence | Captured |
|---|---|---|---|---|
| 1 | Blitecast/Smith need hourly RH + temp; season-one rules consume exactly that | docs/blight_rules_provenance.md (primary-source pinned) | high | 2026-10-27 |
| 2 | Hobby stations with RH/temp + leaf-wetness + cloud logging exist (Davis Vantage + 6420; Ecowitt WN35 + gateway) | davisinstruments.com; shop.ecowitt.com (web 2026-10-27) | high | 2026-10-27 |
| 3 | ±3% RH sensor error turns the Blitecast trigger into an escalation season | season-one measured finding (docs/farm_season_report_v1.md) | high | 2026-10-27 |
| 4 | Programmatic hourly export per candidate model | NOT YET VERIFIED — spec-doc task | low | 2026-10-27 |
<!-- project-state:end:evidence -->

### Unknowns
- Which candidate station's API surface is actually usable (WeatherLink v2 / Ecowitt local HTTP / other)
- Forecast-vs-actual handling in the cache: does the spine re-write yesterday's forecast rows with actuals, and how is that journaled?
- The recovery budget's number (max unscoreable gap) — to be DERIVED from Blitecast's accumulation logic, not asserted

### Hypotheses (Active)
| ID | Statement | Status | Last-tested |
|---|---|---|---|
| H1 | The F14 cache contract carries live+forecast data unchanged (no schema fork) | open | — |
| H2 | A hobby-grade station materially narrows the season-one escalation interval vs reanalysis RH | open | — |
<!-- project-state:end:hypotheses -->

### Decisions Made
| Decision | Date | Notes |
|---|---|---|
| Two-stage spine: free source first ($0), station second (money-gated) | 2026-10-27 | From the ratified anchor (sensors-first + measured-delta rationale); candidate 1 adopted |
| Sensor site recorded as SHAPE only; coordinates live in an off-repo gitignored config | 2026-10-27 | Privacy rail flow-down — same off-repo pattern as the capital-cap number |
<!-- project-state:end:decisions-made -->

### Pending Decisions
| Decision | Proposer | Blocker | Notes |
|---|---|---|---|
| Station purchase (which model, at what price) | claude (spec doc) | MONEY GATE — user approval with concrete spec+price | Hard pause; fallback = forecast-only season (candidate 3) |
<!-- project-state:end:pending-decisions -->

## Bellman-Inspired Decision Frame

### Current state (one-line summary)
Seeded from the season-two decompose; season-one cache contract + rules exist and are green; no live
ingestion yet; no spec doc; no money spent.

### Target state / terminal condition
Free-source live spine green under tests, sensor spec+price parked at the money gate, recovery budget
declared — then (post-approval) station data flowing through the same contract with divergence logging.

### Progress proxy
MVP criteria met: 0 / 3 (seeded 2026-10-27)

### Candidate next actions
| # | Action | Class | Expected progress | Expected info gain | Uncertainty | Cost |
|---|---|---|---|---|---|---|
| 1 | Off-repo site-config seam (gitignored loader, privacy-rail tested) | edit-local-code | med | low | low | small |
| 2 | Free-source live ingestion + tests (open-meteo → F14 contract) | edit-local-code | high | high | med | med |
| 3 | Recovery-budget note DERIVED from Blitecast accumulation logic | write-plan | med | high | low | small |
| 4 | Sensor spec doc with per-model API verification → money gate | research | high | high | med | med |
<!-- project-state:end:candidate-actions -->

### Re-evaluation trigger
- **Default:** re-run `/project-state` after any action class fires
- **Manual override:** user invokes `/project-state farm-live-sensor-spine` at any time

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
| 1 | 2026-10-27 | propose | /project-init invoked (Soraya self-init, season-two decompose) | ledger created |
<!-- project-state:end:action-log -->

## Open Questions for User
- The sensor-station purchase itself (milestone 2 → money gate): approval waits on the spec+price doc —
  nothing to decide yet.
- Confirm the off-repo site-config pattern is acceptable (coordinates in a gitignored local file,
  SHAPE-only in repo). Default assumed yes (mirrors the cap-number pattern you ratified).

## Last Evaluation (v0.2 placeholder — not enforced in v0.1)
- **Date:** 2026-10-27
- **Progress signal:** (none yet — init only)
