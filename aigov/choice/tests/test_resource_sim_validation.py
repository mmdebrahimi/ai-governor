"""Validation harness for the closed-loop resource model (family mars-gov-resource-sim).

MVP contract: per-capita O2/CO2/food match BVAD-style analog references within +/-10%,
the model scales linearly across the N=10..1000 crew contract, and the plant subsystem
reproduces the bioregenerative O2 over-production hazard. Confirming this suite is the
empirical basis for hypothesis H1.
"""
import math

import pytest

from models.resource_sim import (
    per_capita_o2_kg,
    per_capita_co2_kg,
    per_capita_food_dry_kg,
    per_capita_water_kg,
    simulate,
    oxygen_balance,
    O2_REF_KG,
    CO2_REF_KG,
    FOOD_DRY_REF_KG,
)

TOL = 0.10  # +/-10% validation contract


def within(value, ref, tol=TOL):
    return abs(value - ref) <= tol * ref


# --- first-principles validation vs BVAD-style analog references ---
def test_per_capita_o2_within_tolerance():
    assert within(per_capita_o2_kg(), O2_REF_KG)


def test_per_capita_co2_within_tolerance():
    assert within(per_capita_co2_kg(), CO2_REF_KG)


def test_per_capita_food_within_tolerance():
    assert within(per_capita_food_dry_kg(), FOOD_DRY_REF_KG)


def test_water_demand_positive():
    assert per_capita_water_kg() > 0


# --- linear scaling across the N=10..1000 contract ---
@pytest.mark.parametrize("n", [10, 50, 100, 500, 1000])
def test_linear_scaling(n):
    one = simulate(1)
    many = simulate(n)
    assert math.isclose(many.o2_kg, one.o2_kg * n, rel_tol=1e-9)
    assert math.isclose(many.co2_kg, one.co2_kg * n, rel_tol=1e-9)


def test_per_capita_invariant_across_population():
    pc10 = simulate(10).per_capita_day
    pc1000 = simulate(1000).per_capita_day
    assert math.isclose(pc10.o2_kg, pc1000.o2_kg, rel_tol=1e-9)
    assert math.isclose(pc10.co2_kg, pc1000.co2_kg, rel_tol=1e-9)


def test_positive_and_multiday():
    t = simulate(100, days=30)
    assert t.o2_kg > 0 and t.co2_kg > 0 and t.water_kg > 0 and t.food_dry_kg > 0
    assert math.isclose(t.o2_kg, simulate(100).o2_kg * 30, rel_tol=1e-9)


def test_invalid_inputs():
    with pytest.raises(ValueError):
        simulate(0)
    with pytest.raises(ValueError):
        simulate(10, days=0)


# --- plant O2 over-production hazard (Mars One failure mode) ---
def test_full_food_closure_overproduces_o2():
    bal = oxygen_balance(100, crop_fraction=1.0)
    assert bal.overproduction is True
    assert bal.net_o2_kg > 0


def test_partial_closure_needs_supplemental_o2():
    bal = oxygen_balance(100, crop_fraction=0.5)
    assert bal.overproduction is False
    assert bal.net_o2_kg < 0


def test_balance_crossover():
    # break-even at crop_fraction = 1 / overproduction_factor (~0.667)
    assert oxygen_balance(100, crop_fraction=0.66).overproduction is False
    assert oxygen_balance(100, crop_fraction=0.68).overproduction is True


def test_crop_fraction_bounds():
    with pytest.raises(ValueError):
        oxygen_balance(100, crop_fraction=1.5)
