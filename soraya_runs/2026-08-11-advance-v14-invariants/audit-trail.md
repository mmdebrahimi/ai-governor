# Audit trail - soraya --advance, 2026-08-11 (V14 invariants)

Gate mode: money-only. Every step classified `auto` by `action_gate` (local edits + local tests).
Pre-planned estimate 30 steps; actual ~28. No mid-run extension needed.

## Step 4 note - the code-owned gate was UNINFORMATIVE, and that is itself a finding
`advance_ranker.rank` returned `portfolio_status=ok`, 7 eligible, 0 blocked - but every family's
`next_action` cell was a SEEDING-ERA action already completed ("Write contract.py dataclasses",
"Draft clause list"). The eligibility gate is sound; the candidate-action data feeding it is stale.
Batch selection was therefore MODEL judgment, declared as such rather than dressed up as the
ranker's output.

| # | Step | Outcome |
|---|---|---|
| 1 | Lock + run dir | acquired; `soraya_runs/2026-08-11-advance-v14-invariants` |
| 2 | Ranker + classify planned actions | 7 eligible / 0 blocked; all planned steps `auto` |
| 3 | Add ClassificationBasis, EquilibriumKind, PersonClassification; extend Metric / Instrument / DepartmentSpec | new fields default to "unassessed", so the invariants bite by construction |
| 4 | Implement I4', I8b, I12, I13, I14 in `validate` | each a distinct, individually-triggerable error code |
| 5 | **Run against the LIVE specs** | 10 errors across D1+D2 - all five fire on real content, none on a fixture |
| 6 | Fix D1 (tiers + capture checks + equilibrium) and D2 (the MISSING target metric + equilibrium) | registry back to 0 errors |
| 7 | Write `tests/test_contract_v14_invariants.py` | 30 tests, deep copies of live specs (not toys), each invariant + its boundary |
| 8 | Charter C32-C36 + IMPLEMENTED_INVARIANTS + NON_NEGOTIABLES | fraction 0.72 -> 0.7667 MEASURED; integrity errors 0 |
| 9 | Update count-coupled pin + regenerate docs/charter.md + department-ontology table | pin updated deliberately, with its 4th provenance entry |
| 10 | **Kill-test: does the runtime enforce any of this?** | NO - Governor admitted a registry with 6 violations and proposed from it |
| 11 | Kernel admission gate + `InvalidRegistryError` + 4 tests | closed at the boundary |
| 12 | Mutation proof + full regression | 16/30 red under a no-op validator; root 219; organ 193/193 |

## Verify-in-batch
Not "tests pass". Every invariant was executed against the live registry BEFORE the specs were
fixed (step 5), the kernel gap was found by RUNNING the kernel rather than reading it (step 10),
and the new tests were mutation-proved (step 12).

## Terminal
`--advance` step-8 checklist item (3): remaining candidates are stale/low after a re-rank, and the
next genuinely high-VOI moves are an AUTHORITY fork (the anti-mimicry rail, pending decision) and a
USER-INPUT-BOUND probe (decision elicitation). Banked rather than manufacturing another artifact.
**terminal_reason: re-aimed once (contract -> kernel), then next move is authority/user-bound.**
