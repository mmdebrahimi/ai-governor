"""Positive tests: the two reference specs are valid, and the contract's semantics hold."""

import pytest

from aigov.contract import (
    GuidelineType, InstrumentClass, Legitimacy, ProvenanceKind, Role, fuller_lint,
    validate, validate_registry, Rule,
)
from aigov.guidelines import RATIFIED
from aigov.specs.d1_lifesupport import SPEC as D1
from aigov.specs.d2_economy import SPEC as D2

ALL_SPECS = [D1, D2]


# ---------------------------------------------------------------- H1: both specs are expressible

def test_d1_validates_clean():
    assert validate(D1, RATIFIED) == []


def test_d2_validates_clean():
    assert validate(D2, RATIFIED) == []


def test_registry_validates_clean():
    """H1: a HIGH- and a LOW-legitimacy department are both expressible under ONE schema."""
    assert validate_registry(ALL_SPECS, RATIFIED) == []


def test_specs_span_opposite_legitimacy_ratings():
    ratings = {s.central_legitimacy for s in ALL_SPECS}
    assert Legitimacy.HIGH in ratings and Legitimacy.LOW in ratings


# ---------------------------------------------------------------- I6: the falsification tests run

@pytest.mark.parametrize("spec", ALL_SPECS, ids=lambda s: s.id)
def test_falsification_test_is_executable(spec):
    assert callable(spec.falsification_test)
    assert isinstance(spec.falsification_test(), bool)


@pytest.mark.parametrize("spec", ALL_SPECS, ids=lambda s: s.id)
def test_falsification_test_currently_holds(spec):
    assert spec.falsification_test() is True


# ---------------------------------------------------------------- I8: the subsidiarity engine

def test_low_legitimacy_department_uses_only_rules_and_prices():
    assert D2.central_legitimacy is Legitimacy.LOW
    classes = {i.iclass for i in D2.instruments}
    assert InstrumentClass.QUANTITY_ALLOCATION not in classes
    assert classes <= {InstrumentClass.RULE, InstrumentClass.PRICE}


def test_high_legitimacy_department_may_allocate_quantities():
    """The asymmetry is the point: the same instrument class is legal here and illegal in D2."""
    assert D1.central_legitimacy is Legitimacy.HIGH
    assert any(i.iclass is InstrumentClass.QUANTITY_ALLOCATION for i in D1.instruments)
    assert validate(D1, RATIFIED) == []


# ---------------------------------------------------------------- I3: coupling is bilateral

def test_d1_d2_contention_is_declared_by_both_sides():
    d1_vars = {c.shared_var for c in D1.couplings if c.other_dept == "D2"}
    d2_vars = {c.shared_var for c in D2.couplings if c.other_dept == "D1"}
    assert d1_vars == d2_vars == {"pressurized_volume_m3", "power_kw"}


# ---------------------------------------------------------------- I9: separation of powers

@pytest.mark.parametrize("spec", ALL_SPECS, ids=lambda s: s.id)
def test_no_department_holds_two_powers(spec):
    assert len(spec.roles) <= 1


def test_reference_departments_only_generate():
    """Neither reference department decides or verifies — that is D3's and D15's job (D1 ratified)."""
    for spec in ALL_SPECS:
        assert spec.roles == frozenset({Role.GENERATE})


# ---------------------------------------------------------------- I11 + the guideline partition

@pytest.mark.parametrize("spec", ALL_SPECS, ids=lambda s: s.id)
def test_every_threshold_traces_to_a_guideline_or_a_constant(spec):
    carriers = list(spec.objectives_received) + list(spec.hard_constraints)
    for c in carriers:
        if c.threshold is not None:
            assert c.threshold_provenance is not None
            assert c.threshold_provenance.kind is not ProvenanceKind.AI_SUPPLIED


def test_aspiration_guideline_is_never_referenced():
    """G-A-006 is ratified but type A: it may not bind anything (probe B1)."""
    assert RATIFIED["G-A-006"].gtype is GuidelineType.A
    assert RATIFIED["G-A-006"].is_binding() is False
    referenced = {o.guideline_id for s in ALL_SPECS for o in s.objectives_received}
    referenced |= {c.guideline_id for s in ALL_SPECS for c in s.hard_constraints}
    assert "G-A-006" not in referenced


def test_ordering_guideline_binds_without_any_number():
    """The clean compile: G-O-002 constrains a SHAPE, so it needs no elicited level."""
    c = next(c for c in D2.hard_constraints if c.guideline_id == "G-O-002")
    assert c.threshold is None
    assert RATIFIED["G-O-002"].gtype is GuidelineType.O
    assert validate(D2, RATIFIED) == []


def test_floor_guidelines_carry_an_elicited_level():
    for gid in ("G-F-003", "G-F-004"):
        g = RATIFIED[gid]
        assert g.gtype is GuidelineType.F
        assert g.level is not None, "type-F guideline must arrive with its level elicited"
        assert g.elicitation_complete()


def test_direction_guideline_carries_a_metric():
    g = RATIFIED["G-D-005"]
    assert g.gtype is GuidelineType.D and g.metric and g.elicitation_complete()


# ---------------------------------------------------------------- I4 / I7 / I10

@pytest.mark.parametrize("spec", ALL_SPECS, ids=lambda s: s.id)
def test_every_metric_declares_a_gaming_model(spec):
    assert spec.metrics, "a department with no metrics cannot be audited"
    for m in spec.metrics:
        assert m.gaming_model.strip()


@pytest.mark.parametrize("spec", ALL_SPECS, ids=lambda s: s.id)
def test_every_department_sunsets(spec):
    assert spec.sunset_cycles > 0


def test_emitted_rules_pass_the_fuller_linter():
    for r in D2.rules:
        assert fuller_lint(r, current_cycle=0, dept="D2") == []


def test_fuller_linter_catches_a_bad_rule():
    """The linter must be able to fail, or it is not a linter."""
    bad = Rule(id="R-BAD", applies_to_class="person:citizen-17", published=False,
               effective_cycle=-5, predicate="", enforcement_ref="", sunset_cycles=0)
    codes = {e.code for e in fuller_lint(bad, current_cycle=3, dept="D2")}
    assert codes == {"FULLER-1", "FULLER-2", "FULLER-3", "FULLER-4", "FULLER-7", "FULLER-8"}
