# AI Government F3 — Department Contract (the department SDK)
<!-- project-schema: 0.1 -->

> Initialized 2026-08-11. Project ID: aigov-dept-contract. Originating goal (verbatim): "Build the DepartmentSpec contract plus a validator enforcing invariants I1-I10, such that two structurally different departments (HIGH and LOW central-legitimacy) are both expressible, their coupling is declared bilaterally, and I6 is demonstrated by a mutated spec that FAILS validation."
> Seeded by Soraya `decompose` (2026-08-11) by executing `/project-init`'s protocol by hand against the schema loaded in-session — the Skill tool ran the umbrella; the three family ledgers reuse the same loaded protocol. Parent umbrella: `aigov`.

## Project Context
- **Project ID:** aigov-dept-contract
- **Project root:** C:\Users\Farshad\PythonProjects\Skill_Development\AI_Governor
- **Captured:** 2026-08-11
- **Originating goal:** (see verbatim above)
- **Refined goal (if 3c produced one):** A `DepartmentSpec` dataclass + `validate(spec) -> [Error]` in which each of the invariants I1–I10 (`docs/department-ontology.md` §3) is a distinct, individually-triggerable validation error; two reference specs at opposite `central_legitimacy` ratings (D1 life-support HIGH, D2 economy LOW) both validate clean; their shared-variable contention is declared by BOTH sides; and for each invariant a mutated spec exists that the validator rejects.
- **Role:** FAMILY ledger under umbrella `aigov`. Critical-path position: **Gate B — the scaling primitive.**
- **Horizon (months):** 3
- **Schema:** project-schema 0.1

## Empirical Concerns
- **Verdict:** N-A
- **Check status:** not-applicable
- **Provisional:** NO
- **Findings:** (no factual-shape claims in goal text; the goal is a construction task over an internally-defined contract — empirical check not applicable. The *design* claims it encodes — Hayek's knowledge problem behind I8, Goodhart behind I4, Fuller behind I10 — are queued for audit-tier verification in family `aigov-foundations`, not here.)

## Project vs Research-Program
- **Verdict:** PASS
- **Provisional:** NO
- **Classification:** project
- **Rationale:** Bounded scope (one module + one validator + two reference specs + a mutation suite), measurable success criterion (each invariant individually triggerable; mutation rejected), horizon 3 ≤ 12.

## Refinement Candidates
- **Verdict:** PASS
- **Provisional:** NO
- **Refined-from:** originating-goal
- **Candidates:** C1 (top-ranked, = refined goal above): full I1–I10 validator + two opposite-legitimacy reference specs + per-invariant mutation tests. C2 (minimal): I1, I3, I5, I8 only — the four that carry the constitutional and subsidiarity semantics — deferring the hygiene invariants. C3 (schema-first): publish the spec schema as data (JSON-schema/TOML) with a thin Python loader, so departments are declarative artifacts rather than code.

## MVP Criteria
<!-- attempt-budget: 3 -->
- file-exists aigov/contract.py
- file-exists aigov/specs/d1_lifesupport.py
- file-exists aigov/specs/d2_economy.py
- test-exit-0 python -m pytest tests/test_contract.py -q
- test-exit-0 python -m pytest tests/test_contract_mutations.py -q
- project-state-row project_state/aigov.md:F3-contract-mutation-proof-landed
<!-- project-state:end:mvp-criteria -->

> **Predicate defect found + fixed 2026-08-11 (before any `--until-mvp` loop ran).** This criterion
> originally read `project-state-row project_state/aigov-dept-contract.md:I6-mutation-proof-demonstrated`
> — pointing at THE SAME LEDGER that contains the criterion, so the pattern matched its own criterion
> line and the predicate was **self-satisfying**: it evaluated MET before any work existed. Repointed at
> the UMBRELLA ledger, which the criterion text does not live in. **General rule: a
> `project-state-row` predicate must never target the ledger that holds it.** Same class as the
> string-presence-tests-green-on-words trap.

> **Bar status: PROPOSED (draft-then-ratify).** Written under the v1.12 execute-mode exception — the invoking
> directive carries explicit execute-mode authorization ("think as thoroughly as you need for as many steps as
> you need"). Soraya proceeds on this bar and surfaces it for redirect; it is NOT user-confirmed yet.

## Goal Hierarchy
### Long-term (12+ months tier)
A department contract stable enough that the remaining thirteen departments are additive artifacts rather than bespoke rewrites.

### Mid-term (3-12 months)
| # | Milestone | Success Criterion | Horizon |
|---|---|---|---|
| 1 | `DepartmentSpec` + sub-types defined | Both reference specs express fully; no field is "misc"/free-form | ≤1 mo |
| 2 | Validator I1–I10 | Each invariant individually triggerable by a distinct mutated spec | ≤2 mo |
| 3 | Bilateral coupling machinery | D1↔D2 contention on pressurized volume + power declared by both; one-sided declaration REJECTED | ≤2 mo |
| 4 | Fuller legality linter (I10) | 8 desiderata checked against a machine-emitted rule | ≤3 mo |

### Short-term (≤1 month)
| # | Action | Class | Owner | Horizon |
|---|---|---|---|---|
| 1 | Write `aigov/contract.py` (dataclasses + enums) | edit-local-code | claude | ≤1 wk |
| 2 | Write the two reference specs (D1 HIGH, D2 LOW) | edit-local-code | claude | ≤1 wk |
| 3 | Write `validate()` covering I1–I10 | edit-local-code | claude | ≤2 wk |
| 4 | Write `tests/test_contract_mutations.py` — one mutation per invariant | run-tests | claude | ≤2 wk |
| 5 | Verify-in-batch: run the validator on both specs + inspect output, not just exit code | run-tests | claude | ≤2 wk |

## State Snapshot
### Assumptions
- Two departments at opposite central-legitimacy ratings are expressible under one schema — confidence: medium (this family's H1)
- Coupling can be declared statically rather than discovered at runtime — confidence: medium
- A validator can distinguish "rule/price setting" from "quantity allocation" mechanically (I8) — confidence: low (the hard one)
- Fuller's eight desiderata are checkable against a formal rule representation — confidence: medium
### Evidence
| # | Claim | Source | Confidence | Captured |
|---|---|---|---|---|
| 1 | Ten of sixteen departments already have a concrete tested primitive to bind against | docs/department-ontology.md §2; Mars_Governance 193/193 | high | 2026-08-11 |
<!-- project-state:end:evidence -->
### Unknowns
- Whether I8 (rule/price vs quantity allocation) admits a mechanical test or degrades to a label the author self-asserts
- What formal representation a "rule" needs so the Fuller linter is more than string matching
- Whether `latent` state variables can be represented without inviting fabricated observability
### Hypotheses (Active)
| ID | Statement | Status (open/under-investigation/falsified/confirmed) | Last-tested |
|---|---|---|---|
| H1 | D1 (HIGH) and D2 (LOW) are both expressible under one DepartmentSpec without shared mutable state | confirmed | 2026-08-11 |
| H2 | I8 is mechanically checkable rather than an author-asserted label | confirmed | 2026-08-11 |
| H3 | Every invariant I1–I11 has a mutation that the validator rejects and a clean spec it accepts | confirmed | 2026-08-11 |
<!-- project-state:end:hypotheses -->
### Decisions Made
| Decision | Date | Notes |
|---|---|---|
| DC1 — I6 requires a mutation-proof: a falsification test that cannot fail is not a test | 2026-08-11 | anti-theater; inherited from the /innovate falsification discipline |
| I6-mutation-proof-demonstrated | 2026-08-11 | TWO levels. (a) Spec falsification tests can come out FALSE: D1's O2-supply claim fails at a 0.25 life-support power share; D2's revenue claim fails at a 0.90 volume-tax rate (test_I6_falsification_tests_can_actually_fail). (b) The invariants themselves are non-vacuous: with the validator patched to a no-op, 24 of 28 mutation tests go RED; the 4 survivors are exactly the negative controls (assert-does-NOT-fire / no-validate-dependency). Suite: 56 passed. |
| Hypothesis H1 updated | 2026-08-11 | Status → confirmed. A HIGH- and a LOW-central-legitimacy department are both fully expressible under ONE DepartmentSpec; both validate with 0 errors; shared variables (pressurized_volume_m3, power_kw) are carried as declared bilateral Couplings with arbiter D13, NOT as shared mutable state. Assumption A1 survives its first real test. |
| Hypothesis H2 updated | 2026-08-11 | Status → confirmed, WITH A NAMED RESIDUAL. The I8 check is fully mechanical — `validate()` deterministically rejects a QUANTITY_ALLOCATION instrument on a LOW-legitimacy department and deterministically accepts the same class on a HIGH one. Residual: the InstrumentClass assignment is AUTHOR-DECLARED, so a mislabelled instrument evades the check. Subsidiarity is therefore mechanically ENFORCED over declared classes and AUDITED at the classification step (D15's job) — say that, never "subsidiarity is proven". |
| Hypothesis H3 updated | 2026-08-11 | Status → confirmed. Extended from I1–I10 to I1–I11 (I11 added by probe B1). test_all_eleven_invariants_have_at_least_one_triggering_mutation is the standing coverage guard: a new invariant landing without a mutation fails it. |
<!-- project-state:end:decisions-made -->
### Pending Decisions
| Decision | Proposer | Blocker | Notes |
|---|---|---|---|
| Spec substrate: Python dataclasses vs declarative data (C3) | claude | none — decide at first commit | dataclasses first; C3 is a cheap later refactor |
| Whether I8 stays mechanical or degrades to a reviewed label | claude | H2 outcome | if H2 falsifies, I8 becomes an audited label and that MUST be stated, not hidden |
<!-- project-state:end:pending-decisions -->

## Bellman-Inspired Decision Frame
### Current state (one-line summary)
Contract designed on paper (`docs/department-ontology.md` §3: schema + I1–I10 + rationale per invariant); zero code written.

### Target state / terminal condition
See ## MVP Criteria — module + two opposite-legitimacy reference specs + per-invariant mutation tests, all green, with the I6 mutation-proof recorded in this ledger.

### Progress proxy
- **MVP bar:** 6 / 6 criteria met (see `## MVP Criteria`) — bar REACHED 2026-08-11
- **v0.1 metric:** `unknowns-retired` count + `gates-passed` count (raw counts, unweighted)
- **v0.2+:** weighted combination (TBD)

### Candidate next actions
| # | Action | Class | Expected progress | Expected info gain | Uncertainty | Cost |
|---|---|---|---|---|---|---|
| 1 | Write contract.py dataclasses | edit-local-code | high | medium | low | low |
| 2 | Write the two reference specs | edit-local-code | high | high (tests H1 directly) | medium | low |
| 3 | Implement validate() I1-I10 | edit-local-code | high | high (tests H2) | medium | low |
| 4 | Mutation suite | run-tests | medium | high (tests H3) | low | low |
<!-- project-state:end:candidate-actions -->

### Re-evaluation trigger
- **Default:** re-run `/project-state` after any action class fires
- **Manual override:** `/project-state aigov-dept-contract`

## Allowed Action Classes (v0.2 placeholder — not enforced in v0.1)
- `propose` · `research` · `write-plan` · `edit-local-code` (requires approval) · `run-tests` · `ask-user` · `stop`

## Action Log
| # | Date | Action class | Description | Outcome |
|---|---|---|---|---|
| 1 | 2026-08-11 | propose | /project-init protocol executed by hand (family seed) | ledger created |
| 2 | 2026-08-11 | propose | Probe B1 added invariant I11 (threshold provenance) to the contract scope | I11 = no numeric threshold without a ratified-guideline or physical-constant provenance |
| 3 | 2026-08-11 | edit-local-code | Wrote aigov/contract.py (types + validate + validate_registry + fuller_lint, I1-I11) | module imports; 0 errors on both reference specs |
| 4 | 2026-08-11 | edit-local-code | Wrote aigov/guidelines.py (6 ratified guidelines across all 5 probe-B1 types) | G-A-006 aspiration present and provably non-binding |
| 5 | 2026-08-11 | edit-local-code | Wrote aigov/specs/d1_lifesupport.py (HIGH) + aigov/specs/d2_economy.py (LOW) | both validate clean; opposite legitimacy ratings |
| 6 | 2026-08-11 | run-tests | Verify-in-batch: inspected D1 falsification numbers, not just exit code | D1 test passed with a ~5x margin (could not fail); tightened to a defensible 0.40 power share, 0.20 kg O2/kWh envelope |
| 7 | 2026-08-11 | run-tests | Wrote + ran tests/test_contract.py + tests/test_contract_mutations.py | 56 passed in 0.25s |
| 8 | 2026-08-11 | run-tests | Mutation-proofed the SUITE: patched validate to a no-op | 24 of 28 mutation tests went RED; 4 survivors are the negative controls |
| 9 | 2026-08-11 | edit-local-code | Added an N/M MVP-bar fraction to ### Progress proxy; prior version in git history | 6 / 6 — terminal_met=met |
<!-- project-state:end:action-log -->

## Open Questions for User
- MVP bar above is PROPOSED under the execute-mode exception, not confirmed. Redirect it if the six predicates are the wrong bar.
- If H2 falsifies (I8 not mechanically checkable), the subsidiarity guarantee weakens from enforced to audited. That is a material change to what the project can claim and will be surfaced, not absorbed.

## Last Evaluation (v0.2 placeholder — not enforced in v0.1)
- **Date:** 2026-08-11
- **Progress signal:** (init only)
