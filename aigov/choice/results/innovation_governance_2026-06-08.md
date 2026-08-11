# Anti-capture made PANEL-AGNOSTIC by construction — not tuned to the one synthetic panel

**Date:** 2026-06-08
**Module:** GOVERNANCE (`Mars_Governance/`) — AI agenda-advisor kept contestable; anti-capture = keep the strongest from quietly taking over.
**Pass type:** INNOVATION on MECHANISM (not parameter tuning). New code: `governance/panel_agnostic.py` + `exogenous_review_full` (whole-grid audit) in `governance/exogenous_preferences.py`. Tests: `tests/test_panel_agnostic.py` (12). **Full suite 127/127 green** (was 115; +12).

---

## Root blocker (the wall the prior result hit)

The 2026-06-07 result ("anti-capture HOLDS under an exogenous yardstick") was real but **rested on ONE synthetic panel** (`DEFAULT_PANEL`, citizen optimum cf≈0.78) that the modeler authored. The catch boundary, the protection radius, the whole result, were computed against that single panel. Critic's exact objection: the audit is **"independent of the advisor, but not of the author."** Pick a different panel and the boundary moves. Validity rested on the specific panel + chosen threshold.

## The mechanism innovation (reduces panel-dependence by construction)

Two moves, both reusing the existing sandbox, that make anti-capture hold **across a class of panels** rather than for one:

### (1) Menu-completeness proof — panel-AGNOSTIC, checkable without trusting the agenda-setter
`menu_completeness` certifies the menu's **feasible** options mesh-cover the **physical** feasible lever range (from the pluralism grid, which the captor cannot forge) with no gap wider than `mesh_tol`. If it passes, then for **ANY** single-peaked panel the citizen optimum lies within `mesh_tol` of some option **on the menu** — by construction, quantified over all panels at once, verifiable from cf-values alone (no preference model, no named panel). The captor cannot hide the citizen optimum by omission for every panel simultaneously.
- Honest complete menu: `max_gap = 0.06` (tol 0.06) → **PASS**.
- Gross-capture menu omitting the optimum band: `max_gap = 0.18`, worst uncovered interval `(0.67, 0.85)` → **FAIL, visibly**. No panel consulted.

### (2) Panel-ensemble robustness — the result is now distributional, not hand-picked
`panel_ensemble_sweep` draws a **randomized ensemble** of panels (random ideals, tolerances, weights, 2–4 archetypes) and measures whether the catch property holds across them. The author no longer fixes the one panel the result depends on.

### Composition bug found + fixed (load-bearing)
The two moves did **not** compose under the old `exogenous_review`: it scans only **omitted** options. A captor who builds a **dense / completeness-passing** menu puts the citizen optimum **on** the menu (so it isn't "omitted"), then steers the tally elsewhere — and the omitted-only scan reports `gap=0`, **steering=False**, even when the elected winner is cf=1.0 (citizen-cost 0.44). New `exogenous_review_full` compares the winner against the best feasible option on the **whole grid** (menu ∪ omitted); it catches the dense-capture dodge (`gap=0.443`, steering=True). Completeness forces the optimum onto the grid; the whole-grid audit measures the winner against it. **Now they compose** (`panel_agnostic_gate`).

## Model-tested result — robustness ACROSS panels

`panel_ensemble_sweep`, 500 random panels/cell, two scenarios, deterministic (local RNG):

| Scenario | Threshold | **In-domain held-rate** | Single-peaked share | Mean protection radius | Completeness pass-rate |
|---|---|---|---|---|---|
| nominal | 0.05 | **1.0** | 0.776 | 0.036 | 1.0 |
| nominal | **0.10** | **1.0** | 0.776 | 0.055 | 1.0 |
| nominal | 0.20 | **1.0** | 0.776 | 0.086 | 1.0 |
| scarcity | 0.05–0.20 | **1.0** | 1.0 | n/a* | 1.0 |

\* scarcity's feasible floor is high → citizen optimum sits at the top of the range → no above-optimum steering exists.

- **In-domain held-rate = 1.0** everywhere: for **every** randomly drawn panel whose aggregate is monotone-falling above its peak (the class the completeness proof covers), the whole-grid audit's citizen-cost gap is faithful (monotone in displacement, no blind spot) — so `caught ⇔ citizen-cost > threshold` is exact. **Not an artifact of the authored panel.**
- **Completeness pass-rate = 1.0**: the panel-agnostic proof always passes for an honest complete menu, for every panel.
- Held-rate is **threshold-independent** (threshold sets *where* the boundary sits, not whether the gap is a valid signal).

## The honest boundary — NARROWED, not erased

The completeness proof quantifies over **single-peaked** preferences. A weighted **sum** of single-peaked kernels can be **multi-peaked** (a strong high-cf archetype creates a second local max to the right of the global peak). Steering toward that secondary peak *reduces* the citizen-cost gap, breaking catch-faithfulness. This is **out of the proof's domain** and is **named, not hidden**: `aggregate_single_peaked` flags it, the ensemble reports `single_peaked_share` (0.776 in nominal). Every one of the 112/500 faithfulness failures is exactly a right-side-multi-peaked panel — the delineation is clean (`overall_held = sp_share` to the digit). Multi-peaked electorates are the classic hard case in social choice (Condorcet cycles live there); claiming to "solve" them in-sim would be p-hacking.

**What this innovation did:** moved the result from "holds for the cf=0.78 panel the author wrote" → "holds **by construction** for the whole class of single-peaked-aggregate panels, across a randomized ensemble, with the out-of-domain multi-peaked class explicitly marked." That genuinely **reduces** author-dependence. It does **not** reach the human axis.

## Residual — the human wall (1 line)
Still **synthetic** panels only: whether **real** citizen preferences over crop_fraction are single-peaked, and whether a **human** adversary stays inside the modeled "force a winner" capture move, is settleable only by the Stage-B human field-test (`docs/governance_field_test_design.md`) — no in-sim sweep can.

## Reproduce
```bash
cd Mars_Governance
python -m pytest tests/test_panel_agnostic.py -q
python -c "from governance.panel_agnostic import panel_ensemble_sweep as s; \
  r=s('nominal',200,threshold=0.10,n_panels=500,seed=1); \
  print('in_domain_held',r.in_domain_held_rate,'sp_share',r.single_peaked_share,'completeness',r.completeness_pass_rate)"
```
