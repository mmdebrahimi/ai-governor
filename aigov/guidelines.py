"""The ratified guideline set — PRODUCED BY AN INTAKE ROUND, not hand-authored.

This module used to declare `level=25.0` with a comment saying "ELICITED by the assembly". The comment
asserted a provenance the code did not have: the number was typed by the author. That is the exact
overclaim pattern `charter_invariants` detects for invariants, reappearing in the data path.

Now the levels are produced by running `aigov.intake` for real: a reproducible sortition panel is drawn,
per-topic proposals are aggregated by median with fail-closed escalation, and `compile_guidelines`
refuses any binding type-F guideline whose level did not come from that aggregation. Change the panel's
proposals and the levels change; make the panel polarized and compilation FAILS rather than inventing a
number.

**Honest label — what is real and what is a fixture.** The MECHANISM is real (sortition, quadratic budget,
median aggregation, fail-closed escalation, refusal on incomplete elicitation). The CITIZENS are not: the
proposal sets below are a deterministic FIXTURE standing in for a deliberating assembly. Nothing here is
evidence about what a real polity would choose — only about what the pipeline does with what it is given.
Replacing the fixture with real panel data is a Stage-B activity, unchanged from the inherited
`mars-governance` D1 staging.
"""

from __future__ import annotations

from .contract import GuidelineType
from .intake import (
    AGGREGATED, GuidelineDraft, PriorityBallot, audit_record, compile_guidelines, draw_panel,
    elicit_level, tally_priorities,
)

#: Colony electorate at the ratified V1 scale (D2: 100-1000).
ELECTORATE = tuple("c{:03d}".format(i) for i in range(400))

#: Reproducible sortition panel. The seed is the audit handle — anyone can redraw this exact panel.
PANEL = draw_panel(ELECTORATE, size=16, seed=20260811, panel_id="P-2026-08-11")

#: What the (fixture) panel proposed, per topic. These stand in for a deliberating assembly.
PANEL_PROPOSALS = {
    "volume_per_person_m3": [24, 25, 25, 26, 25, 24, 26, 25, 25, 26, 24, 25, 25, 25, 26, 24],
    "o2_floor_kpa":         [16, 16.2, 15.8, 16, 16.1, 15.9, 16, 16, 16.3, 15.7, 16, 16.1,
                             15.9, 16, 16.2, 15.8],
}

#: Quadratic priority budget: what the panel wanted the government to work on first.
PRIORITY_BALLOTS = (
    [PriorityBallot(m, {"life_support": 4, "housing": 2}) for m in PANEL.members[:9]]
    + [PriorityBallot(m, {"housing": 4, "innovation": 2}) for m in PANEL.members[9:]]
)
PRIORITY_BUDGET = 25

ELICITATIONS = {
    topic: elicit_level(topic, proposals, PANEL)
    for topic, proposals in PANEL_PROPOSALS.items()
}

PRIORITY_RANKING, _priority_errors = tally_priorities(PRIORITY_BALLOTS, PRIORITY_BUDGET)

_DRAFTS = [
    GuidelineDraft(
        id="G-P-001",
        text="We want people to be free to invent things without a committee deciding what is worth "
             "inventing.",
        gtype=GuidelineType.P, ratified=True),
    GuidelineDraft(
        id="G-O-002",
        text="People who use more should pay more.",
        gtype=GuidelineType.O, ratified=True),
    GuidelineDraft(
        id="G-F-003",
        text="Everyone should have enough living space to be healthy.",
        gtype=GuidelineType.F, elicitation=ELICITATIONS["volume_per_person_m3"], ratified=True),
    GuidelineDraft(
        id="G-F-004",
        text="Breathable air must never fall below a safe level.",
        gtype=GuidelineType.F, elicitation=ELICITATIONS["o2_floor_kpa"], ratified=True),
    GuidelineDraft(
        id="G-D-005",
        text="We should keep getting better at recycling what we have.",
        gtype=GuidelineType.D, metric="closure_fraction", ratified=True),
    GuidelineDraft(
        id="G-A-006",
        text="No one should die from a life-support failure the colony could have foreseen.",
        gtype=GuidelineType.A, ratified=True),
]

_compiled, COMPILE_ERRORS = compile_guidelines(_DRAFTS, PANEL)

#: The registry every department binds against. Levels here came out of ELICITATIONS.
RATIFIED = {g.id: g for g in _compiled}

#: The reproducible record of the round that produced RATIFIED.
INTAKE_RECORD = audit_record(PANEL, PRIORITY_RANKING, list(ELICITATIONS.values()),
                             _compiled, list(_priority_errors) + list(COMPILE_ERRORS))


def level_of(guideline_id: str) -> float:
    """The elicited level for a guideline. Departments call THIS instead of restating a number.

    Restating a threshold in a department spec is how the two copies drift, and a drifted copy is
    indistinguishable from an AI-supplied one (contract invariant I11 catches it, but only after the fact).
    """
    g = RATIFIED.get(guideline_id)
    if g is None:
        raise KeyError("no ratified guideline {!r} — a department may not bind to a guideline the "
                       "polity did not produce".format(guideline_id))
    if g.level is None:
        raise ValueError("guideline {} carries no elicited level (type {})".format(
            guideline_id, g.gtype.value))
    return g.level
