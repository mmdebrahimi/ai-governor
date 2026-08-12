# Audit trail - soraya --advance, 2026-08-12 (polarization threshold + V15)

Gate mode money-only; every step `auto`. Pre-planned ~30 steps, ran ~28.

## Why this target
A four-model heterogeneous panel - the obvious follow-on from the V15 research - requires paid API
access, which is a MONEY action and a hard gate. So the run re-aimed to the highest-VOI move that is
free and code-closable: the polarization threshold defect, outstanding across three prior runs and
sitting in the UNSAFE direction.

| # | Step | Outcome |
|---|---|---|
| 1 | Lock + locate the threshold | one constant, two call sites |
| 2 | Measure derivation cost + seed stability | 0.13s/derivation; best_threshold swings 0.880-0.900 across seeds at n=16 |
| 3 | Design: derive per panel size, median over 5 fixed seeds | single-seed noise would otherwise enter the binding path |
| 4 | Ordering bug (my own) | block referenced MIN_CAMP_SHARE + calibrate_polarization before definition; moved |
| 5 | Verify across sizes | 0.975 (n=4) -> 0.800 (n=100), monotone |
| 6 | **Trace the live path** | tolerance_for called 4x at n=16 - the derivation IS live, not bypassed |
| 7 | Find a real panel where the fix changes behaviour | two-camp panel, gap 5.89 vs spread 1.55, score 0.853 |
| 8 | 17 tests + 2 fixture bugs of my own | Panel signature, LevelElicitation field name |
| 9 | Mutation proof + regression | mutant RED; root 300; organ 193/193 |
| 10 | V15 research memo | the persona/council findings, durable |

## Honest note
The defect was LATENT, not active: the only live panel is n=16, the exact size the constant was
derived at. It would have bitten the moment anyone changed panel size. That is also why three prior
runs could defer it without anything breaking.

## Terminal
Next moves are the real decision-inventory session (needs the user) and a live multi-model panel
(needs money). Both hard stops.
**terminal_reason: remaining frontier is user-input-bound or money-gated.**
