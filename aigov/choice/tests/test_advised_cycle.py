"""Phase-2 integration: AI-advised sandbox cycle (mars-gov-ai-advisor -> mars-gov-sandbox).

A certified, non-steering AI menu is applied via approval disposal; a strawman (optimum-omitting /
steering) menu is refused and the colony falls back to the caretaker (unchanged) policy.
"""
from governance.ai_advisor import optimal_cf, strawman_agenda
from sandbox.governance_sandbox import AdvisedCycleResult, ColonyState, run_advised_cycle


def test_certified_menu_is_applied():
    state = ColonyState(n=300, crop_fraction=0.85, scrubbing=True)
    r = run_advised_cycle(state, "nominal", 300)
    assert r.diversity_ok is True
    assert r.steering_detected is False
    assert r.applied is True
    assert abs(r.state.crop_fraction - optimal_cf("nominal", 300)) <= 0.05


def test_strawman_menu_is_refused_caretaker_holds():
    state = ColonyState(n=300, crop_fraction=0.85, scrubbing=True)
    r = run_advised_cycle(state, "nominal", 300, agenda=strawman_agenda("nominal", 300))
    assert (r.diversity_ok is False) or (r.steering_detected is True)
    assert r.applied is False
    assert r.state == state  # caretaker: policy unchanged


def test_result_is_frozen():
    state = ColonyState(n=200, crop_fraction=0.85, scrubbing=True)
    r = run_advised_cycle(state, "nominal", 200)
    assert isinstance(r, AdvisedCycleResult)


def test_captured_menu_refused_by_exogenous_gate_caretaker_holds():
    """C2-b / D7: a captured menu that PASSES diversity + the endogenous review is still REFUSED by
    the advised cycle because the exogenous (independent-preference) audit flags steering."""
    from governance.ai_advisor import (STATUS_QUO_CF, Option, feasible_grid, models_for)

    def captured_utility(cf, model, n):
        return -10.0 * max(0.0, -model.margin(cf)) + cf  # captor: maximal crop_fraction "best"

    def captured_make_option(cf, scenario, n):
        a, b = models_for(scenario)
        cf = round(cf, 4)
        return Option(cf=cf, feasible_A=a.feasible(cf), feasible_B=b.feasible(cf),
                      scrubbing=False, utility=round(captured_utility(cf, a, n), 5))

    grid = feasible_grid("nominal", 300)
    a, _ = models_for("nominal")
    capt_opt = max(grid, key=lambda cf: captured_utility(cf, a, 300))
    cfs = sorted({0.66, 0.72, 0.80, STATUS_QUO_CF, capt_opt})
    captured_menu = tuple(captured_make_option(cf, "nominal", 300) for cf in cfs)

    state = ColonyState(n=300, crop_fraction=0.85, scrubbing=True)
    r = run_advised_cycle(state, "nominal", 300, agenda=captured_menu)

    assert r.steering_detected is False        # endogenous review fooled
    assert r.exo_steering_detected is True     # exogenous audit catches it
    assert r.applied is False                  # cycle refuses the captured menu
    assert r.state == state                    # caretaker holds
