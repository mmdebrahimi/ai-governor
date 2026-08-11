"""Mechanism-aware binding-election contract (family mars-gov-binding-elections) — resolves C1.

Replaces the ad-hoc reuse of `paper_rla` for every tally. Each MECHANISM owns its own contract:
ballot schema + validity, tally, winner/margin, and a tamper/audit rule. A result is RATIFIED only when
ballots are valid, quorum holds, AND the mechanism's audit finds no tamper. The AI advisor proposes a
menu; it never owns the tally — `run_advised_cycle` routes its approval result through `ratify(...)`.

Two mechanisms shipped:
  - SINGLE_CHOICE: paper + risk-limiting audit (reuses mock_election.detect_tamper; one choice/voter).
  - APPROVAL: approval voting + status-quo finalist + an APPROVAL-SPECIFIC comparison audit. Approval
    ballots are SETS per voter, so the single-choice audit is NOT a drop-in (the 2026-06-06 review's C1).
"""
from __future__ import annotations

import random
from collections import Counter
from dataclasses import dataclass
from typing import Callable

from prototypes.verify_mechanisms.mock_election import detect_tamper as _single_choice_detect
from governance.ruleset import NONE_OF_THESE, approval_winner

SINGLE_CHOICE = "single_choice"
APPROVAL = "approval"


# --------------------------------------------------------------------------- single-choice (paper + RLA)
def _sc_validate(ballots, options):
    opts = set(options)
    return all(b in opts for b in ballots)


def _sc_tally(ballots, options):
    return dict(Counter(ballots))


def _sc_winner(tally, status_quo, options):
    if not tally:
        return NONE_OF_THESE
    best = max(tally.values())
    leaders = [o for o in options if tally.get(o, 0) == best]
    return status_quo if status_quo in leaders else leaders[0]


def _sc_audit(true_ballots, published_ballots, audit_fraction, seed):
    # reuse the single-choice RLA tamper model (sequence compare); returns True iff tamper detected
    return _single_choice_detect("paper_rla", tuple(true_ballots), tuple(published_ballots),
                                 audit_fraction=audit_fraction, seed=seed)


# --------------------------------------------------------------------------- approval (sets per voter)
def _ap_validate(ballots, options):
    opts = set(options)
    return all(isinstance(b, (set, frozenset)) and set(b) <= opts for b in ballots)


def _ap_tally(ballots, options):
    counts = {o: 0 for o in options}
    for b in ballots:
        for o in b:
            counts[o] = counts.get(o, 0) + 1
    return counts


def _ap_winner(tally, status_quo, options):
    return approval_winner(tally, status_quo_id=status_quo, tiebreak_order=list(options))


def _ap_audit(true_ballots, published_ballots, audit_fraction, seed):
    """Approval-specific risk-limiting comparison audit: sample voters; tamper detected iff a sampled
    voter's published approval-SET differs from the true set. A structural length mismatch = tamper."""
    n = len(true_ballots)
    if n == 0 or len(published_ballots) != n:
        return True
    changed = {i for i in range(n) if set(true_ballots[i]) != set(published_ballots[i])}
    if not changed:
        return False
    k = max(1, min(int(round(audit_fraction * n)), n))
    sample = random.Random(seed).sample(range(n), k)
    return any(i in changed for i in sample)


# --------------------------------------------------------------------------- risk-limiting audit math
# The voting family SELECTED paper+RLA, but ratify defaulted to audit_fraction=1.0 (a full recount, not a
# risk-LIMITING audit). A real RLA samples FEWER ballots when the margin is wide. Guarantee: if at least a
# `margin` fraction of ballots were altered (an outcome-changing tamper), a uniform sample of `k` ballots
# misses ALL of them with probability (1 - margin)^k; choosing k = ceil(ln(risk_limit)/ln(1-margin)) makes
# that miss-probability <= risk_limit. So a passing RLA certifies the outcome at confidence 1 - risk_limit.
import math


def rla_sample_size(margin, risk_limit=0.05, n=None):
    """Ballots to sample so an outcome-changing tamper (>= `margin` fraction altered) is detected with
    probability >= 1 - risk_limit. `margin` in (0,1]; tighter margin -> larger sample. Capped at n."""
    if not 0.0 < margin <= 1.0:
        raise ValueError("margin must be in (0, 1]")
    if not 0.0 < risk_limit < 1.0:
        raise ValueError("risk_limit must be in (0, 1)")
    if margin >= 1.0:
        k = 1
    else:
        k = math.ceil(math.log(risk_limit) / math.log(1.0 - margin))
    if n is not None:
        k = min(k, n)
    return max(1, k)


def risk_limiting_audit_fraction(margin, n, risk_limit=0.05):
    """The principled `audit_fraction` for `ratify(...)`: rla_sample_size / n. Replaces the placeholder
    full-audit (1.0) with a margin-driven fraction that still meets the risk limit."""
    if n <= 0:
        raise ValueError("n must be positive")
    return rla_sample_size(margin, risk_limit, n) / n


@dataclass(frozen=True)
class MechanismContract:
    name: str
    validate: Callable
    tally: Callable
    winner: Callable
    audit: Callable


MECHANISMS = {
    SINGLE_CHOICE: MechanismContract(SINGLE_CHOICE, _sc_validate, _sc_tally, _sc_winner, _sc_audit),
    APPROVAL: MechanismContract(APPROVAL, _ap_validate, _ap_tally, _ap_winner, _ap_audit),
}


@dataclass(frozen=True)
class Ratification:
    ok: bool
    winner: object
    reasons: tuple


def ratify(mechanism, true_ballots, published_ballots, options, status_quo, eligible,
           quorum=0.5, audit_fraction=1.0, seed=0):
    """Ratify a binding result under the named mechanism's own contract. ok iff ballots valid AND quorum
    holds AND the mechanism audit finds no tamper. Returns Ratification(ok, winner, reasons)."""
    if mechanism not in MECHANISMS:
        raise ValueError(f"unknown mechanism: {mechanism}")
    if status_quo not in options:
        raise ValueError("status_quo must be an option (mandatory status-quo)")
    c = MECHANISMS[mechanism]
    reasons = []
    if not c.validate(published_ballots, options):
        reasons.append("invalid-ballots")
    turnout = len(published_ballots)
    if eligible <= 0 or turnout / eligible < quorum:
        reasons.append("quorum-not-met")
    if c.audit(true_ballots, published_ballots, audit_fraction, seed):
        reasons.append("tamper-detected")
    winner = c.winner(c.tally(published_ballots, options), status_quo, options)
    return Ratification(ok=(len(reasons) == 0), winner=winner, reasons=tuple(reasons))
