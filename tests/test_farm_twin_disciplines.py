"""F14 milestone 3: the FarmTwin wrapper enforces the three twin disciplines.

Coverage, observability-enforced reads, per-tick physical bounds (tripwires that HALT, not clamps),
plus the harvest-day termination contract. See ``docs/farm_twin_world_spec.md`` §4.
"""

import pytest

pytest.importorskip("pcse", reason="pcse not installed (F14 dependency; pip install pcse)")

from aigov.farm_twin import (  # noqa: E402
    MAX_DAILY_TWSO_GAIN_KG_HA,
    FarmTickReport,
    FarmTwin,
    FarmTwinHalted,
    ObservabilityRefused,
    check_coverage,
)


@pytest.fixture(scope="module")
def twin():
    return FarmTwin("Fontane", "lelystad", 2020)


def test_coverage_forward_and_reverse(twin):
    assert check_coverage(twin) == []


def test_read_refuses_undeclared_variable(twin):
    # The PP world has no soil water; serving a plausible-sounding undeclared name would be fiction.
    with pytest.raises(ObservabilityRefused):
        twin.read("soil_moisture")
    with pytest.raises(ObservabilityRefused):
        twin.read("late_blight_severity")  # F15's composition surface, NOT this world's


def test_every_served_variable_reads_mid_season():
    t = FarmTwin("Innovator", "lelystad", 2020)
    for _ in range(40):
        t.tick()
    assert t.read("dvs") > 0.0
    assert t.read("lai") > 0.0
    assert t.read("twso_kg_ha") >= 0.0
    assert t.read("day").year == 2020


def test_bounds_tripwire_halts_on_impossible_state():
    t = FarmTwin("Markies", "lelystad", 2020)
    for _ in range(50):
        t.tick()
    # Forge an impossible previous state: a huge recorded TWSO means the next tick "decreases".
    t._prev["twso_kg_ha"] = 1e9
    with pytest.raises(FarmTwinHalted):
        t.tick()


def test_tick_report_flags_excess_daily_gain():
    report = FarmTickReport(day=None, dvs=1.0, lai=3.0, twso_kg_ha=0.0)
    assert report.ok
    report.violations.append(f"TWSO gained 9999 kg/ha in one day (> {MAX_DAILY_TWSO_GAIN_KG_HA:.0f})")
    assert not report.ok


def test_season_terminates_and_refuses_post_harvest_ticks():
    t = FarmTwin("Premiere", "vredepeel", 2020)
    summary = t.run_season()
    assert t.terminated
    assert summary["TWSO"] > 0.0
    with pytest.raises(FarmTwinHalted):
        t.tick()
