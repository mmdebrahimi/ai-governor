"""EXOGENOUS preference/utility model for the AI-advisor anti-capture audit (gap C2-b / D7).

WHY THIS EXISTS
---------------
`governance/ai_advisor.py` certifies an agenda as "non-steering" via `option_diversity` +
`adversarial_review`. Both grade the advisor's menu against the SAME `_utility` / `optimal_cf`
surface the advisor used to BUILD the menu. That certification is therefore ENDOGENOUS: a
*captured* `_utility` makes `optimal_cf` point at the captor's preferred policy, the menu
"contains the optimum" by construction, and the adversarial review (which re-tallies omitted
options under the same captured utility) sees no steering. The audit grades the advisor against
its own ruler -- a captured ruler passes its own audit. (docs/ai_advisor_spec.md, C2-b.)

WHAT THIS PROVIDES
------------------
A STRUCTURALLY INDEPENDENT yardstick that is NOT derived from `_utility` / `optimal_cf`:

  - A small synthetic human-preference-elicitation surface. Instead of the advisor's
    margin/|O2-net|/farming-cost analytic cost function, the exogenous utility is the AGGREGATE
    SATISFACTION of a panel of citizen archetypes, each parameterized from an INDEPENDENT concern
    (O2-safety margin, labor burden, import-dependence/resilience). Each archetype has its own
    ideal crop_fraction and tolerance; satisfaction is a triangular preference kernel over cf.
  - Different FUNCTIONAL FORM (sum of preference kernels, not an analytic cost), different INPUTS
    (elicited ideals + tolerances, not model.margin / O2-net), and it CAN disagree with the
    advisor surface (the panel optimum need not coincide with `optimal_cf`).

Feasibility is still taken from the pluralism gate (`models_for`) so we never score a starving
option as "good" -- but the RANKING among feasible options is fully exogenous. This module imports
nothing from `_utility` / `optimal_cf`; it only borrows the feasibility predicate and the option
lever range, which are physical, not preference, facts.
"""
from __future__ import annotations

from dataclasses import dataclass

from governance.ai_advisor import feasible_grid
from governance.ruleset import NONE_OF_THESE

# Audit threshold on the EXOGENOUS satisfaction scale (0..1). If an omitted feasible option beats
# the advisor's winner by more than this on exogenous utility, the winner is exogenously steered.
EXOGENOUS_STEERING_THRESHOLD = 0.10
# Material-distinctness eps for the omitted-option sweep (mirrors the endogenous review).
MATERIAL_DISTINCT_EPS = 0.03


@dataclass(frozen=True)
class CitizenArchetype:
    """One elicited human-preference profile over crop_fraction.

    `ideal` = the crop_fraction this constituency would pick if it alone decided; `tolerance` =
    half-width of the triangular satisfaction kernel (satisfaction falls linearly to 0 at
    ideal +/- tolerance); `weight` = its share of the panel. These come from a (synthetic) human
    elicitation, NOT from the advisor's analytic `_utility`.
    """
    name: str
    concern: str
    ideal: float
    tolerance: float
    weight: float = 1.0

    def satisfaction(self, cf):
        d = abs(cf - self.ideal)
        if d >= self.tolerance:
            return 0.0
        return 1.0 - d / self.tolerance


# Default synthetic elicitation panel. Ideals are spread across the feasible lever range and are
# deliberately NOT centered on the advisor's analytic optimum (cf ~ 0.667): the panel can disagree.
#   - safety-margin: wants a real food buffer above the feasibility edge -> mid-high cf.
#   - labor-burden: wants minimal farming effort -> low cf (near the feasible floor).
#   - resilience: wants independence from imports -> high cf.
# Their weighted aggregate satisfaction has its own optimum, independent of `optimal_cf`.
DEFAULT_PANEL = (
    CitizenArchetype("safety-margin", "food-buffer", ideal=0.78, tolerance=0.22, weight=1.0),
    CitizenArchetype("labor-burden", "min-effort", ideal=0.62, tolerance=0.20, weight=1.0),
    CitizenArchetype("resilience", "import-independence", ideal=0.90, tolerance=0.25, weight=0.6),
)


def exogenous_utility(cf, panel=DEFAULT_PANEL):
    """Weighted-mean panel satisfaction at crop_fraction `cf` (0..1). Independent of `_utility`."""
    wsum = sum(a.weight for a in panel)
    if wsum <= 0:
        raise ValueError("panel weights must sum to a positive value")
    return sum(a.weight * a.satisfaction(cf) for a in panel) / wsum


def exogenous_optimal_cf(scenario, n, panel=DEFAULT_PANEL, step=0.01):
    """Best FEASIBLE crop_fraction under the exogenous panel. Feasibility from the pluralism gate
    (both A and B agree); ranking from the exogenous panel -- never from `optimal_cf`."""
    grid = feasible_grid(scenario, n, step=step)
    if not grid:
        return None
    return max(grid, key=lambda cf: exogenous_utility(cf, panel))


@dataclass(frozen=True)
class ExogenousReview:
    winner: object              # the advisor's winning crop_fraction (or NONE_OF_THESE)
    winner_exo_utility: object  # exogenous utility of the winner (None if NONE_OF_THESE)
    best_omitted: object        # the omitted feasible cf with the highest exogenous utility
    best_omitted_exo_utility: object
    exo_gap: object             # best_omitted_exo_utility - winner_exo_utility (None if winner is NoT)
    steering_detected: bool
    exo_optimal_cf: object      # the exogenous panel optimum over the whole feasible grid


def exogenous_review(menu, winner, scenario, n, panel=DEFAULT_PANEL,
                     threshold=EXOGENOUS_STEERING_THRESHOLD):
    """Score the advisor's WINNER against the EXOGENOUS optimum.

    Steering is flagged if some FEASIBLE option the advisor OMITTED from the menu would have given
    citizens materially (> `threshold`) more exogenous satisfaction than the winner. This catches
    capture the endogenous review misses: when the advisor's `_utility` is captured, both the menu
    AND the endogenous re-tally agree on the captured winner, so endogenous steering = False -- but
    the independent panel still prefers the omitted, genuinely-better option, so exogenous
    steering = True.

    `winner` is the disposal outcome from `agenda_outcome` / `ratify`. If it is NONE_OF_THESE the
    advisor steered nothing through, so there is nothing to flag here (caretaker holds).
    """
    grid = feasible_grid(scenario, n)
    exo_opt = exogenous_optimal_cf(scenario, n, panel)
    existing = [o.cf for o in menu]
    omitted = [cf for cf in grid
               if all(abs(cf - e) > MATERIAL_DISTINCT_EPS for e in existing)]

    if not omitted:
        best_omitted = best_omitted_u = None
    else:
        best_omitted = max(omitted, key=lambda cf: exogenous_utility(cf, panel))
        best_omitted_u = exogenous_utility(best_omitted, panel)

    if winner == NONE_OF_THESE:
        return ExogenousReview(winner=winner, winner_exo_utility=None,
                               best_omitted=best_omitted, best_omitted_exo_utility=best_omitted_u,
                               exo_gap=None, steering_detected=False, exo_optimal_cf=exo_opt)

    winner_u = exogenous_utility(winner, panel)
    if best_omitted_u is None:
        gap = 0.0
    else:
        gap = best_omitted_u - winner_u
    steering = gap > threshold
    return ExogenousReview(winner=winner, winner_exo_utility=winner_u,
                           best_omitted=best_omitted, best_omitted_exo_utility=best_omitted_u,
                           exo_gap=gap, steering_detected=steering, exo_optimal_cf=exo_opt)


def exogenous_review_full(winner, scenario, n, panel=DEFAULT_PANEL,
                          threshold=EXOGENOUS_STEERING_THRESHOLD):
    """WHOLE-GRID variant of `exogenous_review`: score the winner against the best feasible option on the
    ENTIRE grid (menu UNION omitted), not only the omitted ones.

    WHY (composition bug found 2026-06-08): `exogenous_review` compares the winner against the best
    *omitted* feasible option. A captor who builds a DENSE / completeness-passing menu puts the citizen
    optimum ON the menu, so it is no longer "omitted" -- the omitted-only scan then finds nothing better
    and reports gap=0 even when the elected winner is far from the citizen optimum. (Reproduced: a dense
    menu electing cf=1.0 costs citizens 0.44 satisfaction yet `exogenous_review` reports steering=False.)

    The whole-grid comparison closes that hole: it asks "is the winner within `threshold` of the BEST
    feasible policy the citizens could have had?" -- regardless of whether that best policy sits on the
    menu or off it. This is the term that COMPOSES with the menu-completeness proof: completeness forces
    the citizen optimum onto the grid where this scan always sees it. Independent of the menu's framing,
    so it cannot be dodged by padding the ballot with the optimum while steering the tally elsewhere.
    """
    grid = feasible_grid(scenario, n)
    exo_opt = exogenous_optimal_cf(scenario, n, panel)
    if not grid:
        best = best_u = None
    else:
        best = max(grid, key=lambda cf: exogenous_utility(cf, panel))
        best_u = exogenous_utility(best, panel)
    if winner == NONE_OF_THESE:
        return ExogenousReview(winner=winner, winner_exo_utility=None,
                               best_omitted=best, best_omitted_exo_utility=best_u,
                               exo_gap=None, steering_detected=False, exo_optimal_cf=exo_opt)
    winner_u = exogenous_utility(winner, panel)
    gap = 0.0 if best_u is None else best_u - winner_u
    return ExogenousReview(winner=winner, winner_exo_utility=winner_u,
                           best_omitted=best, best_omitted_exo_utility=best_u,
                           exo_gap=gap, steering_detected=(gap > threshold), exo_optimal_cf=exo_opt)


# --------------------------------------------------------------------------- anti-capture sweep (D7 re-exam)
# Re-examination harness (2026-06-07): the endogenous certification was FALSIFIED (a captured `_utility`
# passes its own audit). This sweep answers the follow-up question with the EXISTING machinery: against an
# adversary that steers the elected winner away from the citizen optimum, OVER WHAT (threshold, adversary-
# strength) REGION does the exogenous audit still catch the capture? It reuses `exogenous_review` verbatim;
# it invents no numbers. "adversary strength" = the displacement of the captor-forced winner cf above the
# exogenous (citizen) optimum -- i.e. how hard the captor pushes the outcome toward the captor-preferred,
# citizen-dispreferred policy. The captor always builds a DIVERSITY-PASSING menu (the hard case: it clears
# every existing gate, so only the exogenous audit can catch it).
@dataclass(frozen=True)
class SweepCell:
    threshold: float
    target_cf: float            # captor-forced winner crop_fraction
    displacement: float         # target_cf - exogenous optimum (adversary strength)
    citizen_cost: float         # exogenous-utility lost vs the citizen optimum
    diversity_ok: bool          # captor menu cleared the endogenous diversity gate
    winner: object              # actual elected winner (should equal target_cf when forced)
    caught: bool                # exogenous audit flagged steering
    exo_gap: object


def _capture_menu(target_cf, scenario, n):
    """A diversity-PASSING menu that elects `target_cf`: mandatory status quo, spans the lever range,
    contains the endogenous optimum (so `option_diversity` cannot reject it), with `target_cf` given the
    top utility so the sincere approval tally elects it. The honest move for a captor who wants to look
    clean to every endogenous check. Utility here is a forcing label, not a claim about real preference."""
    from governance.ai_advisor import (Option, models_for, optimal_cf, STATUS_QUO_CF, CF_MIN, CF_MAX)
    a, b = models_for(scenario)
    endo_opt = optimal_cf(scenario, n)
    cfs = sorted({CF_MIN, endo_opt, STATUS_QUO_CF, round(target_cf, 4), CF_MAX})
    opts = []
    for cf in cfs:
        cf = round(cf, 4)
        u = 1.0 if abs(cf - round(target_cf, 4)) < 1e-9 else 0.0
        opts.append(Option(cf=cf, feasible_A=a.feasible(cf), feasible_B=b.feasible(cf),
                           scrubbing=False, utility=u))
    return tuple(opts)


def anti_capture_sweep(scenario, n, thresholds=(0.05, 0.10, 0.20),
                       targets=None, panel=DEFAULT_PANEL):
    """Sweep (threshold x captor-forced winner cf) through the EXISTING exogenous audit. Returns a list of
    SweepCell. For each cell: a diversity-passing captured menu electing `target_cf` is scored by
    `exogenous_review`; `caught` is whether the independent panel detects steering. Deterministic; no RNG.

    Reading the result: for a fixed threshold there is a CATCH BOUNDARY -- the smallest displacement above
    the citizen optimum at which `caught` flips True. Below it lies the residual (uncaught) capture zone,
    whose width is set by `threshold`. This is the in-sim condition under which anti-capture HOLDS:
    any capture that costs citizens MORE THAN `threshold` exogenous-satisfaction is detected.
    """
    from governance.ai_advisor import agenda_outcome
    grid = feasible_grid(scenario, n)
    exo_opt = exogenous_optimal_cf(scenario, n, panel)
    if targets is None:
        targets = [cf for cf in grid if cf >= exo_opt]
    cells = []
    for thr in thresholds:
        for t in targets:
            menu = _capture_menu(t, scenario, n)
            from governance.ai_advisor import option_diversity
            div = option_diversity(menu, scenario, n)
            winner = agenda_outcome(menu, n).winner
            review = exogenous_review(menu, winner, scenario, n, panel=panel, threshold=thr)
            cells.append(SweepCell(
                threshold=thr, target_cf=round(t, 4),
                displacement=round(t - exo_opt, 4),
                citizen_cost=round(exogenous_utility(exo_opt, panel) - exogenous_utility(t, panel), 4),
                diversity_ok=div.ok, winner=winner,
                caught=review.steering_detected, exo_gap=review.exo_gap))
    return cells


def catch_boundary(scenario, n, threshold, panel=DEFAULT_PANEL):
    """Smallest captor-forced winner cf strictly above the citizen optimum that the exogenous audit CATCHES
    at `threshold`, as a SweepCell -- or None if nothing above the optimum is caught. The protection radius."""
    exo_opt = exogenous_optimal_cf(scenario, n, panel)
    cells = anti_capture_sweep(scenario, n, thresholds=(threshold,), panel=panel)
    above = [c for c in cells if c.target_cf > exo_opt and c.winner == c.target_cf]
    caught = [c for c in above if c.caught]
    return min(caught, key=lambda c: c.target_cf) if caught else None
