# Result - soraya --advance, 2026-08-12

## Closed: the polarization threshold (outstanding across 3 runs)

The intake escalates to deliberation when a panel is genuinely two camps rather than silently
averaging them. That decision used ONE threshold (0.900), derived at panel_size=16 and applied to
every panel size.

That is a scope error, not a judgement call. The score is computed over n points, so with fewer
points a 2-means split fits noise more easily and the unimodal score distribution shifts upward as n
falls. Measured, median over 5 fixed seeds:

| n | derived tolerance | vs the fixed 0.900 |
|---|---|---|
| 4 | 0.975 | too tight - false-escalates (safe direction) |
| 8 | 0.910 | too tight |
| 12 | 0.900 | same |
| 16 | 0.895 | ~same (its own calibration size) |
| 24 | 0.850 | **too loose** |
| 50 | 0.825 | **too loose** |
| 100 | 0.800 | **too loose - MISSES real polarization** |

Above n=16 the constant escalates LESS than it should. That is the UNSAFE direction: a split panel
gets aggregated into a median sitting in the empty gap between the camps - a binding number nobody
proposed.

**Fix:** `tolerance_for(panel_size)` derives at the size in use; `elicit_level` resolves from
`len(panel.members)` by default; an explicitly-passed tolerance still pins. Below
`MIN_CALIBRATABLE_PANEL` (= 4, DERIVED from MIN_CAMP_SHARE, not chosen) no threshold exists, so the
mechanism ESCALATES rather than falling back to a default.

## Verified behaviourally, not just numerically
Found a genuinely two-camp panel - camps separated by 5.89 against a within-camp spread of 1.55 -
scoring 0.853. The old constant **aggregated** it; the derived threshold **escalates** it. Pinned as
a test that reproduces the panel deterministically rather than hard-coding it.

## Still no invented number
The value is the MEDIAN `best_threshold` over 5 fixed seeds (a single seed carries ~0.02 of noise,
measured 0.880-0.900 at n=16). Provenance stays GUIDELINE - so intake invariant G2 still passes - and
records the seed spread rather than hiding it.

## Why it was never caught
The only live panel in this repo is n=16 - the exact size the constant was correct for. The defect
was LATENT, not active, which is also why three prior runs could defer it with nothing breaking.

## Also landed
`research_outputs/aigov-v15-persona-panels-and-model-diversity.md` - the persona-database and
expert-council research, with the headline that persona prompts change style but not judgment, model
heterogeneity is the real decorrelation lever, and interviews beat personas (85% vs 74%).

## Measured
root **283 -> 300** (+17), 0 regressions; organ **193/193**; mutant reverting to the constant turns 2
tests RED; `intake.py` restored byte-identical. Suite time **2.5s -> 19s** - the derivations are real
computation, not free.

## Honest limits
- Derivation is simulation-based. It calibrates against SIMULATED unimodal and two-camp panels; a
  real assembly may not match those generators.
- The residual class overlap is real: a weakly-separated two-camp panel genuinely resembles a wide
  unimodal one, and no threshold separates them cleanly.
- Two test-fixture bugs of my own this run (Panel signature, field name). Neither reached src.
