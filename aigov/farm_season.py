"""F16: one full replayed potato season under the UNCHANGED aigov kernel.

The composition this module runs, day by day over the cached reference season:
F14's world (``FarmTwin``) grows the crop; F15's observation layer measures blight risk as
``Estimate``\\ s; a rule-following farm department proposes the ratified Blitecast decision; the
kernel certifies (``farm_fail_safe_gate``) and applies — or refuses/escalates. NOTHING applies
outside ``Governor.apply``.

**Cadence (resolves the F16 ledger unknown — design decision, recorded here):** proposals are
ON-CHANGE, not per-tick. A proposal's information content is the CHANGE of the rule's decision
against the currently-applied state; proposing an identical setting 150 times would flood the
ratification seam with noise. Ambiguous days (measurement straddles the threshold) generate NO
proposal and are counted — they are the governed loop's escalation pressure.

**Two governed arms, both through the kernel:**

- ``governed-precision``: the observation carries its honest error bar (±3% RH recount). Where the
  interval straddles the published threshold the certifier ESCALATEs — on reanalysis-grade RH this
  is the dominant outcome (the F15 measured finding), and surfacing it is the point.
- ``governed-nominal``: sensitivity arm — the same chain with the sensor-error term set to zero
  (``rel_error=0``; still an Estimate, stated in its method string). Shows the chain completing
  with a certified, applied spray when the measurement is taken at face value, which is how the
  published rule is operated in practice.

**Comparison arms (no kernel — counters over the same season data):**

- ``calendar``: protectant sprays every 7 days from 50% emergence (the conventional-practice
  comparator used by the published Blitecast validations; UMaine/WSU spray-interval convention).
- ``never-treat``: nothing, ever.

Honesty (inherited D7 + the F16 ledger's own flag): the PP-mode world has NO disease, so YIELD is
identical across arms by construction — the report's yield figure is a model-coherent ceiling,
never an outcome claim. The yield-denominated comparison is the registered v2 arm
(``van Oijen dynamic LAI damage coupling``), constraint ``van-oijen-coupling-paywall``.
The scripted ratifier below is SIMULATED conventional-practice authority (a replay has no live
assembly); it is named here and in the report, and `RatificationRecord.is_genuine` still refuses
self-referring bodies.
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass, field

from .blight_rules import BLITECAST_SEVERITY_THRESHOLD, smith_day, smith_periods
from .farm_observation import FarmObservation
from .farm_twin import EMERGENCE_DAYS, FarmTwin, TRIALS
from .farm_certifier import DONT_TREAT, TREAT
from .kernel import CandidateAction, Governor, RatificationRecord
from .twin import ColonyTwin, Estimate

CALENDAR_SPRAY_INTERVAL_DAYS = 7  # conventional weekly protectant schedule (UMaine/WSU convention)

FARM_DEPT = "farm-ops"
RATIFYING_BODY = "family-assembly (SIMULATED conventional-practice ratifier — replay seam)"


@dataclass
class GovernedDayRecord:
    day: datetime.date
    decision: str                      # treat / dont-treat / ambiguous
    proposed: bool = False
    verdict: str = ""                  # certify / steering / escalate-* / "" (no proposal)
    applied: bool = False


@dataclass
class ArmResult:
    name: str
    spray_events: int = 0
    protection_start: datetime.date | None = None
    protected_days: int = 0
    ambiguous_days: int = 0
    escalations: int = 0
    refusals: int = 0
    applied_actions: int = 0
    ungated_applications: int = 0      # must stay 0 — pinned by tests
    unprotected_full_smith_periods: int = 0
    unprotected_severity_total: int = 0
    records: list = field(default_factory=list)


@dataclass
class SeasonReport:
    cultivar: str
    site: str
    year: int
    emergence_50pct: datetime.date
    season_end: datetime.date
    season_days: int
    final_twso_kg_ha: float            # model-coherent PP ceiling — identical across arms
    nominal_first_trigger: datetime.date | None
    full_smith_periods: int
    near_miss_smith_periods: int
    arms: dict = field(default_factory=dict)


def _scripted_ratifier(action: CandidateAction) -> RatificationRecord:
    """The replay's ratification seam — simulated conventional-practice authority (named)."""
    key = "{}::{}={}".format(action.dept_id, action.instrument, action.value)
    return RatificationRecord(ratified_by=RATIFYING_BODY, action_key=key)


def _decision_from(acc: Estimate) -> str:
    lo, hi = acc.interval
    if lo >= BLITECAST_SEVERITY_THRESHOLD:
        return "treat"
    if hi < BLITECAST_SEVERITY_THRESHOLD:
        return "dont-treat"
    return "ambiguous"


def run_governed_season(cultivar: str = "Fontane", site: str = "lelystad", year: int = 2020,
                        panel=None) -> SeasonReport:
    """Run the full composition. Deterministic: cached weather, seeded panel, no other RNG."""
    if panel is None:
        import random
        from .choice.governance.panel_agnostic import aggregate_single_peaked, random_panel
        rng = random.Random(7)
        panel = next(p for p in (random_panel(rng) for _ in range(400))
                     if aggregate_single_peaked(p, "nominal", 200))

    obs = FarmObservation(site)
    trial = TRIALS[(site, year)]
    emergence = trial["planting"] + datetime.timedelta(days=EMERGENCE_DAYS[(cultivar, site)])
    season_end = trial["crop_end"]
    season_days = [d for d in sorted(obs._by_day) if emergence <= d <= season_end]

    # --- risk accumulates over the replayed weather (world ticks live inside each governed arm) --
    daily_acc: dict[datetime.date, Estimate] = {
        d: obs.accumulated_severity(emergence, d) for d in season_days
    }
    nominal_first_trigger = next(
        (d for d in season_days if daily_acc[d].value >= BLITECAST_SEVERITY_THRESHOLD), None)
    smith = smith_periods([smith_day(d, obs.hours(d)) for d in season_days])

    report = SeasonReport(
        cultivar=cultivar, site=site, year=year, emergence_50pct=emergence,
        season_end=season_end, season_days=len(season_days),
        final_twso_kg_ha=0.0,  # filled from the first governed arm's completed world below
        nominal_first_trigger=nominal_first_trigger,
        full_smith_periods=sum(1 for s in smith if s.full),
        near_miss_smith_periods=sum(1 for s in smith if not s.full),
    )

    # --- the two governed arms, both through the UNCHANGED kernel -------------------------------
    from .guidelines import RATIFIED
    from .specs.d1_lifesupport import SPEC as D1
    from .specs.d2_economy import SPEC as D2

    for arm_name, strip_error in (("governed-precision", False), ("governed-nominal", True)):
        arm = ArmResult(name=arm_name)
        # The kernel holds the SAME live twin the season ticks — its constraint probe replays a
        # fresh replica to the twin's current day (see FarmTwin.probe_next_tick).
        twin = FarmTwin(cultivar, site, year)
        gov = Governor([D1, D2], RATIFIED, ColonyTwin(), scenario="nominal", farm_twin=twin)
        applied_state = DONT_TREAT
        for d in season_days:
            # The world and the weather spine advance in lockstep: one twin tick per season day.
            if not twin.terminated:
                twin.tick()
            acc = daily_acc[d]
            if strip_error:
                acc = Estimate(name=acc.name + "[nominal-sensitivity]", value=acc.value,
                               method=acc.method + " | SENSITIVITY ARM: sensor-error term set to 0",
                               rel_error=0.0)
            decision = _decision_from(acc)
            rec = GovernedDayRecord(day=d, decision=decision)
            if decision == "ambiguous":
                arm.ambiguous_days += 1
                # The published rule has NOMINALLY triggered but the measurement cannot support an
                # honest binary: route it through the kernel ONCE so the ESCALATE verdict (and the
                # human hand-off) is on the record, not silently swallowed by the cadence.
                if (acc.value >= BLITECAST_SEVERITY_THRESHOLD and applied_state == DONT_TREAT
                        and not arm.escalations):
                    action = CandidateAction(FARM_DEPT, "blight_treatment_trigger", TREAT,
                                             "nominal Blitecast trigger under ambiguous measurement")
                    cert = gov.certify(action, panel, _scripted_ratifier(action), observation=acc)
                    rec.proposed, rec.verdict = True, cert.non_steering
                    if cert.appliable:  # cannot happen while ambiguous; counted if it ever did
                        gov.apply(cert)
                        arm.applied_actions += 1
                    elif cert.non_steering.startswith("escalate"):
                        arm.escalations += 1
                    else:
                        arm.refusals += 1
            else:
                wanted = TREAT if decision == "treat" else DONT_TREAT
                if wanted != applied_state:
                    action = CandidateAction(FARM_DEPT, "blight_treatment_trigger", wanted,
                                             "published Blitecast rule decision changed")
                    cert = gov.certify(action, panel, _scripted_ratifier(action), observation=acc)
                    rec.proposed, rec.verdict = True, cert.non_steering
                    if cert.appliable:
                        gov.apply(cert)              # the ONLY apply path
                        applied_state = wanted
                        rec.applied = True
                        arm.applied_actions += 1
                        if wanted == TREAT:
                            arm.spray_events += 1
                            arm.protection_start = arm.protection_start or d
                    elif cert.non_steering.startswith("escalate"):
                        arm.escalations += 1
                    else:
                        arm.refusals += 1
            if applied_state == TREAT:
                arm.protected_days += 1
            else:
                arm.unprotected_severity_total = int(daily_acc[d].value)
            arm.records.append(rec)
        arm.unprotected_full_smith_periods = sum(
            1 for s in smith if s.full
            and (arm.protection_start is None or s.start < arm.protection_start))
        while not twin.terminated and twin.ticks < 250:
            twin.tick()  # the crop finishes even after decisions stop changing
        if report.final_twso_kg_ha == 0.0:
            report.final_twso_kg_ha = twin.summary()["TWSO"]
        report.arms[arm_name] = arm

    # --- comparison arms (counters over the same data; no kernel) -------------------------------
    calendar = ArmResult(name="calendar")
    calendar.protection_start = emergence
    calendar.spray_events = 1 + (season_end - emergence).days // CALENDAR_SPRAY_INTERVAL_DAYS
    calendar.protected_days = len(season_days)
    report.arms["calendar"] = calendar

    never = ArmResult(name="never-treat")
    never.unprotected_full_smith_periods = report.full_smith_periods
    never.unprotected_severity_total = int(daily_acc[season_days[-1]].value)
    report.arms["never-treat"] = never

    return report
