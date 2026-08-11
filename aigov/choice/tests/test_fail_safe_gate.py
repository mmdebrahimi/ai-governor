"""Regression tests for the fail-CLOSED anti-capture gate (multi-peaked escalation)."""
from governance.fail_safe_gate import (
    fail_safe_gate,
    fail_safe_ensemble_sweep,
    CERTIFY,
    STEERING_DETECTED,
    ESCALATE,
)
from governance.panel_agnostic import (
    aggregate_single_peaked,
    complete_menu,
    random_panel,
)
from governance.ai_advisor import agenda_outcome
import random


SCEN, N = "nominal", 200


def test_no_silent_failures_among_certified():
    """The headline soundness property: across a 500-panel ensemble, NO panel the gate certifies
    (in-domain) suffers a catch-faithfulness failure — because every potentially-failing
    (multi-peaked) panel is escalated first."""
    st = fail_safe_ensemble_sweep(SCEN, N, threshold=0.10, n_panels=500, seed=1)
    assert st.silent_failures_among_certified == 0


def test_escalated_set_is_exactly_the_multipeaked_set():
    """Escalation fires on precisely the out-of-domain (multi-peaked) panels — not over-conservative,
    not leaky. This is what makes the certified set sound without needlessly escalating valid panels."""
    st = fail_safe_ensemble_sweep(SCEN, N, threshold=0.10, n_panels=500, seed=1)
    assert st.escalated_equals_multipeaked is True
    # nominal has a real multi-peaked minority -> escalation must actually fire sometimes
    assert 0 < st.n_escalated < st.n_panels


def test_single_peaked_scenario_never_escalates():
    """In a scenario whose aggregates are always single-peaked (scarcity), the gate escalates nothing
    and still has zero silent failures — escalation is targeted, not blanket."""
    st = fail_safe_ensemble_sweep("scarcity", N, threshold=0.10, n_panels=300, seed=3)
    assert st.n_escalated == 0
    assert st.silent_failures_among_certified == 0


def test_gate_escalates_a_multipeaked_panel():
    """Unit: hand a known multi-peaked panel to the gate -> it returns ESCALATE with a routed
    procedure, never CERTIFY."""
    rng = random.Random(0)
    # draw panels until we find a multi-peaked one (the out-of-domain case)
    mp_panel = None
    for _ in range(200):
        p = random_panel(rng)
        if not aggregate_single_peaked(p, SCEN, N):
            mp_panel = p
            break
    assert mp_panel is not None, "expected at least one multi-peaked panel in 200 draws"
    menu = complete_menu(SCEN, N)
    winner = agenda_outcome(menu, N).winner
    v = fail_safe_gate(menu, winner, SCEN, N, mp_panel)
    assert v.label == ESCALATE
    assert v.in_domain is False
    assert v.recommended_procedure  # non-empty routed procedure
    assert v.inner is None


def test_gate_certifies_an_honest_single_peaked_menu():
    """Unit: a single-peaked panel + an honest complete menu electing its own winner -> CERTIFY
    (in-domain, completeness passes, no steering)."""
    rng = random.Random(7)
    sp_panel = None
    for _ in range(200):
        p = random_panel(rng)
        if aggregate_single_peaked(p, SCEN, N):
            sp_panel = p
            break
    assert sp_panel is not None
    menu = complete_menu(SCEN, N)
    winner = agenda_outcome(menu, N).winner
    v = fail_safe_gate(menu, winner, SCEN, N, sp_panel)
    assert v.label in (CERTIFY, STEERING_DETECTED)   # in-domain -> a real verdict, not escalation
    assert v.in_domain is True
    assert v.inner is not None


if __name__ == "__main__":
    import sys
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))
