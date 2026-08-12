# Audit trail - soraya --advance, 2026-08-12 (recommendations executed)

Execute-mode directive: "move forward with the recommendations and use your best judgement".
Gate mode money-only. Pre-planned ~60 steps; ran ~85.

## The three recommendations, in order

| # | Recommendation | Outcome |
|---|---|---|
| 1 | Commit + push the 38 files | DONE - privacy-scanned first, then 676b1c3 pushed |
| 2 | Refresh the stale ledger frame | DONE - and refreshed a SECOND time after finding #3 falsified it |
| 3 | Build the MEDIUM department, close phase 1 | PARTIAL - department built and valid; phase 1 NOT closed, reason below |

## Step log

| # | Step | Outcome |
|---|---|---|
| 1 | Lock + run dir | acquired |
| 2 | Privacy scan (repo is PUBLIC) | clean - only local machine path + already-public gh handle |
| 3 | Verify repo boundary | AI_Governor is its OWN repo on main; all 38 files in scope |
| 4 | Commit + push | 9762406..676b1c3 |
| 5 | Live-number check for the frame | found MY OWN report wrong: 32 clauses, not 38 |
| 6 | Frame refresh #1 | 247->383 tests, I1-I14->18 invariants, 30->32 clauses, 12/3->14/1 attacks |
| 7 | Read I8 / I8b / I15 / I8c / I5 / I4' | MEDIUM permits allocation; load moves to I8b |
| 8 | Pick the anchor guideline | G-P-001 - binding, and forbids ranking proposals |
| 9 | 4 ratified vocabulary entries | I8c/I15 satisfied; integrity clean |
| 10 | Write D3 | validated CLEAN first attempt, 0 errors |
| 11 | Fix my own `__import__` hack | replaced with a real import |
| 12 | **Kernel REFUSED the 3-dept registry** | I3: unmirrored coupling. The admission gate working. |
| 13 | Mirror in D1 -> broke the 2-dept registry | I3 rejects a reference to an absent department |
| 14 | New `aigov/registry.py` | couplings are relative to a COMPOSITION; both worlds valid |
| 15 | **Run 12 cycles and INSPECT** | applied=0; D3 proposed NOTHING |
| 16 | Diagnose | `propose()` hard-codes 2 instrument names; CERTIFIABLE_INSTRUMENTS holds 1 |
| 17 | 19 tests incl. 2 assert-the-defect pins | 402 root / 193 organ, 0 regressions |
| 18 | Frame refresh #2 + ledger rows 51-52 | corrected the claim I made in refresh #1 |
| 19 | Commit + push | 676b1c3..4ff1f91 |

## The correction that matters

In the state analysis I told the user phase 1 was "one missing piece away" and that the MEDIUM
department was "the only thing standing between here and a finished phase 1". That was WRONG, and
running the thing is what showed it. The department was necessary; it was nowhere near sufficient.

`Governor.propose` is a stub hard-coding `crop_area_allocation` and `volume_tax_rate`. D3 therefore
proposes nothing, and the three-department run exercises D3's CONTRACT but not its BEHAVIOUR.
`CERTIFIABLE_INSTRUMENTS` holds one instrument, so everything else is refused out-of-domain and
`applied` was 0 across all twelve cycles.

Both are pinned as tests that ASSERT THE DEFECT, with instructions to invert rather than delete.

## What I deliberately did NOT do

Extend the non-steering certification gate to cover D3's instruments. It would have made the
numbers look like phase-1 completion. The foundations rule (V1) is to certify only inside the
domain where the property is faithful, and widening a safety gate so a run looks finished is
precisely the theater this project exists to avoid. Named as the next real design increment.

## My own errors this run

1. Reported 38 charter clauses in the state analysis; the real count is 32 (IDs are non-contiguous,
   C01-C25 then C32-C38). Corrected in the frame and to the user.
2. Wrote an `__import__(...)` hack for RatificationClass instead of importing it. Caught on reread.
3. Mirrored D3's coupling into D1 statically, which silently invalidated the two-department
   registry every other test file uses. Caught by running the baseline, not by the suite.

## Terminal

**terminal_reason:** the next real move (proposal layer + certification domain) is design work that
should not be rushed at the end of an 85-step run; the alternative moves are user-bound.
**budget_verdict:** within self-budget (~85 of ~100).
