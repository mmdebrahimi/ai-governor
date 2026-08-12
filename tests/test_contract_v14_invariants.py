"""V14 invariants: I4' (target-metric gaming), I8b (allocative tier + capture), I12 (redress),
I13 (no profile-by-resemblance), I14 (equilibrium).

Every test mutates a DEEP COPY of a LIVE reference spec rather than a toy fixture. A toy spec has
none of the surrounding complexity that lets an invariant pass for the wrong reason — and the
first thing these invariants found was a real gap in D2, not a synthetic one.

Each invariant must be INDIVIDUALLY triggerable, and each must have a stated boundary where it
correctly does NOT fire. An invariant that fires on everything is not a check, it is a tax.
"""

import copy
from dataclasses import replace

import pytest

from aigov.contract import (
    ClassificationBasis, Direction, EquilibriumKind, Instrument, InstrumentClass, Metric,
    ObjectiveRef, PersonClassification, RatificationClass, Reversibility, validate,
    validate_registry,
)
from aigov.guidelines import RATIFIED
from aigov.specs.d1_lifesupport import SPEC as D1
from aigov.specs.d2_economy import SPEC as D2


def codes(errs):
    return [e.code for e in errs]


def only(errs, code):
    return [e for e in errs if e.code == code]


# ---------------------------------------------------------------- the live registry is clean

def test_live_registry_satisfies_every_v14_invariant():
    """The reference departments must actually SATISFY the new invariants, not merely coexist."""
    assert validate_registry([D1, D2], RATIFIED) == []


@pytest.mark.parametrize("spec", [D1, D2])
def test_every_live_target_metric_is_declared_with_its_gaming_exposure(spec):
    """Regression pin for the real defect I4' found: D2 was JUDGED on a metric it never declared.

    This is the gap that mattered — the two metrics carrying gaming models were the two nobody
    scored the department against.
    """
    declared = {m.name: m for m in spec.metrics}
    for obj in spec.objectives_received:
        m = declared.get(obj.metric)
        assert m is not None, "{} is targeted on undeclared metric {!r}".format(spec.id, obj.metric)
        assert m.gaming_model.strip()
        assert m.ratchet_exposed is not None and m.threshold_exposed is not None


@pytest.mark.parametrize("spec", [D1, D2])
def test_every_live_department_has_assessed_its_equilibrium(spec):
    assert spec.equilibrium is not EquilibriumKind.UNASSESSED


# ---------------------------------------------------------------- I4'

def test_objective_on_an_undeclared_metric_is_an_error():
    bad = copy.deepcopy(D1)
    bad.objectives_received = [ObjectiveRef(guideline_id="G-D-005", metric="unmodelled_thing",
                                            direction=Direction.RAISE)]
    errs = only(validate(bad, RATIFIED), "I4'")
    assert errs and "no Metric declares it" in errs[0].message


def test_target_metric_with_unassessed_gaming_shapes_is_an_error():
    bad = copy.deepcopy(D1)
    bad.metrics = [replace(m, ratchet_exposed=None, threshold_exposed=None)
                   if m.name == "closure_fraction" else m for m in D1.metrics]
    errs = only(validate(bad, RATIFIED), "I4'")
    assert errs and "unassessed for the named gaming shapes" in errs[0].message


def test_half_assessed_is_still_unassessed():
    """Answering the ratchet question and skipping the threshold one is not an assessment."""
    bad = copy.deepcopy(D1)
    bad.metrics = [replace(m, threshold_exposed=None) if m.name == "closure_fraction" else m
                   for m in D1.metrics]
    assert only(validate(bad, RATIFIED), "I4'")


def test_a_NON_target_metric_needs_no_gaming_exposure():
    """BOUNDARY. I4' bites on the measure the department is JUDGED on, not on every diagnostic.

    D1's o2_margin_days is a live example: declared, useful, unassessed, and correctly silent.
    """
    m = {x.name: x for x in D1.metrics}["o2_margin_days"]
    assert m.ratchet_exposed is None and m.threshold_exposed is None
    assert only(validate(D1, RATIFIED), "I4'") == []


# ---------------------------------------------------------------- I8b

def _allocative(**kw):
    base = dict(name="rationing", iclass=InstrumentClass.QUANTITY_ALLOCATION, bounds=(0.0, 1.0),
                latency_cycles=1, reversibility=Reversibility.REVERSIBLE,
                ratification_class=RatificationClass.SIMPLE,
                discretion_tier="central", capture_check="audited by D15")
    base.update(kw)
    return Instrument(**base)


def test_allocative_instrument_without_a_named_discretion_tier_is_an_error():
    bad = copy.deepcopy(D1)
    bad.instruments = [_allocative(discretion_tier="")]
    errs = only(validate(bad, RATIFIED), "I8b")
    assert errs and "tier at which discretion actually sits" in errs[0].message


def test_allocative_instrument_without_a_capture_check_is_an_error():
    bad = copy.deepcopy(D1)
    bad.instruments = [_allocative(capture_check="")]
    errs = only(validate(bad, RATIFIED), "I8b")
    assert errs and "capture check" in errs[0].message


def test_the_two_I8b_failures_are_independent():
    bad = copy.deepcopy(D1)
    bad.instruments = [_allocative(discretion_tier="", capture_check="")]
    assert len(only(validate(bad, RATIFIED), "I8b")) == 2


def test_price_and_rule_instruments_need_no_tier_or_capture_check():
    """BOUNDARY. Capture is an ALLOCATION risk. D2 sets prices and rules only and never trips I8b."""
    assert only(validate(D2, RATIFIED), "I8b") == []


def test_I8b_fires_even_at_HIGH_legitimacy():
    """HIGH legitimacy licenses allocation (I8); it does not excuse naming where discretion sits.

    Without this, subsidiarity would read as 'devolution is good', which is the reading the
    evidence rejects.
    """
    from aigov.contract import Legitimacy
    bad = copy.deepcopy(D1)
    assert bad.central_legitimacy is Legitimacy.HIGH
    bad.instruments = [_allocative(discretion_tier="")]
    assert only(validate(bad, RATIFIED), "I8b")


# ---------------------------------------------------------------- I12

def _classification(**kw):
    base = dict(name="benefit_eligibility", basis=ClassificationBasis.DECLARED_RULE,
                accountable_human="D15 case officer, named per decision",
                redress_route="appeal to D13 with the department bearing the burden of proof")
    base.update(kw)
    return PersonClassification(**base)


def test_a_well_formed_person_classification_is_accepted():
    ok = copy.deepcopy(D1)
    ok.person_classifications = [_classification()]
    assert only(validate(ok, RATIFIED), "I12") == []


@pytest.mark.parametrize("field,value,fragment", [
    ("accountable_human", "", "names no accountable human"),
    ("redress_route", "", "no redress route"),
    ("redress_requires_subject_to_disprove", True, "burden on the SUBJECT"),
    ("cited_as_justification", True, "cited AS the justification"),
])
def test_each_redress_failure_is_individually_triggerable(field, value, fragment):
    bad = copy.deepcopy(D1)
    bad.person_classifications = [_classification(**{field: value})]
    errs = only(validate(bad, RATIFIED), "I12")
    assert len(errs) == 1 and fragment in errs[0].message


def test_a_department_that_classifies_nobody_trips_nothing():
    """BOUNDARY. Most departments act on things, not people."""
    assert D1.person_classifications == [] and D2.person_classifications == []
    assert only(validate_registry([D1, D2], RATIFIED), "I12") == []


# ---------------------------------------------------------------- I13

def test_classification_by_resemblance_to_a_prior_adverse_case_is_refused():
    bad = copy.deepcopy(D1)
    bad.person_classifications = [
        _classification(basis=ClassificationBasis.SIMILARITY_TO_PRIOR_ADVERSE_CASE)]
    errs = only(validate(bad, RATIFIED), "I13")
    assert errs and "prior adverse case" in errs[0].message


def test_I13_fires_on_an_OTHERWISE_PERFECT_classification():
    """The distinct failure. Named human, real redress, not cited as justification — and still
    refused, because the CATEGORY itself was never authorised by anyone.

    This is the separation that matters: I12 is about what happens after you are classified,
    I13 is about whether the class should exist. A system with flawless redress that still
    profiles by resemblance has fixed the visible half.
    """
    bad = copy.deepcopy(D1)
    pc = _classification(basis=ClassificationBasis.SIMILARITY_TO_PRIOR_ADVERSE_CASE)
    bad.person_classifications = [pc]
    errs = validate(bad, RATIFIED)
    assert only(errs, "I13") and only(errs, "I12") == []


@pytest.mark.parametrize("basis", [ClassificationBasis.DECLARED_RULE,
                                   ClassificationBasis.MEASURED_ATTRIBUTE])
def test_authorised_bases_pass(basis):
    ok = copy.deepcopy(D1)
    ok.person_classifications = [_classification(basis=basis)]
    assert only(validate(ok, RATIFIED), "I13") == []


# ---------------------------------------------------------------- I14

def test_a_department_with_instruments_must_have_assessed_its_equilibrium():
    bad = copy.deepcopy(D1)
    bad.equilibrium = EquilibriumKind.UNASSESSED
    errs = only(validate(bad, RATIFIED), "I14")
    assert errs and "self-reinforcing adverse equilibrium" in errs[0].message


def test_unassessed_is_the_DEFAULT_so_the_invariant_bites_by_construction():
    """A new department must opt IN to 'incremental action is safe here'."""
    from aigov.contract import DepartmentSpec, VSMLayer, Legitimacy
    fresh = DepartmentSpec(id="Dx", vsm_layer=VSMLayer.S1, central_legitimacy=Legitimacy.HIGH)
    assert fresh.equilibrium is EquilibriumKind.UNASSESSED


def test_adverse_equilibrium_without_an_escalation_route_is_an_error():
    """Rothstein's case: a body that can only emit a smaller version of the same advice."""
    bad = copy.deepcopy(D2)
    bad.equilibrium = EquilibriumKind.SELF_REINFORCING_ADVERSE
    bad.no_safe_increment_escalation = ""
    errs = only(validate(bad, RATIFIED), "I14")
    assert errs and "no incremental recommendation is safe here" in errs[0].message


def test_adverse_equilibrium_WITH_an_escalation_route_is_accepted():
    """The point of I14: the system must be ABLE to represent 'nothing incremental is safe'.

    If this test failed, I14 would be forbidding the finding instead of encoding it.
    """
    ok = copy.deepcopy(D2)
    ok.equilibrium = EquilibriumKind.SELF_REINFORCING_ADVERSE
    ok.no_safe_increment_escalation = ("escalate to D13 with a NO-INCREMENT finding; the fiscal "
                                       "instruments are withheld rather than re-tuned")
    assert only(validate(ok, RATIFIED), "I14") == []


def test_a_department_with_no_instruments_need_not_assess():
    """BOUNDARY. I14 is about ACTING incrementally. An advisory-only department cannot act."""
    from aigov.contract import DepartmentSpec, VSMLayer, Legitimacy
    watcher = DepartmentSpec(id="Dw", vsm_layer=VSMLayer.S4, central_legitimacy=Legitimacy.MEDIUM)
    assert watcher.equilibrium is EquilibriumKind.UNASSESSED
    assert only(validate(watcher, RATIFIED), "I14") == []


# ---------------------------------------------------------------- the admission gate

def _invalid_registry():
    bad = copy.deepcopy(D1)
    bad.equilibrium = EquilibriumKind.UNASSESSED
    bad.person_classifications = [
        PersonClassification("risk_profile", ClassificationBasis.SIMILARITY_TO_PRIOR_ADVERSE_CASE,
                             accountable_human="", redress_route="",
                             redress_requires_subject_to_disprove=True,
                             cited_as_justification=True)]
    return [bad, copy.deepcopy(D2)]


def test_the_kernel_refuses_a_registry_that_violates_the_contract():
    """The gap this closed: `validate` existed and fired, but NOTHING at the runtime boundary
    called it, so the invariants bound only at authoring time — by discipline, not by structure.

    Found by running the kernel against a deliberately invalid spec. It constructed happily with
    six violations outstanding and then proposed two actions from the offending department.
    """
    from aigov.kernel import Governor, InvalidRegistryError
    from aigov.twin import ColonyTwin
    with pytest.raises(InvalidRegistryError) as exc:
        Governor(_invalid_registry(), RATIFIED, ColonyTwin())
    msg = str(exc.value)
    assert "I13" in msg and "I14" in msg and "I12" in msg


def test_the_valid_live_registry_is_still_admitted():
    """The gate must not be a wall. The real departments go through unchanged."""
    from aigov.kernel import Governor
    from aigov.twin import ColonyTwin
    g = Governor([D1, D2], RATIFIED, ColonyTwin())
    assert set(g.specs) == {"D1", "D2"}


def test_the_refusal_precedes_any_proposal():
    """Anti-vacuous: refusing at APPLY time would still have let a broken department propose.

    The object must not exist at all, so there is no instance to call propose() on.
    """
    from aigov.kernel import Governor, InvalidRegistryError
    from aigov.twin import ColonyTwin
    try:
        Governor(_invalid_registry(), RATIFIED, ColonyTwin())
    except InvalidRegistryError:
        return
    pytest.fail("kernel admitted an invalid registry")


def test_admission_and_action_gating_are_different_refusals():
    """InvalidRegistryError rejects a REGISTRY at construction; UngatedActionError rejects one
    ACTION at apply. Collapsing them would lose the distinction between a broken department and
    a legitimate department proposing something unratified."""
    from aigov.kernel import InvalidRegistryError, UngatedActionError
    assert not issubclass(InvalidRegistryError, UngatedActionError)
    assert not issubclass(UngatedActionError, InvalidRegistryError)


# ---------------------------------------------------------------- anti-vacuous-pass

def test_the_five_new_invariants_are_all_reachable_from_one_registry():
    """Guard against a check that can never fire. Every V14 code must be producible.

    The prior failure mode in this project was a test that was green because nothing happened;
    this asserts the opposite — that each new invariant CAN come out non-empty.
    """
    bad1 = copy.deepcopy(D1)
    bad1.metrics = [replace(m, ratchet_exposed=None, threshold_exposed=None)
                    if m.name == "closure_fraction" else m for m in D1.metrics]
    bad1.instruments = [_allocative(discretion_tier="", capture_check="")]
    bad1.equilibrium = EquilibriumKind.UNASSESSED
    bad1.person_classifications = [
        _classification(basis=ClassificationBasis.SIMILARITY_TO_PRIOR_ADVERSE_CASE,
                        accountable_human="")]
    produced = set(codes(validate(bad1, RATIFIED)))
    assert {"I4'", "I8b", "I12", "I13", "I14"} <= produced, produced
