# AI Government F1 — Constitutional Core & Machine Limits (D0)
<!-- project-schema: 0.1 -->

> Initialized 2026-08-11. Project ID: aigov-constitution. Originating goal (verbatim): "Write the charter that bounds the AI Governor - what it may never do - such that every clause is either machine-checkable (enforced by an executable invariant) or explicitly labelled aspirational, and the machine-checkable fraction is reported as a measured number rather than asserted."
> Seeded by Soraya `decompose` (2026-08-11), `/project-init` protocol executed by hand. Parent umbrella: `aigov`.

## Project Context
- **Project ID:** aigov-constitution
- **Project root:** C:\Users\Farshad\PythonProjects\Skill_Development\AI_Governor
- **Captured:** 2026-08-11
- **Originating goal:** (see verbatim above)
- **Refined goal (if 3c produced one):** A charter document plus an executable invariant module in which (a) every clause carries an explicit `enforced-by` field naming either an invariant function or the literal label `aspirational`, (b) the fraction of clauses backed by an executable invariant is computed by a test rather than claimed in prose, and (c) at least the four non-negotiable limits — objective-selection, self-amendment, exception-holding, and role-separation — are backed by invariants that a violating fixture actually trips.
- **Role:** FAMILY ledger under umbrella `aigov`. Critical-path position: **Gate A** (parallel with `aigov-foundations`).
- **Horizon (months):** 3
- **Schema:** project-schema 0.1

## Empirical Concerns
- **Verdict:** FLAG
- **Check status:** attempted
- **Provisional:** YES
- **Findings:** The goal embeds one contested premise: **that an AI can be constitutionally constrained by rules it also executes** (umbrella assumption A7, confidence low). This is not a factual error but it is load-bearing and known-fragile: the whole Soraya honesty class OT1/T1=(c) exists because in-process, model-executed constraints are best-effort discipline, NOT enforcement — a model cannot intercept its own tool calls. **Design consequence, recorded now so it cannot quietly become a false claim:** the charter's guarantees must be sited *outside* the constrained actor wherever they matter — a separate verifier process, an append-only log the governor cannot write, and human ratification — exactly the `generator ≠ tally ≠ verifier` separation. Any clause that depends on the governor policing itself is `aspirational` by definition and must be labelled so.

## Project vs Research-Program
- **Verdict:** PASS
- **Provisional:** NO
- **Classification:** project
- **Rationale:** Bounded (one charter + one invariant module + a measured fraction), measurable (the fraction is computed by a test; the four non-negotiables have tripping fixtures), horizon 3 ≤ 12. The broader question "what should a colony's constitution say" is a research program and stays with `aigov-foundations`; this family only asks what is *enforceable*.

## Refinement Candidates
- **Verdict:** PASS
- **Provisional:** NO
- **Refined-from:** originating-goal
- **Candidates:** C1 (= refined goal): full clause list with `enforced-by` fields + invariant module + measured checkable fraction. C2 (non-negotiables only): implement invariants for just the four hard limits; label everything else aspirational — faster, and honest. C3 (external-verifier-first): build the independent verifier process before any charter text, on the theory that the enforcement site determines which clauses are writable at all.

## MVP Criteria
<!-- attempt-budget: 3 -->
- file-exists docs/charter.md
- file-exists aigov/charter_invariants.py
- test-exit-0 python -m pytest tests/test_charter_invariants.py -q
- project-state-row project_state/aigov.md:F1-charter-checkable-fraction-landed
<!-- project-state:end:mvp-criteria -->

> **Predicate repointed 2026-08-11** — see the defect note in `aigov-dept-contract.md`: a
> `project-state-row` predicate must never target the ledger that holds it, or it matches its own
> criterion line and is self-satisfying. Now correctly **unmet**.

> **Bar status: PROPOSED (draft-then-ratify)** under the v1.12 execute-mode exception. Not user-confirmed.

## Goal Hierarchy
### Long-term (12+ months tier)
A charter whose binding clauses are enforced somewhere the governor cannot reach, and whose unenforceable clauses are honestly labelled as aspirations rather than sold as guarantees.

### Mid-term (3-12 months)
| # | Milestone | Success Criterion | Horizon |
|---|---|---|---|
| 1 | Clause list with `enforced-by` fields | Every clause has an invariant name or the literal `aspirational` | ≤1 mo |
| 2 | Invariants for the four non-negotiables | Each has a violating fixture that trips it | ≤2 mo |
| 3 | Checkable fraction measured by test | A test computes and asserts the fraction; the number is in this ledger | ≤2 mo |
| 4 | Emergency-authority clause (declare / exercise / terminate / audit split) | Four distinct actors; automatic expiry; post-hoc audit mandatory | ≤3 mo |

### Short-term (≤1 month)
| # | Action | Class | Owner | Horizon |
|---|---|---|---|---|
| 1 | Draft the clause list (target 20–30 clauses) | write-plan | claude | ≤1 wk |
| 2 | Classify each clause: enforceable-where? (in-governor / external verifier / human-only) | propose | claude | ≤1 wk |
| 3 | Implement invariants for the four non-negotiables | edit-local-code | claude | ≤2 wk |
| 4 | Write the fraction-measuring test; record the number here | run-tests | claude | ≤3 wk |
| 5 | Draft the emergency-authority clause against the L5 canon | write-plan | claude | ≤4 wk |

## State Snapshot
### Assumptions
- An AI can be constitutionally constrained by rules it also executes — confidence: LOW (see Empirical FLAG; mitigation is external siting)
- A meaningful fraction of constitutional clauses is machine-checkable at all — confidence: medium (this family's H1)
- The four non-negotiables are the right four — confidence: medium
### Evidence
| # | Claim | Source | Confidence | Captured |
|---|---|---|---|---|
| 1 | In-process, model-executed constraints are best-effort discipline, not enforcement | Soraya named residuals T1=(c) / OT1 (`~/.claude/skills/soraya/SKILL.md`) | high | 2026-08-11 |
| 2 | Fail-closed escalation beats silent certification: 0 silent failures across 500-panel ensembles | Mars_Governance results/innovation_governance_failsafe_2026-06-08.md | medium | 2026-08-11 |
<!-- project-state:end:evidence -->
### Unknowns
- What fraction of clauses is machine-checkable (the number this family exists to measure)
- Where the external verifier runs, and who owns it, in a colony with one compute substrate
- Whether "the AI may never select the objective" is checkable or only auditable
- Who terminates an emergency if the terminating body is itself incapacitated
### Hypotheses (Active)
| ID | Statement | Status (open/under-investigation/falsified/confirmed) | Last-tested |
|---|---|---|---|
| H1 | The machine-checkable fraction of charter clauses exceeds 0.5 | confirmed | 2026-08-11 |
| H2 | Each of the four non-negotiables admits a violating fixture that an invariant trips | confirmed | 2026-08-11 |
| H3 | Every clause that depends on the governor policing itself can be re-sited to an external verifier or is genuinely aspirational | confirmed | 2026-08-11 |
<!-- project-state:end:hypotheses -->
### Decisions Made
| Decision | Date | Notes |
|---|---|---|
| DK1 — Any clause enforced only by the governor's own compliance is labelled `aspirational`, never `enforced` | 2026-08-11 | direct transfer of the OT1 honesty rail; prevents the project's central false claim. MECHANIZED: `Clause.is_enforced` requires site in {external_verifier, human_only}, and `clause_integrity_errors` rejects any clause claiming enforcement while sited IN_GOVERNOR. |
| DK2 — `enforced_by` must resolve to an IMPLEMENTED invariant in this repo; otherwise ASPIRATIONAL or PENDING:<family> | 2026-08-11 | Added after the fraction pin failed. Naming a real-but-unwired invariant (C15's fail_safe_gate, which lives in Mars_Governance) inflated the measured fraction from 0.7083 to 0.75. PENDING is tracked separately from ASPIRATIONAL so "cannot be enforced" stays distinguishable from "not enforced YET". |
| checkable-fraction-measured | 2026-08-11 | 17 enforced / 1 pending / 6 aspirational of 24 clauses = **0.7083**, computed by `checkable_fraction()` and pinned by `test_checkable_fraction_matches_the_recorded_number`. H1 (>0.5) CONFIRMED. Answers the family's central unknown with a number rather than a claim. |
| Hypothesis H1 updated | 2026-08-11 | Status → confirmed. Measured 0.7083 > 0.5. |
| Hypothesis H2 updated | 2026-08-11 | Status → confirmed. All four non-negotiables trip on violating fixtures: N1 on an AI_SUPPLIED threshold; N2 on an unratified change, a self-issued ratification (5 parametrized bodies), and a record covering a different change; N3 on the AI holding declare or terminate, on role collapse, on missing auto-expiry, on optional post-hoc audit, and on a missing role; N4 on generate+decide and generate+verify. |
| Hypothesis H3 updated | 2026-08-11 | Status → confirmed, with a NAMED RESIDUAL. Every clause resolved to one of {externally-sited enforced, PENDING with a named family, honestly aspirational} — 0 integrity errors. RESIDUAL: siting at external_verifier is a DEPLOYMENT property; this proves the invariant exists and fires, NOT that the verifier runs as a genuinely separate actor from the Governor. That proof is family aigov-audit-arbitration's (D15). Honest claim: "the limit is checkable and checked", never "enforced against an adversarial Governor". |
<!-- project-state:end:decisions-made -->
### Pending Decisions
| Decision | Proposer | Blocker | Notes |
|---|---|---|---|
| Whether to build the external verifier first (C3) before charter text | claude | none | C3 is the more honest order; costs a week |
| Emergency-authority design: who declares vs exercises vs terminates vs audits | claude | F0 canon evidence (L5) | four distinct actors is the drafted position |
<!-- project-state:end:pending-decisions -->

## Bellman-Inspired Decision Frame
### Current state (one-line summary)
Charter not yet drafted; the four non-negotiables and the separation-of-powers invariant are stated in `docs/department-ontology.md` and `docs/idea-anchor-DRAFT-2026-08-11.md`; enforcement-siting problem identified and FLAGged.

### Target state / terminal condition
See ## MVP Criteria — charter + invariant module + a measured (not asserted) checkable fraction.

### Progress proxy
- **MVP bar:** 4 / 4 criteria met (see `## MVP Criteria`) — bar REACHED 2026-08-11
- **v0.1 metric:** `unknowns-retired` count + `gates-passed` count
- **v0.2+:** weighted combination (TBD)

### Candidate next actions
| # | Action | Class | Expected progress | Expected info gain | Uncertainty | Cost |
|---|---|---|---|---|---|---|
| 1 | Draft clause list | write-plan | high | high | low | low |
| 2 | Classify enforcement site per clause | propose | high | highest (settles H3) | medium | low |
| 3 | Implement four non-negotiable invariants | edit-local-code | high | high | medium | low |
| 4 | Measure checkable fraction | run-tests | medium | high (settles H1) | low | low |
<!-- project-state:end:candidate-actions -->

### Re-evaluation trigger
- **Default:** re-run `/project-state` after any action class fires
- **Manual override:** `/project-state aigov-constitution`

## Allowed Action Classes (v0.2 placeholder — not enforced in v0.1)
- `propose` · `research` · `write-plan` · `edit-local-code` (requires approval) · `run-tests` · `ask-user` · `stop`

## Action Log
| # | Date | Action class | Description | Outcome |
|---|---|---|---|---|
| 1 | 2026-08-11 | propose | /project-init protocol executed by hand (family seed) | ledger created |
| 2 | 2026-08-11 | edit-local-code | Wrote aigov/charter_invariants.py: 24 clauses + N1-N4 invariants + DK1/DK2 mechanized | 0 integrity errors |
| 3 | 2026-08-11 | run-tests | Wrote + ran tests/test_charter_invariants.py | fraction pin FAILED at 18/24 vs predicted 17/24 |
| 4 | 2026-08-11 | edit-local-code | Diagnosed the pin failure: C15 named an unwired invariant (overclaim), not a bad expectation | added PENDING status + overclaim detection; fraction corrected to 0.7083 |
| 5 | 2026-08-11 | edit-local-code | Wrote aigov/render_charter.py; generated docs/charter.md from the enforcing code | regeneration idempotent; doc cannot drift from invariants |
| 6 | 2026-08-11 | run-tests | Full suite after charter landed | 88 passed in 0.28s |
| 7 | 2026-08-11 | edit-local-code | Added an N/M MVP-bar fraction to ### Progress proxy; prior version in git history | 4 / 4 — terminal_met=met |
<!-- project-state:end:action-log -->

## Open Questions for User
- **FLAG resolution needed for `Empirical Concerns`:**
  - Why it's flagged: the goal assumes an AI can be constrained by rules it also executes (A7, low confidence) — the same class as Soraya's own T1=(c)/OT1 residual.
  - Recommended resolution: adopt DK1 (self-policed clauses are labelled `aspirational`) and prefer C3 (build the external verifier before the charter text). Then re-run this gate.
  - If that doesn't converge: run `/brainstorm` on the enforcement-siting question, then `/review` to pick.
- MVP bar is PROPOSED under the execute-mode exception, not confirmed.

## Last Evaluation (v0.2 placeholder — not enforced in v0.1)
- **Date:** 2026-08-11
- **Progress signal:** (init only)
