"""M1 (invariant-checked min-survival caretaker) + M2 (per-stage audit) — 2026-06-06 review fixes.

M1: caretaker is a real transition — holds the prior state only when it's invariant-safe, else moves to
the least-effort feasible min-survival policy (or flags famine when none exists).
M2: the advised cycle audits the stages UPSTREAM of the tally (menu disclosure + ballot collection).
"""
from governance.ai_advisor import (
    StageAudit,
    min_survival_policy,
    stage_audit,
    state_invariants_ok,
    honest_agenda,
)
from sandbox.governance_sandbox import ColonyState, run_advised_cycle


# --- M1 unit: invariants + min-survival ------------------------------------
def test_safe_state_is_invariant_ok():
    # cf=0.85 with scrubbing feeds the colony and manages O2 over-production
    assert state_invariants_ok(0.85, True, "nominal", 300) is True


def test_overproducing_state_without_scrubbing_is_unsafe():
    assert state_invariants_ok(0.85, False, "nominal", 300) is False


def test_starving_state_is_unsafe():
    # far below feasibility under scarcity -> not invariant-safe regardless of scrubbing
    assert state_invariants_ok(0.50, True, "scarcity", 300) is False


def test_min_survival_policy_is_feasible_and_minimal():
    surv = min_survival_policy("nominal", 300)
    assert surv is not None
    cf, scrub = surv
    assert state_invariants_ok(cf, scrub, "nominal", 300) is True


# --- M1 integration: caretaker behaviour in the cycle -----------------------
def test_caretaker_holds_when_prior_state_safe():
    state = ColonyState(n=300, crop_fraction=0.85, scrubbing=True)  # safe
    r = run_advised_cycle(state, "nominal", 300, agenda=_strawman(300))
    assert r.applied is False
    assert r.state == state                                   # held unchanged
    assert r.caretaker_reason == "refused-prior-state-safe-hold"


def test_caretaker_transitions_when_prior_state_unsafe():
    state = ColonyState(n=300, crop_fraction=0.85, scrubbing=False)  # O2 over-production unscrubbed
    r = run_advised_cycle(state, "nominal", 300, agenda=_strawman(300))
    assert r.applied is False
    assert r.caretaker_reason == "refused-transitioned-to-min-survival"
    assert state_invariants_ok(r.state.crop_fraction, r.state.scrubbing, "nominal", 300) is True
    assert r.state != state


# --- M2: per-stage audit ----------------------------------------------------
def test_stage_audit_passes_for_honest_menu():
    menu = honest_agenda("nominal", 300)
    ballots = [frozenset(o.cf for o in menu)] * 300
    s = stage_audit(menu, ballots, 300)
    assert isinstance(s, StageAudit) and s.all_ok is True


def test_stage_audit_flags_short_ballot_collection():
    menu = honest_agenda("nominal", 300)
    ballots = [frozenset(o.cf for o in menu)] * 299      # one voter missing
    s = stage_audit(menu, ballots, 300)
    assert s.ballot_collection is False and s.all_ok is False
    assert "ballot-collection-invalid" in s.reasons


def test_stage_audit_flags_out_of_menu_ballot():
    menu = honest_agenda("nominal", 300)
    ballots = [frozenset({0.123})] * 300                 # approval for a non-menu option
    s = stage_audit(menu, ballots, 300)
    assert s.ballot_collection is False


def test_advised_cycle_exposes_stage_audit():
    state = ColonyState(n=300, crop_fraction=0.85, scrubbing=True)
    r = run_advised_cycle(state, "nominal", 300)
    assert r.stages_ok is True


def _strawman(n):
    from governance.ai_advisor import strawman_agenda
    return strawman_agenda("nominal", n)
