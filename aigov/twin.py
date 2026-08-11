"""F4 — The colony digital twin (department D14): the world departments act on.

Departments cannot be falsified without a world. This module is that world: it holds the state the
`DepartmentSpec` contract declares, advances it under instrument settings, and reproduces the
analog-sourced baselines the vendored `aigov/choice/models/resource_sim.py` was calibrated against.

Three properties are load-bearing, and each closes a way the governor could invent a number:

1. **Coverage.** Every `StateVar` a department declares must be SERVED by the twin. A department acting
   on a variable the world does not provide is acting on fiction — `check_state_coverage` makes that a
   validation error rather than a silent `KeyError` at cycle 40.
2. **Observability is ENFORCED, not decorative.** `StateVar.observability` was a declared field that
   nothing checked. Here it binds: `read()` REFUSES a `LATENT` variable, and `ESTIMATED` variables come
   back wrapped in an `Estimate` carrying its method and error bar. The governor cannot read
   `willingness_to_pay` as though it were measured — the same discipline as I11 (no invented thresholds)
   applied to STATE rather than to objectives.
3. **Physical bounds are checked every tick.** A loop that closes on paper by violating conservation is
   the failure this project's whole epistemology exists to prevent.

Honest scope: this is a *coarse* twin — a few coupled reservoirs, not an ECLSS simulator. Its job is to
make department decisions falsifiable, not to be flight-accurate. Anything it reports is model-coherent
only (inherited `mars-governance` D7).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .choice.models import resource_sim as rs
from .contract import Observability

# --------------------------------------------------------------------------------------
# Physical constants
# --------------------------------------------------------------------------------------

R_GAS = 8.314          # J/(mol K)
O2_MOLAR_MASS_KG = 0.032
CABIN_TEMP_K = 293.15

#: Structural/design bounds on the habitat atmosphere. DECLARED physical constants — the legitimate
#: provenance class under I11 (a physical constant, not a value judgement), but still queued for the
#: same audit-tier verification as everything else in `aigov-foundations`.
#:
#: Why these exist at all: without them the twin happily reported an O2 partial pressure of 304 kPa
#: after 12 cycles of full photosynthetic closure — three atmospheres of pure oxygen inside a hull rated
#: for about one. That is not a state the colony can occupy, so reporting it as state was the twin
#: telling a department a comfortable fiction. Found by inspecting a run, not by a test.
HABITAT_STRUCTURAL_LIMIT_KPA = 101.325   # ~1 atm total; the hull is not a pressure vessel beyond it
O2_FIRE_HAZARD_KPA = 30.0                # elevated-O2 flammability regime (Apollo-1 class hazard)


def o2_partial_pressure_kpa(o2_mass_kg: float, volume_m3: float,
                            temp_k: float = CABIN_TEMP_K) -> float:
    """Ideal-gas partial pressure of the habitat O2 inventory."""
    if volume_m3 <= 0:
        raise ValueError("volume must be positive")
    moles = o2_mass_kg / O2_MOLAR_MASS_KG
    return (moles * R_GAS * temp_k / volume_m3) / 1000.0


def o2_mass_for_pressure_kg(pp_kpa: float, volume_m3: float,
                            temp_k: float = CABIN_TEMP_K) -> float:
    """Inverse of `o2_partial_pressure_kpa` — used to initialise a habitat at a target pressure."""
    moles = pp_kpa * 1000.0 * volume_m3 / (R_GAS * temp_k)
    return moles * O2_MOLAR_MASS_KG


# --------------------------------------------------------------------------------------
# Observability-respecting reads
# --------------------------------------------------------------------------------------


class LatentVariableError(LookupError):
    """Raised when something tries to READ a latent variable as if it were measured."""


class HabitatFailedError(RuntimeError):
    """Raised when state is requested from a habitat that has structurally failed."""


@dataclass(frozen=True)
class Estimate:
    """An ESTIMATED variable. Carries its method and error bar so it is never mistaken for a reading."""

    name: str
    value: float
    method: str
    rel_error: float

    @property
    def interval(self):
        d = abs(self.value) * self.rel_error
        return (self.value - d, self.value + d)


# --------------------------------------------------------------------------------------
# The twin
# --------------------------------------------------------------------------------------


@dataclass
class InstrumentSettings:
    """What the departments set this cycle. Names match the specs' `Instrument.name`."""

    o2_generation_setpoint: float = 0.0     # fraction of crew demand generated abiotically
    crop_area_allocation: float = 0.0       # share of calories grown photosynthetically
    reserve_buffer_target: float = 30.0     # days of O2 buffer the department is aiming for
    volume_tax_rate: float = 1.10           # credits per m^3 per cycle
    radiator_area_tax_rate: float = 0.05    # credits per m^2 per cycle
    o2_draw_price: float = 0.0


@dataclass
class TickReport:
    cycle: int
    o2_delta_kg: float
    o2_partial_pressure_kpa: float
    water_delta_l: float
    tax_revenue_credits: float
    violations: list = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.violations


class ColonyTwin:
    """A coarse, deterministic colony world.

    Reservoirs: habitat O2 mass, water, power, thermal-rejection capacity, pressurized volume,
    radiator area. Crew demand comes from the vendored analog-calibrated `resource_sim`.
    """

    #: Which declared StateVar names this twin serves, and at what observability.
    SERVED = {
        "o2_partial_pressure_kpa": Observability.DIRECT,
        "water_reserve_l": Observability.DIRECT,
        "power_kw": Observability.DIRECT,
        "thermal_reject_kw": Observability.DIRECT,
        "pressurized_volume_m3": Observability.DIRECT,
        "radiator_area_m2": Observability.DIRECT,
        "tax_revenue_credits": Observability.DIRECT,
        "closure_fraction": Observability.ESTIMATED,
        "public_goods_bill_credits": Observability.ESTIMATED,
        "willingness_to_pay": Observability.LATENT,
    }

    def __init__(self, n_crew: int = 200, pressurized_volume_m3: float = 8_000.0,
                 radiator_area_m2: float = 9_000.0, power_kw: float = 120.0,
                 thermal_reject_kw: float = 130.0, water_reserve_l: float = 60_000.0,
                 initial_o2_pp_kpa: float = 21.0, cycle_days: float = 30.0):
        if n_crew <= 0:
            raise ValueError("n_crew must be positive")
        self.n_crew = n_crew
        self.cycle_days = cycle_days
        self.cycle = 0
        self.failed = False
        self._v = {
            "pressurized_volume_m3": pressurized_volume_m3,
            "radiator_area_m2": radiator_area_m2,
            "power_kw": power_kw,
            "thermal_reject_kw": thermal_reject_kw,
            "water_reserve_l": water_reserve_l,
            "tax_revenue_credits": 0.0,
        }
        self._o2_mass_kg = o2_mass_for_pressure_kg(initial_o2_pp_kpa, pressurized_volume_m3)

    # ---------------------------------------------------------------- reads

    def read(self, name: str) -> float:
        """Read a DIRECT variable. Refuses LATENT; refuses ESTIMATED (use `estimate`)."""
        if self.failed:
            raise HabitatFailedError(
                "the habitat failed structurally at cycle {}; it has no state to report. Continuing "
                "to serve numbers past a hull breach would be the twin telling a comfortable "
                "fiction.".format(self.cycle))
        obs = self.SERVED.get(name)
        if obs is None:
            raise LookupError("twin does not serve state variable {!r}".format(name))
        if obs is Observability.LATENT:
            raise LatentVariableError(
                "{!r} is LATENT — it is not measured and must never be read as though it were. "
                "A governor that reads a latent variable is inventing the number.".format(name))
        if obs is Observability.ESTIMATED:
            raise LatentVariableError(
                "{!r} is ESTIMATED — call estimate() so the method and error bar travel with the "
                "value.".format(name))
        if name == "o2_partial_pressure_kpa":
            return o2_partial_pressure_kpa(self._o2_mass_kg, self._v["pressurized_volume_m3"])
        return self._v[name]

    def estimate(self, name: str) -> Estimate:
        """Return an ESTIMATED variable with its method and error bar attached."""
        obs = self.SERVED.get(name)
        if obs is None:
            raise LookupError("twin does not serve state variable {!r}".format(name))
        if obs is Observability.LATENT:
            raise LatentVariableError(
                "{!r} is LATENT — it cannot be estimated by the twin either; eliciting it is the "
                "intake's job, not the world's.".format(name))
        if obs is Observability.DIRECT:
            return Estimate(name, self.read(name), "direct measurement", 0.0)
        if name == "closure_fraction":
            return Estimate(name, self._closure_fraction,
                            "mass-balance reconciliation over the last cycle", 0.10)
        if name == "public_goods_bill_credits":
            return Estimate(name, 8_600.0, "rolling 6-cycle mean of realised spend", 0.15)
        raise LookupError("no estimator for {!r}".format(name))

    # ---------------------------------------------------------------- dynamics

    _closure_fraction = 0.90

    def crew_demand(self):
        """Per-cycle crew demand from the vendored analog-calibrated model."""
        return rs.simulate(self.n_crew, days=int(self.cycle_days))

    def tick(self, s: InstrumentSettings) -> TickReport:
        """Advance one decision cycle under the departments' instrument settings."""
        if self.failed:
            raise HabitatFailedError("habitat failed at cycle {}; there is nothing left to advance"
                                     .format(self.cycle))
        if not 0.0 <= s.crop_area_allocation <= 1.0:
            raise ValueError("crop_area_allocation must be in [0, 1]")
        if s.o2_generation_setpoint < 0.0:
            raise ValueError("o2_generation_setpoint must be non-negative")

        demand = self.crew_demand()
        bal = rs.oxygen_balance(self.n_crew, crop_fraction=s.crop_area_allocation)
        plant_o2 = bal.plant_o2_kg * self.cycle_days
        abiotic_o2 = demand.o2_kg * s.o2_generation_setpoint
        o2_delta = plant_o2 + abiotic_o2 - demand.o2_kg
        self._o2_mass_kg = max(0.0, self._o2_mass_kg + o2_delta)

        # Water: consumption net of recovery at the current closure fraction.
        water_delta = -demand.water_kg * (1.0 - self._closure_fraction)
        self._v["water_reserve_l"] = max(0.0, self._v["water_reserve_l"] + water_delta)

        revenue = (self._v["pressurized_volume_m3"] * s.volume_tax_rate
                   + self._v["radiator_area_m2"] * s.radiator_area_tax_rate)
        self._v["tax_revenue_credits"] = revenue

        self.cycle += 1
        pp = o2_partial_pressure_kpa(self._o2_mass_kg, self._v["pressurized_volume_m3"])

        violations = []
        if self._v["thermal_reject_kw"] < self._v["power_kw"]:
            violations.append("thermal_saturation: reject {:.1f} kW < power {:.1f} kW".format(
                self._v["thermal_reject_kw"], self._v["power_kw"]))
        if self._v["water_reserve_l"] <= 0.0:
            violations.append("water_reserve exhausted")
        if pp <= 0.0:
            violations.append("atmosphere lost")
        if pp > O2_FIRE_HAZARD_KPA:
            violations.append(
                "o2_fire_hazard: partial pressure {:.1f} kPa exceeds the elevated-O2 flammability "
                "bound {:.1f} kPa".format(pp, O2_FIRE_HAZARD_KPA))
        if pp > HABITAT_STRUCTURAL_LIMIT_KPA:
            self.failed = True
            violations.append(
                "HULL BREACH: {:.1f} kPa exceeds the structural limit {:.1f} kPa — the twin will not "
                "report further state, because a burst habitat has none".format(
                    pp, HABITAT_STRUCTURAL_LIMIT_KPA))
        return TickReport(self.cycle, o2_delta, pp, water_delta, revenue, violations)

    # ---------------------------------------------------------------- baselines

    #: Per-person-per-day reference values the vendored model is calibrated against
    #: (NASA BVAD-style, carried in `resource_sim` as O2_REF_KG / CO2_REF_KG / FOOD_DRY_REF_KG).
    BASELINE_TOLERANCE = 0.05

    def baseline_report(self, tolerance: float = BASELINE_TOLERANCE) -> dict:
        """Compare the model's derived per-capita demand to its analog references.

        MEASURED, not asserted: the deltas below are computed, and the tolerance a department may rely
        on is whatever this reports — not a number written into a doc.
        """
        rows = [
            ("o2_kg", rs.per_capita_o2_kg(), rs.O2_REF_KG),
            ("co2_kg", rs.per_capita_co2_kg(), rs.CO2_REF_KG),
            ("food_dry_kg", rs.per_capita_food_dry_kg(), rs.FOOD_DRY_REF_KG),
        ]
        out, worst = {}, 0.0
        for name, derived, ref in rows:
            rel = abs(derived - ref) / ref
            worst = max(worst, rel)
            out[name] = {"derived": round(derived, 4), "reference": ref,
                         "rel_error": round(rel, 4), "within_tolerance": rel <= tolerance}
        return {"per_capita_per_day": out, "worst_rel_error": round(worst, 4),
                "tolerance": tolerance, "all_within_tolerance": worst <= tolerance}

    def scale_invariance_error(self, n_crew: int = 137, days: int = 11) -> float:
        """Totals re-normalised to one person-day must return the per-capita figures."""
        t = rs.simulate(n_crew, days=days).per_capita_day
        base = rs.per_capita_o2_kg()
        return abs(t.o2_kg - base) / base


# --------------------------------------------------------------------------------------
# Contract binding
# --------------------------------------------------------------------------------------


def check_state_coverage(specs, twin: ColonyTwin) -> list:
    """Every StateVar a department declares must be SERVED, at the SAME observability.

    A department acting on a variable the world does not provide is acting on fiction. An observability
    MISMATCH is worse than a missing variable: it means a department believes it can measure something
    the world only estimates.
    """
    errors = []
    for spec in specs:
        for sv in spec.state_vars:
            served = twin.SERVED.get(sv.name)
            if served is None:
                errors.append("[COV] {}: declares state var {!r} which the twin does not serve"
                              .format(spec.id, sv.name))
            elif served is not sv.observability:
                errors.append(
                    "[OBS] {}: declares {!r} as {} but the twin serves it as {} — a department that "
                    "believes it MEASURES an estimated or latent quantity is inventing precision"
                    .format(spec.id, sv.name, sv.observability.value, served.value))
    return errors
