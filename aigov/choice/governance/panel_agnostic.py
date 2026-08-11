"""ADVERSARY-AGNOSTIC anti-capture mechanism -- reduce the result's dependence on the ONE synthetic panel.

WHY THIS EXISTS (the root blocker)
----------------------------------
`governance/exogenous_preferences.py` catches advisor capture with a STRUCTURALLY INDEPENDENT citizen
panel -- independent of the advisor's `_utility`. But the catch boundary, and the whole "anti-capture
HOLDS" result, is computed against a SINGLE synthetic panel (`DEFAULT_PANEL`, citizen optimum cf~0.78)
that the MODELER authored. A critic's exact objection: the audit is "independent of the advisor, but not
of the author." Pick a different panel and the catch boundary moves. The validity of the result rests on
the specific panel + the chosen steering threshold.

THE INNOVATION (mechanism, not parameter tuning)
------------------------------------------------
Two mechanism-level moves make anti-capture depend LESS on any one panel:

  (1) MENU-COMPLETENESS PROOF -- a property checkable WITHOUT naming a panel and WITHOUT trusting the
      agenda-setter. If the menu's FEASIBLE options form a mesh whose largest gap across the feasible
      lever range is <= `mesh_tol`, then for ANY single-peaked citizen preference, the citizen optimum
      is within `mesh_tol` of some option ON THE MENU -- BY CONSTRUCTION. The captor therefore cannot
      hide the citizen optimum by omission, for EVERY panel at once, not just `DEFAULT_PANEL`. This is a
      structural guarantee: it quantifies over all single-peaked panels, and it is verifiable from the
      menu's cf-values alone (no preference model required).

  (2) PANEL-ENSEMBLE ROBUSTNESS -- instead of evaluating the catch property against one author-chosen
      panel, draw a RANDOMIZED ENSEMBLE of panels (random ideals, tolerances, weights, archetype count)
      and measure the catch-rate of the capture sweep ACROSS the ensemble. This converts "anti-capture
      holds for the cf=0.78 panel" into a distributional claim: "for a randomly drawn single-peaked
      panel, a capture costing citizens > threshold is detected with probability ~p". The author no
      longer hand-picks the one panel the result depends on; the result is averaged over a broad class.

The honest boundary is NARROWED, not erased: (1)+(2) make the result robust to ARBITRARY single-peaked
SYNTHETIC panels. They do NOT make it robust to real humans -- whether real citizen preferences are
single-peaked over crop_fraction, and whether a human adversary stays inside the modeled capture move,
remain Stage-B (human field-test) questions. See docs/governance_field_test_design.md.

This module imports only the physical feasibility grid + the existing exogenous machinery; it invents no
new preference structure beyond RANDOMIZING the existing `CitizenArchetype` kernel.
"""
from __future__ import annotations

import random
from dataclasses import dataclass

from governance.ai_advisor import CF_MIN, CF_MAX, feasible_grid
from governance.exogenous_preferences import (
    CitizenArchetype,
    MATERIAL_DISTINCT_EPS,
    anti_capture_sweep,
    exogenous_optimal_cf,
    exogenous_review_full,
    exogenous_utility,
)

# Default mesh tolerance for the completeness proof. A menu whose feasible options leave no gap wider
# than this across the feasible range provably contains every single-peaked panel's optimum to within it.
DEFAULT_MESH_TOL = 0.06


# --------------------------------------------------------------------------- (1) menu-completeness proof
@dataclass(frozen=True)
class CompletenessCert:
    """Panel-AGNOSTIC certificate that the menu's feasible options mesh-cover the feasible lever range.

    `max_gap` = the widest gap (including the two end-gaps to the feasible range boundary) between
    consecutive feasible menu options. `ok` = max_gap <= mesh_tol. If `ok`, then for ANY single-peaked
    citizen preference over crop_fraction, the citizen optimum lies within `mesh_tol` of some MENU option
    -- the captor cannot omit the citizen optimum, for every panel simultaneously. Verifiable from the
    cf-values alone -- no preference model, no trust in the agenda-setter.
    """
    ok: bool
    max_gap: float
    mesh_tol: float
    feasible_lo: object
    feasible_hi: object
    n_feasible_options: int
    worst_gap_at: tuple   # (lo, hi) of the widest uncovered interval


def menu_completeness(menu, scenario, n, mesh_tol=DEFAULT_MESH_TOL):
    """Certify that the menu's FEASIBLE options cover the feasible lever range with no gap > `mesh_tol`.

    The feasible range is taken from the PHYSICAL pluralism grid (both feasibility models agree) -- a
    fact the captor cannot forge. We require the menu to reach both ends of that range (no end-gap wider
    than mesh_tol) AND to leave no interior gap wider than mesh_tol. Single-peaked-ness of the (unknown)
    panel does the rest: the optimum of any single-peaked utility over [lo, hi] is in [lo, hi], hence
    within mesh_tol/... of the nearest covering option. We report the conservative `max_gap` so the
    guarantee is "optimum within max_gap of a menu option" for the worst single-peaked panel.
    """
    grid = feasible_grid(scenario, n)
    if not grid:
        return CompletenessCert(ok=False, max_gap=float("inf"), mesh_tol=mesh_tol,
                                feasible_lo=None, feasible_hi=None, n_feasible_options=0,
                                worst_gap_at=(None, None))
    lo, hi = min(grid), max(grid)
    feas_cfs = sorted(o.cf for o in menu if o.feasible and lo - 1e-9 <= o.cf <= hi + 1e-9)
    # Boundary points anchor the end-gaps: a menu that does not reach lo/hi leaves an uncovered tail.
    pts = [lo] + feas_cfs + [hi]
    pts = sorted(set(round(p, 6) for p in pts))
    max_gap, worst = 0.0, (lo, lo)
    for a, b in zip(pts, pts[1:]):
        g = b - a
        if g > max_gap:
            max_gap, worst = g, (a, b)
    return CompletenessCert(
        ok=(max_gap <= mesh_tol + 1e-9), max_gap=round(max_gap, 4), mesh_tol=mesh_tol,
        feasible_lo=lo, feasible_hi=hi, n_feasible_options=len(feas_cfs),
        worst_gap_at=(round(worst[0], 4), round(worst[1], 4)))


def complete_menu(scenario, n, mesh_tol=DEFAULT_MESH_TOL):
    """A minimal menu that PROVABLY passes `menu_completeness`: feasible options spaced <= mesh_tol across
    the whole feasible range (plus the mandatory status quo if it is feasible). This is the constructive
    side -- it shows an honest advisor CAN always satisfy the completeness proof, so the captor is forced
    either to fail it (visibly) or to leave the citizen optimum on the menu (where the exogenous audit
    can compare against it). Either branch defeats omission-capture for every single-peaked panel."""
    from governance.ai_advisor import make_option, STATUS_QUO_CF
    grid = feasible_grid(scenario, n)
    if not grid:
        return tuple()
    lo, hi = min(grid), max(grid)
    cfs, cf = set(), lo
    step = mesh_tol * 0.9   # strictly below the tolerance so the proof passes with margin
    while cf <= hi + 1e-9:
        # snap onto the physical grid so the option is genuinely feasible
        snapped = min(grid, key=lambda g: abs(g - cf))
        cfs.add(round(snapped, 4))
        cf += step
    cfs.add(round(hi, 4))
    if lo - 1e-9 <= STATUS_QUO_CF <= hi + 1e-9:
        cfs.add(round(min(grid, key=lambda g: abs(g - STATUS_QUO_CF)), 4))
    return tuple(make_option(c, scenario, n) for c in sorted(cfs))


# --------------------------------------------------------------------------- (2) panel-ensemble robustness
def aggregate_single_peaked(panel, scenario, n):
    """True iff the panel's WEIGHTED-AGGREGATE exogenous utility is MONOTONE-FALLING above its peak over
    the feasible grid -- the exact property the anti-capture mechanism needs.

    Capture steers the winner ABOVE the citizen optimum, so the catch property depends only on the
    RIGHT side of the peak: a costlier (higher-cf) steer must yield a strictly larger citizen-cost gap.
    A weighted SUM of single-peaked kernels can put a SECOND local maximum to the right of the global peak
    (e.g. a strong high-cf archetype) -- then a steer toward that secondary peak REDUCES the gap, breaking
    catch-faithfulness. That right-side multi-modality is exactly what is OUT of the completeness proof's
    domain. (Left-of-peak wiggles do not affect above-optimum capture and are ignored.) This predicate
    marks the in-domain vs out-of-domain boundary of the panel-agnostic result explicitly."""
    grid = feasible_grid(scenario, n)
    if not grid:
        return True
    us = [exogenous_utility(cf, panel) for cf in grid]
    peak = us.index(max(us))
    falling = all(us[i + 1] <= us[i] + 1e-9 for i in range(peak, len(us) - 1))
    return falling


def random_panel(rng, n_archetypes=None):
    """Draw a RANDOM single-peaked citizen panel. Ideals uniform over the feasible lever range, tolerances
    uniform over a plausible band, weights uniform positive, 2..4 archetypes. This is the class of panels
    the result must be robust ACROSS -- the author no longer fixes one. Single-peaked by construction
    (triangular kernel), which is exactly the class `menu_completeness` quantifies over."""
    k = n_archetypes if n_archetypes is not None else rng.randint(2, 4)
    panel = []
    for i in range(k):
        ideal = round(rng.uniform(CF_MIN, CF_MAX), 4)
        tol = round(rng.uniform(0.12, 0.30), 4)
        w = round(rng.uniform(0.4, 1.0), 4)
        panel.append(CitizenArchetype(f"rnd{i}", "random", ideal=ideal, tolerance=tol, weight=w))
    return tuple(panel)


@dataclass(frozen=True)
class EnsembleStat:
    threshold: float
    n_panels: int
    # `catch_property` = the citizen-cost GAP from the whole-grid audit is faithful (monotone in
    # displacement, never zero where the winner is steered above the optimum) -- so `caught == gap>thr`
    # is exact and the protection radius is well-defined. Reported OVERALL and IN-DOMAIN (single-peaked
    # aggregate). The completeness proof is panel-agnostic (should be 1.0 for every panel).
    catch_property_held_rate: float         # over ALL random panels (incl. multi-peaked aggregates)
    in_domain_held_rate: float              # over single-peaked-aggregate panels only (the proof's domain)
    single_peaked_share: float              # fraction of random panels whose aggregate is single-peaked
    mean_protection_radius: object          # mean catch-boundary displacement, in-domain panels
    completeness_pass_rate: float           # honest complete_menu passes the panel-AGNOSTIC proof
    n_property_failures: int                # overall faithfulness failures (all multi-peaked aggregates)


def _forced_winners_above_optimum(scenario, n, panel):
    """Forced-winner crop_fractions strictly above THIS panel's exogenous optimum, each with its
    citizen-cost GAP (threshold-independent). Reuses the existing capture sweep's targets (every feasible
    cf > optimum) but scores each with the WHOLE-GRID audit so the result composes with menu-completeness
    (the omitted-only audit has a blind spot when the optimum is on a dense menu -- see
    exogenous_review_full). The catch decision is applied by the caller at its own threshold, so this
    function never bakes in a threshold."""
    from governance.exogenous_preferences import _capture_menu
    from governance.ai_advisor import agenda_outcome
    exo_opt = exogenous_optimal_cf(scenario, n, panel)
    grid = feasible_grid(scenario, n)
    out = []
    for t in [cf for cf in grid if cf > exo_opt]:
        menu = _capture_menu(t, scenario, n)
        winner = agenda_outcome(menu, n).winner
        if winner != t:
            continue
        rev = exogenous_review_full(winner, scenario, n, panel=panel)
        out.append((t, exo_opt, rev.exo_gap))   # gap only; threshold applied by caller
    return out


def _catch_property_holds_for_panel(scenario, n, panel, threshold):
    """For ONE panel: does the WHOLE-GRID exogenous audit catch every above-optimum forced winner that
    costs citizens > threshold, and abstain on those costing <= threshold? Returns
    (held: bool, protection_radius|None). The catch decision is `gap > threshold`, evaluated at the SAME
    threshold throughout -- so the rule is `caught(thr) == (gap > thr)` by definition, and the meaningful
    content is that the gap is a faithful, monotone citizen-cost signal (no inversions / no blind spots)."""
    rows = _forced_winners_above_optimum(scenario, n, panel)
    if not rows:
        return True, None  # vacuously holds (panel optimum at the top of the range)
    # Faithfulness check: gap must be non-decreasing in displacement (no inversion where a costlier steer
    # produces a smaller gap), and strictly positive for every above-optimum forced winner (no blind spot
    # like the omitted-only audit's dense-menu hole). If both hold, `caught(thr) == gap>thr` is exact.
    rows_sorted = sorted(rows, key=lambda r: r[0])
    gaps = [g for (_t, _o, g) in rows_sorted]
    monotone = all(b >= a - 1e-9 for a, b in zip(gaps, gaps[1:]))
    no_blind_spot = all(g > 0.0 for g in gaps)
    held = monotone and no_blind_spot
    caught_radii = [t - o for (t, o, g) in rows if g > threshold]
    radius = min(caught_radii) if caught_radii else None
    return held, radius


def panel_ensemble_sweep(scenario, n, threshold=0.10, n_panels=200, seed=0,
                         mesh_tol=DEFAULT_MESH_TOL):
    """Measure the anti-capture catch property ACROSS a randomized ensemble of single-peaked panels.

    The headline robustness number: `catch_property_held_rate` -- the fraction of randomly drawn panels
    for which the threshold-conditional catch rule (caught <=> citizen-cost > threshold) holds EXACTLY.
    If this is ~1.0, the result is not an artifact of the one authored panel: the SAME mechanism, with the
    SAME threshold, catches capture across the whole class of single-peaked panels. Also reports the
    completeness-proof pass rate for an honest `complete_menu` (panel-agnostic, so it should be 1.0).

    Deterministic given `seed`. RNG is local (`random.Random`) -- never touches global state.
    """
    rng = random.Random(seed)
    held = 0
    radii = []
    failures = 0
    comp_pass = 0
    sp_total = sp_held = 0
    for _ in range(n_panels):
        panel = random_panel(rng)
        ok, radius = _catch_property_holds_for_panel(scenario, n, panel, threshold)
        if ok:
            held += 1
        else:
            failures += 1
        if aggregate_single_peaked(panel, scenario, n):
            sp_total += 1
            if ok:
                sp_held += 1
                if radius is not None:
                    radii.append(radius)
        # completeness proof is panel-AGNOSTIC -- an honest complete menu passes regardless of the panel
        cm = complete_menu(scenario, n, mesh_tol=mesh_tol)
        if menu_completeness(cm, scenario, n, mesh_tol=mesh_tol).ok:
            comp_pass += 1
    return EnsembleStat(
        threshold=threshold, n_panels=n_panels,
        catch_property_held_rate=round(held / n_panels, 4),
        in_domain_held_rate=(round(sp_held / sp_total, 4) if sp_total else None),
        single_peaked_share=round(sp_total / n_panels, 4),
        mean_protection_radius=(round(sum(radii) / len(radii), 4) if radii else None),
        completeness_pass_rate=round(comp_pass / n_panels, 4),
        n_property_failures=failures)


# --------------------------------------------------------------------------- combined gate (composition)
@dataclass(frozen=True)
class PanelAgnosticVerdict:
    applied: bool
    completeness: CompletenessCert
    exo_steering_detected: bool      # whole-grid audit (composes with completeness)
    winner: object
    exo_gap: object


def panel_agnostic_gate(menu, winner, scenario, n, panel, mesh_tol=DEFAULT_MESH_TOL,
                        threshold=None):
    """The two mechanism moves COMPOSED into one gate:

      (1) the menu must pass the panel-AGNOSTIC completeness proof (citizen optimum provably on/near the
          menu for EVERY single-peaked panel), AND
      (2) the WHOLE-GRID exogenous audit must not flag the elected winner against the supplied panel.

    Completeness alone does not stop steering (a dense menu can still elect a far winner); the whole-grid
    audit alone has no panel-agnostic anchor. Together: completeness forces the citizen optimum into the
    grid; the whole-grid audit then measures the winner against it -- regardless of which single-peaked
    panel is drawn. A menu is `applied` only if it passes both.
    """
    from governance.exogenous_preferences import EXOGENOUS_STEERING_THRESHOLD
    thr = EXOGENOUS_STEERING_THRESHOLD if threshold is None else threshold
    cert = menu_completeness(menu, scenario, n, mesh_tol=mesh_tol)
    rev = exogenous_review_full(winner, scenario, n, panel=panel, threshold=thr)
    applied = cert.ok and not rev.steering_detected
    return PanelAgnosticVerdict(applied=applied, completeness=cert,
                                exo_steering_detected=rev.steering_detected,
                                winner=winner, exo_gap=rev.exo_gap)
