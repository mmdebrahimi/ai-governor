"""Validation suite for the governance ruleset predicates (family mars-gov-ruleset). MVP gate.

Demonstrates H1: a direct-democracy ruleset expressed as machine-checkable predicates, enforceable by
the SELECTED verification mechanism (paper_rla). One flat suite mirroring the resource-sim pattern.
"""
import pytest

from governance.ruleset import (
    Outcome,
    amendment_cooldown_ok,
    amendment_latency_ok,
    dispute_within_sla,
    evaluate_referendum,
    quorum_met,
    recall_petition_valid,
    result_ratifiable,
    simple_majority,
    supermajority,
)
from prototypes.verify_mechanisms.mock_election import apply_tamper, generate_electorate


# --- threshold rules --------------------------------------------------------
def test_quorum_boundary():
    assert quorum_met(50, 100) is True
    assert quorum_met(49, 100) is False


def test_simple_majority_tie_fails():
    assert simple_majority(60, 40) is True
    assert simple_majority(50, 50) is False  # tie is not a majority


def test_supermajority_two_thirds():
    assert supermajority(67, 33) is True
    assert supermajority(60, 40) is False


def test_recall_petition_threshold():
    assert recall_petition_valid(40, 100) is True
    assert recall_petition_valid(39, 100) is False


@pytest.mark.parametrize("fn,args", [
    (quorum_met, (10, 0)),
    (quorum_met, (200, 100)),
    (simple_majority, (-1, 5)),
    (supermajority, (5, -1)),
    (recall_petition_valid, (5, 0)),
])
def test_threshold_rules_reject_bad_inputs(fn, args):
    with pytest.raises(ValueError):
        fn(*args)


# --- timing rules -----------------------------------------------------------
def test_amendment_latency():
    assert amendment_latency_ok(0, 7) is True
    assert amendment_latency_ok(0, 6) is False
    with pytest.raises(ValueError):
        amendment_latency_ok(10, 5)


def test_amendment_cooldown():
    assert amendment_cooldown_ok(None, 5) is True       # no prior failure
    assert amendment_cooldown_ok(0, 90) is True
    assert amendment_cooldown_ok(0, 89) is False


def test_dispute_sla():
    assert dispute_within_sla(0, 14) is True
    assert dispute_within_sla(0, 15) is False
    assert dispute_within_sla(0, None) is False         # unresolved breaches SLA
    with pytest.raises(ValueError):
        dispute_within_sla(10, 5)


# --- mechanism binding (H1 enforceability) ----------------------------------
def test_result_ratifiable_clean():
    ballots = generate_electorate(120, seed=1).ballots
    assert result_ratifiable(ballots, ballots) is True


def test_result_not_ratifiable_when_tampered():
    true = generate_electorate(120, seed=1).ballots
    tampered, _ = apply_tamper(true, n_flip=3, seed=2)
    assert result_ratifiable(true, tampered) is False


# --- composition ------------------------------------------------------------
def test_ordinary_referendum_passes():
    out = evaluate_referendum(yes=60, no=40, turnout=80, eligible=100, kind="ordinary")
    assert out.passed is True and out.reasons == ()


def test_amendment_needs_supermajority():
    out = evaluate_referendum(yes=60, no=40, turnout=80, eligible=100, kind="amendment")
    assert out.passed is False
    assert "threshold-not-met" in out.reasons


def test_quorum_failure_blocks_pass():
    out = evaluate_referendum(yes=30, no=5, turnout=35, eligible=100, kind="ordinary")
    assert out.passed is False
    assert "quorum-not-met" in out.reasons


def test_tamper_blocks_ratification_in_composition():
    true = generate_electorate(100, seed=5).ballots
    tampered, _ = apply_tamper(true, n_flip=4, seed=6)
    out = evaluate_referendum(yes=70, no=30, turnout=100, eligible=100, kind="ordinary",
                              true_ballots=true, published_ballots=tampered)
    assert out.passed is False
    assert "verification-failed" in out.reasons


def test_unknown_kind_rejected():
    with pytest.raises(ValueError):
        evaluate_referendum(yes=1, no=0, turnout=60, eligible=100, kind="dictatorship")


def test_outcome_is_frozen():
    out = evaluate_referendum(yes=60, no=40, turnout=80, eligible=100)
    assert isinstance(out, Outcome)
    with pytest.raises(Exception):
        out.passed = False  # frozen dataclass
