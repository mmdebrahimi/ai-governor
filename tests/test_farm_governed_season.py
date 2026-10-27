"""F16 MVP criterion 1: one full replayed season under the UNCHANGED kernel, zero bypasses.

Pins the governed-season runner (``aigov/farm_season.py``) on the ratified reference season
(Fontane @ Lelystad 2020): completion, determinism, the zero-ungated-application invariant (H1),
and the two governed arms' kernel events — ESCALATE under honest error bars, CERTIFY+apply under
the nominal-sensitivity reading, both on the published rule's trigger date.
"""

import datetime

import pytest

pytest.importorskip("pcse", reason="pcse not installed (farm-season dependency)")

from aigov.farm_season import run_governed_season  # noqa: E402


@pytest.fixture(scope="module")
def report():
    return run_governed_season("Fontane", "lelystad", 2020)


def test_season_completes_with_positive_model_coherent_yield(report):
    assert report.season_days == 125
    assert report.final_twso_kg_ha > 0  # PP ceiling — identical across arms by construction


def test_h1_zero_ungated_applications_in_both_governed_arms(report):
    for arm_name in ("governed-precision", "governed-nominal"):
        arm = report.arms[arm_name]
        assert arm.ungated_applications == 0
        applied_records = [r for r in arm.records if r.applied]
        assert len(applied_records) == arm.applied_actions
        for rec in applied_records:
            # every application went through a proposal and a CERTIFY verdict — no other path exists
            assert rec.proposed and rec.verdict == "certify"


def test_precision_arm_escalates_once_at_nominal_trigger_and_never_sprays(report):
    arm = report.arms["governed-precision"]
    assert arm.spray_events == 0 and arm.applied_actions == 0
    assert arm.escalations == 1
    kernel_events = [r for r in arm.records if r.proposed]
    assert len(kernel_events) == 1
    event = kernel_events[0]
    assert event.day == report.nominal_first_trigger
    assert event.verdict.startswith("escalate") and not event.applied
    assert arm.ambiguous_days > 30  # the measured measurement-limited regime, not a one-off


def test_nominal_arm_certifies_and_sprays_on_the_published_trigger_date(report):
    arm = report.arms["governed-nominal"]
    assert report.nominal_first_trigger == datetime.date(2020, 9, 9)
    assert arm.protection_start == report.nominal_first_trigger
    assert arm.spray_events == 1 and arm.applied_actions == 1
    assert arm.escalations == 0 and arm.refusals == 0


def test_comparison_arms_bracket_the_governed_run(report):
    calendar, never = report.arms["calendar"], report.arms["never-treat"]
    governed = report.arms["governed-nominal"]
    assert calendar.spray_events == 18          # weekly from 50% emergence (convention, cited)
    assert never.spray_events == 0
    assert 0 < governed.spray_events < calendar.spray_events
    assert never.unprotected_full_smith_periods == report.full_smith_periods == 2


def test_season_is_deterministic():
    a = run_governed_season("Fontane", "lelystad", 2020)
    b = run_governed_season("Fontane", "lelystad", 2020)
    assert a.final_twso_kg_ha == b.final_twso_kg_ha
    for k in a.arms:
        assert (a.arms[k].spray_events, a.arms[k].escalations, a.arms[k].ambiguous_days,
                a.arms[k].protected_days) == (
            b.arms[k].spray_events, b.arms[k].escalations, b.arms[k].ambiguous_days,
            b.arms[k].protected_days)
