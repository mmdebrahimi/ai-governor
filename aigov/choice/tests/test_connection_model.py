"""Validation for the Earth<->Mars connection model (family mars-gov-connection-model).

H1: the model reproduces the umbilical->tether->handshake arc — early cycles import-dependent
(veto-survivable False), late cycles self-sufficient (veto-survivable True), with a computable crossover;
blackout cycles force zero-Earth-contact governance; latency stays within light-time bounds.
H2: the resupplier-as-coercer veto is LIVE while import-dependent and VOID once self-sufficient — a
withheld resupply starves the colony in the tether phase but not the handshake phase.
"""
import pytest

from governance.connection import (
    LATENCY_MAX_MIN,
    LATENCY_MIN_MIN,
    connection_at,
    crop_capacity_pc,
    demand_pc,
    import_needed_pc,
    imported_food_pc,
    is_blackout,
    resupplier_veto_survivable,
    round_trip_latency_min,
    self_sufficiency_cycle,
    self_sufficient,
    timeline,
)

N = 300


# --- blackout (zero-Earth-contact governance) -------------------------------
def test_blackout_periodic():
    assert is_blackout(0) and is_blackout(1)        # conjunction window
    assert not is_blackout(5)
    assert is_blackout(26) and is_blackout(27)      # next synodic period
    assert not is_blackout(13)


def test_blackout_rejects_negative():
    with pytest.raises(ValueError):
        is_blackout(-1)


# --- latency within physical bounds -----------------------------------------
@pytest.mark.parametrize("cycle", [0, 3, 7, 13, 20, 26, 40])
def test_latency_in_bounds(cycle):
    lat = round_trip_latency_min(cycle)
    assert LATENCY_MIN_MIN - 1e-9 <= lat <= LATENCY_MAX_MIN + 1e-9


# --- the umbilical -> tether -> handshake arc (H1) ---------------------------
def test_early_import_dependent():
    assert self_sufficient(0) is False
    assert import_needed_pc(0) > 0
    assert connection_at(0).phase in ("umbilical", "tether")


def test_late_self_sufficient():
    xover = self_sufficiency_cycle()
    late = xover + 5
    assert self_sufficient(late) is True
    assert import_needed_pc(late) == 0.0
    assert connection_at(late).phase == "handshake"


def test_crossover_is_computable_and_monotone():
    xover = self_sufficiency_cycle()
    assert xover is not None and xover > 0
    assert self_sufficient(xover) is True
    assert self_sufficient(xover - 1) is False
    # capacity is monotone non-decreasing
    caps = [crop_capacity_pc(c) for c in range(0, xover + 10, 5)]
    assert all(b >= a for a, b in zip(caps, caps[1:]))


def test_capacity_never_closes_loop_when_growth_zero():
    assert self_sufficiency_cycle(growth=0.0) is None
    assert self_sufficient(1000, growth=0.0) is False


# --- resupplier-as-coercer survival veto (H2) -------------------------------
def test_veto_live_while_import_dependent():
    assert resupplier_veto_survivable(0) is False        # veto LIVE
    # withholding resupply in the tether phase leaves a food deficit
    assert imported_food_pc(0, withheld=True) == 0.0
    assert import_needed_pc(0) > 0                        # demand unmet -> coercion bites


def test_veto_void_once_self_sufficient():
    late = self_sufficiency_cycle() + 5
    assert resupplier_veto_survivable(late) is True       # veto VOID
    assert import_needed_pc(late) == 0.0
    # withholding resupply now changes nothing — the colony needs no imports
    assert imported_food_pc(late, withheld=True) == imported_food_pc(late, withheld=False) == 0.0


def test_veto_survivability_flips_exactly_at_crossover():
    xover = self_sufficiency_cycle()
    assert resupplier_veto_survivable(xover - 1) is False
    assert resupplier_veto_survivable(xover) is True


# --- timeline + guards ------------------------------------------------------
def test_timeline_shape():
    tl = timeline(60)
    assert len(tl) == 60
    assert any(not s.earth_contact for s in tl)          # at least one blackout
    assert tl[0].cycle == 0 and tl[-1].cycle == 59
    # the arc: starts veto-live, ends veto-void
    assert tl[0].veto_survivable is False
    assert tl[-1].veto_survivable is True


def test_guards():
    with pytest.raises(ValueError):
        timeline(0)
    with pytest.raises(ValueError):
        connection_at(-1)
    assert demand_pc() > 0
