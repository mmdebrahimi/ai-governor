"""Adversary-AGNOSTIC anti-capture mechanism (innovation pass, 2026-06-08).

Pins the two mechanism moves that reduce the result's dependence on the ONE synthetic panel
(`DEFAULT_PANEL`) the modeler authored -- the critic's "independent of the advisor, not of the author":

  (1) MENU-COMPLETENESS PROOF (`menu_completeness`) -- panel-AGNOSTIC: an honest complete menu mesh-covers
      the feasible range so the citizen optimum is on/near the menu for EVERY single-peaked panel; a
      gross-capture menu that omits the optimum band FAILS the proof, visibly.
  (2) WHOLE-GRID exogenous audit (`exogenous_review_full`) -- closes the omitted-only audit's blind spot
      where a DENSE / completeness-passing capture menu dodges detection (optimum on-menu => not omitted).
  (1)+(2) COMPOSE in `panel_agnostic_gate`.
  ENSEMBLE robustness (`panel_ensemble_sweep`) -- the catch property holds across a RANDOMIZED ensemble of
  single-peaked-aggregate panels (in-domain held-rate = 1.0), not just the one authored panel.

HONEST BOUNDARY pinned here too: a randomized multi-archetype panel can have a MULTI-peaked aggregate,
which is OUT of the completeness proof's single-peaked domain; the in-domain/out-of-domain split is
reported, not hidden. Synthetic panels only -- the human axis is Stage B. Deterministic; local RNG.
"""
import random

import pytest

from governance.ai_advisor import Option, agenda_outcome, feasible_grid, models_for, STATUS_QUO_CF
from governance.exogenous_preferences import (
    DEFAULT_PANEL,
    _capture_menu,
    exogenous_optimal_cf,
    exogenous_review,
    exogenous_review_full,
    exogenous_utility,
)
from governance.panel_agnostic import (
    aggregate_single_peaked,
    complete_menu,
    menu_completeness,
    panel_agnostic_gate,
    panel_ensemble_sweep,
    random_panel,
)

N = 200
SC = "nominal"


def _dense_capture_menu(target, scenario, n, mesh=0.05):
    """A DENSE menu (mesh-covers the range, would PASS completeness) whose utility labels force `target`
    to win. The hard case for the omitted-only audit: the citizen optimum is ON the menu, so it is not
    'omitted' and the omitted-only scan misses the steer."""
    a, b = models_for(scenario)
    grid = feasible_grid(scenario, n)
    lo, hi = min(grid), max(grid)
    cfs, cf = set(), lo
    while cf <= hi + 1e-9:
        cfs.add(round(min(grid, key=lambda g: abs(g - cf)), 4))
        cf += mesh
    cfs.add(round(STATUS_QUO_CF, 4))
    cfs.add(round(target, 4))
    return tuple(Option(cf=cf, feasible_A=a.feasible(cf), feasible_B=b.feasible(cf), scrubbing=False,
                        utility=(1.0 if abs(cf - round(target, 4)) < 1e-9 else 0.0))
                for cf in sorted(cfs))


# --------------------------------------------------------------------------- (1) completeness proof
def test_honest_complete_menu_passes_completeness():
    cm = complete_menu(SC, N)
    cert = menu_completeness(cm, SC, N)
    assert cert.ok is True
    assert cert.max_gap <= cert.mesh_tol + 1e-9


def test_gross_capture_menu_fails_completeness():
    """A captor menu that omits the citizen-optimum band leaves a wide uncovered gap -> proof FAILS,
    visibly, with no panel named. This is the panel-AGNOSTIC catch."""
    capm = _capture_menu(1.0, SC, N)
    cert = menu_completeness(capm, SC, N)
    assert cert.ok is False
    assert cert.max_gap > cert.mesh_tol


def test_completeness_is_panel_agnostic():
    """The proof reads only cf-values + the physical feasible range -- no panel. Same verdict whichever
    panel we (don't) pass."""
    cm = complete_menu(SC, N)
    c1 = menu_completeness(cm, SC, N)
    c2 = menu_completeness(cm, SC, N, mesh_tol=c1.mesh_tol)
    assert (c1.ok, c1.max_gap) == (c2.ok, c2.max_gap)


# --------------------------------------------------------------------------- (2) whole-grid audit closes blind spot
def test_omitted_only_audit_has_dense_menu_blind_spot():
    """Document the bug the whole-grid audit fixes: a dense capture menu electing cf=1.0 (citizen-cost
    ~0.44) is NOT flagged by the omitted-only `exogenous_review` because the optimum is on the menu."""
    m = _dense_capture_menu(1.0, SC, N)
    w = agenda_outcome(m, N).winner
    assert w == 1.0
    old = exogenous_review(m, w, SC, N)
    assert old.steering_detected is False  # the blind spot
    assert old.exo_gap == 0.0


def test_whole_grid_audit_catches_dense_capture():
    """`exogenous_review_full` compares the winner against the best feasible option on the WHOLE grid,
    so the dense-menu dodge fails -- the steer to cf=1.0 is caught."""
    m = _dense_capture_menu(1.0, SC, N)
    w = agenda_outcome(m, N).winner
    new = exogenous_review_full(w, SC, N)
    assert new.steering_detected is True
    assert new.exo_gap > 0.4  # ~0.44 citizen-cost


# --------------------------------------------------------------------------- composition gate
def test_gate_rejects_dense_capture_and_accepts_honest_optimum():
    # captor: dense menu, far winner -> rejected (completeness passes but whole-grid audit flags)
    m = _dense_capture_menu(1.0, SC, N)
    w = agenda_outcome(m, N).winner
    v = panel_agnostic_gate(m, w, SC, N, DEFAULT_PANEL)
    assert v.applied is False
    assert v.completeness.ok is True and v.exo_steering_detected is True

    # honest: dense menu electing the citizen optimum -> applied, no false positive
    opt = exogenous_optimal_cf(SC, N, DEFAULT_PANEL)
    hm = _dense_capture_menu(opt, SC, N)
    hw = agenda_outcome(hm, N).winner
    hv = panel_agnostic_gate(hm, hw, SC, N, DEFAULT_PANEL)
    assert hv.applied is True
    assert hv.exo_steering_detected is False


def test_gate_rejects_optimum_omitting_menu_on_completeness():
    """A captor who instead OMITS the optimum band is stopped by the completeness term, before any panel
    is consulted."""
    capm = _capture_menu(1.0, SC, N)
    w = agenda_outcome(capm, N).winner
    v = panel_agnostic_gate(capm, w, SC, N, DEFAULT_PANEL)
    assert v.applied is False
    assert v.completeness.ok is False


# --------------------------------------------------------------------------- (3) ensemble robustness
def test_ensemble_in_domain_catch_property_holds():
    """THE PANEL-DEPENDENCE REDUCTION: across a randomized ensemble of single-peaked-aggregate panels,
    the whole-grid audit's citizen-cost gap is faithful (monotone, no blind spot) for EVERY one -- so the
    catch property is not an artifact of the single authored panel."""
    s = panel_ensemble_sweep(SC, N, threshold=0.10, n_panels=300, seed=1)
    assert s.in_domain_held_rate == 1.0
    assert s.completeness_pass_rate == 1.0          # panel-agnostic proof always passes for honest menus
    assert 0.0 < s.single_peaked_share <= 1.0


def test_ensemble_is_deterministic():
    a = panel_ensemble_sweep(SC, N, threshold=0.10, n_panels=120, seed=3)
    b = panel_ensemble_sweep(SC, N, threshold=0.10, n_panels=120, seed=3)
    assert (a.in_domain_held_rate, a.single_peaked_share, a.n_property_failures) == \
           (b.in_domain_held_rate, b.single_peaked_share, b.n_property_failures)


def test_held_rate_is_threshold_independent():
    """Faithfulness of the citizen-cost gap (monotone, no blind spot) does not depend on the threshold --
    the threshold only sets WHERE the catch boundary sits, not whether the gap is a valid signal."""
    r = [panel_ensemble_sweep(SC, N, threshold=t, n_panels=120, seed=4).in_domain_held_rate
         for t in (0.05, 0.10, 0.20)]
    assert r[0] == r[1] == r[2]


# --------------------------------------------------------------------------- honest boundary: multi-peaked
def test_multi_peaked_aggregate_is_named_out_of_domain():
    """The honest wall: a weighted SUM of single-peaked kernels can be MULTI-peaked, which is OUT of the
    completeness proof's domain. We do not hide this -- such panels exist in the ensemble and are flagged
    by `aggregate_single_peaked`."""
    rng = random.Random(1)
    sp = mp = 0
    for _ in range(300):
        p = random_panel(rng)
        if aggregate_single_peaked(p, SC, N):
            sp += 1
        else:
            mp += 1
    assert sp > 0 and mp > 0, "the ensemble must contain BOTH single- and multi-peaked aggregates"


def test_default_panel_is_single_peaked_and_in_domain():
    assert aggregate_single_peaked(DEFAULT_PANEL, SC, N) is True
