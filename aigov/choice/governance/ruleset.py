"""Direct-democracy governance ruleset as machine-checkable predicates (family mars-gov-ruleset).

Each governance rule is a pure, falsifiable predicate. The ruleset BINDS to the selected verification
mechanism (`paper_rla`, per family mars-gov-voting-verification): a result is ratifiable only if that
mechanism's tamper check passes. Thresholds are documented constants (docs/ruleset_predicates.md).

This module is the enforcement layer the integrated sandbox (mars-gov-sandbox) will execute.
"""
from __future__ import annotations

from dataclasses import dataclass

from prototypes.verify_mechanisms.mock_election import detect_tamper

# --- documented thresholds (docs/ruleset_predicates.md) ---
QUORUM_FRACTION = 0.50             # turnout / eligible must be >= this for any vote to be valid
SIMPLE_MAJORITY = 0.50            # ordinary referendum: yes-share strictly greater than this
AMENDMENT_SUPERMAJORITY = 2 / 3   # constitutional-amendment threshold (>=)
RECALL_PETITION_FRACTION = 0.40   # recall petition signatures / eligible (>=)
MIN_DELIBERATION_DAYS = 7         # proposal -> vote minimum deliberation window
AMENDMENT_COOLDOWN_DAYS = 90      # a failed amendment cannot be re-proposed within this window
DISPUTE_SLA_DAYS = 14             # dispute raised -> resolved maximum

SELECTED_MECHANISM = "paper_rla"  # from mars-gov-voting-verification (D: mechanism-selected)


# --------------------------------------------------------------------------- threshold rules
def quorum_met(turnout, eligible, fraction=QUORUM_FRACTION):
    if eligible <= 0:
        raise ValueError("eligible must be positive")
    if not 0 <= turnout <= eligible:
        raise ValueError("turnout out of range")
    return turnout / eligible >= fraction


def simple_majority(yes, no):
    if yes < 0 or no < 0:
        raise ValueError("counts must be non-negative")
    total = yes + no
    return total > 0 and yes / total > SIMPLE_MAJORITY


def supermajority(yes, no, threshold=AMENDMENT_SUPERMAJORITY):
    if yes < 0 or no < 0:
        raise ValueError("counts must be non-negative")
    total = yes + no
    return total > 0 and yes / total >= threshold


def recall_petition_valid(signatures, eligible, fraction=RECALL_PETITION_FRACTION):
    if eligible <= 0:
        raise ValueError("eligible must be positive")
    if signatures < 0:
        raise ValueError("signatures must be non-negative")
    return signatures / eligible >= fraction


# --------------------------------------------------------------------------- timing rules
def amendment_latency_ok(proposed_day, vote_day, min_days=MIN_DELIBERATION_DAYS):
    if vote_day < proposed_day:
        raise ValueError("vote_day before proposed_day")
    return (vote_day - proposed_day) >= min_days


def amendment_cooldown_ok(last_failed_day, new_proposal_day, cooldown=AMENDMENT_COOLDOWN_DAYS):
    if last_failed_day is None:
        return True  # no prior failed amendment
    if new_proposal_day < last_failed_day:
        raise ValueError("new proposal before prior failure")
    return (new_proposal_day - last_failed_day) >= cooldown


def dispute_within_sla(raised_day, resolved_day, max_days=DISPUTE_SLA_DAYS):
    if resolved_day is None:
        return False  # unresolved -> breaches the SLA
    if resolved_day < raised_day:
        raise ValueError("resolved before raised")
    return (resolved_day - raised_day) <= max_days


# --------------------------------------------------------------------------- mechanism binding
def result_ratifiable(true_ballots, published_ballots, mechanism=SELECTED_MECHANISM):
    """A result is ratifiable iff the SELECTED verification mechanism finds no tamper
    (full audit). This is the rule -> mechanism binding that makes H1 enforceable, not abstract."""
    return not detect_tamper(mechanism, true_ballots, published_ballots, audit_fraction=1.0)


# --------------------------------------------------------------------------- composition
@dataclass(frozen=True)
class Outcome:
    passed: bool
    reasons: tuple  # rule violations; empty when passed


def evaluate_referendum(*, yes, no, turnout, eligible, kind="ordinary",
                        true_ballots=None, published_ballots=None):
    """Compose the rules for one referendum. `kind` in {"ordinary", "amendment"}.

    A referendum passes iff quorum is met AND the kind-appropriate threshold is met AND (when ballots
    are supplied) the selected mechanism ratifies the result. Returns an Outcome with violation reasons.
    """
    if kind not in ("ordinary", "amendment"):
        raise ValueError(f"unknown kind: {kind}")
    reasons = []
    if not quorum_met(turnout, eligible):
        reasons.append("quorum-not-met")
    threshold_ok = supermajority(yes, no) if kind == "amendment" else simple_majority(yes, no)
    if not threshold_ok:
        reasons.append("threshold-not-met")
    if true_ballots is not None and published_ballots is not None:
        if not result_ratifiable(true_ballots, published_ballots):
            reasons.append("verification-failed")
    return Outcome(passed=(len(reasons) == 0), reasons=tuple(reasons))


# --------------------------------------------------------------------------- multi-option primitive (C1)
# Added for family mars-gov-ai-advisor: the binary yes/no referendum cannot express an option MENU, so
# agenda-setting needs a multi-option social-choice rule. Approval voting + a status-quo finalist.
NONE_OF_THESE = "none-of-these"


def approval_winner(approvals, status_quo_id, tiebreak_order=None):
    """Multi-option approval tally with a STATUS-QUO FINALIST.

    `approvals`: {option_id: approval_count}. Returns the winning option_id, or NONE_OF_THESE when no
    option strictly beats the status quo's approval count (so a fragmented/weak field does not adopt a
    policy merely by plurality). Ties broken by `tiebreak_order` (earlier = preferred), else sorted id.
    The status quo MUST be present (mandatory-status-quo rule)."""
    if not approvals:
        raise ValueError("approvals must be non-empty")
    if status_quo_id not in approvals:
        raise ValueError("status_quo_id must be present (mandatory status-quo option)")
    order = list(tiebreak_order) if tiebreak_order else sorted(approvals, key=str)
    rank = {oid: i for i, oid in enumerate(order)}
    best_id = max(approvals, key=lambda oid: (approvals[oid], -rank.get(oid, len(order))))
    if best_id != status_quo_id and approvals[best_id] <= approvals[status_quo_id]:
        return NONE_OF_THESE
    return best_id
