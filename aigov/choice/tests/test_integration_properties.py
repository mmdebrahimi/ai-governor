"""Property-based integration harness for the AI-advised governance cycle (Stage-C method 1).

The 2026-06-06 review: "the governance risk lives in the TRANSITIONS, not the pure predicates; the
dangerous failures are integration failures." This sweep generates many (scenario, menu, prior-state)
cases — honest / strawman / captured / random / adversarial-infeasible menus — and asserts the
INTEGRATION THEOREM on every resulting cycle:

  SAFETY        applied  => ratified ∧ diversity_ok ∧ ¬steer ∧ ¬exo_steer ∧ stages_ok
  FEASIBILITY   applied  => the applied state satisfies the survival invariants
  CARETAKER     ¬applied => the caretaker state satisfies the invariants OR honestly flags famine

Deterministic: every case is seeded (stdlib random, no external dep), so a failure is reproducible.
"""
import random

import pytest

from governance.ai_advisor import (
    CF_MIN,
    CF_MAX,
    STATUS_QUO_CF,
    Option,
    feasible_grid,
    honest_agenda,
    models_for,
    state_invariants_ok,
    strawman_agenda,
)
from governance.ruleset import NONE_OF_THESE
from sandbox.governance_sandbox import ColonyState, run_advised_cycle

SCENARIOS = ("nominal", "scarcity")
N = 200
CASES = 400


def _rand_option(rng, scenario, n, utility=None):
    a, b = models_for(scenario)
    cf = round(rng.uniform(CF_MIN, CF_MAX), 4)
    u = rng.uniform(-1.0, 1.0) if utility is None else utility
    return Option(cf=cf, feasible_A=a.feasible(cf), feasible_B=b.feasible(cf),
                  scrubbing=False, utility=round(u, 5))


def _random_menu(rng, scenario, n):
    """A menu that always contains the status quo (else agenda_outcome raises) + 2-5 random options."""
    a, b = models_for(scenario)
    sq = Option(cf=STATUS_QUO_CF, feasible_A=a.feasible(STATUS_QUO_CF),
                feasible_B=b.feasible(STATUS_QUO_CF), scrubbing=False, utility=round(rng.uniform(-1, 1), 5))
    opts = [sq] + [_rand_option(rng, scenario, n) for _ in range(rng.randint(2, 5))]
    rng.shuffle(opts)
    return tuple(opts)


def _infeasible_favoured_menu(rng, scenario, n):
    """ADVERSARIAL: an infeasible option carries the TOP utility, so the disposer would elect a starving
    policy unless the cycle guards feasibility on the applied path. The hard case for the theorem."""
    a, b = models_for(scenario)
    grid = feasible_grid(scenario, n)
    lo = min(grid) if grid else CF_MAX
    bad_cf = round(max(CF_MIN, lo - 0.10), 4)  # below the feasible floor -> starving
    sq = Option(STATUS_QUO_CF, a.feasible(STATUS_QUO_CF), b.feasible(STATUS_QUO_CF), False, 0.0)
    bad = Option(bad_cf, a.feasible(bad_cf), b.feasible(bad_cf), False, 5.0)  # top utility
    mid = _rand_option(rng, scenario, n, utility=0.1)
    return (sq, bad, mid)


def _menu_factories():
    return [
        lambda rng, s, n: honest_agenda(s, n),
        lambda rng, s, n: strawman_agenda(s, n),
        _random_menu,
        _infeasible_favoured_menu,
    ]


def _prior_state(rng, n):
    cf = round(rng.uniform(CF_MIN, CF_MAX), 4)
    return ColonyState(n=n, crop_fraction=cf, scrubbing=rng.random() < 0.5)


def test_integration_theorem_holds_over_random_cycles():
    rng = random.Random(20260606)
    factories = _menu_factories()
    checked = 0
    for i in range(CASES):
        scenario = SCENARIOS[i % len(SCENARIOS)]
        menu = factories[i % len(factories)](rng, scenario, N)
        prior = _prior_state(rng, N)
        r = run_advised_cycle(prior, scenario, N, agenda=menu)
        checked += 1

        if r.applied:
            # SAFETY: the applied path must have cleared every gate.
            assert r.ratified and r.diversity_ok, (scenario, i, "applied without ratify/diversity")
            assert not r.steering_detected and not r.exo_steering_detected, (i, "applied while steered")
            assert r.stages_ok, (i, "applied with failed stage audit")
            assert r.winner != NONE_OF_THESE
            # FEASIBILITY: an applied state must satisfy the survival invariants.
            assert state_invariants_ok(r.state.crop_fraction, r.state.scrubbing, scenario, N), \
                (scenario, i, "APPLIED A STATE THAT VIOLATES SURVIVAL INVARIANTS", r.state)
        else:
            # CARETAKER: safe state, or an honest famine flag.
            safe = state_invariants_ok(r.state.crop_fraction, r.state.scrubbing, scenario, N)
            famine = "famine" in r.caretaker_reason
            assert safe or famine, (scenario, i, "caretaker left an unsafe state", r.caretaker_reason)
    assert checked == CASES


@pytest.mark.parametrize("scenario", SCENARIOS)
def test_infeasible_favoured_menu_is_never_applied_starving(scenario):
    """Direct regression: a menu whose top-utility option is infeasible must NOT apply a starving state."""
    rng = random.Random(7)
    menu = _infeasible_favoured_menu(rng, scenario, N)
    prior = ColonyState(n=N, crop_fraction=STATUS_QUO_CF, scrubbing=True)
    r = run_advised_cycle(prior, scenario, N, agenda=menu)
    # whatever the cycle decides, the resulting state must be survivable
    assert state_invariants_ok(r.state.crop_fraction, r.state.scrubbing, scenario, N)
