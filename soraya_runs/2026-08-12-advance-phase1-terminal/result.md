# Result - soraya --advance, 2026-08-12

## 1. Everything is backed up (recommendation 1)

Two commits pushed to `github.com/mmdebrahimi/ai-governor`: `676b1c3` (six increments that existed
only on this disk) and `4ff1f91` (this run). The repo previously had ONE commit and 38 uncommitted
files on a machine with 15 GB free.

Privacy-scanned before pushing, because the repo is public: no family composition, no capital
position, no property holdings. Only hits were the local machine path and the already-public
GitHub handle.

## 2. The ledger tells the truth again (recommendation 2)

The frame was ~3 weeks stale and the ranking tool reads it. Corrected against LIVE numbers:

| | ledger said | actual |
|---|---|---|
| root tests | 247 | **402** |
| invariants | I1-I14 | **18** (I1-I15 + I8'/I8b/I8c) |
| charter | 30 clauses, 0.7667 | **32 clauses, 0.78125** |
| adversarial | 12 attacks, 3 residuals | **14 attacks, 1 residual (A10)** |

I also corrected MY OWN prior report, which said 38 clauses. The IDs run C01-C25 then C32-C38 -
non-contiguous, 32 total.

## 3. D3 exists, and phase 1 is NOT closed (recommendation 3)

**Built:** the MEDIUM-legitimacy department, anchored on ratified guideline G-P-001 - *people should
be free to invent things without a committee deciding what is worth inventing.*

That sentence is what makes it MEDIUM rather than HIGH. The colony may centrally schedule a scarce
machine; it may not centrally rank the proposals competing for it. So D3 allocates machine-hours by
published-seed lottery among the safety-qualified, discretion sits with the draw rather than any
officer, and `project_value` is declared **LATENT** - the worth of an unbuilt invention is exactly
what no central body can observe. It receives **no objective at all**: its job is a procedure that
stays honest, not a level to hit. That makes it structurally different from D1 (physical floor) and
D2 (fiscal target), which is why it is worth having as the third department.

Validated clean on the first attempt. 12 cycles run across the full HIGH/MEDIUM/LOW span.

**Two things the run taught that reading could not:**

**(a) The kernel refused the first three-department registry.** I3 requires bilateral couplings and
I had declared contention only from D3's side. The admission gate did its job. Fixing it revealed
something real: a coupling list is a property of a department IN A COMPOSITION, not of the
department alone - a D3-aware D1 is *invalid* in a colony without D3. New `aigov/registry.py`
composes both worlds explicitly; both validate.

**(b) THE CORRECTION. Phase 1 is not one department away, and I said it was.**

`applied` was **0** across all twelve cycles, and **D3 proposed nothing**. `Governor.propose` is a
stub hard-coding two instrument names; `CERTIFIABLE_INSTRUMENTS` holds exactly one. So the
three-department run exercises D3's CONTRACT but not its BEHAVIOUR, and every other action is
refused out-of-domain.

The remaining phase-1 gap is **the proposal layer and the non-steering certification domain** - not
another department. Both are pinned as tests that ASSERT THE DEFECT, to be inverted rather than
deleted, because a green suite over a silent department is the vacuous pass this codebase keeps
catching.

## Deliberately not done

Extending the certification gate to cover D3. It would have made this look like phase-1 completion.
The foundations rule is to certify only inside the domain where the property is faithful; widening
a safety gate so a run reads as finished is the theater the project exists to prevent.

## Measured

root **383 -> 402** (+19), organ **193/193**, 0 regressions. Two commits pushed.

## My own errors

- Said 38 charter clauses; it is 32.
- An `__import__` hack instead of a real import; caught on reread.
- Statically mirrored D3's coupling into D1, silently invalidating the two-department registry six
  test files use. Caught by running the baseline, not by the suite.
