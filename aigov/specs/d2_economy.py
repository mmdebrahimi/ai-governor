"""D2 Economy & Fiscal — the LOW central-legitimacy reference department.

This is the case where central planning is FORBIDDEN by the design (Hayek's knowledge problem).
Under I8 this department may set RULES and PRICES only; a QUANTITY_ALLOCATION instrument here is a
validation error, not a policy choice. That single mechanical rule is the subsidiarity engine.

The fiscal instrument is the colony analogue of a land value tax: the inelastically-supplied fixed
factor is pressurized VOLUME (and radiator area), which is physically enumerable and therefore hard
to evade. Guideline G-O-002 ("people who use more should pay more") compiles to a MONOTONICITY
constraint — a shape, not a level — which is why it binds without anyone supplying a number.
"""

from ..guidelines import level_of
from ..contract import (
    Constraint, ConstraintSource, Coupling, CouplingDirection, DepartmentSpec, Direction,
    Instrument, InstrumentClass, Legitimacy, Metric, FailureMode, Observability, ObjectiveRef,
    Provenance, ProvenanceKind, RatificationClass, Reversibility, Role, Rule, StateVar, VSMLayer,
)


def _falsification_test() -> bool:
    """Falsifiable claim: the volume/area tax at the ratified rate funds the public-goods bill.

    A real number, computed from the declared envelope, that can come out FALSE.
    """
    pressurized_volume_m3 = 200 * 40.0     # 200 colonists at 40 m^3 average holding
    tax_rate_per_m3_cycle = 1.10           # credits per m^3 per cycle
    radiator_area_m2 = 9_000.0
    area_rate_per_m2_cycle = 0.05
    revenue = (pressurized_volume_m3 * tax_rate_per_m3_cycle
               + radiator_area_m2 * area_rate_per_m2_cycle)
    public_goods_bill = 8_600.0            # infrastructure + life-support subsidy per cycle
    return revenue >= public_goods_bill


SPEC = DepartmentSpec(
    id="D2",
    vsm_layer=VSMLayer.S3,
    central_legitimacy=Legitimacy.LOW,
    roles=frozenset({Role.GENERATE}),
    sunset_cycles=12,
    state_vars=[
        StateVar("pressurized_volume_m3", "m^3", Observability.DIRECT, "D1"),
        StateVar("power_kw", "kW", Observability.DIRECT, "D1"),
        StateVar("radiator_area_m2", "m^2", Observability.DIRECT, "D2"),
        StateVar("tax_revenue_credits", "credits", Observability.DIRECT, "D2"),
        StateVar("public_goods_bill_credits", "credits", Observability.ESTIMATED, "D2"),
        StateVar("willingness_to_pay", "credits", Observability.LATENT, "D2"),
    ],
    instruments=[
        # RULE and PRICE only. A QUANTITY_ALLOCATION instrument here trips I8.
        Instrument("volume_tax_rate", InstrumentClass.PRICE,
                   (0.0, 5.0), 1, Reversibility.REVERSIBLE, RatificationClass.SIMPLE),
        Instrument("radiator_area_tax_rate", InstrumentClass.PRICE,
                   (0.0, 1.0), 1, Reversibility.REVERSIBLE, RatificationClass.SIMPLE),
        Instrument("o2_draw_price", InstrumentClass.PRICE,
                   (0.0, 10.0), 1, Reversibility.REVERSIBLE, RatificationClass.SIMPLE),
        Instrument("self_assessed_valuation_rule", InstrumentClass.RULE,
                   (0.0, 1.0), 2, Reversibility.REVERSIBLE, RatificationClass.SIMPLE),
    ],
    objectives_received=[
        ObjectiveRef(
            guideline_id="G-F-003",
            metric="volume_per_person_m3",
            direction=Direction.HOLD_WITHIN,
            threshold=level_of("G-F-003"),
            threshold_provenance=Provenance(ProvenanceKind.GUIDELINE, "G-F-003"),
        ),
    ],
    hard_constraints=[
        # The clean compile from probe B1: an ORDERING, so it binds with no number at all.
        Constraint(
            name="tax_monotonic_in_use",
            predicate="d(tax)/d(pressurized_volume_m3) > 0",
            source=ConstraintSource.CONSTITUTION,
            guideline_id="G-O-002",
        ),
        Constraint(
            name="min_volume_floor",
            predicate="volume_per_person_m3 >= level_of('G-F-003')",
            source=ConstraintSource.CONSTITUTION,
            threshold=level_of("G-F-003"),
            threshold_provenance=Provenance(ProvenanceKind.GUIDELINE, "G-F-003"),
            guideline_id="G-F-003",
        ),
    ],
    couplings=[
        Coupling("D1", "pressurized_volume_m3", CouplingDirection.CONTENDS),
        Coupling("D1", "power_kw", CouplingDirection.CONTENDS),
    ],
    metrics=[
        Metric(
            name="revenue_coverage",
            formula="tax_revenue_credits / public_goods_bill_credits",
            gaming_model="Deferring maintenance shrinks the denominator and makes coverage look "
                         "healthy while capital decays; audited against the twin's deferred-"
                         "maintenance backlog.",
            rotation_policy="re-baseline the bill every 6 cycles",
        ),
        Metric(
            name="effective_progressivity",
            formula="corr(tax_paid, pressurized_volume_m3)",
            gaming_model="Splitting a holding across nominal persons reduces measured volume per "
                         "payer; mitigated by self-assessed valuation with a purchase option.",
            rotation_policy="recompute on the household-linked register each cycle",
        ),
    ],
    failure_modes=[
        FailureMode("revenue_shortfall", "revenue_coverage < 1.0", "D13"),
        FailureMode("regressive_drift", "effective_progressivity < 0", "D15"),
        FailureMode("valuation_collusion", "self-assessment below clearing price for 3 cycles",
                    "D15"),
    ],
    rules=[
        Rule(
            id="R-D2-01",
            applies_to_class="all volume holders",
            published=True,
            effective_cycle=1,
            predicate="tax_due = volume_tax_rate * pressurized_volume_m3",
            enforcement_ref="D4:collections",
            sunset_cycles=12,
        ),
        Rule(
            id="R-D2-02",
            applies_to_class="all volume holders",
            published=True,
            effective_cycle=1,
            predicate="self_assessed_value binds the holder to sell at that value",
            enforcement_ref="D4:purchase-option",
            sunset_cycles=12,
        ),
    ],
    falsification_test=_falsification_test,
)
