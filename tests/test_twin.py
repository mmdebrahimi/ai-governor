"""F4 twin tests: the world must serve the contract, respect observability, and be able to FAIL."""

import pytest

from aigov.contract import Observability
from aigov.specs.d1_lifesupport import SPEC as D1
from aigov.specs.d2_economy import SPEC as D2
from aigov.twin import (
    CABIN_TEMP_K, ColonyTwin, Estimate, HABITAT_STRUCTURAL_LIMIT_KPA, HabitatFailedError,
    InstrumentSettings, LatentVariableError, O2_FIRE_HAZARD_KPA, check_state_coverage,
    o2_mass_for_pressure_kg, o2_partial_pressure_kpa,
)

SPECS = [D1, D2]
BREAK_EVEN_CROP = 1.0 / 1.5     # plant O2 exactly matches crew demand


def nominal():
    return InstrumentSettings(crop_area_allocation=BREAK_EVEN_CROP)


# ---------------------------------------------------------------- gas law

def test_partial_pressure_round_trips():
    m = o2_mass_for_pressure_kg(21.0, 8_000.0)
    assert o2_partial_pressure_kpa(m, 8_000.0) == pytest.approx(21.0)


def test_partial_pressure_scales_inversely_with_volume():
    m = o2_mass_for_pressure_kg(21.0, 8_000.0)
    assert o2_partial_pressure_kpa(m, 16_000.0) == pytest.approx(10.5)


def test_zero_volume_is_refused():
    with pytest.raises(ValueError):
        o2_partial_pressure_kpa(100.0, 0.0)


# ---------------------------------------------------------------- baselines (the family's bar)

def test_baselines_reproduce_within_the_stated_tolerance():
    rep = ColonyTwin().baseline_report()
    assert rep["all_within_tolerance"], rep
    assert rep["worst_rel_error"] <= rep["tolerance"]


def test_baseline_report_pins_the_measured_errors():
    """MEASURED, not asserted — a silent recalibration of the vendored model fails here."""
    rep = ColonyTwin().baseline_report()["per_capita_per_day"]
    assert rep["o2_kg"]["rel_error"] == pytest.approx(0.0101, abs=5e-4)
    assert rep["co2_kg"]["rel_error"] == pytest.approx(0.0492, abs=5e-4)
    assert rep["food_dry_kg"]["rel_error"] == pytest.approx(0.0011, abs=5e-4)


def test_co2_is_the_loosest_baseline():
    """Worth knowing which reference is nearest the tolerance edge."""
    rep = ColonyTwin().baseline_report()["per_capita_per_day"]
    worst = max(rep, key=lambda k: rep[k]["rel_error"])
    assert worst == "co2_kg"


def test_a_tighter_tolerance_would_fail_and_the_report_says_so():
    """The report must be able to come out FALSE."""
    rep = ColonyTwin().baseline_report(tolerance=0.02)
    assert rep["all_within_tolerance"] is False
    assert rep["per_capita_per_day"]["co2_kg"]["within_tolerance"] is False


def test_scale_invariance_holds_to_machine_precision():
    assert ColonyTwin().scale_invariance_error() < 1e-12


# ---------------------------------------------------------------- contract coverage

def test_every_declared_state_var_is_served():
    assert check_state_coverage(SPECS, ColonyTwin()) == []


def test_an_unserved_state_var_is_a_coverage_error():
    import copy
    from aigov.contract import StateVar
    bad = copy.deepcopy(D1)
    bad.state_vars = list(D1.state_vars) + [
        StateVar("regolith_throughput_kg", "kg", Observability.DIRECT, "D1")]
    errs = check_state_coverage([bad], ColonyTwin())
    assert any(e.startswith("[COV]") for e in errs)


def test_an_observability_mismatch_is_its_own_error():
    """Worse than a missing variable: a department believing it MEASURES an estimate."""
    import copy
    from dataclasses import replace
    bad = copy.deepcopy(D1)
    bad.state_vars = [replace(sv, observability=Observability.DIRECT)
                      if sv.name == "closure_fraction" else sv for sv in D1.state_vars]
    errs = check_state_coverage([bad], ColonyTwin())
    assert any(e.startswith("[OBS]") and "inventing precision" in e for e in errs)


# ---------------------------------------------------------------- observability is ENFORCED

def test_direct_variables_read():
    t = ColonyTwin()
    assert t.read("o2_partial_pressure_kpa") == pytest.approx(21.0)
    assert t.read("pressurized_volume_m3") == 8_000.0


def test_latent_variable_cannot_be_read():
    """The governor must not be able to read willingness-to-pay as though it were measured."""
    with pytest.raises(LatentVariableError):
        ColonyTwin().read("willingness_to_pay")


def test_latent_variable_cannot_be_estimated_either():
    with pytest.raises(LatentVariableError):
        ColonyTwin().estimate("willingness_to_pay")


def test_estimated_variable_refuses_a_bare_read():
    with pytest.raises(LatentVariableError):
        ColonyTwin().read("closure_fraction")


def test_estimated_variable_carries_its_method_and_error_bar():
    e = ColonyTwin().estimate("closure_fraction")
    assert isinstance(e, Estimate) and e.method and e.rel_error > 0
    lo, hi = e.interval
    assert lo < e.value < hi


def test_unknown_variable_is_refused():
    with pytest.raises(LookupError):
        ColonyTwin().read("unicorn_density")


# ---------------------------------------------------------------- dynamics

def test_break_even_crop_fraction_holds_pressure_flat():
    t = ColonyTwin()
    for _ in range(12):
        r = t.tick(nominal())
    assert r.cycle == 12
    assert r.o2_partial_pressure_kpa == pytest.approx(21.0)
    assert r.o2_delta_kg == pytest.approx(0.0, abs=1e-6)


def test_revenue_tracks_the_tax_instruments():
    t = ColonyTwin()
    r = t.tick(InstrumentSettings(crop_area_allocation=BREAK_EVEN_CROP,
                                  volume_tax_rate=1.10, radiator_area_tax_rate=0.05))
    assert r.tax_revenue_credits == pytest.approx(8_000 * 1.10 + 9_000 * 0.05)


@pytest.mark.parametrize("bad", [-0.1, 1.1])
def test_out_of_range_crop_fraction_is_refused(bad):
    with pytest.raises(ValueError):
        ColonyTwin().tick(InstrumentSettings(crop_area_allocation=bad))


# ---------------------------------------------------------------- the twin must be able to FAIL

def test_no_o2_source_loses_the_atmosphere():
    r = ColonyTwin().tick(InstrumentSettings(crop_area_allocation=0.0, o2_generation_setpoint=0.0))
    assert "atmosphere lost" in r.violations and not r.ok


def test_thermal_saturation_is_detected():
    t = ColonyTwin(power_kw=150.0, thermal_reject_kw=130.0)
    r = t.tick(nominal())
    assert any(v.startswith("thermal_saturation") for v in r.violations)


def test_water_reserve_exhausts_on_a_long_run():
    """A real, checkable prediction: 90% closure with no ISRU makeup drains the reserve."""
    t = ColonyTwin()
    first = None
    for _ in range(60):
        r = t.tick(nominal())
        if any("water_reserve" in v for v in r.violations):
            first = r.cycle
            break
    assert first == 31, "water should exhaust at cycle 31, got {}".format(first)


def test_full_closure_trips_the_fire_hazard_bound_immediately():
    """D1's declared plant_o2_overproduction failure mode, reproduced by the world."""
    r = ColonyTwin().tick(InstrumentSettings(crop_area_allocation=1.0))
    assert r.o2_partial_pressure_kpa > O2_FIRE_HAZARD_KPA
    assert any(v.startswith("o2_fire_hazard") for v in r.violations)


def test_sustained_overproduction_breaches_the_hull_and_the_twin_stops_reporting():
    """Before the structural bound existed the twin cheerfully reported 304 kPa at cycle 12 —
    three atmospheres of pure O2 in a hull rated for about one. Reporting a state the colony
    cannot occupy is the twin telling a department a comfortable fiction."""
    t = ColonyTwin()
    s = InstrumentSettings(crop_area_allocation=1.0)
    breach = None
    for _ in range(6):
        r = t.tick(s)
        if any(v.startswith("HULL BREACH") for v in r.violations):
            breach = r.cycle
            break
    assert breach == 4, "hull should breach at cycle 4, got {}".format(breach)
    assert t.failed
    with pytest.raises(HabitatFailedError):
        t.tick(s)
    with pytest.raises(HabitatFailedError):
        t.read("o2_partial_pressure_kpa")


def test_structural_limit_is_above_the_fire_bound():
    assert O2_FIRE_HAZARD_KPA < HABITAT_STRUCTURAL_LIMIT_KPA


def test_nominal_operation_never_trips_a_bound():
    t = ColonyTwin()
    for _ in range(25):
        r = t.tick(nominal())
        assert r.ok, "nominal run tripped {} at cycle {}".format(r.violations, r.cycle)
