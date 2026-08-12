"""The advisory panel. The tests that matter here pin the REFUSALS, not the happy path."""

import inspect

import pytest

from aigov.panel import (
    Concurrence,
    MIN_VOTING_PANEL,
    NotRatifiableError,
    PanelReading,
    Seat,
    SeatOpinion,
    elicit,
    read,
    seat_errors,
    strict_majority,
)


def claude(**kw):
    return Seat(id=kw.pop("id", "S-claude"), model=kw.pop("model", "claude-opus-5"),
                operator=kw.pop("operator", "anthropic"), **kw)


def gpt(**kw):
    return Seat(id=kw.pop("id", "S-gpt"), model=kw.pop("model", "gpt-5.5"),
                operator=kw.pop("operator", "openai"), **kw)


# --------------------------------------------------------------------------------------
# The derived threshold
# --------------------------------------------------------------------------------------


def test_min_voting_panel_is_derived_not_asserted():
    """It is the first n whose strict majority is short of unanimity. That is arithmetic."""
    assert MIN_VOTING_PANEL == 3
    assert strict_majority(2) == 2          # a 2-seat "majority" IS unanimity
    assert strict_majority(3) == 2 < 3      # the first n where a majority is genuinely weaker


@pytest.mark.parametrize("n,expected", [(1, 1), (2, 2), (3, 2), (4, 3), (5, 3), (16, 9)])
def test_strict_majority_arithmetic(n, expected):
    assert strict_majority(n) == expected


def test_two_seats_below_the_voting_floor():
    """The panel the user actually has (Claude + GPT) is below it. That must be visible."""
    assert 2 < MIN_VOTING_PANEL


# --------------------------------------------------------------------------------------
# A reading is not a ratification -- the structural rail
# --------------------------------------------------------------------------------------


def test_reading_refuses_to_be_ratification():
    r = read("q", (SeatOpinion("S-claude", "yes"), SeatOpinion("S-gpt", "yes")))
    with pytest.raises(NotRatifiableError):
        r.ratified_by


def test_reading_refusal_survives_getattr_with_a_default():
    """The escape hatch a duck-typed ratification path would actually use.

    `getattr(obj, name, default)` swallows only AttributeError. NotRatifiableError is a TypeError,
    so a caller probing for `ratified_by` with a fallback still fails loudly instead of quietly
    reading the default and treating model output as ratified. Making the error subclass
    AttributeError would silently reopen that hole -- this test is what stops that change.
    """
    r = read("q", (SeatOpinion("S-claude", "yes"),))
    with pytest.raises(NotRatifiableError):
        getattr(r, "ratified_by")
    with pytest.raises(NotRatifiableError):
        getattr(r, "ratified_by", "fallback")
    assert not issubclass(NotRatifiableError, AttributeError)


def test_reading_is_never_actionable_alone():
    r = read("q", (SeatOpinion("a", "yes"), SeatOpinion("b", "yes"), SeatOpinion("c", "yes")))
    assert r.is_actionable_alone() is False


# --------------------------------------------------------------------------------------
# Concurrence classification
# --------------------------------------------------------------------------------------


def test_two_seat_agreement_is_reported_as_unanimity_not_majority():
    r = read("q", (SeatOpinion("S-claude", "yes"), SeatOpinion("S-gpt", "yes")))
    assert r.concurrence is Concurrence.CONCURRENT
    assert "unanimity" in r.reason
    assert "weak evidence" in r.caveat()


def test_three_seat_agreement_still_carries_the_correlation_caveat():
    r = read("q", (SeatOpinion("a", "yes"), SeatOpinion("b", "yes"), SeatOpinion("c", "yes")))
    assert r.concurrence is Concurrence.CONCURRENT
    assert "unanimity" not in r.reason
    assert "social convergence" in r.caveat()


def test_division_is_never_collapsed_to_the_plurality():
    r = read("q", (SeatOpinion("a", "yes"), SeatOpinion("b", "yes"), SeatOpinion("c", "no")))
    assert r.concurrence is Concurrence.DIVIDED
    assert r.dissent, "the minority position must survive in the output"
    assert "no" in r.dissent[0] and "c" in r.dissent[0]
    assert "NOT collapsed" in r.reason


def test_dissent_names_the_seat_that_held_it():
    r = read("q", (SeatOpinion("a", "yes"), SeatOpinion("b", "yes"), SeatOpinion("c", "maybe")))
    assert any("maybe" in d and "c" in d for d in r.dissent)


def test_a_clean_split_reports_divided_with_no_plurality_winner():
    r = read("q", (SeatOpinion("a", "yes"), SeatOpinion("b", "no")))
    assert r.concurrence is Concurrence.DIVIDED
    assert r.dissent == ()          # nothing is BELOW the top when the top is a tie
    assert "2 distinct verdicts" in r.reason


def test_failed_seats_do_not_count_as_verdicts():
    r = read("q", (SeatOpinion("a", "yes"), SeatOpinion("b", "", failed=True)))
    assert r.concurrence is Concurrence.CONCURRENT
    assert "1 seats concurred" in r.reason


def test_all_seats_failing_is_no_reading_not_agreement():
    r = read("q", (SeatOpinion("a", "", failed=True), SeatOpinion("b", "", failed=True)))
    assert r.concurrence is Concurrence.NO_READING
    assert r.caveat() == ""


def test_blank_verdict_is_not_a_verdict():
    r = read("q", (SeatOpinion("a", "   "), SeatOpinion("b", "yes")))
    assert "1 seats concurred" in r.reason


# --------------------------------------------------------------------------------------
# The bench itself
# --------------------------------------------------------------------------------------


def test_a_healthy_two_model_bench_has_no_errors():
    assert seat_errors([claude(), gpt()]) == []


def test_identical_model_and_visibility_is_one_seat_counted_twice():
    errs = seat_errors([claude(id="A"), claude(id="B")])
    assert any("counted twice" in e for e in errs)


def test_same_model_with_different_visibility_is_allowed():
    """Different evidence is the second decorrelation lever -- it must not be rejected."""
    a = claude(id="A", visibility=frozenset({"ledger"}))
    b = claude(id="B", visibility=frozenset({"source"}))
    assert not any("counted twice" in e for e in seat_errors([a, b]))


def test_single_operator_bench_is_flagged():
    a = claude(id="A", visibility=frozenset({"x"}))
    b = claude(id="B", visibility=frozenset({"y"}))
    errs = seat_errors([a, b])
    assert any("ACROSS" in e and "anthropic" in e for e in errs)


def test_cross_operator_bench_is_not_flagged_for_operator():
    assert not any("ACROSS" in e for e in seat_errors([claude(), gpt()]))


def test_duplicate_seat_id_rejected():
    assert any("duplicate seat id" in e for e in seat_errors([claude(id="X"), gpt(id="X")]))


def test_seat_without_model_rejected():
    assert any("names no model" in e for e in seat_errors([Seat("A", "", "anthropic")]))


def test_seat_without_operator_rejected():
    assert any("names no operator" in e for e in seat_errors([Seat("A", "m", "")]))


def test_empty_bench_rejected():
    assert seat_errors([]) == ["[PANEL] no seats"]


def test_a_persona_field_on_a_seat_subclass_is_rejected():
    """The V15 finding encoded as a refusal: personality is not a decorrelation lever."""
    from dataclasses import dataclass

    @dataclass(frozen=True)
    class PersonaSeat(Seat):
        persona: str = "grizzled agronomist"

    errs = seat_errors([PersonaSeat("A", "m", "o"), gpt()])
    assert any("persona field" in e and "not judgment" in e for e in errs)


# --------------------------------------------------------------------------------------
# Independence is structural, not promised
# --------------------------------------------------------------------------------------


def test_ask_receives_only_seat_and_question():
    """No parameter exists through which one seat's answer could reach another."""
    seen = []

    def ask(seat, question):
        seen.append((seat.id, question))
        return SeatOpinion(seat.id, "yes")

    elicit([claude(), gpt()], "Q?", ask)
    assert seen == [("S-claude", "Q?"), ("S-gpt", "Q?")]


def test_elicit_signature_exposes_no_history_channel():
    params = list(inspect.signature(elicit).parameters)
    assert params == ["seats", "question", "ask"]
    for forbidden in ("history", "transcript", "prior", "rounds", "context"):
        assert forbidden not in params


def test_a_seat_that_raises_becomes_a_failed_opinion_not_a_verdict():
    def ask(seat, question):
        if seat.id == "S-gpt":
            raise RuntimeError("codex timed out")
        return SeatOpinion(seat.id, "yes")

    r = elicit([claude(), gpt()], "Q?", ask)
    failed = [o for o in r.opinions if o.failed]
    assert len(failed) == 1 and "codex timed out" in failed[0].raw
    assert r.concurrence is Concurrence.CONCURRENT
    assert "1 seats concurred" in r.reason


def test_one_seat_crashing_does_not_lose_the_other_seats_answer():
    def ask(seat, question):
        if seat.id == "S-claude":
            raise RuntimeError("boom")
        return SeatOpinion(seat.id, "no")

    r = elicit([claude(), gpt()], "Q?", ask)
    assert [o.verdict for o in r.opinions if not o.failed] == ["no"]


def test_seat_fingerprint_changes_with_visibility():
    a = claude(visibility=frozenset({"ledger"}))
    b = claude(visibility=frozenset({"ledger", "source"}))
    assert a.fingerprint() != b.fingerprint()
