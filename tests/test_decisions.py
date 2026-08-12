"""The decision inventory: structure must be COMPUTED from what was elicited, never chosen.

The ratified constraint (Pending Decision 5) is traceability — a recommendation has to be
derivable from what was elicited. These tests pin that as a property: every capability carries its
source decisions, no verdict is reachable without user-supplied inputs, and there is no threshold
anywhere for the instrument to have invented.

The chaining section is the important one. An earlier version grouped by connected components over
shared facts, and a test in this file PINNED that chaining as desired behaviour. Both are gone; a
refusal test stands where the pin was.
"""

import pytest

from aigov.decisions import (
    AccountabilitySlot, CandidateCoupling, ConfirmedCapability, CouplingRecord, DecisionRecord,
    Assurance, FactKind, Reversibility, Sourcing, UngroupedCouplingLinks, accountability,
    build_inventory, classify_assurance,
    classify_sourcing, coupling_candidates, derive_capabilities, interview_questions,
    render_report,
)


def rec(**kw):
    base = dict(id="D1", question="a real decision someone faces",
                frequency_per_year=1.0, external_engagement_cost=100.0,
                internal_annual_cost=50.0, external_market_exists=True,
                information_needs=frozenset({"x"}),
                fact_kinds=(("x", FactKind.TACIT_CONTEXT),),
                accountable_role="the person who runs the place", atomic=True)
    base.update(kw)
    return DecisionRecord(**base)


def tacit(*facts):
    """A decision whose facts are all the expensive kind — the coupling-candidate case."""
    return dict(information_needs=frozenset(facts),
                fact_kinds=tuple((f, FactKind.TACIT_CONTEXT) for f in facts))


def cheap(*facts):
    """A decision whose facts are all written down — shared data, not shared context."""
    return dict(information_needs=frozenset(facts),
                fact_kinds=tuple((f, FactKind.TRANSFERABLE_RECORD) for f in facts))


def yes(a, b):
    return CouplingRecord(a, b, True)


def no(a, b):
    return CouplingRecord(a, b, False)


# ---------------------------------------------------------------- the Coase test

def test_internalize_when_the_market_costs_more_over_a_year():
    v = classify_sourcing(rec(frequency_per_year=10, external_engagement_cost=100,
                              internal_annual_cost=500))
    assert v.sourcing is Sourcing.INTERNALIZE
    assert "cheaper to own" in v.rationale


def test_market_when_buying_is_cheaper_and_nothing_is_private():
    v = classify_sourcing(rec(frequency_per_year=1, external_engagement_cost=100,
                              internal_annual_cost=5_000))
    assert v.sourcing is Sourcing.MARKET
    assert not v.market_option_degraded


def test_no_market_forces_internalization_regardless_of_cost():
    v = classify_sourcing(rec(external_market_exists=False,
                              external_engagement_cost=1, internal_annual_cost=10_000))
    assert v.sourcing is Sourcing.INTERNALIZE
    assert "nothing to buy" in v.rationale


def test_the_boundary_is_exact_with_no_tolerance_band():
    """No invented threshold. At equal cost the verdict flips with no dead zone, because a
    tolerance band would be a number the instrument chose."""
    equal = classify_sourcing(rec(frequency_per_year=1, external_engagement_cost=100,
                                  internal_annual_cost=100))
    just_over = classify_sourcing(rec(frequency_per_year=1, external_engagement_cost=100.01,
                                      internal_annual_cost=100))
    assert equal.sourcing is Sourcing.MARKET
    assert just_over.sourcing is Sourcing.INTERNALIZE


# ---------------------------------------------------------------- HYBRID: the first defect found

def test_private_information_produces_HYBRID_not_market():
    """LIVE DEFECT on the first run of this module: private information was recorded, printed as a
    'degraded' note, and then had NO effect on the verdict — a declared field nothing acted on."""
    v = classify_sourcing(rec(frequency_per_year=1, external_engagement_cost=100,
                              internal_annual_cost=5_000,
                              private_information=("what our family will actually tolerate",)))
    assert v.sourcing is Sourcing.HYBRID
    assert v.market_option_degraded
    assert "cannot supply the JUDGMENT" in v.rationale


# ---------------------------------------------------------------- the unanswered question

@pytest.mark.parametrize("field", ["frequency_per_year", "external_engagement_cost",
                                   "internal_annual_cost", "external_market_exists"])
def test_any_missing_input_yields_UNDECIDABLE_and_names_the_gap(field):
    v = classify_sourcing(rec(**{field: None}))
    assert v.sourcing is Sourcing.UNDECIDABLE
    assert field in v.missing and field in v.rationale


def test_undecidable_applies_no_default():
    v = classify_sourcing(rec(internal_annual_cost=None))
    assert v.sourcing is not Sourcing.MARKET and v.sourcing is not Sourcing.INTERNALIZE
    assert "No default is applied" in v.rationale


# ---------------------------------------------------------------- chaining is REFUSED

def test_chaining_is_refused_where_the_old_version_pinned_it():
    """THE REGRESSION GUARD. A-B affirmed and B-C affirmed does NOT imply A-C.

    An earlier version computed connected components over shared facts and a test in this file
    asserted the chaining was correct. It was not: it merged decisions that share nothing through
    an intermediary. The component {A,B,C} needs three affirmed pairs and has two, so it yields no
    capability at all — it is handed back for a human to group.
    """
    a = rec(id="A", internal_annual_cost=10, **tacit("x"))
    b = rec(id="B", internal_annual_cost=10, **tacit("x", "y"))
    c = rec(id="C", internal_annual_cost=10, **tacit("y"))
    confirmed, ungrouped = derive_capabilities([a, b, c], [yes("A", "B"), yes("B", "C")])
    assert confirmed == []
    assert len(ungrouped) == 1
    assert ungrouped[0].decision_ids == ("A", "B", "C")
    assert ungrouped[0].missing_pairs == (("A", "C"),)


def test_a_complete_triangle_does_form_one_capability():
    """The other half: when every pair IS affirmed, the group is real."""
    a = rec(id="A", internal_annual_cost=10, **tacit("x"))
    b = rec(id="B", internal_annual_cost=10, **tacit("x", "y"))
    c = rec(id="C", internal_annual_cost=10, **tacit("y"))
    confirmed, ungrouped = derive_capabilities(
        [a, b, c], [yes("A", "B"), yes("B", "C"), yes("A", "C")])
    assert ungrouped == []
    assert len(confirmed) == 1 and confirmed[0].decision_ids == ("A", "B", "C")
    assert len(confirmed[0].affirmed_pairs) == 3


def test_an_explicit_no_keeps_two_decisions_apart():
    a = rec(id="A", internal_annual_cost=10, **tacit("x"))
    b = rec(id="B", internal_annual_cost=10, **tacit("x"))
    confirmed, ungrouped = derive_capabilities([a, b], [no("A", "B")])
    assert confirmed == [] and ungrouped == []


def test_an_affirmed_pair_is_a_capability():
    a = rec(id="A", internal_annual_cost=10, question="qa", **tacit("x"))
    b = rec(id="B", internal_annual_cost=10, question="qb", **tacit("x"))
    confirmed, ungrouped = derive_capabilities([a, b], [yes("A", "B")])
    assert len(confirmed) == 1
    assert confirmed[0].decision_ids == ("A", "B")
    assert set(confirmed[0].derived_from) == {"qa", "qb"}


def test_no_coupling_answers_means_no_structure_at_all():
    """Silence is not agreement. Nothing groups until the user says so."""
    a = rec(id="A", internal_annual_cost=10, **tacit("x"))
    b = rec(id="B", internal_annual_cost=10, **tacit("x"))
    confirmed, ungrouped = derive_capabilities([a, b], [])
    assert confirmed == [] and ungrouped == []


def test_two_disjoint_affirmed_pairs_stay_two_capabilities():
    ds = [rec(id=i, internal_annual_cost=10, **tacit(i.lower())) for i in ("A", "B", "C", "D")]
    confirmed, _ = derive_capabilities(ds, [yes("A", "B"), yes("C", "D")])
    assert [c.decision_ids for c in confirmed] == [("A", "B"), ("C", "D")]


# ---------------------------------------------------------------- the fact-kind gate

def test_a_shared_transferable_record_is_not_a_coupling_candidate():
    """THE SECOND DEFECT. 'Should we acquire this building' and 'can we run payroll Friday' were
    grouped because both need cash_available — a number in a spreadsheet."""
    a = rec(id="A", internal_annual_cost=10, **cheap("cash_available"))
    b = rec(id="B", internal_annual_cost=10, **cheap("cash_available"))
    assert coupling_candidates([a, b]) == []


def test_a_shared_tacit_fact_is_a_coupling_candidate():
    a = rec(id="A", internal_annual_cost=10, **tacit("who we can actually trust"))
    b = rec(id="B", internal_annual_cost=10, **tacit("who we can actually trust"))
    cands = coupling_candidates([a, b])
    assert len(cands) == 1 and cands[0].shared_facts == ("who we can actually trust",)


def test_organization_specific_context_also_couples():
    facts = dict(information_needs=frozenset({"how we phase cash"}),
                 fact_kinds=(("how we phase cash", FactKind.ORGANIZATION_SPECIFIC_CONTEXT),))
    a = rec(id="A", internal_annual_cost=10, **facts)
    b = rec(id="B", internal_annual_cost=10, **facts)
    assert len(coupling_candidates([a, b])) == 1


def test_an_unclassified_fact_generates_no_candidate():
    """Fail closed. Assuming an unclassified fact is expensive would manufacture the coupling."""
    a = rec(id="A", internal_annual_cost=10, information_needs=frozenset({"z"}), fact_kinds=())
    b = rec(id="B", internal_annual_cost=10, information_needs=frozenset({"z"}), fact_kinds=())
    assert coupling_candidates([a, b]) == []
    assert a.unclassified_facts() == ("z",)


def test_market_decisions_are_never_coupling_candidates():
    """You do not group a capability you buy outright."""
    a = rec(id="A", internal_annual_cost=5_000, **tacit("x"))
    b = rec(id="B", internal_annual_cost=5_000, **tacit("x"))
    assert classify_sourcing(a).sourcing is Sourcing.MARKET
    assert coupling_candidates([a, b]) == []


def test_undecidable_decisions_are_never_coupling_candidates():
    a = rec(id="A", frequency_per_year=None, **tacit("x"))
    b = rec(id="B", internal_annual_cost=10, **tacit("x"))
    assert coupling_candidates([a, b]) == []


def test_the_candidate_filter_is_a_real_reduction_not_a_relabel():
    """The reason the filter exists: asking every pair is quadratic and nobody answers honestly."""
    ds = [rec(id="D{}".format(i), internal_annual_cost=10,
              **(tacit("shared") if i < 2 else cheap("ledger"))) for i in range(6)]
    total_pairs = 6 * 5 // 2
    assert total_pairs == 15
    assert len(coupling_candidates(ds)) == 1


# ---------------------------------------------------------------- accountability is a ROLE

def test_every_decision_gets_an_accountability_slot_regardless_of_sourcing():
    """Outsourcing the work does not outsource the accountability."""
    bought = rec(id="M", internal_annual_cost=5_000)
    assert classify_sourcing(bought).sourcing is Sourcing.MARKET
    slots = accountability([bought])
    assert slots == [AccountabilitySlot("M", "the person who runs the place")]


def test_an_unfilled_slot_is_reported_not_invented():
    r = build_inventory([rec(id="A", internal_annual_cost=10, accountable_role="")])
    assert r.unowned == ("A",)
    assert not r.is_complete


def test_an_unfilled_slot_does_not_block_derivation():
    a = rec(id="A", internal_annual_cost=10, accountable_role="", **tacit("x"))
    b = rec(id="B", internal_annual_cost=10, accountable_role="", **tacit("x"))
    r = build_inventory([a, b], [yes("A", "B")])
    assert len(r.capabilities) == 1
    assert r.unowned == ("A", "B")


def test_the_field_is_a_role_slot_not_a_person_field():
    """A name in a persisted artifact is a privacy leak waiting to happen."""
    assert "accountable_role" in DecisionRecord.__dataclass_fields__
    for forbidden in ("accountable_owner", "owner", "person", "owner_name", "assignee"):
        assert forbidden not in DecisionRecord.__dataclass_fields__


# ---------------------------------------------------------------- atomicity gates everything

def test_a_compound_decision_gets_no_verdict_at_all():
    """"Manage financing" and "should we offer 1.2M for 123 Main St" are both legitimate English
    and produce completely different structures. A verdict on the first is meaningless, not
    approximate."""
    v = classify_sourcing(rec(atomic=False))
    assert v.sourcing is Sourcing.UNDECIDABLE
    assert "split it and re-run" in v.rationale
    assert "atomic" in v.missing


def test_compound_beats_complete_cost_answers():
    """Ordering matters: every cost field answered does not rescue a malformed question."""
    fully_costed = rec(atomic=False, frequency_per_year=10, external_engagement_cost=1,
                       internal_annual_cost=1_000_000, external_market_exists=True)
    assert fully_costed.missing_fields() == ()
    assert classify_sourcing(fully_costed).sourcing is Sourcing.UNDECIDABLE


def test_a_compound_decision_joins_no_capability():
    a = rec(id="A", atomic=False, internal_annual_cost=10, **tacit("x"))
    b = rec(id="B", internal_annual_cost=10, **tacit("x"))
    assert coupling_candidates([a, b]) == []


def test_unasked_atomicity_does_not_block():
    """`None` is merely unasked. Blocking on silence would make every existing decision
    UNDECIDABLE, and the four cost fields are what the verdict actually consumes."""
    v = classify_sourcing(rec(atomic=None, internal_annual_cost=10))
    assert v.sourcing is Sourcing.INTERNALIZE


def test_unasked_atomicity_still_generates_the_question():
    d = rec(atomic=None, private_information=("p",), reversibility=Reversibility.COSTLY)
    assert any("ONE decision, or several" in q for q in interview_questions(d))


def test_atomicity_answered_yes_generates_no_question():
    d = rec(atomic=True, private_information=("p",), reversibility=Reversibility.COSTLY)
    assert interview_questions(d) == ["[D1] a real decision someone faces"]


# ---------------------------------------------------------------- assurance is a SEPARATE axis

@pytest.mark.parametrize("rev,expected", [
    (Reversibility.REVERSIBLE, Assurance.SELF_CHECK),
    (Reversibility.COSTLY, Assurance.SECOND_OPINION),
    (Reversibility.IRREVERSIBLE, Assurance.INDEPENDENT_REVIEW),
])
def test_consequence_sets_the_checking_requirement(rev, expected):
    assert classify_assurance(rec(reversibility=rev)).assurance is expected


def test_unanswered_consequence_yields_UNDECIDABLE_not_a_default():
    v = classify_assurance(rec(reversibility=None))
    assert v.assurance is Assurance.UNDECIDABLE
    assert "No default is applied" in v.rationale


def test_a_bought_decision_can_still_require_independent_review():
    """THE POINT OF THE SPLIT. Brain surgery is high-consequence and still bought.

    Sourcing says who holds the capability; assurance says how hard to check. Conflating them was
    the modelling error — and `reversibility` was elicited, asked about, and fed nothing at all.
    """
    bought = rec(internal_annual_cost=5_000, reversibility=Reversibility.IRREVERSIBLE)
    assert classify_sourcing(bought).sourcing is Sourcing.MARKET
    v = classify_assurance(bought, Sourcing.MARKET)
    assert v.assurance is Assurance.INDEPENDENT_REVIEW


def test_sourcing_never_changes_the_assurance_LEVEL():
    """Orthogonality, pinned: the same consequence gives the same level under every verdict."""
    levels = set()
    for cost in (10, 5_000):                      # INTERNALIZE, then MARKET
        d = rec(internal_annual_cost=cost, reversibility=Reversibility.IRREVERSIBLE)
        levels.add(classify_assurance(d, classify_sourcing(d).sourcing).assurance)
    assert levels == {Assurance.INDEPENDENT_REVIEW}


def test_a_bought_irreversible_decision_flags_the_supplier_conflict():
    d = rec(internal_annual_cost=5_000, reversibility=Reversibility.IRREVERSIBLE)
    v = classify_assurance(d, Sourcing.MARKET)
    assert v.supplier_conflicted
    assert "independent of the supplier" in v.rationale


def test_a_held_irreversible_decision_has_no_supplier_conflict():
    d = rec(internal_annual_cost=10, reversibility=Reversibility.IRREVERSIBLE)
    v = classify_assurance(d, Sourcing.INTERNALIZE)
    assert not v.supplier_conflicted
    assert "independent of the supplier" not in v.rationale


def test_stake_is_never_consulted_because_it_would_need_a_threshold():
    """`stake_per_decision` is context for humans. Turning money into a level needs a cutoff."""
    cheap_stake = rec(reversibility=Reversibility.COSTLY, stake_per_decision=1.0)
    huge_stake = rec(reversibility=Reversibility.COSTLY, stake_per_decision=10_000_000.0)
    assert (classify_assurance(cheap_stake).assurance
            is classify_assurance(huge_stake).assurance)


def test_unassured_decisions_are_reported_and_block_completeness():
    r = build_inventory([rec(id="A", internal_annual_cost=10, private_information=("p",))])
    assert r.unassured == ("A",)
    assert not r.is_complete


def test_the_report_shows_assurance_as_its_own_section():
    r = build_inventory([rec(id="A", internal_annual_cost=10, private_information=("p",),
                             reversibility=Reversibility.IRREVERSIBLE)])
    text = render_report(r)
    assert "ASSURANCE (how hard to check - a SEPARATE question from who holds it)" in text
    assert "independent_review" in text


# ---------------------------------------------------------------- traceability (the ratified rail)

def test_every_capability_cites_the_decisions_it_came_from():
    """This IS the ratified constraint. A capability nobody can trace is a template in disguise."""
    a = rec(id="A", internal_annual_cost=10, question="how do we water block 3?", **tacit("w"))
    b = rec(id="B", internal_annual_cost=10, question="when do we pump?", **tacit("w"))
    cap = derive_capabilities([a, b], [yes("A", "B")])[0][0]
    assert set(cap.derived_from) == {"how do we water block 3?", "when do we pump?"}
    assert cap.decision_ids == ("A", "B")


def test_capabilities_are_never_auto_named():
    a = rec(id="A", internal_annual_cost=10, **tacit("x"))
    b = rec(id="B", internal_annual_cost=10, **tacit("x"))
    assert derive_capabilities([a, b], [yes("A", "B")])[0][0].label == ""


def test_the_word_department_is_gone_from_the_public_surface():
    """Renaming the class alone would leave the defect at the API boundary.

    The old names, the old report field, and the old rendered heading all have to go — a caller
    reading `report.departments` would otherwise still treat a candidate grouping as settled
    organisational structure.
    """
    import aigov.decisions as m
    assert not hasattr(m, "DerivedDepartment")
    assert not hasattr(m, "derive_departments")
    assert "departments" not in m.InventoryReport.__dataclass_fields__
    assert "capabilities" in m.InventoryReport.__dataclass_fields__


def test_a_capability_cannot_exist_without_source_decisions():
    empty = ConfirmedCapability(decision_ids=(), derived_from=(), affirmed_pairs=())
    assert empty.size() == 0
    assert derive_capabilities([], []) == ([], [])


# ---------------------------------------------------------------- the interrogation side

def test_only_unanswered_fields_generate_questions():
    """A second pass must be short, or nobody completes it."""
    full = rec(private_information=("p",), reversibility=Reversibility.REVERSIBLE)
    assert interview_questions(full) == ["[D1] a real decision someone faces"]


def test_a_blank_decision_asks_everything():
    blank = DecisionRecord(id="Z", question="something we have never thought about")
    qs = interview_questions(blank)
    assert len(qs) == 10         # header + 4 field questions + 5 standing questions
    assert any("times a year" in q for q in qs)
    assert any("outside expert could not find out" in q for q in qs)
    assert any("the role, not the person" in q for q in qs)


def test_a_decision_with_unclassified_facts_is_asked_to_classify_them():
    d = rec(information_needs=frozenset({"a", "b"}), fact_kinds=(("a", FactKind.TACIT_CONTEXT),),
            private_information=("p",), reversibility=Reversibility.COSTLY)
    joined = " ".join(interview_questions(d))
    assert "never written down" in joined
    assert "unclassified so far: b" in joined


def test_questions_ask_for_the_users_own_numbers_not_estimates_of_an_abstraction():
    blank = DecisionRecord(id="Z", question="q")
    joined = " ".join(interview_questions(blank))
    assert "last two years" in joined
    assert "all-in" in joined


def test_a_pending_coupling_becomes_a_question():
    a = rec(id="A", internal_annual_cost=10, **tacit("x"))
    b = rec(id="B", internal_annual_cost=10, **tacit("x"))
    r = build_inventory([a, b])
    assert len(r.pending_couplings) == 1
    assert any("materially worse" in q for q in r.open_questions)


# ---------------------------------------------------------------- the whole report

def test_an_incomplete_inventory_still_derives_what_it_can_and_names_the_gap():
    """Degrade, do not block — but never let a partial answer look complete."""
    g1 = rec(id="G1", internal_annual_cost=10, **tacit("x"))
    g2 = rec(id="G2", internal_annual_cost=10, **tacit("x"))
    bad = DecisionRecord(id="B", question="unanswered", **tacit("y"))
    r = build_inventory([g1, g2, bad], [yes("G1", "G2")])
    assert not r.is_complete
    assert r.undecided == ("B",)
    assert len(r.capabilities) == 1 and r.capabilities[0].decision_ids == ("G1", "G2")
    assert any("[B]" in q for q in r.open_questions)


def test_a_complete_inventory_reports_complete():
    r = build_inventory([rec(private_information=("p",), reversibility=Reversibility.COSTLY,
                             internal_annual_cost=10)])
    assert r.is_complete and not r.open_questions


def test_an_unanswered_coupling_question_makes_the_inventory_incomplete():
    settled = dict(internal_annual_cost=10, private_information=("p",),
                   reversibility=Reversibility.COSTLY, **tacit("x"))
    r = build_inventory([rec(id="A", **settled), rec(id="B", **settled)])
    assert r.undecided == () and r.unowned == ()   # nothing else is outstanding
    assert len(r.pending_couplings) == 1
    assert not r.is_complete


def test_the_rendered_report_shows_the_derivation_not_a_summary():
    a = rec(id="A", internal_annual_cost=10, question="which parcels do we plant?", **tacit("x"))
    b = rec(id="B", internal_annual_cost=10, question="when do we irrigate?", **tacit("x"))
    text = render_report(build_inventory([a, b], [yes("A", "B")]))
    assert "RETAINED CAPABILITIES" in text
    assert "DEPARTMENTS DERIVED" not in text
    assert "<- which parcels do we plant?" in text


def test_the_rendered_report_names_the_human_grouping_task():
    ds = [rec(id=i, internal_annual_cost=10, **tacit("x")) for i in ("A", "B", "C")]
    text = render_report(build_inventory(ds, [yes("A", "B"), yes("B", "C")]))
    assert "HUMAN GROUPING REQUIRED" in text
    assert "never affirmed: A+C" in text


def test_report_survives_an_entirely_empty_inventory():
    r = build_inventory([])
    assert r.is_complete and r.capabilities == () and isinstance(render_report(r), str)
