# Audit trail — 2026-08-12-1100-advance-entry-derivation-proof

**Mode:** `/soraya --advance`, bound to the `AI_Governor` project root (invoking cwd has no
`project_state/`). **Planned estimate:** ~12 steps. **Executed:** 16.

| # | step | gate | outcome |
|---|---|---|---|
| 1 | `is_run_active` / `open_run` / `acquire_lock` | auto | clean; run dir under `soraya_runs/` |
| 2 | `advance_ranker.rank` | auto | 1 eligible (`aigov-land-enterprise`), 0 blocked |
| 3 | **Session board consulted** (R4/B, before any plateau call) | auto | 6 live rows; **none owns `AI_Governor`** → no collision, no handoff owed |
| 4 | Coverage probe of `tests/test_decisions.py` | auto | 54 tests, all unit-scale — **largest decision set exercised anywhere is 4** |
| 5 | Record forecast (E1) | auto | predicted: coupling questions >20 → usability wall |
| 6 | Write `tests/test_entry_inventory_endtoend.py` | auto | synthetic fully-answered 18-decision fixture |
| 7 | **Run it** | auto | **3 failed, 5 passed** |
| 8 | Diagnose failure 1 (E02/E06 not HYBRID) | auto | **fixture wrong, code right** — `8x9000 > 55000`, so market was dearer and INTERNALIZE was correct |
| 9 | Diagnose failure 2 (7 pairs, not ≥15) | auto | **expectation wrong, code right** — read `coupling_candidates`: it pairs only over RETAINED (INTERNALIZE/HYBRID) decisions |
| 10 | Diagnose failure 3 (`CouplingRecord` kwarg) | auto | my error; field is `coupled`, not `must_be_made_together` |
| 11 | Fix fixture + rewrite the count test around the real mechanism | auto | test now pins BOTH the naive bound (40) and the actual (7) |
| 12 | Re-run | auto | 8 passed |
| 13 | **Inspect the derivation output** (not just exit code) | auto | see findings below |
| 14 | Score forecast **miss**; consolidate 3 retry-duplicate rows → 1 at the contract path | auto | my own noise from running record/score in separate processes |
| 15 | Full suite | auto | **410 passed** (402 → 410), 0 regressions |
| 16 | 2 × `ce_ledger.append_action`; commit; push | auto / irreversible(reversible=True) | rollback: `git push --force-with-lease origin <prior-sha>:main` |

## What the probe found

At full size, with every cost field answered:

| | |
|---|---|
| sourcing | 10 MARKET · 4 INTERNALIZE · 4 HYBRID |
| assurance | 5 self-check · 9 second-opinion · 3 independent-review · 1 undecidable |
| coupling questions asked | **7** (naive pairwise bound on this fixture: 40) |
| capabilities derived (all pairs affirmed) | 2 |

**The forecast was a MISS, and the miss is the finding.** I predicted a pairwise blow-up making
the coupling stage a usability wall. It does not happen: `coupling_candidates` pairs only over
RETAINED decisions, because you are not asked whether two decisions must be made together when
you have already decided to buy both. MARKET and UNDECIDABLE are excluded at the source. That
prunes 40 → 7 on this fixture. The design already handles the scaling concern; the concern was
mine, not the code's.

**Both derived capabilities are non-trivial.** `{E02, E06, E07, E13}` groups jurisdiction-regime
read, partner diligence, partner rights and partner-claim verification — all coupled by one tacit
fact, "how we read a counterparty from past deals". `{E01, E10}` groups the stability screen with
capital commitment via risk tolerance.

> **Honesty rail on that result:** the fixture is SYNTHETIC. This shows the instrument CAN derive
> a coherent counterparty-judgement capability at full size. It is **not** a finding about the
> user's enterprise, and must not be reported as one.

## Named residual (unchanged from the prior run, still not diagnosed)

`resume_state --cwd .` from this root still returns an unrelated DNA/FBA checkpoint. Flagged, not
fixed, not acted on.
