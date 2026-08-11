# AI Government F4 — Colony Digital Twin (D14): the world departments act on
<!-- project-schema: 0.1 -->

> Initialized 2026-08-11. Project ID: aigov-twin. Originating goal (verbatim): "Build the colony digital twin that serves every StateVar the department contract declares, reproduces the vendored analog-calibrated ECLSS baselines within a stated tolerance, ENFORCES the observability field so a latent variable can never be read as a measurement, and is able to FAIL - so department decisions become falsifiable instead of merely expressible."
> Seeded by Soraya `--advance` (2026-08-11), `/project-init` protocol executed by hand. Parent umbrella: `aigov`. Self-init 7/25.

## Project Context
- **Project ID:** aigov-twin
- **Project root:** C:\Users\Farshad\PythonProjects\Skill_Development\AI_Governor
- **Captured:** 2026-08-11
- **Originating goal:** (see verbatim above)
- **Refined goal (if 3c produced one):** An `aigov/twin.py` in which (a) `check_state_coverage` makes an unserved or observability-mismatched StateVar a validation error, (b) `read()` REFUSES `LATENT` and `ESTIMATED` variables and `estimate()` returns a method + error bar, (c) `baseline_report()` COMPUTES the per-capita deltas against the vendored BVAD/NSS references rather than asserting them, and (d) the twin reproduces every failure mode D1 declares and refuses to serve state past a structural failure.
- **Role:** FAMILY ledger under umbrella `aigov`. Critical-path position: **Gate C — the last prerequisite before the kernel (F5).**
- **Horizon (months):** 3
- **Schema:** project-schema 0.1

## Empirical Concerns
- **Verdict:** PASS
- **Check status:** attempted
- **Provisional:** NO
- **Findings:** The twin's per-capita demand is not authored here — it is taken from the vendored `aigov/choice/models/resource_sim.py`, which carries its own analog-sourced constants (METABOLIC_RATE_W 136.7 W/person from NSS ECLSS analog data; RESPIRATORY_QUOTIENT 0.87; FOOD_ENERGY_DENSITY 4.57 kcal/g on the BVAD dry-food basis; WATER_INTAKE 3.6 kg/day) and its own NASA-BVAD-style validation references (O2_REF 0.835, CO2_REF 1.040, FOOD_DRY_REF 0.617 kg/person/day). Those constants are INHERITED, not verified by this project: they carry the vendored tree's provenance, which is a WORKING-TREE state (see `aigov-collective-choice`), and they have NOT been promoted to audit tier in `aigov-foundations`. Honest label: baselines are reproduced against the model's OWN references, which is an internal-consistency check, NOT external validation.

## Project vs Research-Program
- **Verdict:** PASS
- **Provisional:** NO
- **Classification:** project
- **Rationale:** Bounded (one module + one test file over a fixed set of reservoirs), mechanically measurable (coverage errors empty; baseline deltas within a stated tolerance; each declared failure mode reproduced), horizon 3 ≤ 12. The unbounded version — "simulate a Mars colony accurately" — is explicitly NOT this family's goal and would be unfalsifiable at this scope.

## Refinement Candidates
- **Verdict:** PASS
- **Provisional:** NO
- **Refined-from:** originating-goal
- **Candidates:** C1 (= refined goal, EXECUTED): a coarse reservoir twin bound to the contract. C2 (wrap V-HAB / HERITAGE): higher fidelity, but imports a heavy external dependency and its own calibration burden — DEFERRED until a department decision actually turns on sub-5% accuracy. C3 (stochastic twin with failure sampling): needed for the adversarial suite (F10), DEFERRED to that family.

## MVP Criteria
<!-- attempt-budget: 3 -->
- file-exists aigov/twin.py
- test-exit-0 python -m pytest tests/test_twin.py -q
- project-state-row project_state/aigov.md:F4-twin-baselines-reproduced
<!-- project-state:end:mvp-criteria -->

> **Bar status: PROPOSED (draft-then-ratify)** under the v1.12 execute-mode exception. Predicate targets the
> UMBRELLA per the self-satisfying-predicate rule.

## Goal Hierarchy
### Long-term (12+ months tier)
A world honest enough that a department's decision can be shown to be WRONG in it — including by the world refusing to report a state the colony could not physically occupy.

### Mid-term (3-12 months)
| # | Milestone | Success Criterion | Horizon |
|---|---|---|---|
| 1 | Contract coverage + observability enforcement | unserved var and observability mismatch are distinct errors; latent read refused | ≤1 mo |
| 2 | Baseline reproduction | computed deltas vs the model's own references within a stated tolerance | ≤1 mo |
| 3 | Failure modes reproduce | every failure mode D1 declares is producible; twin stops reporting past structural failure | ≤2 mo |
| 4 | Kernel binding (F5) | departments act on twin state through the kernel's cycle | ≤3 mo |

### Short-term (≤1 month)
| # | Action | Class | Owner | Horizon |
|---|---|---|---|---|
| 1 | Bind the twin into the kernel decision cycle (F5) | edit-local-code | claude | ≤4 wk |
| 2 | Add ISRU water makeup so the 31-cycle depletion is a POLICY choice, not a fixture | edit-local-code | claude | ≤3 wk |
| 3 | Promote the inherited ECLSS constants to audit tier in aigov-foundations | research | claude | ≤4 wk |
| 4 | Stochastic variant for the adversarial suite (C3) | edit-local-code | claude | ≤4 wk |

## State Snapshot
### Assumptions
- A coarse reservoir model is enough to falsify department decisions — confidence: medium (it is enough to falsify GROSS errors, not marginal ones)
- The vendored analog constants are sound — confidence: medium (inherited, not verified here)
- One habitat atmosphere reservoir is an adequate O2 model — confidence: LOW (no separate stored-O2 tank; see Unknowns)
### Evidence
| # | Claim | Source | Confidence | Captured |
|---|---|---|---|---|
| 1 | Per-capita deltas vs the model's own references: O2 1.01%, CO2 4.92%, food_dry 0.11% — all within a 5% tolerance | `ColonyTwin().baseline_report()`, computed | high | 2026-08-11 |
| 2 | Scale invariance holds to 1.3e-16 (machine precision) | `scale_invariance_error()` | high | 2026-08-11 |
| 3 | At 90% closure with no ISRU makeup the water reserve exhausts at cycle 31 | 60-cycle run, pinned by test | high | 2026-08-11 |
| 4 | Full photosynthetic closure trips the fire-hazard bound at cycle 1 and breaches the hull at cycle 4 | 6-cycle run, pinned by test | high | 2026-08-11 |
| 5 | Break-even crop fraction 1/1.5 holds partial pressure flat at 21.00 kPa over 12 cycles | 12-cycle run, pinned by test | high | 2026-08-11 |
<!-- project-state:end:evidence -->
### Unknowns
- Whether a single-atmosphere O2 reservoir (no separate stored-O2 tank) distorts department decisions
- Whether the inherited BVAD/NSS constants survive audit-tier verification
- What ISRU water makeup rate is achievable — currently zero, which is why depletion is inevitable
- Whether a 5% baseline tolerance is adequate for any decision a department will actually make
### Hypotheses (Active)
| ID | Statement | Status (open/under-investigation/falsified/confirmed) | Last-tested |
|---|---|---|---|
| H1 | The twin serves every StateVar the contract declares, at matching observability | confirmed | 2026-08-11 |
| H2 | Baselines reproduce within a 5% tolerance | confirmed | 2026-08-11 |
| H3 | Every failure mode D1 declares is producible by the twin | confirmed | 2026-08-11 |
| H4 | A coarse reservoir twin is sufficient to falsify real department decisions | open | - |
| H5 | The inherited ECLSS constants survive audit-tier verification | open | - |
<!-- project-state:end:hypotheses -->
### Decisions Made
| Decision | Date | Notes |
|---|---|---|
| DT1 — Observability is ENFORCED, not decorative | 2026-08-11 | `StateVar.observability` was a declared field nothing checked. `read()` now REFUSES a LATENT variable and refuses a bare read of an ESTIMATED one; `estimate()` returns the value WITH its method and error bar. The governor cannot read `willingness_to_pay` as though it were measured — the I11 discipline (no invented numbers) applied to STATE instead of objectives. |
| DT2 — An observability MISMATCH is a distinct, worse error than a missing variable | 2026-08-11 | A department that believes it MEASURES something the world only estimates is inventing precision. `[OBS]` and `[COV]` are separate error codes. |
| DT3 — Structural bounds added after a run inspection, not after a test failure | 2026-08-11 | Before them the twin reported an O2 partial pressure of **304 kPa at cycle 12** under full photosynthetic closure — three atmospheres of pure oxygen inside a hull rated for about one. The tests were all green. Reporting a state the colony cannot occupy is the twin telling a department a comfortable fiction. Added `O2_FIRE_HAZARD_KPA` (30.0, elevated-O2 flammability, Apollo-1 class) and `HABITAT_STRUCTURAL_LIMIT_KPA` (101.325, ~1 atm), both DECLARED physical constants — the legitimate I11 provenance class, still queued for audit-tier verification. |
| DT4 — Past a hull breach the twin REFUSES to serve state | 2026-08-11 | `HabitatFailedError` on both `tick()` and `read()`. A burst habitat has no state; continuing to emit numbers would be the world lying to the government. Same fail-closed discipline as `fail_safe_gate` and the intake's polarization escalation. |
| DT5 — Baselines are an INTERNAL-CONSISTENCY check, not external validation | 2026-08-11 | The references come from the vendored model itself. Say "reproduces the model's own analog references", never "validated against NASA data". Promoting the constants is aigov-foundations' job (H5). |
<!-- project-state:end:decisions-made -->
### Pending Decisions
| Decision | Proposer | Blocker | Notes |
|---|---|---|---|
| Add a separate stored-O2 reservoir, or keep the single-atmosphere model? | claude | H4 | single-atmosphere makes overproduction dramatic fast; a buffered tank is more realistic and less punishing |
| Is 5% the right baseline tolerance? | claude | H4 — depends on what decision turns on it | currently CO2 sits at 4.92%, close to the edge |
<!-- project-state:end:pending-decisions -->

## Bellman-Inspired Decision Frame
### Current state (one-line summary)
`aigov/twin.py` built and tested (34 tests): serves all 10 declared StateVars at matching observability, enforces LATENT/ESTIMATED refusal, reproduces the vendored per-capita references (worst 4.92% on CO2) within a 5% tolerance, holds pressure flat at break-even crop fraction over 12 cycles, and reproduces every failure mode D1 declares — water exhaustion at cycle 31, fire-hazard bound at cycle 1 under full closure, hull breach at cycle 4, thermal saturation on demand — then refuses to serve state.

### Target state / terminal condition
See ## MVP Criteria — module + suite + the umbrella record.

### Progress proxy
- **MVP bar:** 3 / 3 criteria met (see `## MVP Criteria`) — bar REACHED 2026-08-11
- **v0.1 metric:** `unknowns-retired` count + `gates-passed` count

### Candidate next actions
| # | Action | Class | Expected progress | Expected info gain | Uncertainty | Cost |
|---|---|---|---|---|---|---|
| 1 | Bind the twin into the kernel decision cycle (F5) | edit-local-code | high | high | medium | med |
| 2 | ISRU water makeup so depletion is a policy choice | edit-local-code | med | med | low | low |
| 3 | Promote the inherited ECLSS constants to audit tier | research | med | high | low | med |
| 4 | Stochastic variant for the adversarial suite | edit-local-code | med | high | high | med |
<!-- project-state:end:candidate-actions -->

### Re-evaluation trigger
- **Default:** re-run `/project-state` after any action class fires
- **Manual override:** `/project-state aigov-twin`

## Allowed Action Classes (v0.2 placeholder — not enforced in v0.1)
- `propose` · `research` · `write-plan` · `edit-local-code` (requires approval) · `run-tests` · `ask-user` · `stop`

## Action Log
| # | Date | Action class | Description | Outcome |
|---|---|---|---|---|
| 1 | 2026-08-11 | propose | /project-init protocol executed by hand (family seed) | ledger created; self-init 7/25 |
| 2 | 2026-08-11 | research | Read + EXECUTED the vendored resource_sim to get real numbers before wrapping it | per-capita O2 0.8266 / CO2 0.9888 / food 0.6177 / water 3.30 kg/day |
| 3 | 2026-08-11 | edit-local-code | Wrote aigov/twin.py: reservoirs, gas law, coverage check, observability enforcement, tick | coverage clean on D1+D2; latent read refused |
| 4 | 2026-08-11 | run-tests | Verify-in-batch: ran the failure modes rather than trusting the exit code | all 4 producible; BUT full closure reported 304 kPa at cycle 12 — unphysical |
| 5 | 2026-08-11 | edit-local-code | Added O2 fire-hazard + habitat structural bounds and HabitatFailedError | breach now at cycle 4; twin refuses to serve state afterwards; nominal run unaffected |
| 6 | 2026-08-11 | run-tests | Wrote tests/test_twin.py (34 tests) incl. a tighter-tolerance test that must FAIL | root suite 162 passed; vendored organ 193 unaffected |
<!-- project-state:end:action-log -->

## Open Questions for User
- MVP bar is PROPOSED under the execute-mode exception, not confirmed.
- **Honest scope limit:** the baselines are an internal-consistency check against the vendored model's own references. Calling this "validated against NASA data" would be an overclaim; it is not, and H5 tracks the real verification.

## Last Evaluation (v0.2 placeholder — not enforced in v0.1)
- **Date:** 2026-08-11
- **Progress signal:** bar reached 3/3; H1/H2/H3 confirmed; one unphysical-state defect found by run inspection and closed with fail-closed structural bounds
