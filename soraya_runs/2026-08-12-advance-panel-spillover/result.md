# Result - soraya --advance, 2026-08-12

## Closed: the chaining defect that was producing wrong answers

`aigov/decisions.py` derived structure by computing CONNECTED COMPONENTS over "shares at least one
information need". Two consequences, both confirmed by running it:

- A-B share a fact and B-C share a different one, so A and C landed in the same unit while sharing
  NOTHING. Four decisions - refinance, renovate, pick contractor, contractor bonus - collapsed into
  one.
- Cheap facts grouped as hard as tacit ones: "should we acquire this building" and "can we run
  payroll Friday" merged on a shared cash balance, a number in a spreadsheet.

And a test PINNED the chaining as correct, with a docstring arguing for it.

## What replaced it

Grouping now runs over ELICITED affirmed pairs, and a group becomes a capability only if it is
COMPLETE - every internal pair independently affirmed. A merely-connected group is not a smaller
capability; it is not a capability at all, and comes back under HUMAN GROUPING REQUIRED.

`FactKind` gates which pairs are even worth asking about: TRANSFERABLE_RECORD (written down - shared
data, not shared context) proposes nothing; ORGANIZATION_SPECIFIC_CONTEXT and TACIT_CONTEXT do.

No clique enumeration - it is exponential in the worst case and bounding it would need a constant
nobody ratified. Checking whether an already-formed component is complete is O(pairs).

## Verified by RUNNING, on the exact scenario that exposed the defect

| | before | now |
|---|---|---|
| pairs the user is asked about | n/a (never asked) | 6 total -> **2 candidates** |
| contractor-bonus decision | dragged into the merged unit | **excluded** - its only fact is a transferable record |
| A/B/C with A-B and B-C affirmed | one department | **HUMAN GROUPING REQUIRED**, "never affirmed: A+C" |

Mutation-proved: disabling the completeness check turns the chaining guard RED. `decisions.py`
restored byte-identical afterwards.

## Also landed (spillover)

**ASSURANCE split from SOURCING.** Consequence drives how hard a decision is CHECKED, never who
holds the capability - brain surgery is high-consequence and still bought. This closes the third
instance of the module's recurring defect: `reversibility` was elicited, asked about, documented as
a question that "changes the answer", and fed nothing.

On a real inventory it produces something the old model could not express: "do we sell the north
parcel?" comes out MARKET on price and still demands INDEPENDENT_REVIEW by someone independent of
the SUPPLIER - i.e. not the broker earning the commission.

`stake_per_decision` is deliberately not consulted; turning money into a level needs a cutoff nobody
ratified.

**ATOMICITY gate.** A decision the user declares compound gets NO verdict - "manage financing" and
"should we offer 1.2M for 123 Main St" are both legitimate English and produce completely different
structures from the same enterprise. Ordering is pinned: fully-answered cost fields do not rescue a
malformed question.

**Accountability is a ROLE slot**, applied to every decision including MARKET ones, never a person's
name. A test pins that no `owner`/`person`/`assignee` field exists - the repo is public.

## Deliberately NOT built

Item 6 (decision specificity, advisory-only). An elicited field feeding no verdict is the exact
defect shape found twice in this module already. Adding a third on purpose would repeat a known
mistake. If specificity is worth asking, it has to drive something.

## Measured

root **350 -> 383** (+33; `test_decisions` 26 -> 59), organ **193/193**, 0 regressions.
`DerivedDepartment`, `derive_departments` and `report.departments` are gone from the public surface,
pinned by a test - renaming the class alone would have left the defect at the API boundary.

## Honest limits

- The pair filter cannot see a coupling between decisions sharing no RECORDED fact but turning on
  the same unwritten context. Reported, not hidden; the user can add a pair by hand.
- Completeness of the inventory is still unsolved, and now correctly BLOCKED rather than closed
  badly: the coverage-lens criterion was found insufficient by the two-seat panel this session.
- Two errors of my own this run - a vacuous `or True` assertion, and the Coase direction backwards
  in a verification fixture for the second time this session.
