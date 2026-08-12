"""D1 Life-Support & Resources — the HIGH central-legitimacy reference department.

This is the case where central planning is genuinely JUSTIFIED: a closed physical loop with few
state variables, direct observability, tight causality, and death as the failure mode. It is the
honest exception to Hayek's knowledge problem — and the exception does not generalize (see
docs/foundations-canon-map.md section 4).

Because legitimacy is HIGH, I8 permits QUANTITY_ALLOCATION instruments here. Compare
`d2_economy.py`, where the same instrument class is a validation error.
"""

from ..guidelines import level_of
from ..contract import (
    Constraint, ConstraintSource, Coupling, CouplingDirection, DepartmentSpec, Direction,
    EquilibriumKind, Instrument, InstrumentClass, Legitimacy, Metric, FailureMode, Observability,
    ObjectiveRef, Provenance, ProvenanceKind, RatificationClass, Reversibility, Role, StateVar,
    VSMLayer,
)


def _falsification_test() -> bool:
    """The loop must not close on paper by violating the power budget it actually gets.

    Falsifiable claim: the O2 the LIFE-SUPPORT SHARE of colony power can generate covers crew
    demand. Every input below is DECLARED (tier: unverified) — promoting them to measured values is
    family aigov-twin's job (F4), not this spec's. The point here is that the claim is arithmetic
    and can come out FALSE: at a 0.29 power share, or crew 280, or 0.14 kg O2/kWh, it does.
    """
    total_power_kw = 120.0
    life_support_power_share = 0.40      # competes with ISRU, compute, thermal, industry
    o2_kg_per_kwh = 0.20                 # water electrolysis envelope (~5 kWh per kg O2)
    crew = 200
    o2_demand_kg_day = 0.84 * crew                                   # 168.0
    o2_supply_kg_day = total_power_kw * life_support_power_share * 24.0 * o2_kg_per_kwh  # 230.4
    return o2_supply_kg_day >= o2_demand_kg_day


SPEC = DepartmentSpec(
    id="D1",
    vsm_layer=VSMLayer.S1,
    central_legitimacy=Legitimacy.HIGH,
    roles=frozenset({Role.GENERATE}),
    sunset_cycles=24,
    state_vars=[
        StateVar("o2_partial_pressure_kpa", "kPa", Observability.DIRECT, "D1"),
        StateVar("water_reserve_l", "L", Observability.DIRECT, "D1"),
        StateVar("power_kw", "kW", Observability.DIRECT, "D1"),
        StateVar("thermal_reject_kw", "kW", Observability.DIRECT, "D1"),
        StateVar("pressurized_volume_m3", "m^3", Observability.DIRECT, "D1"),
        StateVar("closure_fraction", "ratio", Observability.ESTIMATED, "D1"),
    ],
    instruments=[
        # Legitimate here precisely BECAUSE legitimacy is HIGH (I8). I8b still applies: HIGH
        # legitimacy licenses allocation, it does not excuse the department from naming WHERE the
        # discretion sits or how capture at that tier would be caught.
        Instrument("o2_generation_setpoint", InstrumentClass.QUANTITY_ALLOCATION,
                   (0.0, 1.0), 1, Reversibility.REVERSIBLE, RatificationClass.SIMPLE,
                   discretion_tier="central ECLSS controller; no lower tier exists - the loop is "
                                   "physically single-tier and shared by every colonist",
                   capture_check="setpoint history reconciled by D15 against MEASURED o2 partial "
                                 "pressure; a setpoint persistently above demand is a claim on "
                                 "power that the twin's mass balance exposes"),
        Instrument("crop_area_allocation", InstrumentClass.QUANTITY_ALLOCATION,
                   (0.0, 1.0), 3, Reversibility.REVERSIBLE, RatificationClass.SIMPLE,
                   discretion_tier="central allocator sets the aggregate fraction; the sub-tier is "
                                   "per-module crop bays, which is where allocation is actually "
                                   "exercised and therefore where capture would sit",
                   capture_check="per-bay yield against allocated area; flagged when area "
                                 "concentrates in a bay without a matching yield improvement"),
        Instrument("reserve_buffer_target", InstrumentClass.RULE,
                   (0.0, 90.0), 1, Reversibility.REVERSIBLE, RatificationClass.SIMPLE),
        # Irreversible => supermajority (I2): you cannot un-vent an atmosphere.
        Instrument("emergency_atmosphere_vent", InstrumentClass.QUANTITY_ALLOCATION,
                   (0.0, 1.0), 0, Reversibility.IRREVERSIBLE, RatificationClass.SUPERMAJORITY,
                   discretion_tier="the SPLIT emergency authority (charter C03): declare, exercise, "
                                   "terminate and audit are four distinct actors, never one",
                   capture_check="auto-expiry plus a post-hoc D15 audit naming who declared, who "
                                 "exercised and who terminated; a vent with fewer than four "
                                 "distinct actors in the record is a capture finding"),
    ],
    objectives_received=[
        ObjectiveRef(
            guideline_id="G-D-005",
            metric="closure_fraction",
            direction=Direction.RAISE,
        ),
    ],
    hard_constraints=[
        Constraint(
            name="o2_floor",
            # READ from the ratified registry — never restated. A restated copy drifts, and a
            # drifted copy is indistinguishable from an AI-supplied one.
            predicate="o2_partial_pressure_kpa >= level_of('G-F-004')",
            source=ConstraintSource.PHYSICS,
            threshold=level_of("G-F-004"),
            threshold_provenance=Provenance(ProvenanceKind.GUIDELINE, "G-F-004"),
            guideline_id="G-F-004",
        ),
        Constraint(
            name="thermal_rejection_capacity",
            predicate="thermal_reject_kw >= power_kw",
            source=ConstraintSource.PHYSICS,
        ),
    ],
    couplings=[
        Coupling("D2", "pressurized_volume_m3", CouplingDirection.CONTENDS),
        Coupling("D2", "power_kw", CouplingDirection.CONTENDS),
    ],
    metrics=[
        Metric(
            name="closure_fraction",
            formula="recycled_mass / total_mass_throughput",
            gaming_model="Excluding a hard-to-recycle stream from the denominator raises the ratio "
                         "without improving closure; audited by mass-balance reconciliation against "
                         "the twin's total inventory.",
            rotation_policy="re-derive the denominator definition every 8 cycles",
            # I4': this IS a target (objective G-D-005, direction RAISE).
            # Ratchet: YES - a RAISE objective with no ceiling ratchets by construction, so the
            # department has a standing incentive to bank closure gains rather than book them.
            # Threshold: NO - D1 is a single unit against a single physical loop, so there is no
            # population of heterogeneous units to bunch at a uniform line.
            ratchet_exposed=True,
            threshold_exposed=False,
        ),
        Metric(
            name="o2_margin_days",
            formula="o2_reserve_kg / daily_draw_kg",
            gaming_model="Raising the setpoint just before measurement inflates the margin; "
                         "mitigated by sampling at a randomized cycle offset.",
            rotation_policy="randomize sample offset each cycle",
        ),
    ],
    failure_modes=[
        FailureMode("plant_o2_overproduction", "o2_partial_pressure_kpa > 23.0", "D13"),
        FailureMode("crop_cycle_collapse", "closure_fraction drop > 0.15 in one cycle", "D11"),
        FailureMode("thermal_saturation", "thermal_reject_kw < power_kw", "D13"),
    ],
    rules=[],
    falsification_test=_falsification_test,
    # I14: ORDINARY. The argument is physical, not optimistic — dysfunction in a closed
    # life-support loop is detected by mass balance and partial pressure, not by an oversight body
    # that could itself be captured. There is no self-reinforcing rent to be trapped in when the
    # failure mode is asphyxiation. This is the honest exception; it does NOT generalize to D2.
    equilibrium=EquilibriumKind.ORDINARY,
)
