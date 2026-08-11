"""Exogenous (structurally-independent) anti-steering audit -- gap C2-b / D7.

The endogenous audit (`option_diversity` + `adversarial_review`) grades the advisor's menu against
the SAME `_utility` / `optimal_cf` surface the advisor used to build it. A CAPTURED `_utility` thus
passes its own audit. These tests:

  1. confirm the exogenous model is genuinely INDEPENDENT (its optimum disagrees with `optimal_cf`);
  2. confirm an HONEST agenda passes BOTH the endogenous and the exogenous check (no false positive);
  3. THE LOAD-BEARING TEST: build a CAPTURED advisor (a `_utility` that steers the winner to a
     citizen-dispreferred policy), show the ENDOGENOUS check passes it (steering=False), and show the
     EXOGENOUS check CATCHES it (steering=True). This is the falsification of "model-coherent ==
     non-capturable".

Deterministic, no RNG.
"""
import pytest

from governance.ai_advisor import (
    STATUS_QUO_CF,
    Option,
    adversarial_review,
    agenda_outcome,
    feasible_grid,
    honest_agenda,
    make_option,
    models_for,
    optimal_cf,
    option_diversity,
)
from governance.exogenous_preferences import (
    DEFAULT_PANEL,
    EXOGENOUS_STEERING_THRESHOLD,
    CitizenArchetype,
    exogenous_optimal_cf,
    exogenous_review,
    exogenous_utility,
)

N = 200


# --- a CAPTURED advisor: a utility that monotonically rewards high crop_fraction -------------
# This models a captor who wants maximal "import-independence theatre" (cf -> 1.0), which is
# O2-overproducing and inefficient, and which citizens (the exogenous panel) do NOT want.
def _captured_utility(cf, model, n):
    starve = 10.0 * max(0.0, -model.margin(cf))   # still avoids starvation (so it stays plausible)
    return -starve + cf                            # ...but otherwise: more crop_fraction = "better"


def _captured_make_option(cf, scenario, n):
    a, b = models_for(scenario)
    cf = round(cf, 4)
    return Option(cf=cf, feasible_A=a.feasible(cf), feasible_B=b.feasible(cf),
                  scrubbing=False, utility=round(_captured_utility(cf, a, n), 5))


def _captured_optimal_cf(scenario, n):
    grid = feasible_grid(scenario, n)
    a, _ = models_for(scenario)
    return max(grid, key=lambda cf: _captured_utility(cf, a, n))


def _captured_agenda(scenario, n):
    """A captured menu that PASSES diversity: spans the lever range, includes the status quo AND the
    honest optimum -- but its options carry the CAPTURED utility grades, so the approval tally elects
    the captor's preferred high-cf policy instead of the honest optimum on the same menu."""
    capt_opt = _captured_optimal_cf(scenario, n)
    cfs = sorted({0.66, 0.72, 0.80, STATUS_QUO_CF, capt_opt})
    return tuple(_captured_make_option(cf, scenario, n) for cf in cfs)


# --- 1. independence: the exogenous yardstick is NOT the advisor's yardstick -----------------
def test_exogenous_optimum_disagrees_with_endogenous():
    endo = optimal_cf("nominal", N)
    exo = exogenous_optimal_cf("nominal", N)
    assert endo is not None and exo is not None
    assert abs(endo - exo) > 0.05, (
        f"exogenous optimum {exo} must be able to differ from endogenous {endo}")


def test_exogenous_utility_not_derived_from_advisor_utility():
    # exogenous utility ignores the O2-net / farming-cost structure entirely: it is a panel of
    # preference kernels. A high-cf policy the advisor's _utility penalizes can still satisfy the
    # resilience archetype, and vice versa -- the two surfaces have different shape.
    panel_only = (CitizenArchetype("x", "test", ideal=0.95, tolerance=0.10),)
    assert exogenous_utility(0.95, panel_only) == pytest.approx(1.0)
    assert exogenous_utility(0.67, panel_only) == 0.0  # outside tolerance -> zero satisfaction


# --- 2. no false positive: an HONEST agenda passes BOTH checks -------------------------------
def test_honest_agenda_passes_both_checks():
    menu = honest_agenda("nominal", N)
    winner = agenda_outcome(menu, N).winner
    endo = adversarial_review(menu, "nominal", N)
    exo = exogenous_review(menu, winner, "nominal", N)
    assert endo.steering_detected is False
    assert exo.steering_detected is False
    assert exo.exo_gap <= EXOGENOUS_STEERING_THRESHOLD


# --- 3. THE LOAD-BEARING TEST: exogenous catches what endogenous misses ----------------------
def test_captured_agenda_passes_diversity_and_endogenous_review():
    """Precondition for the catch to be meaningful: the captured menu must clear the EXISTING gates
    (diversity + endogenous adversarial review). If those already rejected it, the exogenous check
    would be redundant rather than additive."""
    menu = _captured_agenda("nominal", N)
    div = option_diversity(menu, "nominal", N)
    assert div.ok is True, f"captured menu unexpectedly failed diversity: {div.reasons}"
    endo = adversarial_review(menu, "nominal", N)
    assert endo.steering_detected is False, "endogenous review should be FOOLED by the captured menu"
    # and the winner the captured menu elects is the captor's policy, far from citizens' preference
    assert endo.winner == _captured_optimal_cf("nominal", N)


def test_exogenous_check_catches_captured_steering():
    """THE FALSIFICATION: the endogenous audit passes the captured agenda (steering=False); the
    structurally-independent exogenous audit CATCHES it (steering=True)."""
    menu = _captured_agenda("nominal", N)
    winner = agenda_outcome(menu, N).winner

    endo = adversarial_review(menu, "nominal", N)
    exo = exogenous_review(menu, winner, "nominal", N)

    # endogenous: fooled
    assert endo.steering_detected is False
    # exogenous: catches it
    assert exo.steering_detected is True
    assert exo.exo_gap > EXOGENOUS_STEERING_THRESHOLD
    # ...and it points at a concretely better, OMITTED-by-the-captor option the citizens prefer
    assert exo.best_omitted is not None
    assert exo.best_omitted_exo_utility > exo.winner_exo_utility


def test_exogenous_review_noop_on_none_of_these():
    # if the disposal already refused everything (caretaker holds), there is nothing to flag.
    from governance.ruleset import NONE_OF_THESE
    menu = honest_agenda("nominal", N)
    exo = exogenous_review(menu, NONE_OF_THESE, "nominal", N)
    assert exo.steering_detected is False
    assert exo.winner_exo_utility is None


def test_exogenous_review_deterministic():
    menu = _captured_agenda("nominal", N)
    winner = agenda_outcome(menu, N).winner
    a = exogenous_review(menu, winner, "nominal", N)
    b = exogenous_review(menu, winner, "nominal", N)
    assert (a.steering_detected, a.exo_gap, a.best_omitted) == \
           (b.steering_detected, b.exo_gap, b.best_omitted)
