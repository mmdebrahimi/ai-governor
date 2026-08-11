# AI Government — Phase-1 Technical Plan (`--plan`, plan-first bounded autonomous completion)

> Soraya `--plan` output (v1.14 "L3.5"): the full ordered path to the checkable phase-1 bar, topologically
> ordered, with independent steps batched, and every step gate-classified. Execution runs under the **UNCHANGED**
> gate table; the ~100-step self-budget is attention/cost, **not** a safety boundary.
> Date: 2026-08-11. Umbrella: `aigov`. Terminal: `project_state/aigov.md` → `## Mission Terminal Condition`.
> **Blocked at step 0** on ratification of the three authority forks.

---

## 0. Plan preconditions

| # | Precondition | Status |
|---|---|---|
| P1 | Three authority forks ratified (AI role / scale / deliverable) | **PENDING — user** |
| P2 | Reuse asset verified green | ✅ `Mars_Governance` 193/193, run 2026-08-11 |
| P3 | Umbrella + Gate-A/B family ledgers seeded, markers valid | ✅ 4 ledgers, 0 missing/dup markers |
| P4 | MVP bars parse as checkable predicates | ✅ 15/15 predicates classify; budget 3 each |
| P5 | Python + pytest available in the AI_Governor root | to confirm at step 1 |

**If P1 resolves differently than drafted, this plan changes shape** — Fork 1 (sovereign vs organ) rewrites
F1/F5/F9 entirely; Fork 2 (scale) rewrites F4; Fork 3 (deliverable) could delete F4–F11 in favour of a document.
That is precisely why P1 is the rank-1 move and why nothing downstream is pre-built.

---

## 1. Step estimate and budget

| Quantity | Value |
|---|---|
| Pre-planned step estimate (phase 1) | **~78 steps** |
| Self-budget ceiling | **100 steps** (`--max-steps` default) |
| Self-extension policy | permitted on best judgement mid-run; each extension recorded in the audit trail, never silent |
| Budget verdict owner | `scripts/plan_budget.py:compute_budget_verdict` → `done` / `budget-exhausted` / `continue`, recomputed from the model-supplied step count + a **live** bar re-eval |
| Honesty | the model counts and honors the budget; a skill cannot intercept tool calls. This is **not** a code-enforced 100-cap (OT1). |

Steps are counted per executed action, not per file. Increments below are the batching unit.

---

## 2. The ordered path

Legend — gate class per `scripts/action_gate.py`: **A** = `auto` (reads, local writes/edits in cwd, local tests,
`/research`, `/project-state`) · **R** = reversible-outward (runs un-gated, emits a rollback note) · **G** =
genuinely-irreversible-outward (Care-PAUSE in all modes) · **$** = money (hard pause). **This whole plan is
class A except where marked.** No step in phase 1 spends money, publishes, sends, or deletes recursively.

### Gate A — foundations + limits (steps 1–18, ~2 weeks)

| # | Increment | Steps | Gate | Depends | Verify-in-batch |
|---|---|---|---|---|---|
| A1 | Environment: confirm python/pytest in AI_Governor root; create `aigov/` package + `tests/` + `pytest.ini` | 3 | A | P1 | run `pytest` on an empty suite → exits 0/5 |
| A2 | `/research` V1 — the five walls (Arrow, G–S, Sen, McKelvey, median-voter, Ashby): exact statements + preconditions | 3 | A | A1 | memo exists; `/research-verify` sidecar shows quotes verbatim |
| A3 | `/research` V4 — Fuller's eight desiderata (cheapest, directly implementable) | 2 | A | A1 | as above |
| A4 | `/research` V2 — Henry George theorem conditions + LVT efficiency | 3 | A | A1 | as above |
| A5 | `/research` V5 — OST Art. II/VI, Artemis Accords, 2015 US / 2017 LU resource laws | 3 | A | A1 | as above |
| A6 | Record FALSIFIED claims + revise the design bounds they supported (DF2) | 1 | A | A2–A5 | umbrella Evidence rows updated; any revision named |
| A7 | Charter clause list (20–30 clauses), each with an `enforced-by` field | 2 | A | A2, A3 | count clauses; count `aspirational` |
| A8 | Classify each clause by **enforcement site**: in-governor / external verifier / human-only | 1 | A | A7 | every clause classified; H3 answered |
| — | **Gate A exit test:** V1/V2/V4/V5 memos exist + charter clause list has zero unclassified clauses | — | — | — | — |

**A2–A5 are independent and batch concurrently.** A6 is the barrier (it needs all four).

### Gate B — the scaling primitive + the crux probe (steps 19–38, ~2 weeks)

| # | Increment | Steps | Gate | Depends | Verify-in-batch |
|---|---|---|---|---|---|
| B1 | **Crux probe (A2):** hand-compile 3 real guideline sentences → `ObjectiveRef` + `Constraint`. Report what breaks. | 2 | A | A7 | the 3 compiled artifacts, inspected — not just "it worked" |
| B2 | `aigov/contract.py` — `DepartmentSpec` + sub-types + enums | 3 | A | A8, B1 | import it; instantiate one spec by hand |
| B3 | Reference spec `aigov/specs/d1_lifesupport.py` (HIGH legitimacy) | 2 | A | B2 | validates clean |
| B4 | Reference spec `aigov/specs/d2_economy.py` (LOW legitimacy) | 2 | A | B2 | validates clean; **H1 answered** |
| B5 | `validate()` invariants I1–I5 (objective provenance, reversibility, bilateral coupling, gaming model, fail-closed) | 4 | A | B2 | each triggers individually |
| B6 | `validate()` invariants I6–I10 (mutation-proof, sunset, **I8 subsidiarity**, role separation, Fuller linter) | 5 | A | B5, A3 | I8 is the risky one — **H2 answered here** |
| B7 | `tests/test_contract.py` + `tests/test_contract_mutations.py` — one mutation per invariant | 4 | A | B6 | mutations REJECTED, clean specs ACCEPTED; inspect messages |
| B8 | Port the `Mars_Governance` organ into `aigov/choice/`; confirm **193/193** from the new root | 3 | A | A1 | run the suite; compare counts to the 2026-08-11 baseline |
| B9 | Charter invariants for the four non-negotiables + the fraction-measuring test; record the number | 3 | A | A8, B6 | the measured fraction goes in the ledger, not prose |
| — | **Gate B exit test:** `aigov-dept-contract` MVP bar (6/6) + `aigov-constitution` bar (4/4) green | — | — | — | — |

**B1 runs FIRST despite low rank-order** — it is the highest-information move in the plan (crux A2) and can
reshape B2's schema. Spending two steps before the contract is far cheaper than rewriting it in week 3.
**B8 is independent of B1–B7 and batches with them.**

### Gate C — the world (steps 39–50, ~2 weeks)

| # | Increment | Steps | Gate | Depends | Verify-in-batch |
|---|---|---|---|---|---|
| C1 | `aigov/twin/` — wrap `resource_sim` behind the contract's `StateVar` interface | 3 | A | B3, B7 | twin ticks; state vars readable |
| C2 | Extend the twin: population, labor, pressurized-volume + radiator-area inventory | 4 | A | C1 | inventory totals sane vs the roadmap envelope |
| C3 | Baseline reproduction test: twin vs the reused ECLSS/analog figures within stated tolerance | 3 | A | C2 | **inspect the numbers**, not just the assertion |
| C4 | Seed families `aigov-twin`, `aigov-guideline-intake`, `aigov-collective-choice` (self-init, 3 slots) | 2 | A | Gate B | `Account.report()` live_count = 7/25 |
| — | **Gate C exit test:** baseline reproduction passes at a tolerance recorded in the ledger | — | — | — | — |

### Gate D — the kernel + three departments (steps 51–68, ~2 weeks)

| # | Increment | Steps | Gate | Depends | Verify-in-batch |
|---|---|---|---|---|---|
| D1 | `aigov/kernel.py` — one cycle: guideline → options → simulate → menu → ratify → apply → audit | 5 | A | B7, B8, C3 | run one cycle end to end; read the trace |
| D2 | Wire the ratify-gate: **no apply without (ratified ∧ certified-non-steering ∧ constraint-satisfying)** | 3 | A | D1 | negative test: unratified action REFUSED |
| D3 | D1 Life-Support department instance (HIGH) | 3 | A | C3, B3 | closed loop respects physical bounds |
| D4 | D2 Economy department instance (LOW): volume/area LVT-analogue + Pigouvian O₂/water pricing | 4 | A | C2, B4, A4 | **compute the yield vs the public-goods bill (H4)** — a number, not a claim |
| D5 | D3 Collective-Choice department binding (the ported organ as the sovereign channel) | 3 | A | B8, D2 | ratify path exercised |
| — | **Gate D exit test:** one full cycle across all three departments, all three legitimacy ratings exercised | — | — | — | — |

### Gate E — the checks (steps 69–74, ~1 week)

| # | Increment | Steps | Gate | Depends | Verify-in-batch |
|---|---|---|---|---|---|
| E1 | D15 audit organ (independent verifier) + D13 arbitration for the D1↔D2 volume/power contention | 4 | A | D5 | arbitration resolves a real contention; audit is structurally independent |
| E2 | Adversarial suite: agenda reordering (W5), metric gaming (W9), preference falsification (Kuran), emergency abuse, capture | 2 | A | E1 | **every attack ends in detection or escalation** — a silent pass is a FAILURE, not a pass |
| — | **Gate E exit test:** zero silent successes across the adversarial suite | — | — | — | — |

### Gate F — terminal (steps 75–78)

| # | Increment | Steps | Gate | Depends | Verify-in-batch |
|---|---|---|---|---|---|
| F1 | Integrated run: ≥12 cycles, ≥3 departments, adversarial load, on the twin | 2 | A | E2 | read the run log; confirm cycle count and per-cycle certification |
| F2 | Reproducibility: whole suite green from a clean checkout | 1 | A | F1 | run it |
| F3 | Assert phase-1 terminal mechanically → **REQUEST USER SIGN-OFF** (never auto-declare) | 1 | A | F2 | — |

---

## 3. Optimization notes (what `optimize_plan` would do to this)

- **Batched (independent, run concurrently):** {A2, A3, A4, A5} · {B1, B8} · {B3, B4} · {D3, D4} — four batch
  points, ~11 steps of wall-clock saved.
- **Reordered against rank:** B1 (crux probe) promoted ahead of B2 despite lower VOI *rank*, because its
  information arrives before the artifact it would invalidate. Rank orders value; **sequencing orders regret.**
- **No irreversible steps.** Zero `R`, zero `G`, zero `$` in phase 1. The plan is entirely local reads/writes/tests.
  If that changes (e.g. publishing a memo, provisioning a paid API), the gate table applies and the step pauses.
- **Rollback:** every step is a local file write inside a git repo. Rollback = `git restore`. No step needs a
  rollback plan beyond that.

---

## 4. Risk register (plan-level, with the step that retires each)

| # | Risk | Retired by | If it fires |
|---|---|---|---|
| R1 | **Guidelines don't compile (A2 false)** — the governor becomes decorative | **B1** | Project reshapes: guideline-intake becomes the primary family, kernel shrinks to an advisory tool. Cheap at step 20; catastrophic at step 60. |
| R2 | **I8 not mechanically checkable (H2 false)** — subsidiarity degrades from enforced to audited | B6 | Say so explicitly; downgrade the claim from "enforced" to "audited". Do not hide it. |
| R3 | **Departments not separable (A1 false)** | B3+B4 | Fall back to a single coupled model with declared sub-systems; the "department" framing becomes presentational and must be relabelled. |
| R4 | **LVT-analogue doesn't fund the bill (H4 false)** | D4 | Fiscal fork K3 reopens; the economy department's instrument set changes. Recorded as a falsified hypothesis, not patched. |
| R5 | **Adversarial suite too weak to mean anything (A6)** | E2 | State the limitation in the terminal report. Synthetic adversaries are weaker than real ones — that boundary is permanent and must not be softened. |
| R6 | **Theater** — artifacts accumulate without falsifiable content | I6 + every verify-in-batch column | The whole plan's structural defence; if it fires anyway, the plateau rule applies: re-aim, don't produce another doc. |
| R7 | **Charter clauses mostly unenforceable (H1 false)** | B9 | The measured fraction is the finding. A low fraction is a *result*, and the honest claim shrinks to match it. |

---

## 5. What this plan explicitly does NOT deliver

Named so scope cannot silently inflate:

- **No real-world deployment, no real citizens, no legal validity.** Everything is simulation.
- **No claim of "governance-validated".** Per inherited `mars-governance` D7, every phase-1 result is
  **model-coherent**, not governance-validated. Stage B (human field test) and Stage C (formal verification)
  are outside this plan.
- **No city / nation / world scale.** `aigov-scale-gates` is deferred to phase 2.
- **Only 3 of 16 departments.** The other thirteen are additive under the contract — which is the entire reason
  the contract is built before any department.
- **No AI sovereignty.** Under the drafted Fork 1, the governor never selects an objective, never amends its
  constraints, never holds the exception. If the user ratifies otherwise, this plan is void and must be redrawn.
