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
<!-- attempt-budget: 3 -->
- test-exit-0 python -m pytest tests/test_farm_twin_smoke.py -q
- file-exists docs/farm_twin_world_spec.md
- test-exit-0 python -m pytest tests/test_farm_twin_validation.py -q
<!-- project-state:end:mvp-criteria -->

(Schema-normalized 2026-10-27 from the seed-time table — same three criteria, no redefinition: smoke
green / world spec exists / validation contract evaluated.)

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
- ~~PCSE × Python 3.14 compatibility~~ RESOLVED 2026-10-27: runs clean (smoke + 13 replayed seasons)
- ~~Which region-season~~ RESOLVED 2026-10-27: ten Den 2022 trial site-seasons (draft-then-ratify)
- ~~NASA POWER daily RH vs hourly~~ RESOLVED 2026-10-27: open-meteo ERA5 hourly RH cached for both sites (Smith Period needs hourly; spine carries it)

### Hypotheses (Active)
| ID | Statement | Status | Last-tested |
|---|---|---|---|
| H1 | PCSE potato runs day-steppable on this host unmodified | confirmed | 2026-10-27 |
| H2 | Sim end-of-season yield falls within the published regional range without local calibration | confirmed | 2026-10-27 |
| H3 | The wrapper can honor observability-enforced reads without forking PCSE internals | confirmed | 2026-10-27 |
<!-- project-state:end:hypotheses -->

### Decisions Made
| Decision | Date | Notes |
|---|---|---|
| World model = PCSE/WOFOST (external author), not in-repo authored agronomy and not DSSAT | 2026-10-27 | Independent-author rail (self-authored sim = self-authored kill test); DSSAT not steppable; verified surfaces in decompose doc §0 |
| Reference region-season = the ten Den et al. 2022 trial site-seasons (Lelystad + Vredepeel NL, 2019+2020) | 2026-10-27 | DRAFT-THEN-RATIFY (user invoked --until-mvp over the drafted fork; surfaced for redirect). Supersedes the "regional yield statistic" draft: field-measured near-potential yields for the EXACT shipped cultivars beat a management-limited regional average. Public criteria only |
| Validation contract frozen BEFORE first run: Layer-1 repro ±10% vs paper-sim, Layer-2 fidelity ±20% vs observed, 2020 gating / 2019 reported | 2026-10-27 | DRAFT-THEN-RATIFY (acceptance bar — user may amend; any band change is a logged contract amendment). docs/farm_twin_world_spec.md §5. Bands NOT widened after results (results landed inside) |
<!-- project-state:end:decisions-made -->

### Pending Decisions
| Decision | Proposer | Blocker | Notes |
|---|---|---|---|
| ~~Reference region-season~~ RESOLVED 2026-10-27 | claude | — | Resolved draft-then-ratify (see Decisions Made); user redirect re-opens it |
<!-- project-state:end:pending-decisions -->

## Bellman-Inspired Decision Frame

### Current state (one-line summary)
**MVP REACHED 2026-10-27** (run `2026-10-27-1100-until-mvp-farm-twin-world`): all 4 milestones MET —
smoke green; data spine cached offline (`data/farm_twin/weather/`, both sites, 2019+2020, daily +
hourly RH); FarmTwin wrapper enforcing the three disciplines (`aigov/farm_twin.py` + 6 tests); frozen
two-layer validation contract EVALUATED AND PASSED (6/6 gating 2020 combos: Layer-1 worst +7.6% of
band ±10%, Layer-2 worst −7.4% of band ±20%; 2019 reported). Repo suite 646 green, 0 regressions.
Gate A done pending user ratification of the two draft-then-ratify decisions (region-season, bands).

### Target state / terminal condition
All four mid-term milestones met: smoke green on this host, one season cached, wrapper honoring the
three disciplines with tests, validation contract evaluated with a recorded verdict.

### Progress proxy
- MVP criteria met: 3 / 3 (measured 2026-10-27, code-owned verdict mvp-reached)

### Candidate next actions
| # | Action | Class | Expected progress | Expected info gain | Uncertainty | Cost |
|---|---|---|---|---|---|---|
| 1 | None live — MVP met 2026-10-27; season-two scope is a NEW planning cycle (idea-anchor drafted, awaiting user confirmation) | stop | — | — | — | — |
<!-- project-state:end:candidate-actions -->

(Table closed 2026-10-27 after mvp-reached — the seed-time candidates were all completed and journaled in this ledger's action log; F14 has no live code candidates.)
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
| 5 | 2026-10-27 | research | Primary source fetched + extracted: ten Den et al. 2022 (EJA 137:126510) — THE paper PCSE's Wofost81 potato parameters come from. Verified by running: shipped Fontane carries calibrated TSUMEM=255 + REALLOC_* params; all 5 trial cultivars present | Reference region-season resolved on public criteria: Lelystad (52.52N,5.47E) + Vredepeel (51.54N,5.88E), 2019+2020 near-potential trials; per-cultivar observed ±sd AND paper-simulated yields (Tables 6+9). Named data defect: Vredepeel 2020 planting printed 24/09/2020 (impossible) → inferred 24/04/2020. [done:6b275b49] |
| 6 | 2026-10-27 | write-plan | docs/farm_twin_world_spec.md authored BEFORE first validation run: world composition, agromanagement derivation, data spine, disciplines, FROZEN two-layer contract (Layer-1 repro ±10% vs paper sim; Layer-2 fidelity ±20% vs observed; 2020 gating, 2019 reported) | MVP criterion 2 MET. Forecast f9 HIT. [done:ce3d0f63] |
| 7 | 2026-10-27 | run-tests | Data spine built: aigov/farm_weather.py exports NASA POWER daily (PCSE CSV) + open-meteo ERA5 hourly RH to data/farm_twin/weather/ (4 files, both sites, 2019+2020); offline load verified with unit round-trip | Milestone 2 MET: re-runs are offline; missing cache raises, never silently re-downloads |
| 8 | 2026-10-27 | edit-local-code | aigov/farm_twin.py: FarmTwin wrapper — SERVED observability map, read() refuses undeclared, per-tick tripwires (DVS/TWSO monotone, LAI bounds, max daily gain) that HALT, harvest-day termination contract, check_coverage. Pinned by tests/test_farm_twin_disciplines.py (6 tests) | Milestone 3 MET. One real defect found by running: harvest-day crop-object removal read as a DVS/TWSO collapse → final tick serves last pre-harvest state. [done:f55e6b17] |
| 9 | 2026-10-27 | run-tests | tests/test_farm_twin_validation.py: contract §5 verbatim — 6 gating 2020 combos (Layer 1 + Layer 2) + 2019 replayed-and-reported | ALL PASS: Layer-1 worst +7.6% (band 10%), Layer-2 worst −7.4% (band 20%). 2019 reported: replay within ±4.7% of paper-sim on all 6; vs observed drifts to +21.1% (mirrors the paper's own evaluation-year drift — non-gating classification vindicated). Milestone 4 + MVP criterion 3 MET. Forecast f10 HIT |
| 10 | 2026-10-27 | run-tests | Full repo regression + code-owned verdict (until_mvp_driver.compute_verdict) | 646 passed, 0 regressions (627 + 19 new). Verdict: mvp-reached (all 3 criteria live-MET). Auto-optimize: skip:no-ceiling-criterion |
<!-- project-state:end:action-log -->

## Open Questions for User
- None yet — region-season choice is drafted-then-ratified when proposed (public criteria only).

## Last Evaluation
- **Date:** 2026-10-27 (until-mvp run close)
- **Progress signal:** mvp-reached — 3/3 criteria live-MET (code-owned verdict); 4/4 milestones; H1–H3 confirmed; unknowns 3/3 resolved; 646-test suite green
