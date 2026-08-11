"""D0 charter tests: the four non-negotiables trip on violating fixtures, and the checkable
fraction is MEASURED rather than asserted in prose."""

import copy

import pytest
from dataclasses import replace

from aigov.charter_invariants import (
    charter_status,
    ASPIRATIONAL, CLAUSES, Clause, NON_NEGOTIABLES, Site, checkable_fraction,
    clause_integrity_errors, constraint_fingerprint, inv_exception_is_split,
    inv_no_self_amendment, inv_objective_provenance, inv_separation_of_powers,
)
from aigov.contract import (
    Constraint, ConstraintSource, Provenance, ProvenanceKind, Role,
)
from aigov.guidelines import RATIFIED
from aigov.specs.d1_lifesupport import SPEC as D1
from aigov.specs.d2_economy import SPEC as D2

SPECS = [D1, D2]

GOOD_EMERGENCY = {
    "declare": "assembly",
    "exercise": "caretaker",
    "terminate": "citizens_council",
    "audit": "D15",
    "auto_expiry_cycles": 3,
    "post_hoc_audit_mandatory": True,
}


# ---------------------------------------------------------------- charter integrity (DK1)

def test_charter_has_no_integrity_errors():
    assert clause_integrity_errors() == []


def test_dk1_rejects_a_self_policed_clause_claiming_enforcement():
    """A rule the Governor checks against itself is ASPIRATIONAL, never ENFORCED."""
    bad = list(CLAUSES) + [Clause("C99", "The Governor shall behave.", "inv_behaves",
                                  Site.IN_GOVERNOR)]
    errs = clause_integrity_errors(bad)
    assert any("IN_GOVERNOR" in e and "C99" in e for e in errs)


def test_in_governor_siting_is_never_counted_as_enforcement():
    """Same implemented invariant, two sites: only the external siting counts as enforcement."""
    c = Clause("CX", "x", "inv_separation_of_powers", Site.IN_GOVERNOR)
    assert c.is_enforced is False
    assert replace(c, site=Site.EXTERNAL_VERIFIER).is_enforced is True


def test_aspirational_clauses_are_labelled_not_hidden():
    aspirational = [c for c in CLAUSES if c.enforced_by == ASPIRATIONAL]
    assert aspirational, "a charter with zero aspirational clauses is overclaiming"
    assert all(not c.is_enforced for c in aspirational)


def test_overclaim_is_detected_when_a_clause_names_a_missing_invariant():
    """Naming an invariant that does not exist here is the quiet way a charter overclaims."""
    bad = list(CLAUSES) + [Clause("C98", "The Governor shall be wise.", "inv_is_wise",
                                  Site.EXTERNAL_VERIFIER)]
    assert any("not an implemented invariant" in e and "C98" in e
               for e in clause_integrity_errors(bad))


def test_pending_is_not_counted_as_enforcement():
    """PENDING never counts as enforcement.

    Tests the MECHANISM with a synthetic clause rather than naming a live one. The original version
    hard-coded C15 as the pending example and broke the moment C15 actually landed (2026-08-11) — a
    test that asserts today's *inventory* instead of the *rule* has to be edited every time reality
    improves, which trains you to edit tests to green.
    """
    pending = Clause("C96", "x", "PENDING:some-family", Site.EXTERNAL_VERIFIER)
    assert pending.is_pending and not pending.is_enforced
    s = charter_status(list(CLAUSES) + [pending])
    assert "C96" in s["pending"] and "C96" not in s["enforced"]


def test_c15_landed_when_the_organ_was_vendored():
    """Regression pin on the actual PENDING -> ENFORCED transition (family aigov-collective-choice)."""
    c15 = next(c for c in CLAUSES if c.id == "C15")
    assert c15.enforced_by == "aigov.choice.governance.fail_safe_gate"
    assert c15.is_enforced and not c15.is_pending


def test_pending_must_name_the_family_that_will_land_it():
    bad = list(CLAUSES) + [Clause("C97", "x", "PENDING:", Site.EXTERNAL_VERIFIER)]
    assert any("PENDING must name the family" in e for e in clause_integrity_errors(bad))


def test_status_partition_is_exhaustive_and_disjoint():
    s = charter_status()
    buckets = s["enforced"] + s["pending"] + s["aspirational"]
    assert len(buckets) == len(set(buckets)) == s["total"]


# ---------------------------------------------------------------- H1: the fraction is MEASURED

def test_checkable_fraction_is_measured_and_recorded():
    frac = checkable_fraction()
    assert 0.0 <= frac <= 1.0
    # H1 of family aigov-constitution: the machine-checkable fraction exceeds 0.5.
    assert frac > 0.5, "measured checkable fraction {:.3f}".format(frac)


def test_checkable_fraction_matches_the_recorded_number():
    """Pins the MEASURED value (18/25 = 0.72) so a silent drift in enforcement claims fails.

    History (both changes deliberate and recorded, never a silent edit-to-green):
    1. The pin first read 18/24 and FAILED against a measured 0.75. The measurement was right and the
       expectation wrong — C15 named `fail_safe_gate`, an invariant that exists in Mars_Governance but
       is not wired into this repo. PENDING + overclaim-detection were added rather than editing the
       pin. The failing test found a real defect.
    2. 2026-08-11: research V5 (OST Art. VI) added clause C25, a DISCLOSURE duty with no executable
       predicate, so it is ASPIRATIONAL. 24 -> 25 clauses with the enforced count unchanged at 17, so
       the fraction FALLS 0.7083 -> 0.68. A falling fraction here is honest: the charter grew a limit
       it cannot mechanically check, and says so.
    3. 2026-08-11: family aigov-collective-choice vendored the Mars_Governance organ in-repo
       (aigov/choice/, 193/193), so C15's `fail_safe_gate` became a real IMPLEMENTED invariant and
       flipped PENDING -> ENFORCED. 17 -> 18 enforced of 25, fraction 0.68 -> 0.72.
    """
    assert round(checkable_fraction(), 4) == round(18 / 25, 4)


def test_every_non_negotiable_is_actually_enforced_or_human_sited():
    for cid in NON_NEGOTIABLES:
        c = next(c for c in CLAUSES if c.id == cid)
        assert c.non_negotiable
        assert c.site in (Site.EXTERNAL_VERIFIER, Site.HUMAN_ONLY)


# ---------------------------------------------------------------- N1 objective provenance

def test_N1_holds_on_the_clean_registry():
    assert inv_objective_provenance(SPECS, RATIFIED) == []


def test_N1_trips_when_the_ai_supplies_a_value():
    bad = copy.deepcopy(D1)
    bad.hard_constraints = [Constraint(
        "o2_floor", "o2_partial_pressure_kpa >= 18.5", ConstraintSource.PHYSICS, threshold=18.5,
        threshold_provenance=Provenance(ProvenanceKind.AI_SUPPLIED, "model judgement"))]
    assert inv_objective_provenance([bad, D2], RATIFIED)


# ---------------------------------------------------------------- N2 no self-amendment

def test_N2_no_change_is_always_legal():
    fp = constraint_fingerprint(SPECS)
    assert inv_no_self_amendment(fp, SPECS, None) == []


def test_N2_trips_on_an_unratified_constraint_change():
    fp = constraint_fingerprint(SPECS)
    weakened = copy.deepcopy(D1)
    weakened.hard_constraints = [
        replace(c, threshold=12.0, predicate="o2_partial_pressure_kpa >= 12.0")
        if c.name == "o2_floor" else c for c in D1.hard_constraints]
    errs = inv_no_self_amendment(fp, [weakened, D2], None)
    assert errs and "NO ratification record" in errs[0]


@pytest.mark.parametrize("body", ["governor", "ai", "kernel", "self", ""])
def test_N2_trips_on_a_self_issued_ratification(body):
    fp = constraint_fingerprint(SPECS)
    weakened = copy.deepcopy(D1)
    weakened.hard_constraints = [
        replace(c, threshold=12.0) if c.name == "o2_floor" else c for c in D1.hard_constraints]
    after = constraint_fingerprint([weakened, D2])
    errs = inv_no_self_amendment(
        fp, [weakened, D2], {"ratified_by": body, "fingerprint_after": after})
    assert errs and "self-issued" in errs[0]


def test_N2_accepts_a_genuine_human_ratification():
    fp = constraint_fingerprint(SPECS)
    weakened = copy.deepcopy(D1)
    weakened.hard_constraints = [
        replace(c, threshold=12.0) if c.name == "o2_floor" else c for c in D1.hard_constraints]
    after = constraint_fingerprint([weakened, D2])
    assert inv_no_self_amendment(
        fp, [weakened, D2], {"ratified_by": "assembly", "fingerprint_after": after}) == []


def test_N2_trips_when_the_record_covers_a_different_change():
    """Ratifying change A and then shipping change B is the subtle attack."""
    fp = constraint_fingerprint(SPECS)
    weakened = copy.deepcopy(D1)
    weakened.hard_constraints = [
        replace(c, threshold=12.0) if c.name == "o2_floor" else c for c in D1.hard_constraints]
    errs = inv_no_self_amendment(
        fp, [weakened, D2], {"ratified_by": "assembly", "fingerprint_after": "some-other-hash"})
    assert errs and "does not cover" in errs[0]


# ---------------------------------------------------------------- N3 the exception

def test_N3_holds_on_a_well_formed_emergency_protocol():
    assert inv_exception_is_split(GOOD_EMERGENCY) == []


@pytest.mark.parametrize("role", ["declare", "terminate"])
def test_N3_trips_when_the_ai_holds_the_exception(role):
    bad = dict(GOOD_EMERGENCY, **{role: "governor"})
    errs = inv_exception_is_split(bad)
    assert any("the exception may never sit with the machine" in e for e in errs)


def test_N3_trips_when_roles_collapse_into_one_actor():
    bad = dict(GOOD_EMERGENCY, terminate="assembly")  # same actor declares and terminates
    assert any("four distinct actors" in e for e in inv_exception_is_split(bad))


def test_N3_trips_without_automatic_expiry():
    assert any("automatic expiry" in e
               for e in inv_exception_is_split(dict(GOOD_EMERGENCY, auto_expiry_cycles=0)))


def test_N3_trips_without_mandatory_post_hoc_audit():
    assert any("post-hoc audit" in e
               for e in inv_exception_is_split(
                   dict(GOOD_EMERGENCY, post_hoc_audit_mandatory=False)))


def test_N3_trips_on_a_missing_role():
    bad = dict(GOOD_EMERGENCY)
    del bad["audit"]
    assert any("no actor assigned to 'audit'" in e for e in inv_exception_is_split(bad))


# ---------------------------------------------------------------- N4 separation of powers

def test_N4_holds_on_the_clean_registry():
    assert inv_separation_of_powers(SPECS) == []


def test_N4_trips_when_one_body_generates_and_decides():
    bad = copy.deepcopy(D2)
    bad.roles = frozenset({Role.GENERATE, Role.DECIDE})
    assert inv_separation_of_powers([D1, bad])


def test_N4_trips_when_the_generator_also_verifies():
    bad = copy.deepcopy(D1)
    bad.roles = frozenset({Role.GENERATE, Role.VERIFY})
    assert inv_separation_of_powers([bad, D2])
