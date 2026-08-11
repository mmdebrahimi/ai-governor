# AI Government F5 — The Governor Kernel: the runtime that cannot act un-gated
<!-- project-schema: 0.1 -->

> Initialized 2026-08-11. Project ID: aigov-kernel. Originating goal (verbatim): "Build the AI Governor runtime whose apply() REFUSES unless an action is (ratified AND certified-non-steering AND constraint-satisfying), with no force path, no default-allow and no warn-only flag - so 'the AI is advisory' is a property of the code rather than a promise about behaviour."
> Seeded by Soraya `--advance` spillover (2026-08-11), `/project-init` protocol executed by hand. Parent umbrella: `aigov`. Self-init 8/25.

## Project Context
- **Project ID:** aigov-kernel
- **Project root:** C:\Users\Farshad\PythonProjects\Skill_Development\AI_Governor
- **Captured:** 2026-08-11
- **Originating goal:** (see verbatim above)
- **Refined goal (if 3c produced one):** An `aigov/kernel.py` in which (a) `Certification.appliable` is the conjunction of exactly three conditions and `apply()` raises `UngatedActionError` on all seven other combinations, (b) a self-issued or mis-targeted ratification does not count, (c) non-steering is certified ONLY where a real certifier exists and every other instrument is REFUSED rather than waved through, (d) constraint checks run on a twin COPY, and (e) a fully-refused cycle leaves the colony's status quo standing rather than running life support at zero.
- **Role:** FAMILY ledger under umbrella `aigov`. Critical-path position: **Gate D — the runtime.**
- **Horizon (months):** 3
- **Schema:** project-schema 0.1

## Empirical Concerns
- **Verdict:** PASS
- **Check status:** attempted
- **Provisional:** NO
- **Findings:** The kernel's one externally-checkable claim — that the bound anti-steering certifier actually discriminates — was verified by execution before it was relied on: over 80 random panels a COMPLETE menu yields 31 certify / 34 steering / 15 escalate, while a STRAWMAN agenda yields **0 certify** / 65 steering / 15 escalate. The certifier is real and it discriminates. Its DOMAIN, however, is the resource (crop-fraction) problem it was built for; the kernel therefore certifies only `crop_area_allocation` and refuses every other instrument as `NOT_CERTIFIABLE`.

## Project vs Research-Program
- **Verdict:** PASS
- **Provisional:** NO
- **Classification:** project
- **Rationale:** Bounded (one module + one test file), mechanically measurable (exhaustive refusal over the 8 gate-condition combinations; a 12-cycle governed run), horizon 3 ≤ 12.

## Refinement Candidates
- **Verdict:** PASS
- **Provisional:** NO
- **Refined-from:** originating-goal
- **Candidates:** C1 (= refined goal, EXECUTED). C2 (generic non-steering certifier for all instruments) — REJECTED for now: a generic check would have to be invented, which is the exact defect this project exists to prevent; the honest form is refusal outside the certified domain. C3 (full ≥12-cycle integrated run with the adversarial suite) — that is F10/F11, not this family.

## MVP Criteria
<!-- attempt-budget: 3 -->
- file-exists aigov/kernel.py
- test-exit-0 python -m pytest tests/test_kernel.py -q
- project-state-row project_state/aigov.md:F5-kernel-cannot-act-ungated
<!-- project-state:end:mvp-criteria -->

> **Bar status: PROPOSED (draft-then-ratify)** under the v1.12 execute-mode exception. Predicate targets the
> UMBRELLA per the self-satisfying-predicate rule.

## Goal Hierarchy
### Long-term (12+ months tier)
A runtime in which the sentence "the AI cannot act without ratification" is checkable by reading the code, not by trusting the operator.

### Mid-term (3-12 months)
| # | Milestone | Success Criterion | Horizon |
|---|---|---|---|
| 1 | Three-condition gate + no override path | 7 of 8 condition combinations raise; `apply()` takes only (self, cert) | ≤1 mo |
| 2 | Real anti-steering binding with an honest domain boundary | strawman agenda never certifies; out-of-domain instruments refused | ≤1 mo |
| 3 | Status quo persists through a fully-refused run | 12 refused cycles leave the atmosphere at 21 kPa | ≤2 mo |
| 4 | Adversarial suite against the kernel (F10) | every named attack ends in detection or escalation | ≤3 mo |

### Short-term (≤1 month)
| # | Action | Class | Owner | Horizon |
|---|---|---|---|---|
| 1 | Wire D15 audit as an independent VERIFY seam (F9) | edit-local-code | claude | ≤4 wk |
| 2 | Adversarial suite: agenda reordering, metric gaming, emergency abuse (F10) | edit-local-code | claude | ≤4 wk |
| 3 | Extend certifiable instruments, or state permanently why they cannot be | research | claude | ≤4 wk |
| 4 | Retire the `aigov/choice/__init__.py` path shim via the C2 namespace migration | edit-local-code | claude | ≤4 wk |

## State Snapshot
### Assumptions
- Three conditions are the right gate — confidence: medium-high (they are D1's three, made mechanical)
- Refusing out-of-domain instruments is better than a generic check — confidence: high (a generic check would be invented)
- A deep-copied twin probe is a faithful simulation of applying an action — confidence: medium
### Evidence
| # | Claim | Source | Confidence | Captured |
|---|---|---|---|---|
| 1 | Strawman agenda NEVER certifies (0/80 panels); complete menu certifies 31/80 | direct execution of the vendored gate | high | 2026-08-11 |
| 2 | Only (ratified, CERTIFY, constraints-ok) applies; the other 7 combinations raise | exhaustive itertools test | high | 2026-08-11 |
| 3 | 12 fully-refused cycles leave partial pressure at 21.00 kPa, no violations | governed run, pinned by test | high | 2026-08-11 |
| 4 | Certification does not mutate the live twin (probe runs on a copy) | pinned by test | high | 2026-08-11 |
<!-- project-state:end:evidence -->
### Unknowns
- Whether any instrument beyond `crop_area_allocation` can ever be non-steering-certified
- Whether a deep-copy probe diverges from real application under stochastic dynamics
- Who plays the ratifier in a real deployment, and how its record is authenticated
- Whether the path shim masks a divergence between the two import styles of the vendored organ
### Hypotheses (Active)
| ID | Statement | Status (open/under-investigation/falsified/confirmed) | Last-tested |
|---|---|---|---|
| H1 | No path through the kernel applies an action failing any of the three conditions | confirmed | 2026-08-11 |
| H2 | The bound anti-steering certifier discriminates honest from strawman agendas | confirmed | 2026-08-11 |
| H3 | A fully-refused run leaves the colony in its status quo, not at zeros | confirmed | 2026-08-11 |
| H4 | The certifier's domain can be widened beyond crop-fraction without inventing a check | open | - |
<!-- project-state:end:hypotheses -->
### Decisions Made
| Decision | Date | Notes |
|---|---|---|
| DK1 — NO override path, by construction | 2026-08-11 | `apply()` takes only `(self, cert)`. Checked behaviourally on the SIGNATURE, not by grepping the source: the first version grepped for the word "override" and failed on its own docstring — the string-presence trap. |
| DK2 — Non-steering certified ONLY inside the certifier's real domain | 2026-08-11 | The vendored `fail_safe_gate` reasons over crop-fraction menus. Bound for `crop_area_allocation`; every other instrument returns `NOT_CERTIFIABLE` and is REFUSED. Inventing a generic steering check would be the exact defect this project exists to prevent. This turns aigov-collective-choice H2 from an open question into an ENFORCED boundary: outside the domain, nothing applies. |
| DK3 — VACUOUS PASS found by run inspection; status quo must persist | 2026-08-11 | `test_twelve_cycles_never_apply_an_ungated_action` was GREEN while the governed run LOST THE ATMOSPHERE at cycle 1: the kernel started from `InstrumentSettings()` zeros, so refusing every action meant running life support at zero — and "nothing applied" was exactly what the test asserted, so it could not see it. Fixed with `status_quo_settings()`, whose crop fraction is DERIVED (`1 / PLANT_O2_OVERPRODUCTION_FACTOR`) from the model's biological constant, not chosen. A dedicated anti-vacuous-pass test now asserts a fully-refused run leaves the colony ALIVE. |
| DK4 — Path shim in `aigov/choice/__init__.py` rather than rewriting vendored imports | 2026-08-11 | The organ imports itself as top-level `governance.*`. Rewriting to relative form is the C2 migration that DV3 deferred, because editing imports during a move risks silent behaviour change in known-good code. The shim reproduces what the vendored conftest does, keeps the subtree byte-identical, and preserves the 193/193 bar. Debt recorded: two import styles coexist and resolve to the same module only because the shim runs first. |
<!-- project-state:end:decisions-made -->
### Pending Decisions
| Decision | Proposer | Blocker | Notes |
|---|---|---|---|
| Widen the certifiable-instrument set, or declare the boundary permanent? | claude | H4 | widening requires a real certifier per domain, not a generic one |
| Who authenticates the ratifier's record in a real deployment? | claude | outside software scope | currently a plain dataclass; a real one needs the D15 audit organ |
<!-- project-state:end:pending-decisions -->

## Bellman-Inspired Decision Frame
### Current state (one-line summary)
`aigov/kernel.py` built and tested (20 tests): three-condition gate with no override path, real anti-steering binding to the vendored organ for `crop_area_allocation` and honest refusal elsewhere, constraint probing on a twin copy, and a status quo that survives a fully-refused run. Root suite 182; vendored organ 193/193 preserved.

### Target state / terminal condition
See ## MVP Criteria — module + suite + the umbrella record.

### Progress proxy
- **MVP bar:** 3 / 3 criteria met (see `## MVP Criteria`) — bar REACHED 2026-08-11
- **v0.1 metric:** `unknowns-retired` count + `gates-passed` count

### Candidate next actions
| # | Action | Class | Expected progress | Expected info gain | Uncertainty | Cost |
|---|---|---|---|---|---|---|
| 1 | D15 independent audit seam (F9) | edit-local-code | high | high | medium | med |
| 2 | Adversarial suite against the kernel (F10) | edit-local-code | high | high | medium | med |
| 3 | Retire the path shim via the C2 namespace migration | edit-local-code | low | low | medium | med |
| 4 | Investigate widening the certifiable-instrument set (H4) | research | med | high | high | med |
<!-- project-state:end:candidate-actions -->

### Re-evaluation trigger
- **Default:** re-run `/project-state` after any action class fires
- **Manual override:** `/project-state aigov-kernel`

## Allowed Action Classes (v0.2 placeholder — not enforced in v0.1)
- `propose` · `research` · `write-plan` · `edit-local-code` (requires approval) · `run-tests` · `ask-user` · `stop`

## Action Log
| # | Date | Action class | Description | Outcome |
|---|---|---|---|---|
| 1 | 2026-08-11 | propose | /project-init protocol executed by hand (family seed, spillover) | ledger created; self-init 8/25 |
| 2 | 2026-08-11 | research | Read the vendored tests for the canonical fail_safe_gate call, then EXERCISED it | complete_menu certifies 31/80 panels; strawman NEVER certifies (0/80) |
| 3 | 2026-08-11 | edit-local-code | Wrote aigov/kernel.py: three-condition gate, domain-bounded non-steering, copy-probe constraints | import failed — vendored organ uses top-level `governance.*` |
| 4 | 2026-08-11 | edit-local-code | Added a documented path shim in aigov/choice/__init__.py instead of rewriting vendored imports | kernel imports cleanly; organ still 193/193 |
| 5 | 2026-08-11 | run-tests | First kernel suite run | override-path test failed on its OWN docstring — replaced with a signature check |
| 6 | 2026-08-11 | run-tests | Verify-in-batch: INSPECTED a 12-cycle governed run rather than trusting green tests | VACUOUS PASS found — every cycle refused, atmosphere lost at cycle 1, suite still green |
| 7 | 2026-08-11 | edit-local-code | Added status_quo_settings() derived from PLANT_O2_OVERPRODUCTION_FACTOR | 12 refused cycles now hold 21.00 kPa; anti-vacuous-pass test added |
| 8 | 2026-08-11 | run-tests | Full verification | root 182 + vendored organ 193 = 375 green |
<!-- project-state:end:action-log -->

## Open Questions for User
- MVP bar is PROPOSED under the execute-mode exception, not confirmed.
- **Honest boundary (DK2):** the kernel can currently certify non-steering for exactly ONE instrument. That is a real limit on what the governor may do, not a temporary gap to paper over — widening it requires a genuine certifier per domain.

## Last Evaluation (v0.2 placeholder — not enforced in v0.1)
- **Date:** 2026-08-11
- **Progress signal:** bar reached 3/3; H1/H2/H3 confirmed; a VACUOUS PASS caught by run inspection and closed
