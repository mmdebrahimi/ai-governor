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
| Criterion | Kind | Predicate |
|---|---|---|
| Rules pinned to published values | test-exit-0 | `python -m pytest tests/test_blight_rules.py -q` |
| Certifier + observation adversarial tests green | test-exit-0 | `python -m pytest tests/test_farm_instrument_certifier.py -q` |
| Provenance record exists | file-exists | `docs/blight_rules_provenance.md` |

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
<!-- project-state:end:evidence -->

### Unknowns
- Primary rule texts — PARTIALLY RESOLVED 2026-10-27: Smith definition pinned (evidence 4); Blitecast threshold-18 + 50%-emergence start pinned (evidence 5,6). STILL OPEN: the Wallin (1962) severity-value TABLE itself (temp range × RH≥90% hours → 0–4) — fetch before implementing the rules module
- ~~Hourly RH availability~~ RESOLVED 2026-10-27: open-meteo ERA5 hourly RH cached for both reference sites (evidence 7)
- Damage coupling: published function vs reframe-to-compliance

### Hypotheses (Active)
| ID | Statement | Status | Last-tested |
|---|---|---|---|
| H1 | Published example weather sequences reproduce published Smith/Blitecast classifications in our implementation | open | never |
| H2 | The binary instrument admits a menu-based anti-steering certifier in the fail_safe_gate pattern | open | never |
| H3 | A published potato late-blight yield-loss function exists with usable inputs | open | never |
<!-- project-state:end:hypotheses -->

### Decisions Made
| Decision | Date | Notes |
|---|---|---|
| ONE instrument deep (treat/don't-treat), not several shallow | 2026-10-27 | Probe issue 2.1: the kernel's NOT_CERTIFIABLE refusal makes uncertified instruments inert; certifier authorship is the core work |
<!-- project-state:end:decisions-made -->

### Pending Decisions
| Decision | Proposer | Blocker | Notes |
|---|---|---|---|
| Blitecast vs Smith as the RATIFIED season-one rule (or both, ensembled) | claude | milestone 1 evidence | drafted: implement BOTH, ratify ONE after seeing them disagree on the replayed season — disagreement is signal, not noise |
<!-- project-state:end:pending-decisions -->

## Bellman-Inspired Decision Frame

### Current state (one-line summary)
Seeded 2026-10-27. Rules identified with secondary-source evidence; nothing implemented; primary-source
fetch is the first action per the standing primary-source-before-load-bearing rule.

### Target state / terminal condition
All four milestones met; every number in the chain traceable to a published source or the replayed
season; the kernel certifies exactly one new instrument.

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
| 2 | 2026-10-27 | research | Spillover from F14 until-mvp run: primary-source fetch for the spray rules (candidate action 1, partial) + hourly-RH confirmation (candidate action 3, complete) | Smith Period definition pinned from the Hutton-supervised GB 2003–2014 review; Blitecast citation + threshold-18 + 50%-emergence accumulation start pinned; hourly RH cached in-repo for both reference sites. REMAINING for action 1: the Wallin 1962 severity TABLE (evidence rows 4–7) |
<!-- project-state:end:action-log -->

## Open Questions for User
- None yet. The bar-reframe fork (yield-denominated vs compliance-denominated) surfaces only if action 4 comes back empty.

## Last Evaluation
- **Date:** 2026-10-27
- **Progress signal:** (init only)
