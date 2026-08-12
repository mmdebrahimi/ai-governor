# Audit trail - soraya --advance, 2026-08-11 (adversarial suite + portfolio truth)

Gate mode money-only; every step classified `auto`. Pre-planned ~30 steps, ran ~38 (self-extended
once, at the point the adversarial suite started finding live defects - noted here, not silent).

## Correction to the previous run's step-4 claim
Last run reported "every family's next_action is a seeding-era action already completed". That was
TOO STRONG. It held for the two TOP-RANKED families (constitution, dept-contract) but NOT across
the portfolio: kernel, twin, guideline-intake and foundations all carried genuinely live
candidates. The stale data was at the top of the ordering, not throughout. Corrected in-run.

| # | Step | Outcome |
|---|---|---|
| 1 | Lock + rank | 7 eligible / 0 blocked; inspected all 7 candidate tables directly |
| 2 | Pick kernel #2 (adversarial suite, F10) | highest-VOI live candidate; also stress-tests last run's invariants |
| 3 | PROBE 5 attacks against the real kernel before writing any test | 5 outcomes measured, not assumed |
| 4 | Close A3 (ratifier-alias evasion) | `is_genuine` was exact-match on 5 strings; `the governor` / `governor-office` passed. Now token-matched |
| 5 | Close A11 (lethal status quo accepted) | new `InvalidStatusQuoError`; the supplied status quo is now probe-ticked like any proposed action |
| 6 | Write the adversarial suite | 12 named attacks, 28 tests; residuals PINNED with reasons |
| 7 | Suite found a test-isolation bug in ITSELF | `Governor` holds specs BY REFERENCE, so A8's mutation leaked into A10. Recorded as part of residual A8 rather than papered over |
| 8 | Mutation proof on both hardenings | revert A3 -> 3 RED; remove A11 check -> 1 RED; source restored byte-identical |
| 9 | `--refresh-frame` REFUSED: schema-drift | the umbrella was MISSING `### Current state (one-line summary)`. The op refusing to auto-fix is correct behaviour |
| 10 | Repair heading, then refresh frame | current state was materially FALSE ("88 tests green", "No kernel, no twin") |
| 11 | Spillover: guideline-intake #3 (threshold re-derivation) | DEFECT found - the 0.900 tolerance is panel-size dependent and applied as a constant |
| 12 | Full regression | root 247, organ 193/193 |

## Terminal
Re-aimed twice within the run (kernel -> ledger truth -> intake calibration). Stopping because the
remaining moves are (a) an AUTHORITY fork, (b) a USER-INPUT-BOUND probe, and (c) a binding-path
parameter redesign that should be decided, not rushed at the end of a long run.
**terminal_reason: two hard stops + one deliberately deferred design decision.**
