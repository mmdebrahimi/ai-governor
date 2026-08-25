"""The answers-intake path: a file a person fills in becomes DecisionRecords.

The load-bearing test here is the ROUND TRIP. `test_entry_inventory_endtoend` builds a fully
answered full-size inventory in Python and asserts what it derives. This module writes that
same inventory out as an answers FILE, reads it back through the intake, and asserts the derived
inventory is identical. If those two disagree, the intake is lossy and every real session would
silently lose part of what the user said.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from aigov.answers import (  # noqa: E402
    AnswersError, AnswersInsideRepo, answered_ids, load_answers, parse_answers, render_template,
)
from aigov.decisions import FactKind, Reversibility, Sourcing, build_inventory  # noqa: E402
from aigov.instances.land_enterprise import ENTRY_CANDIDATES, phase_of  # noqa: E402
from test_entry_inventory_endtoend import answered_entry_inventory  # noqa: E402

QUESTIONS = {d.id: d.question for d in ENTRY_CANDIDATES}

_KIND_WORD = {
    FactKind.TRANSFERABLE_RECORD: "written-down",
    FactKind.ORGANIZATION_SPECIFIC_CONTEXT: "how-we-operate",
    FactKind.TACIT_CONTEXT: "from-experience",
}
_CONSEQUENCE_WORD = {
    Reversibility.REVERSIBLE: "recoverable",
    Reversibility.COSTLY: "expensive",
    Reversibility.IRREVERSIBLE: "permanent",
}


def _toml_str(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def as_answers_file(records) -> str:
    """Serialise DecisionRecords back out as an answers file.

    Test-only. The production module deliberately READS and never WRITES answers - `tomllib` has
    no dump - so this lives here, where it exists purely to close the round trip.
    """
    out = []
    for r in records:
        out.append(f"[{r.id}]")
        if r.frequency_per_year is not None:
            out.append(f"times_per_year = {r.frequency_per_year}")
        if r.external_engagement_cost is not None:
            out.append(f"cost_to_buy_the_call_once = {r.external_engagement_cost}")
        if r.internal_annual_cost is not None:
            out.append(f"cost_per_year_to_hold_it = {r.internal_annual_cost}")
        if r.external_market_exists is not None:
            out.append(f"anyone_sells_this = {str(r.external_market_exists).lower()}")
        if r.private_information:
            items = ", ".join(_toml_str(p) for p in r.private_information)
            out.append(f"what_only_we_know = [{items}]")
        if r.information_needs:
            out.append("must_know_first = [")
            for fact in sorted(r.information_needs):
                kind = r.kind_of(fact)
                if kind is None:
                    out.append(f"  {{ fact = {_toml_str(fact)} }},")
                else:
                    out.append(
                        f"  {{ fact = {_toml_str(fact)}, kind = {_toml_str(_KIND_WORD[kind])} }},"
                    )
            out.append("]")
        if r.accountable_role:
            out.append(f"who_answers = {_toml_str(r.accountable_role)}")
        if r.reversibility is not None:
            out.append(f"if_wrong_once = {_toml_str(_CONSEQUENCE_WORD[r.reversibility])}")
        if r.atomic is not None:
            out.append(f"one_decision = {str(r.atomic).lower()}")
        out.append("")
    return "\n".join(out)


# ---------------------------------------------------------------------------------------------
# The round trip
# ---------------------------------------------------------------------------------------------

def test_round_trip_reproduces_the_inventory_exactly():
    original = answered_entry_inventory()
    reloaded = parse_answers(as_answers_file(original), QUESTIONS)

    a, b = build_inventory(original), build_inventory(reloaded)
    assert [(v.decision_id, v.sourcing) for v in a.verdicts] == \
           [(v.decision_id, v.sourcing) for v in b.verdicts]
    assert [(x.decision_id, x.assurance) for x in a.assurance] == \
           [(x.decision_id, x.assurance) for x in b.assurance]
    assert a.undecided == b.undecided
    assert a.unowned == b.unowned
    assert a.unassured == b.unassured
    assert a.pending_couplings == b.pending_couplings


def test_round_trip_preserves_every_elicited_field():
    by_id = {r.id: r for r in parse_answers(as_answers_file(answered_entry_inventory()), QUESTIONS)}
    for original in answered_entry_inventory():
        got = by_id[original.id]
        for field in ("frequency_per_year", "external_engagement_cost", "internal_annual_cost",
                      "external_market_exists", "private_information", "information_needs",
                      "accountable_role", "atomic", "reversibility"):
            assert getattr(got, field) == getattr(original, field), f"{original.id}.{field}"
        assert dict(got.fact_kinds) == dict(original.fact_kinds), original.id


# ---------------------------------------------------------------------------------------------
# Unanswered stays unanswered
# ---------------------------------------------------------------------------------------------

def test_an_empty_file_yields_every_decision_unanswered():
    records = parse_answers("", QUESTIONS)
    assert len(records) == len(QUESTIONS)
    assert all(len(r.missing_fields()) == 4 for r in records)
    assert build_inventory(records).capabilities == ()


def test_a_partially_answered_decision_reports_exactly_what_is_missing():
    records = parse_answers("[E01]\ntimes_per_year = 4\n", QUESTIONS)
    e01 = next(r for r in records if r.id == "E01")
    assert e01.frequency_per_year == 4
    assert set(e01.missing_fields()) == {
        "external_engagement_cost", "internal_annual_cost", "external_market_exists",
    }


def test_answered_ids_counts_only_fully_sourced_decisions():
    text = (
        "[E01]\ntimes_per_year = 4\ncost_to_buy_the_call_once = 1\n"
        "cost_per_year_to_hold_it = 2\nanyone_sells_this = true\n"
        "[E02a]\ntimes_per_year = 4\n"
    )
    assert answered_ids(parse_answers(text, QUESTIONS)) == ("E01",)


def test_the_question_key_is_never_read_back_from_the_file():
    """A typo in the copied question must not change what the inventory says."""
    text = '[E01]\nquestion = "totally different wording"\ntimes_per_year = 4\n'
    e01 = next(r for r in parse_answers(text, QUESTIONS) if r.id == "E01")
    assert e01.question == QUESTIONS["E01"]


# ---------------------------------------------------------------------------------------------
# Errors a person can act on
# ---------------------------------------------------------------------------------------------

def test_an_unknown_decision_id_is_refused_not_ignored():
    with pytest.raises(AnswersError, match="E99"):
        parse_answers("[E99]\ntimes_per_year = 1\n", QUESTIONS)


def test_a_misspelled_key_is_refused_with_the_known_keys_listed():
    with pytest.raises(AnswersError, match="times_per_yr"):
        parse_answers("[E01]\ntimes_per_yr = 4\n", QUESTIONS)


def test_a_bad_consequence_word_lists_the_three_allowed_words():
    with pytest.raises(AnswersError, match="recoverable"):
        parse_answers('[E01]\nif_wrong_once = "bad"\n', QUESTIONS)


def test_a_bad_fact_kind_lists_the_three_allowed_kinds():
    with pytest.raises(AnswersError, match="from-experience"):
        parse_answers('[E01]\nmust_know_first = [{ fact = "x", kind = "tacit" }]\n', QUESTIONS)


def test_an_unclassified_fact_is_legal_and_reported_as_unclassified():
    text = '[E01]\nmust_know_first = ["a thing we have not classified yet"]\n'
    e01 = next(r for r in parse_answers(text, QUESTIONS) if r.id == "E01")
    assert e01.unclassified_facts() == ("a thing we have not classified yet",)
    assert e01.expensive_facts() == frozenset()


def test_malformed_toml_says_so_plainly():
    with pytest.raises(AnswersError, match="not valid TOML"):
        parse_answers("[E01\ntimes_per_year = 4\n", QUESTIONS)


# ---------------------------------------------------------------------------------------------
# The privacy refusal
# ---------------------------------------------------------------------------------------------

def test_an_answers_file_inside_the_public_repo_is_refused(tmp_path):
    inside = Path(__file__).resolve().parent / "_should_never_be_read.toml"
    inside.write_text("[E01]\ntimes_per_year = 1\n", encoding="utf-8")
    try:
        with pytest.raises(AnswersInsideRepo, match="public repository"):
            load_answers(inside, QUESTIONS)
    finally:
        inside.unlink()


def test_the_refusal_can_be_overridden_explicitly_for_fixtures(tmp_path):
    inside = Path(__file__).resolve().parent / "_fixture_ok.toml"
    inside.write_text("[E01]\ntimes_per_year = 1\n", encoding="utf-8")
    try:
        records = load_answers(inside, QUESTIONS, allow_inside_repo=True)
        assert next(r for r in records if r.id == "E01").frequency_per_year == 1
    finally:
        inside.unlink()


def test_a_file_outside_the_repo_loads(tmp_path):
    outside = tmp_path / "answers.toml"
    outside.write_text("[E01]\ntimes_per_year = 7\n", encoding="utf-8")
    records = load_answers(outside, QUESTIONS)
    assert next(r for r in records if r.id == "E01").frequency_per_year == 7


def test_a_missing_file_is_refused_clearly(tmp_path):
    with pytest.raises(AnswersError, match="no answers file"):
        load_answers(tmp_path / "nope.toml", QUESTIONS)


# ---------------------------------------------------------------------------------------------
# The template
# ---------------------------------------------------------------------------------------------

def test_the_emitted_template_parses_and_answers_nothing():
    text = render_template(ENTRY_CANDIDATES, phase_of=phase_of)
    records = parse_answers(text, QUESTIONS)
    assert len(records) == len(ENTRY_CANDIDATES)
    assert all(len(r.missing_fields()) == 4 for r in records), \
        "a freshly emitted template must answer nothing - every field is commented out"


def test_the_template_carries_every_decision_and_its_phase():
    text = render_template(ENTRY_CANDIDATES, phase_of=phase_of)
    for d in ENTRY_CANDIDATES:
        assert f"[{d.id}]" in text
        assert d.question in text
    assert "SCREENING" in text and "COMMITMENT" in text


def test_the_template_warns_about_the_public_repo():
    text = render_template(ENTRY_CANDIDATES)
    assert "OUTSIDE THE PUBLIC REPOSITORY" in text
