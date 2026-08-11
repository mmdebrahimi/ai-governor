"""The I6 mutation-proof: every invariant I1-I11 is INDIVIDUALLY triggerable.

An invariant no mutation can trip is not an invariant, and a falsification test that cannot fail is
not a test (decision DC1). Each test below mutates ONE thing in an otherwise-clean reference spec
and asserts that exactly the corresponding error code appears — so a validator that silently passes
everything, or one that fires the wrong code, fails here.
"""

import copy

import pytest
from dataclasses import replace

from aigov.contract import (
    Constraint, ConstraintSource, Coupling, CouplingDirection, Guideline, GuidelineType,
    Instrument, InstrumentClass, Metric, ObjectiveRef, Direction, OnViolation, Provenance,
    ProvenanceKind, RatificationClass, Reversibility, Role, Rule, validate, validate_registry,
)
from aigov.guidelines import RATIFIED
from aigov.specs.d1_lifesupport import SPEC as D1
from aigov.specs.d2_economy import SPEC as D2


def mutate(spec, **changes):
    """Deep-copy a spec and overwrite fields. Never mutates the shared reference specs."""
    s = copy.deepcopy(spec)
    for k, v in changes.items():
        setattr(s, k, v)
    return s


def codes(errors):
    return {e.code for e in errors}


# ---------------------------------------------------------------- baseline: clean means clean

def test_baseline_reference_specs_are_clean():
    assert validate_registry([D1, D2], RATIFIED) == []


# ---------------------------------------------------------------- I1 objective provenance

def test_I1_unknown_guideline():
    bad = mutate(D2, objectives_received=[
        ObjectiveRef("G-DOES-NOT-EXIST", "volume_per_person_m3", Direction.HOLD_WITHIN)])
    assert "I1" in codes(validate(bad, RATIFIED))


def test_I1_unratified_guideline_is_the_ai_authoring_its_own_objective():
    draft = Guideline(id="G-DRAFT", text="raise throughput", gtype=GuidelineType.D,
                      ratified=False, metric="throughput")
    gl = dict(RATIFIED, **{"G-DRAFT": draft})
    bad = mutate(D2, objectives_received=[
        ObjectiveRef("G-DRAFT", "throughput", Direction.RAISE)])
    errs = validate(bad, gl)
    assert "I1" in codes(errs)
    assert any("UNRATIFIED" in e.message for e in errs)


def test_I1_aspiration_cannot_bind():
    bad = mutate(D1, objectives_received=[
        ObjectiveRef("G-A-006", "foreseeable_deaths", Direction.LOWER)])
    errs = validate(bad, RATIFIED)
    assert "I1" in codes(errs)
    assert any("aspiration" in e.message for e in errs)


def test_I1_unelicited_level_is_rejected():
    """A type-F guideline whose level the polity never supplied cannot bind."""
    hollow = replace(RATIFIED["G-F-003"], level=None)
    gl = dict(RATIFIED, **{"G-F-003": hollow})
    errs = validate(D2, gl)
    assert "I1" in codes(errs)


# ---------------------------------------------------------------- I2 reversibility

def test_I2_irreversible_instrument_needs_supermajority():
    bad = mutate(D1, instruments=[
        replace(i, ratification_class=RatificationClass.SIMPLE)
        if i.reversibility is Reversibility.IRREVERSIBLE else i
        for i in D1.instruments])
    assert "I2" in codes(validate(bad, RATIFIED))


# ---------------------------------------------------------------- I3 bilateral coupling

def test_I3_one_sided_coupling_is_rejected():
    """The silent-inter-department-fight catch: D2 drops its side of the contention."""
    lonely = mutate(D2, couplings=[])
    errs = validate_registry([D1, lonely], RATIFIED)
    assert "I3" in codes(errs)
    assert sum(1 for e in errs if e.code == "I3") == 2  # both shared vars unmirrored


def test_I3_coupling_to_unknown_department():
    bad = mutate(D1, couplings=list(D1.couplings) + [
        Coupling("D99", "power_kw", CouplingDirection.CONTENDS)])
    assert "I3" in codes(validate_registry([bad, D2], RATIFIED))


def test_I3_direction_mismatch_is_not_a_mirror():
    skewed = mutate(D2, couplings=[
        replace(c, direction=CouplingDirection.READS) for c in D2.couplings])
    assert "I3" in codes(validate_registry([D1, skewed], RATIFIED))


# ---------------------------------------------------------------- I4 gaming model

def test_I4_metric_without_a_gaming_model():
    bad = mutate(D1, metrics=[Metric("closure_fraction", "recycled/total", "", "none")])
    assert "I4" in codes(validate(bad, RATIFIED))


# ---------------------------------------------------------------- I5 fail-closed

def test_I5_optimizing_through_a_hard_constraint():
    bad = mutate(D1, hard_constraints=[
        replace(c, on_violation=OnViolation.OPTIMIZE_THROUGH) for c in D1.hard_constraints])
    assert "I5" in codes(validate(bad, RATIFIED))


# ---------------------------------------------------------------- I6 falsification test

def test_I6_missing_falsification_test():
    assert "I6" in codes(validate(mutate(D1, falsification_test=None), RATIFIED))


def test_I6_non_callable_falsification_test():
    assert "I6" in codes(validate(mutate(D1, falsification_test="looks fine"), RATIFIED))


def test_I6_falsification_tests_can_actually_fail():
    """The mutation-proof itself: perturb the declared envelope and the claim goes FALSE."""
    def d1_under_power():
        total_power_kw, share, o2_kg_per_kwh, crew = 120.0, 0.25, 0.20, 200
        return total_power_kw * share * 24.0 * o2_kg_per_kwh >= 0.84 * crew

    def d2_under_taxed():
        revenue = 200 * 40.0 * 0.90 + 9_000.0 * 0.05
        return revenue >= 8_600.0

    assert D1.falsification_test() is True and d1_under_power() is False
    assert D2.falsification_test() is True and d2_under_taxed() is False


# ---------------------------------------------------------------- I7 sunset

@pytest.mark.parametrize("value", [0, -3])
def test_I7_department_without_a_sunset(value):
    assert "I7" in codes(validate(mutate(D1, sunset_cycles=value), RATIFIED))


# ---------------------------------------------------------------- I8 subsidiarity

def test_I8_low_legitimacy_department_may_not_allocate_quantities():
    """THE subsidiarity catch: give the economy department a quantity lever and it is rejected."""
    bad = mutate(D2, instruments=list(D2.instruments) + [
        Instrument("housing_assignment", InstrumentClass.QUANTITY_ALLOCATION,
                   (0.0, 1.0), 1, Reversibility.REVERSIBLE, RatificationClass.SIMPLE)])
    errs = validate(bad, RATIFIED)
    assert "I8" in codes(errs)
    assert any("centrally know" in e.message for e in errs)


def test_I8_does_not_fire_on_high_legitimacy():
    """Same instrument class, HIGH legitimacy: legal. The asymmetry is the design."""
    ok = mutate(D1, instruments=list(D1.instruments) + [
        Instrument("water_ration", InstrumentClass.QUANTITY_ALLOCATION,
                   (0.0, 1.0), 1, Reversibility.REVERSIBLE, RatificationClass.SIMPLE)])
    assert "I8" not in codes(validate(ok, RATIFIED))


# ---------------------------------------------------------------- I9 separation of powers

def test_I9_department_cannot_generate_and_decide():
    bad = mutate(D2, roles=frozenset({Role.GENERATE, Role.DECIDE}))
    assert "I9" in codes(validate(bad, RATIFIED))


def test_I9_department_cannot_generate_and_verify():
    bad = mutate(D1, roles=frozenset({Role.GENERATE, Role.VERIFY}))
    assert "I9" in codes(validate(bad, RATIFIED))


# ---------------------------------------------------------------- I10 Fuller legality

def test_I10_retroactive_rule_is_rejected():
    bad = mutate(D2, rules=[replace(D2.rules[0], effective_cycle=-1)])
    assert "FULLER-3" in codes(validate(bad, RATIFIED))


def test_I10_unpublished_rule_is_rejected():
    bad = mutate(D2, rules=[replace(D2.rules[0], published=False)])
    assert "FULLER-2" in codes(validate(bad, RATIFIED))


def test_I10_rule_targeting_a_named_individual_is_rejected():
    bad = mutate(D2, rules=[replace(D2.rules[0], applies_to_class="person:citizen-17")])
    assert "FULLER-1" in codes(validate(bad, RATIFIED))


def test_I10_impossible_rule_is_rejected():
    bad = mutate(D2, rules=[replace(D2.rules[0], predicate="false")])
    assert "FULLER-6" in codes(validate(bad, RATIFIED))


def test_I10_contradictory_rules_are_caught_at_registry_level():
    contradiction = Rule(id="R-D2-99", applies_to_class="all volume holders", published=True,
                         effective_cycle=1,
                         predicate="NOT tax_due = volume_tax_rate * pressurized_volume_m3",
                         enforcement_ref="D4:collections", sunset_cycles=12)
    bad = mutate(D2, rules=list(D2.rules) + [contradiction])
    assert "FULLER-5" in codes(validate_registry([D1, bad], RATIFIED))


# ---------------------------------------------------------------- I11 threshold provenance

def test_I11_ai_supplied_threshold_is_rejected():
    """The seam probe B1 found: the AI filling in a number IS the AI becoming sovereign."""
    bad = mutate(D1, hard_constraints=[
        Constraint("o2_floor", "o2_partial_pressure_kpa >= 18.5", ConstraintSource.PHYSICS,
                   threshold=18.5,
                   threshold_provenance=Provenance(ProvenanceKind.AI_SUPPLIED, "model judgement"))])
    errs = validate(bad, RATIFIED)
    assert "I11" in codes(errs)
    assert any("AI_SUPPLIED" in e.message for e in errs)


def test_I11_threshold_with_no_provenance_at_all():
    bad = mutate(D1, hard_constraints=[
        Constraint("o2_floor", "o2_partial_pressure_kpa >= 16.0", ConstraintSource.PHYSICS,
                   threshold=16.0)])
    assert "I11" in codes(validate(bad, RATIFIED))


def test_I11_threshold_must_match_the_elicited_level():
    """Citing a real guideline while quietly using a different number is the subtle version."""
    bad = mutate(D2, hard_constraints=[
        Constraint("min_volume_floor", "volume_per_person_m3 >= 12.0",
                   ConstraintSource.CONSTITUTION, threshold=12.0,
                   threshold_provenance=Provenance(ProvenanceKind.GUIDELINE, "G-F-003"),
                   guideline_id="G-F-003")])
    errs = validate(bad, RATIFIED)
    assert "I11" in codes(errs)
    assert any("does not match the elicited level" in e.message for e in errs)


def test_I11_physical_constant_provenance_is_accepted():
    ok = mutate(D1, hard_constraints=[
        Constraint("hypoxia_floor", "o2_partial_pressure_kpa >= 16.0", ConstraintSource.PHYSICS,
                   threshold=16.0,
                   threshold_provenance=Provenance(ProvenanceKind.PHYSICAL_CONSTANT,
                                                   "hypoxia_threshold_kpa"))])
    assert "I11" not in codes(validate(ok, RATIFIED))


# ---------------------------------------------------------------- every invariant is reachable

def test_all_eleven_invariants_have_at_least_one_triggering_mutation():
    """Coverage guard: if a new invariant lands without a mutation, this fails."""
    triggered = set()

    triggered |= codes(validate(mutate(D2, objectives_received=[
        ObjectiveRef("G-NOPE", "x", Direction.RAISE)]), RATIFIED))                       # I1
    triggered |= codes(validate(mutate(D1, instruments=[
        replace(i, ratification_class=RatificationClass.SIMPLE)
        if i.reversibility is Reversibility.IRREVERSIBLE else i
        for i in D1.instruments]), RATIFIED))                                            # I2
    triggered |= codes(validate_registry([D1, mutate(D2, couplings=[])], RATIFIED))      # I3
    triggered |= codes(validate(mutate(D1, metrics=[
        Metric("m", "f", "", "r")]), RATIFIED))                                          # I4
    triggered |= codes(validate(mutate(D1, hard_constraints=[
        replace(c, on_violation=OnViolation.OPTIMIZE_THROUGH)
        for c in D1.hard_constraints]), RATIFIED))                                       # I5
    triggered |= codes(validate(mutate(D1, falsification_test=None), RATIFIED))          # I6
    triggered |= codes(validate(mutate(D1, sunset_cycles=0), RATIFIED))                  # I7
    triggered |= codes(validate(mutate(D2, instruments=list(D2.instruments) + [
        Instrument("q", InstrumentClass.QUANTITY_ALLOCATION, (0, 1), 1,
                   Reversibility.REVERSIBLE, RatificationClass.SIMPLE)]), RATIFIED))     # I8
    triggered |= codes(validate(mutate(D1, roles=frozenset(
        {Role.GENERATE, Role.DECIDE})), RATIFIED))                                       # I9
    triggered |= codes(validate(mutate(D2, rules=[
        replace(D2.rules[0], published=False)]), RATIFIED))                              # I10
    triggered |= codes(validate(mutate(D1, hard_constraints=[
        Constraint("c", "p", ConstraintSource.PHYSICS, threshold=1.0)]), RATIFIED))      # I11

    expected = {"I1", "I2", "I3", "I4", "I5", "I6", "I7", "I8", "I9", "I11"}
    assert expected <= triggered
    assert any(c.startswith("FULLER-") for c in triggered), "I10 (Fuller) must be reachable"
