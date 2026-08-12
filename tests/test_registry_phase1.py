"""The three-department phase-1 registry, and an honest pin on how far it actually gets.

The phase-1 mechanical terminal asks for >=12 governed cycles across >=3 departments spanning HIGH,
MEDIUM and LOW central legitimacy. D3 (fabrication capacity, MEDIUM) was the missing department and
now exists. These tests pin what that DID close and — more importantly — what it did not, because
running the three-department registry surfaced a blocker that reading the specs would not have.
"""

import random

import pytest

from aigov.choice.governance.panel_agnostic import aggregate_single_peaked, random_panel
from aigov.contract import Legitimacy, validate, validate_registry
from aigov.guidelines import RATIFIED
from aigov.kernel import Governor, InvalidRegistryError, RatificationRecord
from aigov.registry import legitimacy_span, phase1_registry, two_department_registry
from aigov.specs.d3_fabrication import SPEC as D3
from aigov.twin import ColonyTwin
from aigov.vocabulary import RATIFIED_VOCABULARY

SCEN = "nominal"


def panel():
    rng = random.Random(7)
    for _ in range(400):
        p = random_panel(rng)
        if aggregate_single_peaked(p, SCEN, 200):
            return p
    raise AssertionError("no single-peaked panel found")


def ratify_all(action):
    return RatificationRecord("assembly", Governor._key(action))


def gov3():
    return Governor(phase1_registry(), RATIFIED, ColonyTwin(), scenario=SCEN,
                    vocabulary=RATIFIED_VOCABULARY)


# ---------------------------------------------------------------- D3 itself

def test_d3_satisfies_the_contract():
    assert validate(D3, RATIFIED, vocabulary=RATIFIED_VOCABULARY) == []


def test_d3_is_the_medium_legitimacy_department():
    assert D3.central_legitimacy is Legitimacy.MEDIUM


def test_d3_may_allocate_because_i8_binds_only_LOW():
    """I8 forbids QUANTITY_ALLOCATION at LOW legitimacy. MEDIUM is permitted — the load moves
    entirely onto I8b, which is why the allocative instrument must name its discretion tier."""
    alloc = [i for i in D3.instruments if i.iclass.value == "quantity_allocation"]
    assert alloc, "the MEDIUM department must exercise the allocative case, or it tests nothing"
    for ins in alloc:
        assert ins.discretion_tier.strip()
        assert ins.capture_check.strip()


def test_the_allocative_discretion_sits_with_no_officer():
    """MEDIUM means procedure central, judgment distributed. A named official holding the draw
    would make this HIGH-legitimacy central allocation wearing a MEDIUM label."""
    ins = next(i for i in D3.instruments if i.iclass.value == "quantity_allocation")
    assert "lottery" in ins.discretion_tier.lower()
    assert "no officer" in ins.discretion_tier.lower()


def test_project_value_is_declared_LATENT():
    """The load-bearing declaration. G-P-001 says no committee decides what is worth inventing;
    declaring the worth of an unbuilt invention observable would assert the opposite."""
    sv = next(v for v in D3.state_vars if v.name == "project_value")
    assert sv.observability.value == "latent"


def test_d3_receives_no_objective_and_that_is_deliberate():
    """D1 is judged against a physical floor, D2 a fiscal one. D3 has no level to hit — inventing
    one so the field looks populated is the act I11 forbids for thresholds."""
    assert D3.objectives_received == []


def test_topic_blindness_is_a_hard_constraint_not_a_metric_alone():
    names = {c.name for c in D3.hard_constraints}
    assert "allocation_is_topic_blind" in names
    assert "qualification_is_safety_only" in names


def test_d3_instruments_and_rule_classes_come_from_the_ratified_vocabulary():
    """I8c + I15: the department names a key, the vocabulary owns what it means."""
    from aigov.vocabulary import VocabularyKind
    for ins in D3.instruments:
        entry = RATIFIED_VOCABULARY.lookup(ins.name, VocabularyKind.INSTRUMENT)
        assert entry is not None, ins.name
        assert entry.instrument_class == ins.iclass.value
    for r in D3.rules:
        assert RATIFIED_VOCABULARY.lookup(
            r.applies_to_class, VocabularyKind.RULE_TARGET_CLASS) is not None


def test_d3_falsification_test_is_executable_and_can_be_false():
    from aigov.specs.d3_fabrication import _falsification_test
    assert _falsification_test() is True          # holds on the declared envelope
    import inspect
    src = inspect.getsource(_falsification_test)
    assert "applicants_per_cycle" in src and "slots_per_cycle" in src


# ---------------------------------------------------------------- the composition

def test_phase1_registry_spans_all_three_legitimacy_levels():
    span = legitimacy_span(phase1_registry())
    assert span == {Legitimacy.HIGH, Legitimacy.MEDIUM, Legitimacy.LOW}


def test_two_department_registry_does_not_span_medium():
    """Pins WHY D3 had to exist: the interim colony has no MEDIUM department at all."""
    assert Legitimacy.MEDIUM not in legitimacy_span(two_department_registry())


def test_both_registries_are_independently_valid():
    """Couplings are relative to a composition, so both worlds must validate on their own."""
    assert validate_registry(two_department_registry(), RATIFIED,
                             vocabulary=RATIFIED_VOCABULARY) == []
    assert validate_registry(phase1_registry(), RATIFIED,
                             vocabulary=RATIFIED_VOCABULARY) == []


def test_a_d3_aware_d1_is_REJECTED_in_the_two_department_colony():
    """The reason `registry.py` exists. I3 rejects a coupling to an absent department, so the
    D3-aware D1 is invalid precisely where D3 is missing — both specs are right for their world."""
    d1_aware = phase1_registry()[0]
    errs = validate_registry([d1_aware, two_department_registry()[1]], RATIFIED,
                             vocabulary=RATIFIED_VOCABULARY)
    assert any(e.code == "I3" and "unknown department 'D3'" in e.message for e in errs)


def test_an_unmirrored_d3_coupling_is_refused_at_admission():
    """I3 is bilateral. Composing D3 with a D1 that does not know about it must not be admissible —
    this is the exact error the first three-department run produced."""
    plain_d1, d2 = two_department_registry()
    with pytest.raises(InvalidRegistryError) as ei:
        Governor([plain_d1, d2, D3], RATIFIED, ColonyTwin(), scenario=SCEN,
                 vocabulary=RATIFIED_VOCABULARY)
    assert "I3" in str(ei.value) and "not mirrored" in str(ei.value)


# ---------------------------------------------------------------- 12 cycles, and the honest limit

def test_twelve_cycles_run_across_three_departments():
    g = gov3()
    p = panel()
    for _ in range(12):
        g.run_cycle(p, ratify_all)
    assert g.twin.cycle == 12
    assert len(g.history) == 12


def test_every_proposed_action_is_accounted_for_in_every_cycle():
    g = gov3()
    p = panel()
    for _ in range(12):
        rec = g.run_cycle(p, ratify_all)
        assert len(rec.proposed) == len(rec.applied) + len(rec.refused) + len(rec.escalated)


def test_nothing_applies_ungated_across_the_three_department_run():
    from aigov.choice.governance.fail_safe_gate import CERTIFY
    g = gov3()
    p = panel()
    for _ in range(12):
        rec = g.run_cycle(p, ratify_all)
        for _a, cert in rec.applied:
            assert cert.appliable and cert.ratified and cert.non_steering == CERTIFY
        for _a, cert in rec.refused + rec.escalated:
            assert not cert.appliable


def test_D3_PROPOSES_NOTHING_the_blocker_this_run_found():
    """NAMED GAP, pinned so it cannot be quietly forgotten.

    Adding the MEDIUM department was NECESSARY and is not SUFFICIENT. `Governor.propose` is a stub
    that hard-codes two instrument names (`crop_area_allocation`, `volume_tax_rate`), so D3 never
    proposes anything and the three-department run exercises D3's CONTRACT but not its BEHAVIOUR.

    This test asserts the defect deliberately. It must be INVERTED — not deleted — when the
    proposal layer stops being a stub; leaving it green while D3 stays silent is the vacuous pass
    this codebase keeps catching.
    """
    g = gov3()
    p = panel()
    proposers = set()
    for _ in range(12):
        rec = g.run_cycle(p, ratify_all)
        proposers.update(a.dept_id for a in rec.proposed)
    assert proposers == {"D1", "D2"}, (
        "D3 now proposes - INVERT this test and re-check the phase-1 terminal")


def test_the_certifiable_domain_is_a_single_instrument():
    """The second half of the same gap. Non-steering certification is only faithful inside the
    resource-menu domain, so every other instrument is refused out-of-domain. Extending it is real
    design work, not a list edit — V1's rule is to certify only where the property is faithful."""
    from aigov.kernel import CERTIFIABLE_INSTRUMENTS
    assert CERTIFIABLE_INSTRUMENTS == {"crop_area_allocation"}
