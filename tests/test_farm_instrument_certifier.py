"""F15 MVP criterion 2: the farm certifier + observation layer survive adversarial probes.

The certifier recomputes the published rule from an Estimate-wrapped measurement:
- CERTIFY only when the proposal MATCHES the recomputed rule;
- STEERING_DETECTED on contradiction (early spray / withheld spray / off-menu value);
- ESCALATE when the error bar straddles the published threshold, or with no observation at all;
- truth-reads (bare floats) are REFUSED, not coerced.
"""

import datetime

import pytest

from aigov.choice.governance.fail_safe_gate import CERTIFY, ESCALATE, STEERING_DETECTED
from aigov.farm_certifier import BLIGHT_INSTRUMENT, DONT_TREAT, TREAT, farm_fail_safe_gate
from aigov.farm_observation import FarmObservation, TruthReadRefused, rule_decision_from_estimate
from aigov.twin import Estimate


def est(value, rel):
    return Estimate(name="blitecast_accumulated_severity[test]", value=value,
                    method="test fixture", rel_error=rel)


# ------------------------------------------------------------------ rule recomputation

def test_clearly_above_threshold_says_treat():
    assert rule_decision_from_estimate(est(24.0, 0.1)) == "treat"      # interval (21.6, 26.4)


def test_clearly_below_threshold_says_dont_treat():
    assert rule_decision_from_estimate(est(10.0, 0.2)) == "dont-treat"  # interval (8, 12)


def test_interval_straddling_threshold_is_ambiguous():
    assert rule_decision_from_estimate(est(18.0, 0.2)) == "ambiguous"   # interval (14.4, 21.6)


def test_truth_read_is_refused_not_coerced():
    with pytest.raises(TruthReadRefused):
        rule_decision_from_estimate(24.0)  # a bare float is a truth-read


# ------------------------------------------------------------------ certifier verdicts

def test_certify_rule_conforming_proposals():
    assert farm_fail_safe_gate(TREAT, est(24.0, 0.1)).label == CERTIFY
    assert farm_fail_safe_gate(DONT_TREAT, est(10.0, 0.2)).label == CERTIFY


def test_steering_detected_on_contradiction():
    # Withholding a triggered spray, and spraying with no trigger — both steered.
    withheld = farm_fail_safe_gate(DONT_TREAT, est(24.0, 0.1))
    early = farm_fail_safe_gate(TREAT, est(10.0, 0.2))
    assert withheld.label == STEERING_DETECTED and "contradicts" in withheld.recommended_procedure
    assert early.label == STEERING_DETECTED


def test_escalate_when_measurement_straddles_threshold():
    for proposal in (TREAT, DONT_TREAT):
        v = farm_fail_safe_gate(proposal, est(18.0, 0.2))
        assert v.label == ESCALATE
        assert "straddles" in v.recommended_procedure


def test_escalate_with_no_observation_record():
    v = farm_fail_safe_gate(TREAT, None)
    assert v.label == ESCALATE and "refuses" in v.recommended_procedure


def test_off_menu_value_is_steering():
    assert farm_fail_safe_gate(0.5, est(24.0, 0.1)).label == STEERING_DETECTED


def test_certifier_refuses_truth_reads_too():
    with pytest.raises(TruthReadRefused):
        farm_fail_safe_gate(TREAT, 24.0)


# ------------------------------------------------------------------ kernel registration

def test_blight_instrument_is_registered_certifiable():
    from aigov.kernel import CERTIFIABLE_INSTRUMENTS

    assert BLIGHT_INSTRUMENT in CERTIFIABLE_INSTRUMENTS
    # The boundary stays closed: exactly the two instruments with REAL certifiers.
    assert CERTIFIABLE_INSTRUMENTS == {"crop_area_allocation", BLIGHT_INSTRUMENT}


# ------------------------------------------------------------------ observation layer (real cache)

@pytest.fixture(scope="module")
def lelystad():
    return FarmObservation("lelystad")


def test_observation_returns_estimate_with_method_and_interval(lelystad):
    acc = lelystad.accumulated_severity(datetime.date(2020, 5, 22), datetime.date(2020, 7, 31))
    assert isinstance(acc, Estimate)
    assert "RH>=93/87" in acc.method and "Litschmann" in acc.method
    lo, hi = acc.interval
    assert lo <= acc.value <= hi


def test_observation_accumulation_is_monotone_in_window_end(lelystad):
    em = datetime.date(2020, 5, 22)
    values = [
        lelystad.accumulated_severity(em, em + datetime.timedelta(days=n)).value
        for n in (20, 60, 100, 124)
    ]
    assert values == sorted(values)


def test_observation_raises_on_missing_cache_day(lelystad):
    with pytest.raises(KeyError):
        lelystad.hours(datetime.date(1999, 1, 1))
