"""Validation for the civic-education / shared-identity model (family mars-gov-civic-education).

H1: the model penalizes BOTH failure modes — a thin-core/wide-elective/dissent/cross-cutting curriculum
is HEALTHY; a no-core/no-mixing one is FRAGMENTATION; a thick-mandated or low-pluralism one is MONOCULTURE.
H2: curriculum CAPTURE (one source owns the core) is flagged EVEN WHEN cohesion is high — high cohesion
cannot mask the Company-Town failure. Scarcity amplifies division risk (couples to resource/connection).
"""
import pytest

import dataclasses

from governance.civic_education import (
    FRAGMENTATION,
    HEALTHY,
    MONOCULTURE,
    CivicCurriculum,
    capture_detected,
    classify,
    cohesion_index,
    core_source_concentration,
    division_risk,
    pluralism_index,
    robust_healthy,
)


def _healthy():
    return CivicCurriculum(
        core_modules=(("survival-interdependence", "founding"),
                      ("rule-of-law", "origin_A"),
                      ("common-language", "origin_B")),
        elective_traditions=4, dissent_allowed=True, cross_cutting=0.8)


def _captured_high_cohesion():
    # 5-module core ALL authored by the founder, but strong cross-cutting -> HIGH cohesion
    return CivicCurriculum(
        core_modules=tuple((f"core{i}", "founding") for i in range(5)),
        elective_traditions=4, dissent_allowed=True, cross_cutting=0.9)


def _thick_mandated():
    return CivicCurriculum(
        core_modules=tuple((f"core{i}", ("founding", "origin_A", "origin_B")[i % 3]) for i in range(10)),
        elective_traditions=1, dissent_allowed=False, cross_cutting=0.8)


def _fragmented():
    return CivicCurriculum(core_modules=(), elective_traditions=5, dissent_allowed=True, cross_cutting=0.1)


# --- H1: both extremes penalized -------------------------------------------
def test_healthy_classified_healthy():
    a = classify(_healthy())
    assert a.classification == HEALTHY
    assert a.cohesion >= 0.6 and a.pluralism >= 0.5 and a.captured is False


def test_fragmentation_detected():
    a = classify(_fragmented())
    assert a.classification == FRAGMENTATION
    assert a.cohesion < 0.6


def test_thick_mandated_is_monoculture():
    a = classify(_thick_mandated())
    assert a.classification == MONOCULTURE
    assert a.pluralism < 0.5            # thick core + no dissent crushes pluralism (non-vacuous)


# --- H2: capture masked by cohesion -----------------------------------------
def test_capture_flagged_even_with_high_cohesion():
    curr = _captured_high_cohesion()
    assert cohesion_index(curr) >= 0.9          # cohesion is HIGH
    assert capture_detected(curr) is True        # ...yet capture is still caught
    assert classify(curr).classification == MONOCULTURE
    assert core_source_concentration(curr) == 1.0


def test_diverse_core_not_captured():
    assert capture_detected(_healthy()) is False


# --- control-surface capture: laundered through required-electives (review issue 1) ---
def test_laundered_capture_via_practically_required():
    # the declared CORE is diverse (3 sources) and looks clean ...
    laundered = CivicCurriculum(
        core_modules=(("survival", "founding"), ("law", "origin_A"), ("language", "origin_B")),
        elective_traditions=4, dissent_allowed=True, cross_cutting=0.8,
        # ... but every PRACTICALLY-REQUIRED module (credential/employment gate) is the founder's
        practically_required=tuple((f"req{i}", "founding") for i in range(4)))
    assert core_source_concentration(laundered) < 0.5      # core alone looks fine
    assert capture_detected(laundered) is True              # ...control surface is captured
    assert classify(laundered).classification == MONOCULTURE


def test_clean_practically_required_not_captured():
    clean = CivicCurriculum(
        core_modules=(("survival", "founding"), ("law", "origin_A")),
        elective_traditions=4, dissent_allowed=True, cross_cutting=0.8,
        practically_required=(("vocational", "origin_B"), ("history", "origin_C")))
    assert capture_detected(clean) is False


# --- division risk + scarcity coupling --------------------------------------
def test_healthy_low_risk():
    assert division_risk(_healthy(), scarcity=0.0) < 0.25


def test_fragmentation_high_risk():
    # fragmentation risk is materially elevated vs a healthy curriculum (~0.06); 0.57 at scarcity 0.5
    assert division_risk(_fragmented(), scarcity=0.5) > 0.5
    assert division_risk(_fragmented(), scarcity=0.5) > 8 * division_risk(_healthy(), scarcity=0.5)


def test_scarcity_amplifies_division_risk():
    curr = _fragmented()
    assert division_risk(curr, scarcity=0.8) > division_risk(curr, scarcity=0.0)


def test_capture_raises_risk_despite_cohesion():
    # the captured curriculum has high cohesion but capture should keep risk non-trivial
    assert division_risk(_captured_high_cohesion(), scarcity=0.0) > division_risk(_healthy(), scarcity=0.0)


# --- metric ranges + guards -------------------------------------------------
@pytest.mark.parametrize("curr", [_healthy(), _fragmented(), _thick_mandated(), _captured_high_cohesion()])
def test_indices_in_unit_range(curr):
    assert 0.0 <= cohesion_index(curr) <= 1.0
    assert 0.0 <= pluralism_index(curr) <= 1.0
    assert 0.0 <= division_risk(curr, 0.5) <= 1.0


def test_guards():
    with pytest.raises(ValueError):
        CivicCurriculum(core_modules=(), elective_traditions=1, dissent_allowed=True, cross_cutting=1.5)
    with pytest.raises(ValueError):
        division_risk(_healthy(), scarcity=2.0)
    with pytest.raises(ValueError):
        CivicCurriculum(core_modules=(), elective_traditions=1, dissent_allowed=True,
                        cross_cutting=0.5, economic_dependence=1.5)


# --- coercion channel (2026-06-06 review issue 3) ---------------------------
def test_formal_dissent_voided_by_economic_coercion():
    # formally dissent_allowed, but a company-town employer dependence makes it practically false
    company_town = dataclasses.replace(_healthy(), economic_dependence=0.8)
    assert company_town.dissent_allowed is True          # formally allowed
    assert company_town.effective_dissent is False        # ...but economically coerced
    assert classify(company_town).classification == MONOCULTURE


def test_low_dependence_preserves_dissent():
    assert _healthy().effective_dissent is True
    assert classify(_healthy()).classification == HEALTHY


# --- robustness / sensitivity (2026-06-06 review issue 2, alt 2) ------------
def test_strong_healthy_is_robust():
    assert robust_healthy(_healthy()) is True


def test_borderline_healthy_is_fragile():
    # barely-healthy: minimal electives + borderline dependence -> a small perturbation tips it out
    fragile = CivicCurriculum(
        core_modules=(("survival", "founding"), ("law", "origin_A")),
        elective_traditions=2, dissent_allowed=True, cross_cutting=0.6, economic_dependence=0.55)
    assert classify(fragile).classification == HEALTHY    # currently healthy ...
    assert robust_healthy(fragile) is False                # ... but NOT robust


def test_non_healthy_is_not_robust():
    assert robust_healthy(_fragmented()) is False
