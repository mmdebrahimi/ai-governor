# Result - soraya --advance, 2026-08-11 (second run)

## Landed
**Adversarial suite F10** (`tests/test_adversarial_kernel.py`, 28 tests). Written to MAP the
kernel's perimeter, not to assert a wall: 12 named attacks, each RUN, outcome recorded. Attacks
that succeed are pinned as named residuals with reasons, and `test_no_attack_succeeds_undocumented`
fails if any attack succeeds without being on that list.

**Scoreboard: 9 of 12 stopped, 3 pinned open.**

## Two live defects found and closed
1. **A3 - ratifier-alias evasion.** `RatificationRecord.is_genuine` compared the whole string
   against five literals, so `"the governor"` and `"governor-office"` passed as genuine ratifying
   bodies. The machine could ratify its own action by giving itself a slightly longer name. Now
   token-matched, deliberately over-inclusive.
2. **A11 - lethal status quo accepted.** The D16 vacuous pass RETURNING THROUGH A DIFFERENT DOOR.
   D16 was fixed by deriving a survivable DEFAULT status quo, but nothing validated one handed in
   through the constructor: the kernel refused every action correctly, reported a clean fully-gated
   run, and lost the atmosphere at cycle 1. Now `InvalidStatusQuoError`.

## Three residuals PINNED (not closed)
- **A8** post-admission mutation - validation is one-shot AND `Governor` holds the caller's specs by
  reference. Proven accidentally when the suite's own tests cross-contaminated.
- **A9** subsidiarity relabel - I8 reasons over the DECLARED InstrumentClass.
- **A10** profile laundering - I13 reasons over the DECLARED ClassificationBasis. The MEANING
  channel; the most dangerous of the three because nothing downstream can detect it.

All three are the same shape: **author-declaration evasions**. Closing them needs behavioural
classification, not declaration checks.

## A third defect, in a binding-path number (found, NOT fixed)
The intake's polarization tolerance 0.900 was DERIVED at panel_size=16 and is applied as a
CONSTANT. Measured at 600 trials x 4 seeds, `unimodal_p95` falls monotonically with panel size:

| n | unimodal_p95 (4 seeds) | best separating threshold |
|---|---|---|
| 8 | 0.920-0.940 | 0.910-0.935 |
| 12 | 0.873-0.890 | 0.875-0.905 |
| 16 | 0.845-0.863 | 0.880-0.885 |
| 50 | 0.794-0.804 | 0.815-0.830 |

- **n=8:** the fixed threshold sits BELOW unimodal p95, so >5% of genuinely unimodal panels
  false-escalate. Fail-closed, so the SAFE direction.
- **n=50:** the best threshold is ~0.82, well below the fixed 0.900, so the fixed value escalates
  LESS than optimal - **missed escalations, the UNSAFE direction**.

Not fixed here: it changes a parameter on the binding path, which is a design decision.

## Ledger truth restored
`--refresh-frame` REFUSED with schema-drift: the umbrella was missing its
`### Current state (one-line summary)` heading - which is exactly WHY the frame silently went
stale, since no op could reach it. Repaired, then refreshed. The prior text was materially false
("88 tests green", "No kernel, no twin, no departments beyond the two reference specs").

## Measured
root **219 -> 247** (+28), 0 regressions; vendored organ **193/193**; both hardenings
mutation-proved; `kernel.py` restored byte-identical after mutation testing.
