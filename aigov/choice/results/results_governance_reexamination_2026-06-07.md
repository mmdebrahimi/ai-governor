# Anti-capture HOLDS in-sim under an EXOGENOUS yardstick — every capture costing citizens > threshold is caught

**Date:** 2026-06-07
**Module:** GOVERNANCE (`Mars_Governance/`) — Earth-deployable Mars governance sandbox (proposal → direct-democracy vote → resource-constrained outcome; AI agenda-advisor kept contestable).
**Model:** existing sandbox, no new model logic. `governance/exogenous_preferences.py` (`exogenous_review`, new `anti_capture_sweep` / `catch_boundary`), wired into `sandbox/governance_sandbox.py::run_advised_cycle`. Tests: `tests/test_exogenous_review.py` (8) + new `tests/test_anti_capture_sweep.py` (7). **Full suite 115/115 green.**

---

## Result

The failure was an **ARTIFACT of an endogenous yardstick**, not a fundamental wall.

The earlier "anti-capture confirmed" result was certified by `option_diversity` + `adversarial_review`, both of which grade the AI advisor's menu against the **same `_utility` / `optimal_cf` surface the advisor used to build it**. That certification is endogenous: a *captured* `_utility` makes the menu "contain the optimum" by construction, the re-tally agrees, and endogenous steering reads **False**. A rigged agenda certified itself fair. That criterion is correctly FALSIFIED.

Re-run with a **structurally independent (exogenous) citizen-preference panel in the loop** — a different functional form (sum of preference kernels), different inputs (elicited ideals/tolerances, not `model.margin`/O2-net), borrowing only the *physical* feasibility filter — the anti-capture property **HOLDS under a defensible, quantified condition:**

> A captured agenda that clears every endogenous gate (diversity + adversarial review) is caught by the exogenous audit **iff the steered winner costs citizens more exogenous satisfaction than the steering threshold.**

The protection radius is set by the threshold, and it is monotone. Sweep (`nominal`, N=200; citizen optimum cf = 0.78):

| Steering threshold | First captured winner CAUGHT (cf) | Displacement from citizen optimum | Citizen-satisfaction cost |
|---|---|---|---|
| 0.05 | 0.81 | +0.03 | 0.082 |
| **0.10 (ratified default, D6)** | **0.82** | **+0.04** | **0.110** |
| 0.15 | 0.87 | +0.09 | 0.151 |
| 0.20 | 0.91 | +0.13 | 0.203 |
| 0.30 | 0.95 | +0.17 | 0.310 |

At every threshold, **gross capture** (winner pushed to the lever extreme cf = 1.0, citizen-cost 0.443) is caught. The endogenous check missed all of it.

## Why it works (the mechanism)

Three layers, each reusing existing code:

1. **Diversity gate** (`option_diversity`) — rejects a menu that omits the optimum or clusters around the status quo. A captor cannot simply *drop* the good option from the ballot.
2. **Whole-grid omitted-option scan** (`exogenous_review`) — and this is the load-bearing part: the audit does not only inspect the menu, it scores the elected winner against **the best feasible option on the entire grid**, including options the captor omitted. So omitting the citizen optimum to dodge the comparison fails — `best_omitted` still finds it (verified: a menu omitting the 0.78 region is caught with `best_omitted = 0.77`).
3. **Independent yardstick** — the comparison utility is the citizen panel's, not the advisor's. A captured `_utility` cannot move it. This is the structural reason the catch survives capture of the advisor.

`run_advised_cycle` applies a menu only if `diversity_ok ∧ ¬endogenous_steering ∧ ¬exogenous_steering ∧ ratified`. The exogenous term is the one that closes the falsified hole.

## The honest boundary — residual uncaught zone

The mechanism is **not omniscient**. A captor who steers *within* the threshold band escapes: at threshold 0.10, winners cf = 0.79–0.81 (citizen-cost ≤ 0.10) are **not flagged**. This is by design and is pinned by a regression test — the residual uncaught zone is exactly `{winners costing citizens ≤ threshold}`. Tightening the threshold shrinks this zone (and tightens the catch boundary toward the citizen optimum) at the cost of more false-positive sensitivity. **The threshold is a political decision, not a technical one** (open in the ledger: "what counts as the AI steering"). The model bounds the trade-off; it does not pick the number.

## What only a human field-test can settle (the real wall)

This is **model-coherent against a synthetic panel — NOT human-validated.** The exogenous panel (`DEFAULT_PANEL`) is three synthetic archetypes. The whole gain of the exogenous audit is that it is *independent of the advisor*; it is **not** independent of *the modeler*. Three things only a human field-test (Stage B, `docs/governance_field_test_design.md`) can settle, and which no in-sim sweep can:

- **Is the citizen panel real?** In-sim, the modeler authored both the captor and the panel. The field-test substitutes **real, independently-sampled humans** for `CitizenArchetype` — the single most important substitution. Until then, "exogenous" means "structurally independent of the advisor surface," not "independent of the author."
- **Does a *human* adversary stay inside the modeled capture move?** The sweep's captor is a forcing function (top-utility-elects-target). A real red-teamer may attack framing, coercion, abstention, or the override organ — surfaces the resource-lever sweep does not model. The field-test's primary endpoint (M4: exogenous-audit catch-rate on a HUMAN-built captured agenda) is the direct test of exactly this.
- **A pass only fails to kill the mechanism.** Per the field-test honesty preamble: a clean Stage-B run earns "not yet falsified at this scale," never "validated for Mars." Generalization to Mars-scale electorates, real mortality stakes, and multi-year normalization is out of reach of any current instrument.

## Verdict

**HOLDS-under-exogenous-conditions** in software, with the human-validation boundary explicitly open.

- **Falsified criterion:** endogenous anti-capture certification (`option_diversity` + `adversarial_review`) — grades the advisor against its own `_utility`; a captured advisor passes its own audit (steering = False on a rigged agenda).
- **Holds because:** an exogenous, advisor-independent citizen-preference yardstick + whole-grid omitted-option scan, wired into `run_advised_cycle`. Condition: capture costing citizens **> steering threshold** is detected.
- **Key parameter + threshold:** `EXOGENOUS_STEERING_THRESHOLD`. At the ratified default **0.10**, every steered winner displaced ≥ +0.04 from the citizen optimum (citizen-cost > 0.10) is caught, up to and including gross capture (cf = 1.0). Catch boundary tightens monotonically as the threshold tightens.
- **One-line honest caveat:** model-coherent against a *synthetic* panel — independent of the advisor, **not** independent of the modeler; only a human exogenous panel (Stage-B field-test) converts this from "not yet falsified in sim" to a bounded human result.

## Reproduce

```bash
cd Mars_Governance
python -m pytest tests/test_exogenous_review.py tests/test_anti_capture_sweep.py -q
python -c "from governance.exogenous_preferences import catch_boundary; \
  print([(t, c.target_cf, c.citizen_cost) for t in (0.05,0.10,0.15,0.20,0.30) \
         for c in [catch_boundary('nominal',200,t)]])"
```
