"""F2 guideline-intake tests: the threshold gap must be closed AT THE SOURCE.

The central assertion of this file is negative: there must exist NO path through `compile_guidelines`
that yields a binding type-F guideline whose level did not come from a panel.
"""

import pytest
from dataclasses import replace

from aigov.contract import (
    Guideline, GuidelineType, ProvenanceKind, ObjectiveRef, Direction, Provenance, validate,
)
from aigov.intake import (
    AGGREGATED, DEFAULT_POLARIZATION, ESCALATE, GuidelineDraft, IntakeError, LevelElicitation,
    MIN_CAMP_SHARE, Panel, PriorityBallot, ProceduralParameter, audit_record,
    calibrate_polarization, compile_guidelines, draw_panel, elicit_level, qv_cost, tally_priorities,
)
from aigov.specs.d2_economy import SPEC as D2

ELECTORATE = ["c{:03d}".format(i) for i in range(400)]


def codes(errs):
    return {e.code for e in errs}


# ---------------------------------------------------------------- sortition (G4)

def test_panel_draw_is_reproducible_from_the_seed():
    a = draw_panel(ELECTORATE, 24, seed=1234)
    b = draw_panel(ELECTORATE, 24, seed=1234)
    assert a.members == b.members and a.fingerprint() == b.fingerprint()


def test_different_seeds_give_different_panels():
    assert draw_panel(ELECTORATE, 24, seed=1).members != draw_panel(ELECTORATE, 24, seed=2).members


def test_panel_is_a_subset_without_replacement():
    p = draw_panel(ELECTORATE, 30, seed=7)
    assert len(p.members) == len(set(p.members)) == 30
    assert set(p.members) <= set(ELECTORATE)


def test_panel_larger_than_electorate_is_refused():
    with pytest.raises(ValueError):
        draw_panel(["a", "b"], 5, seed=1)


def test_panel_size_must_be_positive():
    with pytest.raises(ValueError):
        draw_panel(ELECTORATE, 0, seed=1)


# ---------------------------------------------------------------- quadratic budget (G5)

def test_cost_is_quadratic_not_linear():
    assert qv_cost([3]) == 9
    assert qv_cost([1, 1, 1]) == 3          # spreading is cheap
    assert qv_cost([5]) == 25 > qv_cost([2, 2, 2, 2])  # concentrating is dear


def test_over_budget_ballot_is_rejected_not_clipped():
    """Clipping would silently rewrite a citizen's expressed intensity."""
    ballots = [PriorityBallot("c001", {"air": 10}),          # cost 100
               PriorityBallot("c002", {"air": 3, "food": 3})]  # cost 18
    ranking, errs = tally_priorities(ballots, budget=25)
    assert "G5" in codes(errs)
    assert dict(ranking) == {"air": 3, "food": 3}, "the rejected ballot must not contribute at all"


def test_negative_votes_are_rejected():
    _, errs = tally_priorities([PriorityBallot("c001", {"air": -4})], budget=100)
    assert "G5" in codes(errs)


def test_ranking_orders_by_total_votes():
    ballots = [PriorityBallot("c001", {"air": 4, "food": 2}),
               PriorityBallot("c002", {"air": 3, "food": 3}),
               PriorityBallot("c003", {"food": 4})]
    ranking, errs = tally_priorities(ballots, budget=25)
    assert errs == []
    assert ranking[0][0] == "food" and dict(ranking) == {"food": 9, "air": 7}


# ---------------------------------------------------------------- level elicitation (G6, G7)

def test_level_is_the_median_not_the_mean():
    """One extreme report must not drag the level — the whole reason median was chosen."""
    p = draw_panel(ELECTORATE, 9, seed=3)
    proposals = [24, 25, 25, 26, 25, 24, 26, 25, 900]   # mean ~120, median 25
    e = elicit_level("volume_per_person_m3", proposals, p)
    assert e.verdict == AGGREGATED
    assert e.level == 25.0


def test_unimodal_panel_aggregates():
    p = draw_panel(ELECTORATE, 8, seed=5)
    e = elicit_level("o2_floor_kpa", [16, 16.2, 15.8, 16.1, 16, 15.9, 16.3, 16], p)
    assert e.verdict == AGGREGATED and 15.8 <= e.level <= 16.3


@pytest.mark.parametrize("proposals,label", [
    ([10, 10, 11, 10, 40, 41, 40, 40], "50/50"),
    ([25] * 11 + [40] * 5, "30/70"),
    ([25] * 12 + [55] * 4, "25/75"),
])
def test_polarized_panel_escalates_rather_than_aggregating(proposals, label):
    """A median is always DEFINED; on two camps it is a number nobody proposed."""
    p = draw_panel(ELECTORATE, 8, seed=6)
    e = elicit_level("volume_per_person_m3", proposals, p)
    assert e.verdict == ESCALATE and e.level is None, label
    assert "polarized" in e.reason


# --- the two defects that a SWEEP found and the unit tests had missed ---

@pytest.mark.parametrize("sd,label", [(0.5, "tight"), (2, "moderate"), (10, "wide")])
def test_unimodal_panels_never_false_escalate_at_any_width(sd, label):
    """Defect 1: the original gap/range metric scored a tight cluster at 0.50 and false-escalated a
    wide unimodal panel. Bimodality must be scale-invariant."""
    import random as _r
    rng = _r.Random(11)
    p = draw_panel(ELECTORATE, 16, seed=12)
    e = elicit_level("v", [25 + rng.gauss(0, sd) for _ in range(16)], p)
    assert e.verdict == AGGREGATED, "{} unimodal panel must aggregate (score {:.3f})".format(
        label, e.spread)


@pytest.mark.parametrize("n_extremists", [1, 2, 3])
def test_a_small_minority_cannot_force_escalation(n_extremists):
    """Defect 2: an unconstrained 2-means split scored ONE outlier at 1.000, handing any single
    panelist a unilateral veto on aggregation — the exact strategic vector the median resists."""
    p = draw_panel(ELECTORATE, 16, seed=13)
    proposals = [25.0] * (16 - n_extremists) + [900.0 + i for i in range(n_extremists)]
    e = elicit_level("v", proposals, p)
    assert e.verdict == AGGREGATED, "{} extremist(s) of 16 forced an escalation".format(n_extremists)
    assert e.level == 25.0, "the median must be untouched by the extremists"


def test_unanimous_panel_scores_zero_polarization():
    p = draw_panel(ELECTORATE, 8, seed=14)
    e = elicit_level("v", [25] * 8, p)
    assert e.spread == 0.0 and e.verdict == AGGREGATED


def test_threshold_is_derived_and_the_derivation_reproduces():
    """The default tolerance must be the CALIBRATED number, not a guess — and re-derivable."""
    cal = calibrate_polarization()
    assert cal == calibrate_polarization(), "calibration must be deterministic"
    assert abs(DEFAULT_POLARIZATION.value - cal["best_threshold"]) <= 0.02, (
        "default {} drifted from the derived best threshold {}".format(
            DEFAULT_POLARIZATION.value, cal["best_threshold"]))
    assert cal["unimodal_p95"] < DEFAULT_POLARIZATION.value < cal["bimodal_p50"]


def test_empty_proposals_escalate():
    p = draw_panel(ELECTORATE, 4, seed=8)
    e = elicit_level("x", [], p)
    assert e.verdict == ESCALATE and "nothing was elicited" in e.reason


def test_unanimous_panel_does_not_false_escalate():
    p = draw_panel(ELECTORATE, 6, seed=9)
    e = elicit_level("x", [25, 25, 25, 25, 25, 25], p)
    assert e.verdict == AGGREGATED and e.level == 25.0


# ---------------------------------------------------------------- THE threshold gap (G1)

def _panel():
    return draw_panel(ELECTORATE, 12, seed=42)


def _good_elicitation(p, level=25.0):
    return LevelElicitation("volume", tuple([level] * 5), AGGREGATED, level, 0.0, p.id, "median")


def test_type_F_without_elicitation_cannot_compile():
    """THE central negative test: no path yields a binding floor the governor invented."""
    p = _panel()
    d = GuidelineDraft("G-F-X", "Everyone should have enough space.", GuidelineType.F,
                       elicitation=None, ratified=True)
    out, errs = compile_guidelines([d], p)
    assert out == []
    assert "G1" in codes(errs)
    assert any("threshold gap" in e.message for e in errs)


def test_type_F_with_escalated_elicitation_cannot_compile():
    p = _panel()
    esc = LevelElicitation("volume", (10, 40), ESCALATE, None, 0.9, p.id, "polarized")
    out, errs = compile_guidelines(
        [GuidelineDraft("G-F-Y", "…", GuidelineType.F, elicitation=esc, ratified=True)], p)
    assert out == [] and "G7" in codes(errs)


def test_type_F_with_a_foreign_panel_cannot_compile():
    """A level laundered through a different panel is not this polity's answer."""
    p, other = _panel(), draw_panel(ELECTORATE, 12, seed=99, panel_id="P-OTHER")
    e = _good_elicitation(other)
    out, errs = compile_guidelines(
        [GuidelineDraft("G-F-Z", "…", GuidelineType.F, elicitation=e, ratified=True)], p)
    assert out == [] and "G4" in codes(errs)


def test_type_F_with_real_elicitation_compiles_and_carries_the_level():
    p = _panel()
    out, errs = compile_guidelines(
        [GuidelineDraft("G-F-003", "Everyone should have enough living space to be healthy.",
                        GuidelineType.F, elicitation=_good_elicitation(p), ratified=True)], p)
    assert errs == [] and len(out) == 1
    g = out[0]
    assert g.gtype is GuidelineType.F and g.level == 25.0
    assert g.is_binding() and g.elicitation_complete()


def test_unratified_draft_never_compiles():
    p = _panel()
    out, errs = compile_guidelines(
        [GuidelineDraft("G-X", "…", GuidelineType.P, ratified=False)], p)
    assert out == [] and "G1" in codes(errs)


def test_type_D_without_a_metric_cannot_compile():
    p = _panel()
    out, errs = compile_guidelines(
        [GuidelineDraft("G-D-X", "We should improve.", GuidelineType.D, ratified=True)], p)
    assert out == [] and "G1" in codes(errs)


# ---------------------------------------------------------------- P/O compile clean; A stays visible (G3)

@pytest.mark.parametrize("gtype,text", [
    (GuidelineType.P, "People should be free to invent without a committee picking winners."),
    (GuidelineType.O, "People who use more should pay more."),
])
def test_P_and_O_compile_with_no_elicited_number(gtype, text):
    """The clean case from probe B1: a SHAPE binds without anyone supplying a number."""
    p = _panel()
    out, errs = compile_guidelines([GuidelineDraft("G-1", text, gtype, ratified=True)], p)
    assert errs == [] and len(out) == 1
    assert out[0].is_binding() and out[0].level is None and out[0].elicitation_complete()


def test_aspiration_is_emitted_but_non_binding_never_silently_dropped():
    p = _panel()
    out, errs = compile_guidelines(
        [GuidelineDraft("G-A-006", "No one should die from a foreseeable failure.",
                        GuidelineType.A, ratified=True)], p)
    assert errs == [] and len(out) == 1
    assert out[0].gtype is GuidelineType.A
    assert not out[0].is_binding(), "an aspiration must never bind"


# ---------------------------------------------------------------- recursive honesty (G2)

def test_ai_supplied_procedural_parameter_is_refused():
    """The governor may not supply the numbers its own procedure runs on."""
    bad = ProceduralParameter("polarization_tolerance", 0.9,
                              ProvenanceKind.AI_SUPPLIED, "model judgement")
    out, errs = compile_guidelines(
        [GuidelineDraft("G-P-1", "…", GuidelineType.P, ratified=True)], _panel(), tolerance=bad)
    assert out == [] and "G2" in codes(errs)
    assert any("its own procedure runs on" in e.message for e in errs)


def test_the_default_procedural_parameter_is_legitimate():
    assert DEFAULT_POLARIZATION.is_legitimate()
    assert DEFAULT_POLARIZATION.provenance_kind is not ProvenanceKind.AI_SUPPLIED


def test_a_parameter_with_empty_provenance_ref_is_illegitimate():
    assert not ProceduralParameter("t", 0.5, ProvenanceKind.GUIDELINE, "").is_legitimate()


# ---------------------------------------------------------------- end-to-end + integration

def test_full_round_produces_a_reproducible_audit_record():
    p = draw_panel(ELECTORATE, 16, seed=2026)
    ballots = [PriorityBallot(m, {"life_support": 3, "housing": 2}) for m in p.members[:8]] + \
              [PriorityBallot(m, {"housing": 4}) for m in p.members[8:]]
    ranking, terrs = tally_priorities(ballots, budget=25)
    el = elicit_level("volume_per_person_m3", [24, 25, 25, 26, 25, 25, 24, 26], p)
    drafts = [
        GuidelineDraft("G-O-002", "People who use more should pay more.", GuidelineType.O, ratified=True),
        GuidelineDraft("G-F-003", "Everyone should have enough living space.", GuidelineType.F,
                       elicitation=el, ratified=True),
        GuidelineDraft("G-A-006", "No one should die from a foreseeable failure.", GuidelineType.A,
                       ratified=True),
    ]
    gs, errs = compile_guidelines(drafts, p)
    rec = audit_record(p, ranking, [el], gs, terrs + errs)

    assert terrs == [] and errs == []
    assert set(rec["binding"]) == {"G-O-002", "G-F-003"}
    assert rec["non_binding"] == ["G-A-006"]
    assert rec["panel_fingerprint"] == draw_panel(ELECTORATE, 16, seed=2026).fingerprint()
    assert rec["priority_ranking"][0][0] == "housing"


def test_intake_output_satisfies_the_department_contract():
    """The real integration: an intake-produced guideline must bind a real department clean."""
    p = _panel()
    gs, errs = compile_guidelines(
        [GuidelineDraft("G-F-003", "Everyone should have enough living space to be healthy.",
                        GuidelineType.F, elicitation=_good_elicitation(p, 25.0), ratified=True)], p)
    assert errs == []
    registry = {g.id: g for g in gs}
    # D2's floor objective + constraint both cite G-F-003 at level 25.0.
    assert [e for e in validate(D2, registry) if e.code == "I11"] == []


def test_intake_level_mismatch_is_caught_downstream_by_I11():
    """Belt and braces: if a level ever diverged, the validator still refuses it."""
    p = _panel()
    gs, _ = compile_guidelines(
        [GuidelineDraft("G-F-003", "…", GuidelineType.F,
                        elicitation=_good_elicitation(p, 12.0), ratified=True)], p)
    registry = {g.id: g for g in gs}          # level 12.0, but D2 hard-codes threshold 25.0
    errs = validate(D2, registry)
    assert "I11" in {e.code for e in errs}
    assert any("does not match the elicited level" in e.message for e in errs)


# ---------------------------------------------------------------- the LIVE registry is intake-derived

def test_live_registry_is_produced_by_a_real_intake_round():
    """`guidelines.py` used to declare `level=25.0` with a comment claiming it was elicited.
    The comment asserted a provenance the code did not have. Now it does."""
    from aigov.guidelines import COMPILE_ERRORS, ELICITATIONS, INTAKE_RECORD, RATIFIED
    assert COMPILE_ERRORS == []
    assert set(INTAKE_RECORD["binding"]) == {g.id for g in RATIFIED.values() if g.is_binding()}
    for g in RATIFIED.values():
        if g.level is not None:
            assert any(e.level == g.level and e.verdict == AGGREGATED
                       for e in ELICITATIONS.values()), \
                "level of {} traces to no elicitation record".format(g.id)


def test_departments_read_thresholds_and_never_restate_them():
    """A restated threshold drifts, and a drifted copy is indistinguishable from an AI-supplied one."""
    from aigov.guidelines import RATIFIED
    from aigov.specs.d1_lifesupport import SPEC as D1
    floor = next(c for c in D2.hard_constraints if c.name == "min_volume_floor")
    o2 = next(c for c in D1.hard_constraints if c.name == "o2_floor")
    assert floor.threshold == RATIFIED["G-F-003"].level
    assert o2.threshold == RATIFIED["G-F-004"].level
    obj = D2.objectives_received[0]
    assert obj.threshold == RATIFIED[obj.guideline_id].level


def test_no_literal_numeric_threshold_survives_in_a_spec_source():
    """Source-level guard: a future edit that types a number back in fails here."""
    import pathlib
    import re
    for f in ("aigov/specs/d1_lifesupport.py", "aigov/specs/d2_economy.py"):
        src = pathlib.Path(f).read_text(encoding="utf-8")
        assert not re.search(r"threshold\s*=\s*[\d.]", src), \
            "{} restates a numeric threshold instead of reading it from the registry".format(f)


def test_level_of_refuses_an_unproduced_guideline():
    from aigov.guidelines import level_of
    with pytest.raises(KeyError):
        level_of("G-NEVER-RATIFIED")


def test_level_of_refuses_a_guideline_with_no_level():
    from aigov.guidelines import level_of
    with pytest.raises(ValueError):
        level_of("G-O-002")          # an ordering carries no level, by design


def test_a_polarized_panel_would_break_the_build_rather_than_invent_a_level():
    """The load-bearing negative: if the fixture panel were polarized, no level would be produced."""
    p = _panel()
    el = elicit_level("volume", [10, 10, 11, 10, 40, 41, 40, 40] * 2, p)
    out, errs = compile_guidelines(
        [GuidelineDraft("G-F-003", "…", GuidelineType.F, elicitation=el, ratified=True)], p)
    assert out == [] and "G7" in codes(errs)
