# Result - soraya --advance, 2026-08-11

## What landed
Five V14 research findings converted from memo prose into **enforcing, individually-triggerable
contract invariants**, wired to charter clauses, and enforced at the runtime boundary.

| Invariant | What it refuses |
|---|---|
| **I4'** | a target metric that is undeclared, or unassessed for ratchet / threshold exposure |
| **I8b** | an allocative instrument that does not name its discretion tier + capture check |
| **I12** | a person classification with no accountable human, no redress, subject-side burden of proof, or cited AS the justification |
| **I13** | a classification derived from resemblance to a prior adverse case |
| **I14** | a department that can act without having assessed whether incremental action is safe |

## Two real defects found by RUNNING, not by reading
1. **D2 was scored on a metric it never declared.** Its objective targets
   `volume_per_person_m3`; its `metrics` list contained only `revenue_coverage` and
   `effective_progressivity`. The two measures carrying gaming models were the two nobody judged
   the department against. Caught by I4' on first execution.
2. **The kernel enforced none of the contract.** `validate` existed and fired, but nothing at the
   runtime boundary called it. A registry with 6 violations - including a profile-by-resemblance
   classification with no accountable human and no redress - constructed happily and proposed two
   actions. Closed with `InvalidRegistryError` at admission.

## Measured
- root suite **185 -> 219** (+34), 0 regressions
- vendored organ **193/193** preserved
- charter checkable fraction **18/25 = 0.72 -> 23/30 = 0.7667**, integrity errors 0
- mutation proof: no-op `validate` -> **16 of 30** V14 tests RED; the 14 survivors are exactly the
  boundary tests that assert NO error (correct shape). Source restored byte-identical.

## Honest limits
- The fraction ROSE only because each clause shipped with an executable check. A clause added as
  prose moves it DOWN, as C25 did. That asymmetry is the point of measuring.
- I12/I13 are enforced over DECLARED person classifications. A department that classifies people
  without declaring it is not caught - same residual class as I8's author-declared InstrumentClass.
- The reserved ids C26-C31 are deliberate: V13's disclosure block is already cited as "C29" in the
  ledger and the anchor, and renumbering would break live references.

## Not resumable from here
Next moves are an authority fork and a user-input-bound probe.
