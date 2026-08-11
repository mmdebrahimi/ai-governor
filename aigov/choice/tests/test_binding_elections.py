"""Validation suite for the mechanism-aware binding-election contract (family mars-gov-binding-elections).

H1: ratify a clean result + reject tamper / quorum-fail / invalid ballots for BOTH single-choice and
approval; approval uses its own set-ballot comparison audit (not the single-choice sequence audit).
"""
import pytest

from governance.ruleset import NONE_OF_THESE
from governance.binding_elections import APPROVAL, SINGLE_CHOICE, ratify

OPTS = ("A", "B", "SQ")


# --- single-choice (paper + RLA) --------------------------------------------
def test_single_choice_clean_ratifies():
    b = ["A"] * 60 + ["B"] * 20 + ["SQ"] * 20
    r = ratify(SINGLE_CHOICE, b, b, OPTS, status_quo="SQ", eligible=100)
    assert r.ok is True and r.winner == "A" and r.reasons == ()


def test_single_choice_tamper_rejected():
    true = ["A"] * 60 + ["B"] * 20 + ["SQ"] * 20
    published = ["B"] + true[1:]  # voter 0 flipped
    r = ratify(SINGLE_CHOICE, true, published, OPTS, status_quo="SQ", eligible=100)
    assert r.ok is False and "tamper-detected" in r.reasons


def test_single_choice_invalid_ballot_rejected():
    b = ["A"] * 50 + ["X"] * 50  # X not an option
    r = ratify(SINGLE_CHOICE, b, b, OPTS, status_quo="SQ", eligible=100)
    assert "invalid-ballots" in r.reasons


# --- approval (sets per voter) ----------------------------------------------
def test_approval_clean_ratifies():
    b = [frozenset({"A", "B"})] * 70 + [frozenset({"SQ"})] * 30
    r = ratify(APPROVAL, b, b, OPTS, status_quo="SQ", eligible=100)
    assert r.ok is True and r.winner == "A"  # A,B tie 70; tiebreak by option order -> A


def test_approval_set_tamper_rejected():
    true = [frozenset({"A", "B"})] * 70 + [frozenset({"SQ"})] * 30
    published = [frozenset({"SQ"})] + true[1:]  # voter 0's approval set altered
    r = ratify(APPROVAL, true, published, OPTS, status_quo="SQ", eligible=100)
    assert r.ok is False and "tamper-detected" in r.reasons


def test_approval_status_quo_finalist_none_of_these():
    b = [frozenset({"A"})] * 50 + [frozenset({"SQ"})] * 50  # A ties SQ -> must not unseat SQ
    r = ratify(APPROVAL, b, b, OPTS, status_quo="SQ", eligible=100)
    assert r.ok is True and r.winner == NONE_OF_THESE


def test_approval_invalid_ballot_rejected():
    b = ["A"] * 100  # strings, not sets
    r = ratify(APPROVAL, b, b, OPTS, status_quo="SQ", eligible=100)
    assert "invalid-ballots" in r.reasons


# --- shared contract guards -------------------------------------------------
def test_quorum_failure_rejected():
    b = ["A"] * 100
    r = ratify(SINGLE_CHOICE, b, b, OPTS, status_quo="SQ", eligible=300)  # 100/300 < 0.5
    assert "quorum-not-met" in r.reasons


def test_unknown_mechanism_rejected():
    with pytest.raises(ValueError):
        ratify("borda", ["A"], ["A"], OPTS, status_quo="SQ", eligible=1)


def test_missing_status_quo_rejected():
    with pytest.raises(ValueError):
        ratify(SINGLE_CHOICE, ["A"], ["A"], ("A", "B"), status_quo="SQ", eligible=1)
