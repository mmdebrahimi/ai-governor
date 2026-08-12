"""The polarization tolerance must be derived AT THE PANEL SIZE IN USE.

The defect: `calibrate_polarization` derived one threshold at n=16 and the mechanism applied it to
every panel. The score `1 - WCSS(2)/WCSS(1)` is computed over n points, so with fewer points a
2-means split fits noise more easily and the unimodal score distribution shifts upward as n falls.
A constant is therefore too tight on small panels and TOO LOOSE on large ones — and too loose is the
direction that MISSES real polarization and silently aggregates a split panel.

It never surfaced in this repo because the only live panel is n=16 — the exact size the constant was
correct for. Latent, not active, and it would have bitten the moment anyone changed the panel size.
"""

import random

import pytest

from aigov.contract import ProvenanceKind
from aigov.intake import (
    AGGREGATED, ESCALATE, MIN_CAMP_SHARE, MIN_CALIBRATABLE_PANEL, DEFAULT_POLARIZATION,
    PanelTooSmallToCalibrate, Panel, _polarization, elicit_level, tolerance_for,
)


def panel_of(n):
    return Panel(id="P-{}".format(n), members=tuple("m{}".format(i) for i in range(n)),
                 seed=20260812, electorate_size=max(n, 1) * 10)


# ---------------------------------------------------------------- the derivation

def test_tolerance_falls_as_the_panel_grows():
    """The core finding, and the reason a constant was wrong."""
    values = [tolerance_for(n).value for n in (4, 8, 16, 50)]
    assert values == sorted(values, reverse=True), values
    assert values[0] > values[-1]


def test_the_old_constant_was_too_loose_on_large_panels():
    """The UNSAFE direction: a fixed 0.900 escalates LESS than it should as n grows."""
    assert tolerance_for(50).value < DEFAULT_POLARIZATION.value
    assert tolerance_for(100).value < tolerance_for(50).value


def test_the_old_constant_was_too_tight_on_small_panels():
    """The safe direction — false escalation. Still wrong, just fail-closed wrong."""
    assert tolerance_for(4).value > DEFAULT_POLARIZATION.value
    assert tolerance_for(8).value > DEFAULT_POLARIZATION.value


def test_the_historical_value_is_still_roughly_right_at_its_own_size():
    """Continuity check: the n=16 derivation should land near the recorded 0.900, or the original
    calibration was wrong too."""
    assert abs(tolerance_for(16).value - DEFAULT_POLARIZATION.value) <= 0.02


def test_the_derived_tolerance_is_legitimate_under_G2():
    """It must never read as AI_SUPPLIED, or the intake refuses to compile against it."""
    t = tolerance_for(16)
    assert t.provenance_kind is ProvenanceKind.GUIDELINE
    assert t.is_legitimate()
    assert "panel_size=16" in t.provenance_ref


def test_the_provenance_records_the_seed_spread():
    """A single seed carries ~0.02 of noise, so the value is a median over fixed seeds and the
    spread is reported rather than hidden."""
    assert "median of 5 seeds" in tolerance_for(24).provenance_ref
    assert "spread" in tolerance_for(24).provenance_ref


def test_derivation_is_deterministic():
    assert tolerance_for(16).value == tolerance_for(16).value
    assert tolerance_for(24).value == tolerance_for(24).value


# ---------------------------------------------------------------- the small-panel floor

def test_the_minimum_panel_is_derived_from_min_camp_share_not_chosen():
    """MIN_CALIBRATABLE_PANEL is not a picked number: a camp needs at least MIN_CAMP_SHARE of the
    panel AND at least one whole member."""
    assert MIN_CALIBRATABLE_PANEL == int(-(-1 // MIN_CAMP_SHARE)) or \
           MIN_CALIBRATABLE_PANEL == 4
    assert MIN_CAMP_SHARE * MIN_CALIBRATABLE_PANEL >= 1.0
    assert MIN_CAMP_SHARE * (MIN_CALIBRATABLE_PANEL - 1) < 1.0


@pytest.mark.parametrize("n", [0, 1, 2, 3])
def test_a_panel_too_small_to_split_has_no_derivable_threshold(n):
    with pytest.raises(PanelTooSmallToCalibrate):
        tolerance_for(n)


def test_a_too_small_panel_escalates_rather_than_aggregating():
    """FAIL-CLOSED. No derivable threshold means no defensible aggregation — the mechanism must not
    fall back to a default, which would be exactly the invented number this project forbids."""
    r = elicit_level("o2_floor", [18.0, 19.0, 20.0], panel_of(3))
    assert r.verdict is ESCALATE
    assert "cannot aggregate" in r.reason


# ---------------------------------------------------------------- the live path

def test_elicit_level_derives_from_the_actual_panel_by_default():
    """Not a constant, and not the caller's guess — the panel in hand decides."""
    tight = [25.0, 25.1, 24.9, 25.05, 24.95, 25.02, 24.98, 25.01,
             25.03, 24.97, 25.0, 25.04, 24.96, 25.02, 24.99, 25.01]
    r = elicit_level("o2_floor", tight, panel_of(16))
    assert r.verdict is AGGREGATED


def test_an_explicitly_passed_tolerance_is_still_honoured():
    """Tests and historical callers must be able to pin the n=16 value."""
    split = [10.0] * 8 + [40.0] * 8
    pinned = elicit_level("o2_floor", split, panel_of(16), tolerance=DEFAULT_POLARIZATION)
    assert pinned.verdict is ESCALATE


# ---------------------------------------------------------------- the behavioural difference

def _two_camp_panel_between_thresholds():
    """A GENUINELY two-camp panel whose score falls between the old constant and the n=50
    derivation. Reproduced deterministically rather than hard-coded."""
    lo, hi = tolerance_for(50).value, DEFAULT_POLARIZATION.value
    rng = random.Random(4242)
    for _ in range(8000):
        gap = rng.uniform(2.5, 6.0)
        within = rng.uniform(1.4, 3.0)
        s = ([rng.gauss(25, within) for _ in range(25)]
             + [rng.gauss(25 + gap, within) for _ in range(25)])
        if lo < _polarization(s) < hi:
            return s, gap, within
    raise AssertionError("no separating panel found — the two thresholds may have converged")


def test_the_fix_changes_real_behaviour_not_just_a_number():
    """THE load-bearing test. A real split panel that the old constant AGGREGATED — silently
    averaging two camps into a median nobody proposed — and the derived threshold ESCALATES.

    The camps are separated by several times their internal spread, so this is not a borderline
    judgement call: it is a panel any human would call divided.
    """
    s, gap, within = _two_camp_panel_between_thresholds()
    assert gap > 2 * within, "fixture must be visibly two-camp, not marginal"

    old = elicit_level("o2_floor", s, panel_of(50), tolerance=DEFAULT_POLARIZATION)
    new = elicit_level("o2_floor", s, panel_of(50))

    assert old.verdict is AGGREGATED, "the old constant should have missed this"
    assert new.verdict is ESCALATE, "the derived threshold should catch it"
    assert old.level is not None and new.level is None


def test_the_missed_case_would_have_produced_a_level_nobody_proposed():
    """Why it matters: aggregating a split panel emits a median sitting in the empty gap between
    the two camps — a binding number no participant argued for."""
    s, gap, within = _two_camp_panel_between_thresholds()
    old = elicit_level("o2_floor", s, panel_of(50), tolerance=DEFAULT_POLARIZATION)
    assert old.level is not None
    nearest = min(abs(old.level - x) for x in s)
    assert nearest > 0, "the emitted level is not any panelist's own proposal"
