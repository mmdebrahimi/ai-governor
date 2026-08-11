# AI Government F2 — Guideline Intake: closing the threshold gap at its source
<!-- project-schema: 0.1 -->

> Initialized 2026-08-11. Project ID: aigov-guideline-intake. Originating goal (verbatim): "Build the mechanism by which a population produces guidelines precise enough to BIND a machine - sortition panel plus quadratic priority budget plus level elicitation - such that a binding type-F or type-D guideline cannot be constructed at all unless the panel supplied the level or metric, closing the threshold gap at the source rather than only at the validator."
> Seeded by Soraya `--advance` (2026-08-11), `/project-init` protocol executed by hand. Parent umbrella: `aigov`. Self-init 6/25.

## Project Context
- **Project ID:** aigov-guideline-intake
- **Project root:** C:\Users\Farshad\PythonProjects\Skill_Development\AI_Governor
- **Captured:** 2026-08-11
- **Originating goal:** (see verbatim above)
- **Refined goal (if 3c produced one):** An `aigov/intake.py` in which (a) panels are drawn by reproducible sortition, (b) agenda priority is set by a quadratic credit budget where an over-budget ballot is REJECTED rather than clipped, (c) levels are aggregated by MEDIAN and the aggregation FAILS CLOSED on a genuinely polarized panel, (d) `compile_guidelines` has no path that emits a binding type-F guideline without a panel-supplied level, and (e) every numeric parameter the procedure itself needs carries non-AI provenance.
- **Role:** FAMILY ledger under umbrella `aigov`. Critical-path position: **Gate B — legitimacy-critical (crux A2).**
- **Horizon (months):** 3
- **Schema:** project-schema 0.1

## Empirical Concerns
- **Verdict:** PASS
- **Check status:** attempted
- **Provisional:** NO
- **Findings:** The design's load-bearing empirical claim — that the MEDIAN is the right aggregator for a one-dimensional level — rests on Black (1948), promoted to CITED tier in `research_outputs/aigov-v1-social-choice-walls.md` (W6: single-peaked ⇒ Condorcet winner is the median; *J. Political Economy* 56(1):23–34). No factual error. The claim's LIMIT is carried: Black holds on a single-peaked ONE-dimensional domain with an odd number of members, and in two dimensions a coordinate-wise median is not a Condorcet winner — so this mechanism is correct for scalar levels only, and a multi-dimensional guideline would need a different aggregator.

## Project vs Research-Program
- **Verdict:** PASS
- **Provisional:** NO
- **Classification:** project
- **Rationale:** Bounded (one module + one test file), mechanically measurable (no compile path yields an un-elicited binding level; the tests assert it negatively), horizon 3 ≤ 12. The unbounded question — "what is the right deliberative process for a real polity" — is explicitly NOT this family's goal.

## Refinement Candidates
- **Verdict:** PASS
- **Provisional:** NO
- **Refined-from:** originating-goal
- **Candidates:** C1 (= refined goal, EXECUTED). C2 (liquid democracy instead of sortition) — REJECTED for V1: delegation concentration (empirically-observed super-voters in LiquidFeedback deployments) reintroduces exactly the capture channel sortition avoids; kept as a comparison arm for later. C3 (deliberative polling with pre/post preference measurement) — DEFERRED: it needs real humans, so it is a Stage-B question, not software.

## MVP Criteria
<!-- attempt-budget: 3 -->
- file-exists aigov/intake.py
- test-exit-0 python -m pytest tests/test_intake.py -q
- project-state-row project_state/aigov.md:F2-threshold-gap-closed-at-source
<!-- project-state:end:mvp-criteria -->

> **Bar status: PROPOSED (draft-then-ratify)** under the v1.12 execute-mode exception. Predicate targets the
> UMBRELLA per the self-satisfying-predicate rule.

## Goal Hierarchy
### Long-term (12+ months tier)
An intake in which the polity's numbers are the only numbers that ever bind — so that "the AI is advisory" is a structural property of the pipeline rather than a promise about behaviour.

### Mid-term (3-12 months)
| # | Milestone | Success Criterion | Horizon |
|---|---|---|---|
| 1 | Sortition + quadratic budget + median elicitation | reproducible from a seed; over-budget ballots rejected; median not mean | ≤1 mo |
| 2 | Fail-closed on polarization, strategy-resistant | genuine camps escalate; a small minority cannot force escalation | ≤1 mo |
| 3 | No un-elicited binding guideline is constructible | negative tests over every compile path | ≤2 mo |
| 4 | Kernel binding: intake output is the kernel's ONLY objective source | F5 wiring | ≤3 mo |

### Short-term (≤1 month)
| # | Action | Class | Owner | Horizon |
|---|---|---|---|---|
| 1 | Wire intake output into the kernel as the sole objective source | edit-local-code | claude | ≤4 wk |
| 2 | Deliberation round-trip: escalated levels return to the panel and re-elicit | edit-local-code | claude | ≤4 wk |
| 3 | Stratified sortition (demographic quotas) as a sampling variant | edit-local-code | claude | ≤4 wk |
| 4 | Re-derive the polarization threshold at other panel sizes (8, 24, 50) | run-tests | claude | ≤2 wk |

## State Snapshot
### Assumptions
- Scalar levels are the common case; multi-dimensional guidelines are rarer — confidence: medium (Black's limit applies)
- A sortition panel's proposal distribution is informative about the electorate's — confidence: medium (sampling error at n=16 is large)
- Escalation to deliberation is an available remedy in a real polity — confidence: medium
### Evidence
| # | Claim | Source | Confidence | Captured |
|---|---|---|---|---|
| 1 | Median is the Condorcet winner on a single-peaked 1-D domain | Black 1948, JPE 56(1):23-34, via research_outputs/aigov-v1-social-choice-walls.md | high | 2026-08-11 |
| 2 | Polarization threshold 0.900 separates unimodal from two-camp panels with 26 errors / 800 trials (3.25%) | `calibrate_polarization()`, deterministic, re-runnable | high | 2026-08-11 |
| 3 | unimodal p95 = 0.867, unimodal max = 0.914, bimodal p05 = 0.893 — the classes genuinely OVERLAP | same calibration | high | 2026-08-11 |
| 4 | 1, 2 and 3 extremists of a 16-panel all still aggregate; median untouched at 25.0 | tests/test_intake.py strategic-manipulation cases | high | 2026-08-11 |
<!-- project-state:end:evidence -->
### Unknowns
- Whether the threshold holds at other panel sizes (calibrated only at n=16)
- What happens to an escalated level in practice — the deliberation round-trip is not built
- Whether a 25% camp floor is the right floor, or whether it silently disenfranchises a real minority position
- Sampling error: how often a 16-person panel misrepresents a 400-person electorate's level
### Hypotheses (Active)
| ID | Statement | Status (open/under-investigation/falsified/confirmed) | Last-tested |
|---|---|---|---|
| H1 | No path through compile_guidelines emits a binding type-F guideline without a panel-supplied level | confirmed | 2026-08-11 |
| H2 | Bimodality is separable from unimodal spread by a scale-invariant metric | confirmed | 2026-08-11 |
| H3 | A small minority cannot force escalation (strategy-resistance holds) | confirmed | 2026-08-11 |
| H4 | The derived threshold generalizes to panel sizes other than 16 | open | - |
| H5 | The 25% camp floor does not disenfranchise a legitimate minority position | open | - |
<!-- project-state:end:hypotheses -->
### Decisions Made
| Decision | Date | Notes |
|---|---|---|
| DI1 — MEDIAN, never mean, for level aggregation | 2026-08-11 | Black (1948, CITED): on a single-peaked 1-D domain the median is the Condorcet winner and is not draggable by one extreme report. A mean is trivially captured by a single absurd proposal. |
| DI2 — Over-budget ballots are REJECTED, never clipped or scaled | 2026-08-11 | Clipping silently rewrites a citizen's expressed intensity, which is a quiet form of the steering this project exists to prevent. |
| DI3 — Fail closed on polarization rather than aggregating | 2026-08-11 | A median is always DEFINED, but on two camps it is a number nobody proposed. Same discipline as fail_safe_gate: never certify what you cannot faithfully aggregate. |
| DI4 — Procedural parameters carry provenance too (recursive honesty) | 2026-08-11 | The polarization tolerance is itself a number. Letting the governor supply it would reproduce the exact defect the module exists to prevent, so `compile_guidelines` REFUSES an AI_SUPPLIED ProceduralParameter (G2). |
| DI5 — The threshold is DERIVED by simulation, not asserted | 2026-08-11 | `calibrate_polarization()` sweeps 400 unimodal + 400 two-camp panels and returns the error-minimising threshold (0.900). Re-derivable by anyone; a test pins the default to within 0.02 of the derivation so it cannot silently drift. |
| DI6 — Minimum camp share 25% | 2026-08-11 | Without it, an unconstrained 2-means split scores ONE outlier at 1.000 and hands any single panelist a unilateral veto on aggregation. Named residual: the floor could in principle mask a genuine <25% minority position (H5). |
| DI7 — TWO metric defects found by SWEEPING, not by unit tests | 2026-08-11 | The unit tests were green on hand-picked fixtures both times. Only a parameter sweep + an adversarial case exposed (a) range-normalisation measuring noise and (b) the single-outlier veto. Verify-in-batch by inspection, not exit code. |
| DI8 — The LIVE registry is now intake-DERIVED, and departments READ levels instead of restating them | 2026-08-11 | `aigov/guidelines.py` previously declared `level=25.0` with a comment saying 'ELICITED by the assembly' — the comment asserted a provenance the code did not have. It now runs a real intake round (seeded panel P-2026-08-11, 16 members of 400; quadratic priority ballots; median elicitation) and `RATIFIED` is its output. D1 and D2 call `level_of('G-F-004')` / `level_of('G-F-003')`; a source-scan test asserts NO literal numeric threshold survives in either spec. If the fixture panel were polarized, the build would FAIL rather than invent a level (pinned by a test). Honest label: the MECHANISM is real, the CITIZENS are a deterministic fixture. |
<!-- project-state:end:decisions-made -->
### Pending Decisions
| Decision | Proposer | Blocker | Notes |
|---|---|---|---|
| Re-derive the threshold per panel size, or keep one global constant? | claude | H4 | one constant is simpler; per-size is more honest if the metric is size-sensitive |
| Should an escalated level block the whole guideline set, or only that guideline? | claude | none — currently only that guideline | current behaviour is per-guideline; a polity might want a stronger coupling |
<!-- project-state:end:pending-decisions -->

## Bellman-Inspired Decision Frame
### Current state (one-line summary)
`aigov/intake.py` built and tested (39 tests): reproducible sortition, quadratic priority budget with reject-not-clip, median level elicitation with a DERIVED fail-closed polarization threshold (0.900, 26 errors/800 trials) and a 25% camp floor that closes the single-outlier veto; `compile_guidelines` has no path to a binding un-elicited level, verified negatively.

### Target state / terminal condition
See ## MVP Criteria — module + suite + the umbrella record.

### Progress proxy
- **MVP bar:** 3 / 3 criteria met (see `## MVP Criteria`) — bar REACHED 2026-08-11; live registry wired 2026-08-11
- **v0.1 metric:** `unknowns-retired` count + `gates-passed` count

### Candidate next actions
| # | Action | Class | Expected progress | Expected info gain | Uncertainty | Cost |
|---|---|---|---|---|---|---|
| 1 | Wire intake output into the kernel as the sole objective source | edit-local-code | high | high | medium | med |
| 2 | Deliberation round-trip for escalated levels | edit-local-code | med | high | high | med |
| 3 | Re-derive threshold at panel sizes 8/24/50 (tests H4) | run-tests | low | high | low | low |
| 4 | Stratified sortition variant | edit-local-code | med | med | medium | med |
<!-- project-state:end:candidate-actions -->

### Re-evaluation trigger
- **Default:** re-run `/project-state` after any action class fires
- **Manual override:** `/project-state aigov-guideline-intake`

## Allowed Action Classes (v0.2 placeholder — not enforced in v0.1)
- `propose` · `research` · `write-plan` · `edit-local-code` (requires approval) · `run-tests` · `ask-user` · `stop`

## Action Log
| # | Date | Action class | Description | Outcome |
|---|---|---|---|---|
| 1 | 2026-08-11 | propose | /project-init protocol executed by hand (family seed) | ledger created; self-init 6/25 |
| 2 | 2026-08-11 | edit-local-code | Wrote aigov/intake.py: sortition, quadratic budget, median elicitation, fail-closed compile | 29 tests green on first run |
| 3 | 2026-08-11 | run-tests | Verify-in-batch SWEEP of the polarization metric (not just exit code) | DEFECT 1: range-normalised gap scored a tight cluster 0.500 and false-escalated a wide unimodal panel |
| 4 | 2026-08-11 | edit-local-code | Replaced with scale-invariant bimodality: 1 - WCSS(2)/WCSS(1) over the exact 1-D 2-means split | fixed unimodal cases; DEFECT 2 exposed: ONE outlier scored 1.000 = unilateral escalation veto |
| 5 | 2026-08-11 | edit-local-code | Added a 25% minimum camp share so an outlier cannot manufacture a camp | 1/2/3 extremists now aggregate with median untouched; genuine 50/50, 30/70, 25/75 camps escalate |
| 6 | 2026-08-11 | run-tests | Re-derived the threshold by simulation (`calibrate_polarization`) | 0.900; errors 36 -> 26 of 800; default pinned to within 0.02 of the derivation by a test |
| 7 | 2026-08-11 | run-tests | Full root suite | 128 passed (89 prior + 39 intake); vendored organ 193 unaffected |
| 8 | 2026-08-11 | edit-local-code | Rewrote aigov/guidelines.py to PRODUCE RATIFIED from a real intake round (panel + elicitations + audit record) | levels 25.0 / 16.0 now derived; COMPILE_ERRORS empty; INTAKE_RECORD exposes panel fingerprint + priority ranking |
| 9 | 2026-08-11 | edit-local-code | Wired D1/D2 to read thresholds via level_of() instead of restating literals | zero hand-typed numeric thresholds remain in either spec (source-scan verified) |
| 10 | 2026-08-11 | run-tests | Added 6 registry-provenance tests incl. a source-scan guard and a polarized-panel-breaks-the-build test | root suite 134 passed; vendored organ 193 unaffected |
<!-- project-state:end:action-log -->

## Open Questions for User
- MVP bar is PROPOSED under the execute-mode exception, not confirmed.
- **Named residual (DI6):** the 25% camp floor closes a strategic veto but could in principle mask a genuine minority position held by fewer than a quarter of a panel. That is a real trade-off between strategy-resistance and minority visibility, and it is a governance value choice, not a technical one — surfaced rather than settled.

## Last Evaluation (v0.2 placeholder — not enforced in v0.1)
- **Date:** 2026-08-11
- **Progress signal:** bar reached 3/3; H1/H2/H3 confirmed; 2 real metric defects found by sweeping and fixed; threshold derived rather than asserted
