"""F5 kernel tests. The central assertions are REFUSALS: nothing applies un-gated."""

import random

import pytest

from aigov.choice.governance.fail_safe_gate import CERTIFY, ESCALATE, STEERING_DETECTED
from aigov.choice.governance.panel_agnostic import aggregate_single_peaked, random_panel
from aigov.guidelines import RATIFIED
from aigov.kernel import (
    CERTIFIABLE_INSTRUMENTS, CandidateAction, Certification, Governor, NOT_CERTIFIABLE,
    RatificationRecord, UngatedActionError,
)
from aigov.specs.d1_lifesupport import SPEC as D1
from aigov.specs.d2_economy import SPEC as D2
from aigov.twin import ColonyTwin

SCEN = "nominal"


def gov():
    return Governor([D1, D2], RATIFIED, ColonyTwin(), scenario=SCEN)


def single_peaked_panel(n_crew=200):
    rng = random.Random(7)
    for _ in range(400):
        p = random_panel(rng)
        if aggregate_single_peaked(p, SCEN, n_crew):
            return p
    raise AssertionError("no single-peaked panel found")


def multi_peaked_panel(n_crew=200):
    rng = random.Random(0)
    for _ in range(400):
        p = random_panel(rng)
        if not aggregate_single_peaked(p, SCEN, n_crew):
            return p
    raise AssertionError("no multi-peaked panel found")


def ratify_all(action):
    return RatificationRecord("assembly", Governor._key(action))


def ratify_none(action):
    return None


# ---------------------------------------------------------------- proposal

def test_departments_propose_actions():
    props = gov().propose()
    assert props, "no department proposed anything"
    assert {a.instrument for a in props} >= {"crop_area_allocation"}


def test_every_proposal_names_a_real_department():
    g = gov()
    assert all(a.dept_id in g.specs for a in g.propose())


# ---------------------------------------------------------------- THE refusal

def test_unratified_action_cannot_be_applied():
    g = gov()
    a = next(x for x in g.propose() if x.instrument == "crop_area_allocation")
    cert = g.certify(a, single_peaked_panel(), None)
    assert not cert.appliable
    with pytest.raises(UngatedActionError):
        g.apply(cert)


def test_self_issued_ratification_does_not_count():
    """A record the governor could mint itself is not ratification."""
    g = gov()
    a = next(x for x in g.propose() if x.instrument == "crop_area_allocation")
    for body in ("governor", "kernel", "ai", "self", ""):
        cert = g.certify(a, single_peaked_panel(), RatificationRecord(body, Governor._key(a)))
        assert not cert.ratified, body
        with pytest.raises(UngatedActionError):
            g.apply(cert)


def test_ratification_for_a_different_action_does_not_transfer():
    """Ratifying action A then shipping action B is the subtle attack."""
    g = gov()
    a = next(x for x in g.propose() if x.instrument == "crop_area_allocation")
    other = CandidateAction(a.dept_id, a.instrument, a.value + 0.11, "swapped")
    cert = g.certify(other, single_peaked_panel(), RatificationRecord("assembly", Governor._key(a)))
    assert not cert.ratified
    with pytest.raises(UngatedActionError):
        g.apply(cert)


def test_there_is_no_override_path():
    """A kernel with a force flag would make 'the AI is advisory' a promise, not a property.

    Checked BEHAVIOURALLY, on the signature — an earlier version grepped the source for the word
    'override' and failed on its own docstring, which is the string-presence trap: it tested words,
    not behaviour.
    """
    import inspect
    params = list(inspect.signature(Governor.apply).parameters)
    assert params == ["self", "cert"], (
        "apply() takes {} — any extra parameter is a potential gate bypass".format(params))


def test_apply_refuses_every_non_appliable_certification_shape():
    """Exhaustive over the 8 combinations of the three gate conditions: only all-true applies."""
    import itertools
    g = gov()
    a = CandidateAction("D1", "crop_area_allocation", 0.6, "probe")
    applied = []
    for ratified, steer, ok in itertools.product([True, False], [CERTIFY, STEERING_DETECTED,
                                                                ESCALATE, NOT_CERTIFIABLE],
                                                 [True, False]):
        cert = Certification(a, ratified, steer, ok)
        if cert.appliable:
            applied.append((ratified, steer, ok))
        else:
            with pytest.raises(UngatedActionError):
                g.apply(cert)
    assert applied == [(True, CERTIFY, True)], applied


# ---------------------------------------------------------------- non-steering boundary

def test_out_of_domain_instrument_is_not_certifiable_and_is_refused():
    """The vendored gate is resource-domain specific. Outside it the kernel REFUSES rather than
    fabricating a steering check it cannot justify."""
    g = gov()
    a = CandidateAction("D2", "volume_tax_rate", 1.10, "hold")
    assert a.instrument not in CERTIFIABLE_INSTRUMENTS
    cert = g.certify(a, single_peaked_panel(), ratify_all(a))
    assert cert.ratified                      # ratified...
    assert cert.non_steering == NOT_CERTIFIABLE
    assert not cert.appliable                 # ...and STILL refused
    with pytest.raises(UngatedActionError):
        g.apply(cert)
    assert any("Refusing rather than waving it through" in n for n in cert.notes)


def test_multi_peaked_panel_escalates_and_does_not_apply():
    g = gov()
    a = next(x for x in g.propose() if x.instrument == "crop_area_allocation")
    cert = g.certify(a, multi_peaked_panel(), ratify_all(a))
    assert cert.non_steering == ESCALATE and not cert.appliable
    assert any("randomized agenda order" in n.lower() for n in cert.notes)


def test_a_fully_gated_action_does_apply():
    """The positive case must exist, or the kernel is just a refusal machine."""
    g = gov()
    a = next(x for x in g.propose() if x.instrument == "crop_area_allocation")
    ok = None
    rng = random.Random(11)
    for _ in range(400):
        p = random_panel(rng)
        cert = g.certify(a, p, ratify_all(a))
        if cert.non_steering == CERTIFY and cert.constraints_satisfied:
            ok = cert
            break
    assert ok is not None, "no panel produced a certifiable action in 400 draws"
    assert ok.appliable
    g.apply(ok)
    assert g.settings.crop_area_allocation == pytest.approx(a.value)


# ---------------------------------------------------------------- constraint satisfaction

def test_an_action_that_would_violate_a_constraint_is_refused():
    g = gov()
    bad = CandidateAction("D1", "crop_area_allocation", 1.0, "full closure")   # trips the fire bound
    cert = g.certify(bad, single_peaked_panel(), ratify_all(bad))
    assert not cert.constraints_satisfied and not cert.appliable
    assert any("would violate" in n for n in cert.notes)


def test_constraint_check_does_not_mutate_the_live_twin():
    """The probe must run on a COPY — a certification that advanced the world would be a side effect."""
    g = gov()
    before_cycle, before_pp = g.twin.cycle, g.twin.read("o2_partial_pressure_kpa")
    g.certify(CandidateAction("D1", "crop_area_allocation", 1.0, "x"),
              single_peaked_panel(), None)
    assert g.twin.cycle == before_cycle
    assert g.twin.read("o2_partial_pressure_kpa") == pytest.approx(before_pp)


# ---------------------------------------------------------------- the cycle

def test_a_cycle_with_no_ratifier_applies_nothing():
    g = gov()
    rec = g.run_cycle(single_peaked_panel(), ratify_none)
    assert rec.proposed and rec.applied == []
    assert len(rec.refused) + len(rec.escalated) == len(rec.proposed)


def test_cycle_advances_the_twin_exactly_once():
    g = gov()
    g.run_cycle(single_peaked_panel(), ratify_none)
    assert g.twin.cycle == 1
    g.run_cycle(single_peaked_panel(), ratify_none)
    assert g.twin.cycle == 2


def test_twelve_cycles_never_apply_an_ungated_action():
    """The phase-1 terminal shape, in miniature: every binding action gated or refused, 12 cycles."""
    g = gov()
    panel = single_peaked_panel()
    for _ in range(12):
        rec = g.run_cycle(panel, ratify_all)
        for _action, cert in rec.applied:
            assert cert.appliable and cert.ratified and cert.non_steering == CERTIFY
        for _action, cert in rec.refused + rec.escalated:
            assert not cert.appliable
    assert g.twin.cycle == 12
    assert len(g.history) == 12


def test_every_proposed_action_is_accounted_for_every_cycle():
    """Nothing may vanish: proposed == applied + refused + escalated."""
    g = gov()
    panel = single_peaked_panel()
    for _ in range(6):
        rec = g.run_cycle(panel, ratify_all)
        assert len(rec.proposed) == len(rec.applied) + len(rec.refused) + len(rec.escalated)


# ---------------------------------------------------------------- anti-vacuous-pass

def test_a_fully_refused_run_leaves_the_colony_ALIVE():
    """The test that was missing, and whose absence let a nonsense run pass.

    `test_twelve_cycles_never_apply_an_ungated_action` was GREEN while the governed run lost the
    atmosphere at cycle 1: the kernel started from `InstrumentSettings()` zeros, so refusing every
    action meant running life support at zero. "Nothing applied" was exactly what that test asserted,
    so it could not see the failure. A refused vote must leave the STATUS QUO standing.
    """
    g = gov()
    for _ in range(12):
        rec = g.run_cycle(single_peaked_panel(), ratify_none)
        assert rec.applied == []
        assert rec.tick.ok, "a fully-refused cycle violated: {}".format(rec.tick.violations)
    assert g.twin.read("o2_partial_pressure_kpa") == pytest.approx(21.0)


def test_status_quo_crop_fraction_is_derived_not_chosen():
    """Break-even = 1 / PLANT_O2_OVERPRODUCTION_FACTOR — from the model's biological constant."""
    from aigov.choice.models.resource_sim import PLANT_O2_OVERPRODUCTION_FACTOR
    from aigov.kernel import status_quo_settings
    assert status_quo_settings().crop_area_allocation == pytest.approx(
        1.0 / PLANT_O2_OVERPRODUCTION_FACTOR)


def test_the_default_status_quo_is_not_zeros():
    from aigov.kernel import status_quo_settings
    assert status_quo_settings().crop_area_allocation > 0.0


def test_an_explicit_status_quo_is_honoured_and_copied():
    from aigov.twin import InstrumentSettings
    sq = InstrumentSettings(crop_area_allocation=0.7)
    g = Governor([D1, D2], RATIFIED, ColonyTwin(), status_quo=sq)
    assert g.settings.crop_area_allocation == pytest.approx(0.7)
    g.settings.crop_area_allocation = 0.1
    assert sq.crop_area_allocation == pytest.approx(0.7), "caller's object was mutated"
