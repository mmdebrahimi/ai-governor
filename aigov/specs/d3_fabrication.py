"""D3 Research & Fabrication Capacity — the MEDIUM central-legitimacy reference department.

WHY THIS DEPARTMENT EXISTS AT ALL. The phase-1 terminal asks for governed cycles across departments
spanning HIGH, MEDIUM and LOW central legitimacy. HIGH (D1) and LOW (D2) are the easy ends: a closed
physical loop nobody disputes the centre should run, and a dispersed-knowledge domain where the
Hayek wall forbids it from trying. MEDIUM is the interesting case and was missing entirely — the
whole phase-1 gap was this one file.

WHAT MEDIUM MEANS, MECHANICALLY. "Procedure central, judgment distributed." The colony owns one set
of fabrication machines; somebody has to say who gets Tuesday. That scheduling is legitimately
central — it is a queue, and queues need an owner. What is NOT central is which project deserves
the slot. G-P-001, ratified, says people should be free to invent things "without a committee
deciding what is worth inventing." So this department may hand out MACHINE-HOURS and may not rank
PROPOSALS, and the split between those two is the entire content of MEDIUM legitimacy here.

Note what this makes D3 structurally: it receives NO objective. D1 is judged against a physical
floor and D2 against a fiscal one, but D3 has no level to hit — its job is a procedure that stays
honest. That is a genuinely different shape from both, which is exactly why it is worth having as
the third department rather than a second variation on the first two.

I8 DOES NOT APPLY HERE, AND THAT IS THE POINT. I8 forbids QUANTITY_ALLOCATION only where legitimacy
is LOW. MEDIUM permits it — so the load is carried entirely by I8b, which demands the allocative
instrument name the tier where discretion actually sits and how capture at that tier would be
caught. Devolving a decision is not the same as making it safe; it can just move the capture. Here
discretion sits with a published-seed lottery among the qualified, so there is no officer to
capture, and the capture check is reproducibility of the draw.

THE FAILURE THIS DESIGN IS SHAPED AGAINST. The obvious way to run a fab queue is to score proposals
on merit. That is efficient, it is what every research funder does, and it is precisely what G-P-001
forbids — because a committee scoring merit IS the committee deciding what is worth inventing. The
lottery is not naivety about quality; it is the only allocation rule that cannot smuggle a merit
judgment past a ratified prohibition.
"""

from ..contract import (
    Constraint, ConstraintSource, Coupling, CouplingDirection, DepartmentSpec,
    EquilibriumKind, Instrument, InstrumentClass, Legitimacy, Metric, FailureMode, Observability,
    RatificationClass, Reversibility, Role, Rule, StateVar, VSMLayer,
)


def _falsification_test() -> bool:
    """Falsifiable claim: declared capacity clears declared demand inside one cycle.

    Real numbers from the declared envelope, and it can come out FALSE — if mean job length rises
    or the applicant pool grows, the queue stops clearing and this returns False rather than
    quietly lengthening waits.
    """
    fab_hours_available_per_cycle = 240.0
    mean_job_hours = 6.0
    applicants_per_cycle = 32
    slots_per_cycle = fab_hours_available_per_cycle / mean_job_hours
    return slots_per_cycle >= applicants_per_cycle


SPEC = DepartmentSpec(
    id="D3",
    # S2 - coordination. D3 does not control a process (S1) or steer the whole (S3); it resolves
    # contention between units for a shared resource, which is what S2 is for.
    vsm_layer=VSMLayer.S2,
    central_legitimacy=Legitimacy.MEDIUM,
    roles=frozenset({Role.GENERATE}),
    sunset_cycles=12,
    state_vars=[
        StateVar("fab_hours_available", "hours", Observability.DIRECT, "D3"),
        StateVar("fab_hours_requested", "hours", Observability.DIRECT, "D3"),
        StateVar("fab_hours_used", "hours", Observability.DIRECT, "D3"),
        StateVar("queue_wait_cycles", "cycles", Observability.DIRECT, "D3"),
        StateVar("power_kw", "kW", Observability.DIRECT, "D1"),
        StateVar("pressurized_volume_m3", "m^3", Observability.DIRECT, "D1"),
        # LATENT on purpose, and the most important declaration in this file. The worth of an
        # un-built invention is exactly the quantity no central body can observe — which is the
        # claim G-P-001 encodes. Declaring it DIRECT or ESTIMATED would assert the opposite.
        StateVar("project_value", "credits", Observability.LATENT, "D3"),
    ],
    instruments=[
        Instrument(
            "fab_slot_allocation", InstrumentClass.QUANTITY_ALLOCATION,
            (0.0, 240.0), 1, Reversibility.REVERSIBLE, RatificationClass.SIMPLE,
            discretion_tier="no officer and no panel: slots are drawn by lottery from a PUBLISHED "
                            "seed among applicants holding the safety qualification. The tier "
                            "holding discretion is the qualified pool itself, which is why there "
                            "is no seat to capture.",
            capture_check="D15 re-runs the draw from the published seed and the applicant "
                          "register; any allocated sequence that cannot be reproduced is a "
                          "finding. A quietly narrowed qualification is caught the same way - the "
                          "register is an input to the replay, so shrinking it changes the "
                          "reproduced sequence.",
        ),
        Instrument("fab_queue_discipline_rule", InstrumentClass.RULE,
                   (0.0, 1.0), 2, Reversibility.REVERSIBLE, RatificationClass.SIMPLE),
        Instrument("fab_overrun_price", InstrumentClass.PRICE,
                   (0.0, 20.0), 1, Reversibility.REVERSIBLE, RatificationClass.SIMPLE),
    ],
    # DELIBERATELY EMPTY. D3 is judged on whether its procedure stayed honest, not on hitting a
    # level. Inventing an objective so the field looks populated would be the instrument supplying
    # the answer it exists to elicit — the same act I11 forbids for thresholds.
    objectives_received=[],
    hard_constraints=[
        # G-P-001 compiled as a PROHIBITION rather than a target: it says what may never be done,
        # so it lands here and not in objectives_received. This is the constraint that makes D3
        # MEDIUM rather than HIGH — without it, a fab department is just a central planner with a
        # machine shop.
        Constraint(
            name="allocation_is_topic_blind",
            predicate="mutual_information(allocated_slots, project_topic) == 0",
            source=ConstraintSource.CONSTITUTION,
            guideline_id="G-P-001",
        ),
        Constraint(
            name="qualification_is_safety_only",
            predicate="eligibility(applicant) depends only on held_safety_qualification",
            source=ConstraintSource.CONSTITUTION,
            guideline_id="G-P-001",
        ),
    ],
    couplings=[
        # Real contention, not decoration: the machines draw power D1 is allocating, and they sit
        # in pressurized volume D1 and D2 are both already contending over.
        Coupling("D1", "power_kw", CouplingDirection.CONTENDS),
        Coupling("D1", "pressurized_volume_m3", CouplingDirection.CONTENDS),
    ],
    metrics=[
        Metric(
            name="topic_blindness",
            formula="mutual_information(allocated_slots, project_topic)",
            gaming_model="A topic can be laundered through the applicant's declared discipline, "
                         "so measuring against the DECLARED field would score the launderer clean. "
                         "Audited by re-deriving topic from the job's material and tool signature "
                         "in machine telemetry, which the applicant does not author.",
            rotation_policy="re-derive the topic basis from telemetry every 6 cycles",
            # Not a target metric (D3 receives no objective), but assessed anyway: declining to
            # assess is the AI deciding the gaming shapes do not apply.
            ratchet_exposed=False,
            threshold_exposed=False,
        ),
        Metric(
            name="queue_wait_dispersion",
            formula="stdev(queue_wait_cycles) across applicant cohorts",
            gaming_model="Splitting one project into many small applications raises an applicant's "
                         "draw probability without raising their need, and flatters dispersion by "
                         "inflating the denominator. Audited against the project-lineage field in "
                         "the applicant register rather than the raw application count.",
            rotation_policy="re-baseline cohorts every 6 cycles",
            ratchet_exposed=False,
            threshold_exposed=False,
        ),
        Metric(
            name="capacity_utilisation",
            formula="fab_hours_used / fab_hours_available",
            gaming_model="Booking a slot and idling it keeps utilisation nominal while starving "
                         "the queue - the classic bums-on-seats measure. Audited against machine "
                         "telemetry rather than the booking ledger, which is why R-D3-02 forfeits "
                         "an unused slot.",
            rotation_policy="reconcile bookings against telemetry every cycle",
            ratchet_exposed=True,   # utilisation is exactly the measure a centre ratchets upward
            threshold_exposed=False,
        ),
    ],
    failure_modes=[
        FailureMode("topic_capture", "topic_blindness > 0 for 3 consecutive cycles", "D15"),
        FailureMode("unreproducible_draw",
                    "allocated sequence not reproducible from the published seed", "D15"),
        FailureMode("queue_starvation",
                    "max(queue_wait_cycles) exceeds the sunset window", "D13"),
    ],
    rules=[
        Rule(
            id="R-D3-01",
            applies_to_class="all qualified fabrication applicants",
            published=True,
            effective_cycle=1,
            predicate="slots are drawn by published-seed lottery among applicants holding the "
                      "safety qualification; no proposal content enters the draw",
            enforcement_ref="D15:draw-replay",
            sunset_cycles=12,
        ),
        Rule(
            id="R-D3-02",
            applies_to_class="all qualified fabrication applicants",
            published=True,
            effective_cycle=1,
            predicate="a slot unused for its first quarter returns to the pool",
            enforcement_ref="D4:queue",
            sunset_cycles=12,
        ),
    ],
    falsification_test=_falsification_test,
    # I14: ORDINARY, with the flip condition named rather than assumed away. The Matthew-effect
    # worry is real — whoever gets machine time produces results, and results usually buy the next
    # slot. It does not bite HERE only because the gate is a SAFETY qualification and the draw is
    # blind, so success cannot compound into access. If the qualification is ever widened to
    # include track record, output or promise, that severs the only thing keeping this ordinary and
    # the department must be re-declared SELF_REINFORCING_ADVERSE.
    equilibrium=EquilibriumKind.ORDINARY,
)
