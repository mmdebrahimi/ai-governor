"""Anti-capture sweep regression (D7 re-examination, 2026-06-07).

Pins the boundary the re-examination established: against a DIVERSITY-PASSING captured menu (one that
clears every endogenous gate), the EXISTING exogenous audit catches capture iff the steered winner costs
citizens MORE than the steering threshold. Tied to `governance/exogenous_preferences.anti_capture_sweep`
/ `catch_boundary`. No RNG; pure-function determinism.

These tests do NOT claim governance validity -- the panel is synthetic. They pin the in-sim CONDITION
under which anti-capture holds (the threshold-set protection radius), and the monotonicity of that radius.
"""
import pytest

from governance.exogenous_preferences import (
    DEFAULT_PANEL,
    anti_capture_sweep,
    catch_boundary,
    exogenous_optimal_cf,
    exogenous_utility,
)

N = 200
SC = "nominal"


def test_sweep_is_deterministic():
    a = anti_capture_sweep(SC, N)
    b = anti_capture_sweep(SC, N)
    assert [(c.threshold, c.target_cf, c.caught, c.exo_gap) for c in a] == \
           [(c.threshold, c.target_cf, c.caught, c.exo_gap) for c in b]


def test_captured_menus_always_pass_diversity():
    # The whole point: these menus clear the endogenous gate, so only the exogenous audit can catch them.
    cells = anti_capture_sweep(SC, N, thresholds=(0.10,))
    assert all(c.diversity_ok for c in cells)


def test_caught_iff_citizen_cost_exceeds_threshold():
    """The core in-sim guarantee: at a given threshold, a forced winner is flagged exactly when it costs
    citizens more exogenous satisfaction than the threshold. This is the condition anti-capture HOLDS under."""
    for thr in (0.05, 0.10, 0.20):
        cells = [c for c in anti_capture_sweep(SC, N, thresholds=(thr,)) if c.winner == c.target_cf]
        assert cells
        for c in cells:
            # exo_gap is the citizen-utility deficit of the winner vs the best omitted feasible option;
            # caught iff that gap strictly exceeds the threshold.
            assert c.caught == (c.exo_gap > thr)


def test_catch_boundary_tightens_as_threshold_tightens():
    """Smaller threshold -> smaller protection radius -> catches steering closer to the citizen optimum.
    Monotone: a stricter audit catches at least as much."""
    b05 = catch_boundary(SC, N, 0.05)
    b10 = catch_boundary(SC, N, 0.10)
    b20 = catch_boundary(SC, N, 0.20)
    assert b05 is not None and b10 is not None and b20 is not None
    # tighter threshold -> first-caught winner sits closer to the citizen optimum (smaller cf)
    assert b05.target_cf <= b10.target_cf <= b20.target_cf


def test_residual_uncaught_zone_is_bounded_by_threshold():
    """Honest boundary: a captor steering WITHIN the threshold band escapes. The residual capture the
    mechanism cannot see is exactly the set of winners costing citizens <= threshold."""
    thr = 0.10
    cells = [c for c in anti_capture_sweep(SC, N, thresholds=(thr,)) if c.winner == c.target_cf]
    uncaught = [c for c in cells if not c.caught]
    assert uncaught, "there must be a residual uncaught zone -- the mechanism is not omniscient"
    assert all(c.exo_gap <= thr for c in uncaught)


def test_large_steering_always_caught_at_default_threshold():
    """A captor pushing the outcome to the lever extreme (cf=1.0), far from the citizen optimum, is caught
    at the ratified default threshold (0.10) -- the gross-capture case the falsified endogenous check missed."""
    cells = anti_capture_sweep(SC, N, thresholds=(0.10,), targets=[1.0])
    assert len(cells) == 1
    assert cells[0].caught is True


def test_winner_at_citizen_optimum_is_not_flagged():
    """No false positive: when the elected winner IS the citizen optimum, the audit does not cry capture."""
    exo_opt = exogenous_optimal_cf(SC, N)
    cells = anti_capture_sweep(SC, N, thresholds=(0.10,), targets=[exo_opt])
    assert cells[0].caught is False
    assert cells[0].citizen_cost == 0.0
