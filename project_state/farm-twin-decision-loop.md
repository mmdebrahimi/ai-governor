# Farm-Season Twin — Governed Decision Loop (F15)

<!-- project-schema: 0.1 -->

> Initialized 2026-10-27 (Soraya self-init, run `2026-10-27-0900-decompose-plan-farm-season-twin`).
> Project ID: farm-twin-decision-loop. Originating goal (verbatim): "Build the governed decision loop
> for the farm-season twin: an Estimate-wrapped observation layer, one instrument (late-blight
> treat/don't-treat) with externally-provenanced thresholds (Blitecast/Smith), a real anti-steering
> certifier, and an externally-provenanced status quo".

> **PRIVACY — STANDING.** Public repo. Concept-level only.

## Project Context
- **Project ID:** farm-twin-decision-loop
- **Project root:** C:\Users\Farshad\PythonProjects\Skill_Development\AI_Governor
- **Captured:** 2026-10-27
- **Originating goal:** (verbatim above)
- **Refined goal (3c top candidate):** ONE instrument — `blight_treatment_trigger` — carried end to end:
  risk rules (Blitecast severity values, threshold 18; Smith Period) implemented with unit tests pinned
  to PUBLISHED example values; an observation layer that returns Estimates (method + error bar), never
  truth-reads; a real anti-steering certifier registered in `CERTIFIABLE_INSTRUMENTS` for this
  instrument; and a status quo whose provenance is the replayed season's conventional practice — zero
  invented numbers anywhere in the chain (I11 end to end).
- **Horizon (months):** 3
- **Relationship to portfolio:** Gate B. Depends on F14 (input shapes). The kernel's refusal boundary
  (`NOT_CERTIFIABLE` → refuse) is the forcing function: without this family the governed loop executes
  NOTHING, by design.

## Empirical Concerns
- **Verdict:** FLAG
- **Check status:** verified-this-run (web, 2026-10-27)
- **Findings:** Published rules verified: Blitecast severity-value threshold 18 (Wisconsin-derived; OSU
  Malheur 1998/2001; Brazilian validations incl. Ciência Rural 2024 — fewer sprays, yield preserved) and
  UK Smith Period (2 consecutive days min temp ≥10°C + ≥11h RH ≥90%; EuroBlight 2013, criteria under
  revision for newer pathogen populations). FLAG on three points: (1) the original Smith rule text and a
  current official threshold table were NOT retrieved — primary-source fetch required before any rule is
  marked ratified-provenance (standing rule: primary source before load-bearing); (2) hourly RH is
  required by Smith and NASA POWER is daily — hourly source (open-meteo historical) must be confirmed;
  (3) the DAMAGE COUPLING (untreated risk → yield loss) has no verified published function yet — if none
  survives scrutiny, F16's bar reframes to compliance-denominated (named in the decompose doc §0).

## Project vs Research-Program
- **Verdict:** PASS (bounded)
- **Rationale:** rule module + tests, observation layer, one certifier, one status-quo derivation —
  each checkable. The "govern the whole farm" ambition is explicitly NOT this family.

## Goal Hierarchy

### Mid-term (≤3 months)
| # | Milestone | Success Criterion |
|---|---|---|
| 1 | Risk rules pinned to published values | Smith + Blitecast unit tests reproduce published example classifications |
| 2 | Observation layer | all decision inputs flow through Estimate-wrapped reads; truth-reads refused in tests |
| 3 | Certifier real | `blight_treatment_trigger` ∈ CERTIFIABLE_INSTRUMENTS with its own fail-safe gate; adversarial tests show refusal on steering |
| 4 | Status quo provenanced | fallback = replayed season's conventional practice, cited; InvalidStatusQuoError otherwise |

### Short-term (≤1 month)
| # | Action | Class | Owner |
|---|---|---|---|
| 1 | Fetch PRIMARY sources: original Smith (1956) criteria + Blitecast (Krause et al. 1975) rule text | research | claude |
| 2 | Implement rules module + published-value unit tests | edit-local-code | claude |
| 3 | Confirm hourly-RH source for the chosen region-season | research | claude |
| 4 | Damage-coupling literature check (published yield-loss function or reframe) | research | claude |

## MVP Criteria
<!-- attempt-budget: 3 -->
- test-exit-0 python -m pytest tests/test_blight_rules.py -q
- test-exit-0 python -m pytest tests/test_farm_instrument_certifier.py -q
- file-exists docs/blight_rules_provenance.md
<!-- project-state:end:mvp-criteria -->

(Schema-normalized 2026-10-27 from the seed-time table — same three criteria, no redefinition: rules
pinned to published values / certifier + observation adversarial tests green / provenance record.)

## State Snapshot

### Assumptions
- Blitecast/Smith primary texts are retrievable and unambiguous enough to implement — confidence: **high**
- A certifier for a binary treat/don't-treat instrument is simpler than the crop-fraction one — confidence: **medium**
- A published yield-loss coupling exists for potato late blight — confidence: **medium** (action 4 decides)

### Evidence
| # | Claim | Source | Confidence | Captured |
|---|---|---|---|---|
| 1 | Blitecast threshold 18 severity values triggers warning/spray recommendation | OSU Malheur 1998-22, 2001-27 | medium (secondary) | 2026-10-27 |
| 2 | Smith Period: 2 consecutive days ≥10°C min + ≥11h RH≥90%, near-miss allowance; under revision | EuroBlight 2013 (Skelsey) | medium (secondary) | 2026-10-27 |
| 3 | Blitecast reduced sprays 25–70% vs weekly calendar with yield preserved (Brazil) | Ciência Rural 2024 + earlier validation | medium | 2026-10-27 |
| 4 | Smith Period full definition: "Two consecutive days where the minimum temperature does not fall below 10°C and there are at least 11 hours in each day where the relative humidity is ≥90%" — defined 1956 by L.P. Smith refining the Beaumont Criteria | Dancey (Hutton/Cooke+Skelsey+Birch-supervised) Smith Period Review, GB 2003–2014 evaluation, eapr.net/sites/default/files/event-document/DANCEY Siobhan.pdf | high (authoritative review; original Smith 1956 Plant Pathology 5 paywalled) | 2026-10-27 |
| 5 | Blitecast primary citation: Krause, Massie & Hyre 1975, "BLITECAST: a computerized forecast of potato late blight", Plant Disease Reporter 59:95–98; combines Wallin 1962 severity values + Hyre 1954 favorable days; accumulation threshold 18 → first spray | OSU Malheur 1998-22 (operational text extracted) + Litschmann et al. 2020 JPPR 60(2) | medium-high (operational statements; Wallin 1962 severity TABLE still to fetch) | 2026-10-27 |
| 6 | Blitecast severity accumulation STARTS at 50% crop emergence (negative prognosis: 70%) — operational detail the rules module needs | Litschmann et al. 2020 JPPR 60(2):440 | medium | 2026-10-27 |
| 7 | Hourly RH for both reference sites CACHED: open-meteo ERA5, data/farm_twin/weather/{lelystad,vredepeel}_hourly_rh.csv, 2019+2020, UTC | built by aigov/farm_weather.py (F14 run 2026-10-27-1100) | high (in-repo) | 2026-10-27 |
| 8 | Potato late-blight yield loss is FULLY explained by reduced light interception (green-LAI reduction via lesion coverage; accelerated senescence ≤15% of loss) — a published, LAI-shaped damage coupling | van Oijen, WUR thesis 1991 ('Identification of the major characteristics of potato cultivars which affect yield loss caused by late blight', advisor Rabbinge) + model papers 1991a/b, 1992 (Springer BF01998073) | medium-high (abstract-level; implementation run must fetch the function's exact form) | 2026-10-27 |
| 9 | MEASURED finding (not published): with ±3% RH error propagated through the 90% threshold, the Lelystad-2020 season-end severity estimate is 18 with interval (−4, 40) — the Blitecast trigger is measurement-limited near its own threshold on reanalysis-grade RH | this repo, docs/blight_rules_provenance.md §measured-finding | high (in-repo, reproducible) | 2026-10-27 |
| 10 | On the replayed Lelystad-2020 season the two rules DISAGREE by two months: Blitecast first spray 2020-09-09 (nominal); first FULL Smith Period 2020-07-08 (+5 near-misses) | this repo, replay observation | high (in-repo, reproducible) | 2026-10-27 |
<!-- project-state:end:evidence -->

### Unknowns
- ~~Primary rule texts~~ RESOLVED 2026-10-27 to the extent paywalls allow: Wallin TABLE retrieved from two concurring published extension sources (1°F band-edge variant named); Smith + Blitecast pinned earlier (evidence 4–6). Residual: the paywalled 1962/1975 primaries themselves — fetch-if-ever-accessible
- ~~Hourly RH availability~~ RESOLVED 2026-10-27: open-meteo ERA5 hourly RH cached for both reference sites (evidence 7)
- ~~Damage coupling~~ RESOLVED 2026-10-27: published LAI-shaped mechanism exists (van Oijen 1991/1992, evidence 8) — exact functional form to be fetched by F16's implementation run

### Hypotheses (Active)
| ID | Statement | Status | Last-tested |
|---|---|---|---|
| H1 | Published example weather sequences reproduce published Smith/Blitecast classifications in our implementation | confirmed | 2026-10-27 |
| H2 | The binary instrument admits a menu-based anti-steering certifier in the fail_safe_gate pattern | confirmed | 2026-10-27 |
| H3 | A published potato late-blight yield-loss function exists with usable inputs | confirmed | 2026-10-27 |
<!-- project-state:end:hypotheses -->

### Decisions Made
| Decision | Date | Notes |
|---|---|---|
| ONE instrument deep (treat/don't-treat), not several shallow | 2026-10-27 | Probe issue 2.1: the kernel's NOT_CERTIFIABLE refusal makes uncertified instruments inert; certifier authorship is the core work |
<!-- project-state:end:decisions-made -->

### Pending Decisions
| Decision | Proposer | Blocker | Notes |
|---|---|---|---|
| Blitecast vs Smith as the RATIFIED season-one rule (or both, ensembled) | claude | USER ratification | Both now implemented; on the replayed Lelystad-2020 season they DISAGREE by two months (evidence 10). DRAFTED: ratify **Blitecast** as the season-one instrument rule (published threshold + validation trail + the certifier already keys on it), keep Smith as a reported diagnostic; UK's own criteria are under revision (Hutton), which weakens Smith as the primary |
<!-- project-state:end:pending-decisions -->

## Bellman-Inspired Decision Frame

### Current state (one-line summary)
**MVP REACHED 2026-10-27** (run `2026-10-27-1300-until-mvp-farm-twin-decision-loop`): rules module
pinned to published values (17 tests incl. UMaine worked examples + every table bucket boundary);
Estimate-wrapped observation layer with a DERIVED ±3%-RH interval; recompute-the-rule certifier
registered in the kernel (CERTIFIABLE_INSTRUMENTS now 2; STEERING/ESCALATE demonstrated end-to-end on
real replayed data); provenance record authored. Suite 679 green, 0 regressions. Milestone 4 (status
quo provenanced) remains open — not in the MVP bar; F16's integration binds it.

### Target state / terminal condition
All four milestones met; every number in the chain traceable to a published source or the replayed
season; the kernel certifies exactly one new instrument.

### Progress proxy
- MVP criteria met: 3 / 3 (measured 2026-10-27, code-owned verdict mvp-reached)

### Candidate next actions
| # | Action | Class | Expected progress | Expected info gain | Uncertainty | Cost |
|---|---|---|---|---|---|---|
| 1 | Fetch primary rule texts | research | medium | high | low | 1-2 hrs |
| 2 | Rules module + published-value tests | edit-local-code | high | high | low | 1 day |
| 3 | Hourly-RH source confirmation | research | low | medium | low | 30 min |
| 4 | Damage-coupling literature check | research | medium | high | medium | 2-3 hrs |
<!-- project-state:end:candidate-actions -->

### Re-evaluation trigger
- after any action; immediately if the damage-coupling check fails (bar reframe is an AUTHORITY decision — surface to user)

## Allowed Action Classes (v0.2 placeholder)
- `propose` / `research` / `write-plan` / `run-tests` / `ask-user` / `stop` — auto
- `edit-local-code` — auto in-cwd

## Action Log
| # | Date | Action class | Description | Outcome |
|---|---|---|---|---|
| 1 | 2026-10-27 | propose | /project-init protocol executed by hand (Soraya self-init, decompose mode) | ledger created |
| 2 | 2026-10-27 | research | Spillover from F14 until-mvp run: primary-source fetch for the spray rules (candidate action 1, partial) + hourly-RH confirmation (candidate action 3, complete) | Smith Period definition pinned from the Hutton-supervised GB 2003–2014 review; Blitecast citation + threshold-18 + 50%-emergence accumulation start pinned; hourly RH cached in-repo for both reference sites. REMAINING for action 1: the Wallin 1962 severity TABLE (evidence rows 4–7) [done:d6a2b468] |
| 3 | 2026-10-27 | research | Wallin severity TABLE retrieved from TWO independent published sources (WSU TB65E / IPM WISDOM 1995; UMaine Bulletin 2418) — hour thresholds agree cell-for-cell; 1°F band-edge variant named; UMaine supplies published worked examples (18h → SV 3/2/1/0/0 at 65/56/50/40/85°F) | Primary-source action closed to the extent the paywalled primaries allow (two concurring extension publications; fetch-if-ever-accessible noted in provenance doc) [done:01b523f7] |
| 4 | 2026-10-27 | edit-local-code | aigov/blight_rules.py: Wallin table (°F, WSU edges), daily SV, Blitecast accumulation from 50% emergence + threshold 18, Smith Period + near-miss. tests/test_blight_rules.py (17 tests) pins published examples + every bucket boundary + real-cache structural run | All green. MVP criterion 1 MET. Forecast f11 HIT [done:4ca940cc] |
| 5 | 2026-10-27 | edit-local-code | aigov/farm_observation.py (Estimate-wrapped reads; interval = recount at RH≥87/93 per published ±3% RH sensor error; truth-reads refused) + aigov/farm_certifier.py (recompute-the-rule gate: CERTIFY / STEERING_DETECTED / ESCALATE-on-straddle / ESCALATE-on-no-observation) + kernel registration (CERTIFIABLE_INSTRUMENTS now 2; certify() routes per-instrument; phase1 pin updated as declared work). tests/test_farm_instrument_certifier.py (16 tests) | All green; full repo suite **679 passed, 0 regressions**. MVP criteria 2+3 MET (provenance doc docs/blight_rules_provenance.md). Forecast f12 HIT. Named gap: kernel._constraints_hold still probes the COLONY twin for farm actions — F16 integration surface |
| 6 | 2026-10-27 | research | Damage-coupling literature check (candidate 4): van Oijen (WUR thesis 1991 + model papers 1991/1992, Springer BF01998073) — potato late-blight yield loss FULLY explained by reduced green leaf area (lesion coverage; accelerated senescence ≤15%) | PUBLISHED MECHANISM EXISTS and is LAI-shaped — implementable against WOFOST's own LAI. F16's bar can stay yield-denominated (drafted position; reframe decision NOT needed). Evidence row 8 [done:04960b16] |
| 7 | 2026-10-27 | run-tests | One-governed-tick integration spike (F16 candidate 1, run inline): real Lelystad mid-July accumulation 9 (interval 3–15) + steered 'treat' proposal → STEERING_DETECTED → kernel REFUSED to apply; tight above-threshold observation + conforming proposal → CERTIFY → applied | Full propose→certify→apply chain works end-to-end on real replayed data; spike recorded in F16 ledger (not yet pinned as a test — F16's own run pins it) |
<!-- project-state:end:action-log -->

## Open Questions for User
- None yet. The bar-reframe fork (yield-denominated vs compliance-denominated) surfaces only if action 4 comes back empty.

## Last Evaluation
- **Date:** 2026-10-27
- **Progress signal:** (init only)
