"""Dense-menu capture regression (exogenous audit composition hole).

governance/exogenous_preferences.py documents (and reproduced) a hole in the OMITTED-ONLY exogenous
review: a captor who builds a DENSE, diversity-passing menu puts the citizen optimum ON the ballot, so
it is no longer "omitted" -- the omitted-only scan then finds nothing better and reports steering=False
even though the elected winner (cf=1.0) costs citizens large satisfaction. run_advised_cycle must use the
WHOLE-GRID variant so a dense captured menu is still caught and refused (caretaker holds).
"""
from governance.ai_advisor import (
    Option,
    STATUS_QUO_CF,
    feasible_grid,
    models_for,
)
from governance.exogenous_preferences import exogenous_utility, exogenous_optimal_cf
from sandbox.governance_sandbox import ColonyState, run_advised_cycle

SCEN = "nominal"
N = 300


def _dense_captured_menu():
    """A dense, diversity-passing menu whose carried utilities force the disposer to elect cf=1.0
    (citizen-dispreferred), while spanning the grid + containing the citizen optimum on-menu."""
    a, b = models_for(SCEN)
    grid = feasible_grid(SCEN, N)
    # dense spread across the feasible grid + the status quo + the captor target (1.0)
    cfs = sorted({round(cf, 4) for cf in grid[::4]} | {STATUS_QUO_CF, round(max(grid), 4)})
    target = round(max(grid), 4)
    opts = []
    for cf in cfs:
        u = 1.0 if abs(cf - target) < 1e-9 else 0.0   # only the captor target is approved
        opts.append(Option(cf=cf, feasible_A=a.feasible(cf), feasible_B=b.feasible(cf),
                           scrubbing=False, utility=u))
    return tuple(opts), target


def test_dense_captured_menu_is_caught_and_refused():
    menu, target = _dense_captured_menu()
    # sanity: the captor target really is citizen-dispreferred vs the exogenous optimum
    opt = exogenous_optimal_cf(SCEN, N)
    assert exogenous_utility(opt, ) - exogenous_utility(target, ) > 0.10, "test menu not adversarial"

    state = ColonyState(n=N, crop_fraction=STATUS_QUO_CF, scrubbing=True)
    r = run_advised_cycle(state, SCEN, N, agenda=menu)

    # the whole-grid exogenous audit must flag the dense capture ...
    assert r.exo_steering_detected is True
    # ... so the captured menu is NOT applied; the caretaker holds the (safe) prior state.
    assert r.applied is False
    assert r.state == state
