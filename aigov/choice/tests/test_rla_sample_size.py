"""Risk-limiting-audit sample-size math (family mars-gov-binding-elections).

Closes the pending item "real margin-driven RLA sample-size math" — the audit was a placeholder full
recount (audit_fraction=1.0). The falsifiable property: an outcome-changing tamper (>= margin fraction
altered) is caught with probability >= 1 - risk_limit while sampling FEWER than all ballots.
"""
import random

import pytest

from governance.binding_elections import (
    APPROVAL,
    SINGLE_CHOICE,
    ratify,
    risk_limiting_audit_fraction,
    rla_sample_size,
)


# --- analytic properties ----------------------------------------------------
def test_tighter_margin_needs_larger_sample():
    assert rla_sample_size(0.01) > rla_sample_size(0.05) > rla_sample_size(0.20)


def test_sample_meets_risk_limit_bound():
    # (1 - margin)^k must be <= risk_limit by construction
    for margin, rl in [(0.05, 0.05), (0.10, 0.01), (0.02, 0.10)]:
        k = rla_sample_size(margin, rl)
        assert (1.0 - margin) ** k <= rl + 1e-12


def test_sample_capped_at_n():
    assert rla_sample_size(0.001, 0.05, n=50) == 50


def test_wide_margin_samples_far_fewer_than_full():
    # the whole point of risk-limiting: a 20% margin audits a small fraction, not everything
    frac = risk_limiting_audit_fraction(0.20, n=1000, risk_limit=0.05)
    assert frac < 0.05            # <5% of ballots, vs the old 100%


def test_guards():
    for bad in [(0.0,), (1.5,)]:
        with pytest.raises(ValueError):
            rla_sample_size(*bad)
    with pytest.raises(ValueError):
        rla_sample_size(0.1, 1.0)
    with pytest.raises(ValueError):
        risk_limiting_audit_fraction(0.1, 0)


# --- empirical: detection rate meets the risk limit -------------------------
def test_empirical_detection_meets_risk_limit():
    """Over many independent audits at margin-level tamper, the empirical CATCH rate must meet the
    guarantee (>= 1 - risk_limit). This is the falsifiable statistical claim, not a self-pin."""
    n, margin, risk_limit, trials = 1000, 0.05, 0.05, 2000
    n_altered = int(margin * n)
    k = rla_sample_size(margin, risk_limit, n)
    rng = random.Random(20260606)
    altered = set(range(n_altered))            # ballots 0..n_altered-1 are tampered
    caught = 0
    for _ in range(trials):
        sample = rng.sample(range(n), k)
        if any(i in altered for i in sample):
            caught += 1
    catch_rate = caught / trials
    assert catch_rate >= 1.0 - risk_limit, (catch_rate, k)


# --- integration: ratify accepts the RLA fraction ---------------------------
def test_ratify_with_rla_fraction_single_choice():
    opts = ("A", "B", "SQ")
    b = ["A"] * 600 + ["B"] * 200 + ["SQ"] * 200
    frac = risk_limiting_audit_fraction(0.10, n=1000, risk_limit=0.05)
    r = ratify(SINGLE_CHOICE, b, b, opts, status_quo="SQ", eligible=1000, audit_fraction=frac)
    assert r.ok is True and r.winner == "A"


def test_ratify_with_rla_fraction_catches_large_tamper_approval():
    opts = ("A", "B", "SQ")
    true = [frozenset({"A"})] * 1000
    published = [frozenset({"SQ"})] * 200 + true[200:]   # 20% of sets altered
    frac = risk_limiting_audit_fraction(0.20, n=1000, risk_limit=0.01)
    r = ratify(APPROVAL, true, published, opts, status_quo="SQ", eligible=1000,
               audit_fraction=frac, seed=3)
    assert r.ok is False and "tamper-detected" in r.reasons
