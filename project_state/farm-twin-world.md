# Farm-Season Twin — World Model (F14)

<!-- project-schema: 0.1 -->

> Initialized 2026-10-27 (Soraya self-init, run `2026-10-27-0900-decompose-plan-farm-season-twin`).
> Project ID: farm-twin-world. Originating goal (verbatim): "Build the ground-truth world for the
> farm-season twin: wrap PCSE/WOFOST potato as a day-steppable twin honoring coverage, observability
> and per-tick bounds, fed by a replayed real historical season and validated against published
> regional yields".

> **PRIVACY — STANDING.** Public repo. No family composition, amounts, holdings or specific locations.
> The reference region for the replayed season is a PUBLIC agronomic choice (a published potato
> region), not a statement about where anything will be bought.

## Project Context
- **Project ID:** farm-twin-world
- **Project root:** C:\Users\Farshad\PythonProjects\Skill_Development\AI_Governor
- **Captured:** 2026-10-27
- **Originating goal:** (verbatim above)
- **Refined goal (3c top candidate):** A day-steppable potato world (PCSE/WOFOST81) wrapped in the twin
  disciplines (coverage, observability-enforced reads, per-tick bounds), driven by one cached real
  historical season (NASA POWER daily + hourly-RH source), whose end-of-season outputs fall inside a
  WRITTEN validation contract against published regional yields — with the contract authored BEFORE the
  first validation run.
- **Horizon (months):** 2
- **Relationship to portfolio:** Gate A of the farm-season-twin venture (see
  `docs/farm-season-twin-decompose-2026-10-27.md`). Sibling of F13 (the venture is STANDALONE — it must
  not distort F13's jurisdiction ranking). The Mars twin (`aigov/twin.py`) is the discipline template;
  its kPa/m³ content does not transfer.

## Empirical Concerns
- **Verdict:** FLAG
- **Check status:** verified-this-run (web, 2026-10-27)
- **Findings:** PCSE confirmed day-steppable (`run()` = one day; `get_variable()` mid-run), EUPL 1.2,
  potato varieties 701–704, built-in NASA POWER provider. FLAG remains on TWO points: (1) PCSE targets
  Python 3.9/3.10 and this host runs 3.14 — unverified until the smoke test passes; (2) WOFOST simulates
  GROWTH only, not late blight — the world is a COMPOSITION (growth model + weather-driven risk + damage
  coupling) and the composition's fidelity is this family's real risk, not PCSE's.

## Project vs Research-Program
- **Verdict:** PASS (bounded project)
- **Rationale:** Every component has a checkable completion state: smoke passes, provider caches a
  season, wrapper honors the three disciplines, validation contract evaluated. No unbounded operating
  state in this family (that lives in F16's explicitly-named non-goal).

## Goal Hierarchy

### Long-term (venture tier)
The venture's ground truth: a world an independent author wrote, replaying a season that really
happened, that the governed loop can be falsified against.

### Mid-term (≤2 months)
| # | Milestone | Success Criterion |
|---|---|---|
| 1 | Steppability proven on this host | smoke test: potato season advances day-by-day on Python 3.14, LAI/TWSO readable mid-run |
| 2 | Data spine owned | one region-season cached locally (daily met + hourly RH); re-run uses cache, no network |
| 3 | Twin disciplines honored | wrapper enforces coverage / observability / per-tick bounds with tests |
| 4 | Validation contract evaluated | written contract (authored first) compares sim yield against published regional range; verdict recorded either way |

### Short-term (≤1 month)
| # | Action | Class | Owner |
|---|---|---|---|
| 1 | `pip install pcse` + day-step smoke on 3.14 | run-tests | claude |
| 2 | Pick the reference region-season (public agronomic criteria) + cache its weather | research | claude |
| 3 | Write the validation contract BEFORE the first validation run (resource_sim_spec pattern) | write-plan | claude |
| 4 | Wrap as FarmTwin honoring the three ColonyTwin disciplines | edit-local-code | claude |

## MVP Criteria
| Criterion | Kind | Predicate |
|---|---|---|
| Day-step smoke green | test-exit-0 | `python -m pytest tests/test_farm_twin_smoke.py -q` |
| World spec exists | file-exists | `docs/farm_twin_world_spec.md` |
| Validation contract evaluated | test-exit-0 | `python -m pytest tests/test_farm_twin_validation.py -q` |

## State Snapshot

### Assumptions
- PCSE runs on Python 3.14 despite 3.9/3.10 target — confidence: **medium** (smoke decides)
- One region-season of NASA POWER + hourly RH suffices for Gate B's rules — confidence: **high**
- Published regional yield ranges exist for the chosen region — confidence: **high**

### Evidence
| # | Claim | Source | Confidence | Captured |
|---|---|---|---|---|
| 1 | PCSE advances one day per `run()`; state readable mid-run via `get_variable` | pcse.readthedocs.io user guide | high | 2026-10-27 |
| 2 | Potato_701–704 available via YAMLCropDataProvider (wofost81 branch) | github.com/ajwdewit/WOFOST_crop_parameters | high | 2026-10-27 |
| 3 | DSSAT py-dssattools is batch-oriented, no steppable surface | py-dssattools docs | medium | 2026-10-27 |
| 4 | NASA POWER agroclimatology: free, daily, global | power.larc.nasa.gov | high | 2026-10-27 |
<!-- project-state:end:evidence -->

### Unknowns
- PCSE × Python 3.14 compatibility (smoke decides; fallback = pinned venv on 3.10)
- Which region-season (candidate criteria: published yield statistics + blight-relevant climate + good POWER coverage)
- Whether NASA POWER daily RH suffices for Smith Period's HOURLY ≥11h RH≥90% clause, or open-meteo hourly is required

### Hypotheses (Active)
| ID | Statement | Status | Last-tested |
|---|---|---|---|
| H1 | PCSE potato runs day-steppable on this host unmodified | confirmed | 2026-10-27 |
| H2 | Sim end-of-season yield falls within the published regional range without local calibration | open | never |
| H3 | The wrapper can honor observability-enforced reads without forking PCSE internals | open | never |
<!-- project-state:end:hypotheses -->

### Decisions Made
| Decision | Date | Notes |
|---|---|---|
| World model = PCSE/WOFOST (external author), not in-repo authored agronomy and not DSSAT | 2026-10-27 | Independent-author rail (self-authored sim = self-authored kill test); DSSAT not steppable; verified surfaces in decompose doc §0 |
<!-- project-state:end:decisions-made -->

### Pending Decisions
| Decision | Proposer | Blocker | Notes |
|---|---|---|---|
| Reference region-season | claude | short-term action 2 | drafted: a published NW-European or Andean potato region with EuroBlight-adjacent data; chosen on PUBLIC criteria only |
<!-- project-state:end:pending-decisions -->

## Bellman-Inspired Decision Frame

### Current state (one-line summary)
Milestone 1 MET (2026-10-27, same-day as seed): PCSE 6.0.13 installed on Python 3.14, full potato
season (Fontane, Wageningen 2006, NASA POWER) ran as 173 individual daily ticks with mid-run state
reads, pinned by `tests/test_farm_twin_smoke.py` (4 tests; repo suite 627 green, 0 regressions).
Next: region-season choice (pending decision 1) + validation contract WRITTEN BEFORE first validation run.

### Target state / terminal condition
All four mid-term milestones met: smoke green on this host, one season cached, wrapper honoring the
three disciplines with tests, validation contract evaluated with a recorded verdict.

### Progress proxy
- unknowns-retired + gates-passed (raw counts)

### Candidate next actions
| # | Action | Class | Expected progress | Expected info gain | Uncertainty | Cost |
|---|---|---|---|---|---|---|
| 1 | pip install pcse + day-step smoke (3.14) | run-tests | high | highest | low | minutes |
| 2 | Pick region-season + cache weather | research | high | high | low | 1-2 hrs |
| 3 | Write validation contract (before first run) | write-plan | medium | medium | low | 1 hr |
| 4 | FarmTwin wrapper + discipline tests | edit-local-code | high | medium | medium | 1-2 days |
<!-- project-state:end:candidate-actions -->

### Re-evaluation trigger
- after any action class fires; immediately if the smoke FAILS on 3.14 (fallback decision needed: pinned venv vs version work)

## Allowed Action Classes (v0.2 placeholder)
- `propose` / `research` / `write-plan` / `run-tests` / `ask-user` / `stop` — auto
- `edit-local-code` — auto in-cwd (Soraya gate table governs)

## Action Log
| # | Date | Action class | Description | Outcome |
|---|---|---|---|---|
| 1 | 2026-10-27 | propose | /project-init protocol executed by hand (Soraya self-init, decompose mode) | ledger created |
| 2 | 2026-10-27 | run-tests | pip install pcse (6.0.13) on Python 3.14; rollback note: pip uninstall pcse -y | Installed clean despite 3.9/3.10 target; forecast f1 HIT. Gotchas found by running: YAMLCropDataProvider must take model=Wofost81_PP (default branch lacks REALLOC_DVS); site provider requires NAVAILI |
| 3 | 2026-10-27 | run-tests | Day-step smoke: full Fontane season, Wageningen 2006, NASA POWER weather, 173 × run(days=1) with mid-run DVS/LAI/TWSO reads | TWSO 22,315 kg/ha dry (PP-mode ceiling, model-coherent only), LAImax 4.78, clean harvest-date termination; forecast f2 HIT. PCSE 6 also ships OpenMeteoWeatherDataProvider — hourly-RH fallback for Smith Period in-package |
| 4 | 2026-10-27 | edit-local-code | Pinned as tests/test_farm_twin_smoke.py (4 tests: >100 daily ticks, mid-run readability, biological monotonicity, shape bounds); H1 → confirmed (mirror: hypothesis row updated by hand, --update-hypothesis semantics) | 4 passed in 2.4s offline-cached; FULL repo suite 627 passed, 0 regressions. MVP criterion 1 of 3 MET |
<!-- project-state:end:action-log -->

## Open Questions for User
- None yet — region-season choice is drafted-then-ratified when proposed (public criteria only).

## Last Evaluation
- **Date:** 2026-10-27
- **Progress signal:** (init only)
