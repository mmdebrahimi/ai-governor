# Audit trail - soraya --advance, 2026-08-11 (decision inventory)

Gate mode money-only; every step `auto`. Pre-planned ~35 steps, ran ~30.

| # | Step | Outcome |
|---|---|---|
| 1 | Lock + classify | all `auto` |
| 2 | Settle the owed Pending Decision 5 | RESOLVED prefix + Decisions Made breadcrumb + Action Log mirror |
| 3 | Build `aigov/decisions.py` | Coase verdict + Galbraith clustering + interview generator |
| 4 | **RUN it on a realistic partial farm inventory** | live defect found (see below) |
| 5 | Add `Sourcing.HYBRID` | private information now DRIVES the verdict instead of annotating it |
| 6 | Re-run + inspect | derivation now produces a non-obvious, defensible structure |
| 7 | 26 tests | incl. exact-boundary (no invented threshold) + traceability pins |
| 8 | Own fixture bug found | had the Coase direction backwards in the test helper; fixed |
| 9 | Mutation proof + full regression | mutant RED; root 283; organ 193/193 |
| 10 | Protocol runbook | docs/decision-inventory-protocol.md |

## The defect (step 4), because it is the point of running things
`private_information` was recorded, printed as a "degraded" note, and then had ZERO effect on the
verdict. Three of four buyable decisions came out MARKET despite depending on knowledge no outsider
could acquire. A declared field nothing acted on - this codebase's recurring failure shape, found
again by RUNNING rather than testing. It was also wrong on the theory: Williamson has asset
specificity DRIVING internalization, not annotating it.

## Terminal
The instrument is built and verified; it now needs the user's real answers to produce a real
inventory. That is user-input-bound, not code-closable.
**terminal_reason: instrument complete, next step needs the user in the room.**
