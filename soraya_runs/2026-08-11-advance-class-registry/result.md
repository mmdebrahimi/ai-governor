# Result - soraya --advance, 2026-08-11 (ratified vocabulary)

## The shape of the fix
Two pinned residuals had the same shape: **an invariant that reads a label the author chooses is not
a control over the author**. Deciding whether a computation "really is" a price or a resemblance is
a semantic property of a program and undecidable in general (Rice), so the fix is not to detect the
lie - it is to take the field away from the author. The department now names a **key**; a ratified
vocabulary owns what the key means.

## Closed this run
| Attack | Was | Now |
|---|---|---|
| **A8** post-admission mutation | RESIDUAL | **DETECTED** - deep-copy at admission (aliasing) + per-cycle re-validation (one-shot) |
| **A9** subsidiarity relabel | RESIDUAL | **DETECTED** - instrument catalogue fixes the class (I8c) |
| **A13** unratified rule-target class | new | **DETECTED** - I15 |
| **A14** self-issued vocabulary | new | **DETECTED** - vocabulary integrity |

**Adversarial scoreboard: 13 of 14 stopped, 1 residual.**

## Still open, and deliberately so
**A10 (profile laundering) is NOT closed** - and this is a design decision, not an oversight. The
mechanism now exists: `VocabularyKind.PERSON_CATEGORY` is declared, and `integrity_errors` REFUSES
any entry under it. Populating that registry is a ratification decision belonging to the polity, not
to the machinery. A dormant people-sorting capability that fails closed is the safer shape than one
with a permissive default, and the first real deployment is operational (parcels, plantings, yields)
rather than people-sorting anyway.

So the honest statement is: **A10's mechanism is built and fail-closed; its authority is not
Soraya's to supply.**

## What was deliberately left undecided
The vocabulary is a DISTINCT artifact - not a sixth `GuidelineType` (which would assert that probe
B1's empirically-derived P/O/F/D/A partition was incomplete) and not a charter clause (which would
stretch the charter from prohibitions-on-the-machine into descriptions-of-the-world). It carries its
own `ratified_by` and records who ratified rather than inventing an answer. If the polity later
decides a vocabulary is legislative or constitutional, it re-homes without rework.

## Measured
- root suite **247 -> 257** (+10), 0 regressions; vendored organ **193/193**
- charter **0.7667 -> 0.78125** (25/32), integrity errors 0 - and both new clauses were added ONLY
  after their invariants fired mechanically, which was an explicit condition set in review
- 4 mutation proofs, each RED: remove I15 / revert deep-copy / remove per-cycle re-validation /
  remove I8c. All sources restored byte-identical.
- live registry validates clean against the vocabulary (0 errors)

## Honest limits
- I15/I8c bind at **authoring time when a vocabulary is supplied, and always at the kernel boundary**.
  A `validate()` call with no vocabulary skips them - deliberate, so authoring stays usable before a
  vocabulary exists, but it means the runtime boundary is where the guarantee lives.
- The catalogue closes relabelling for **catalogued** instruments and **invention** of new ones. It
  does not verify that a catalogued instrument's implementation matches its definition - that would
  be the undecidable problem, and nothing here pretends to solve it.
- A bare `propose()` is not re-validated. Pinned as a boundary test; if propose ever gains the power
  to apply, that boundary must move.
