"""Integrated governance sandbox (family mars-gov-sandbox).

Runs the full decision cycle -- PROPOSAL -> VOTE -> RESOURCE-CONSTRAINED OUTCOME -- over >=10 cycles,
wiring the three built families:
  - mars-gov-resource-sim   (models.resource_sim)      : food feasibility + plant-O2 balance
  - mars-gov-voting-verif.  (prototypes...mock_election): selected paper_rla tamper verification
  - mars-gov-ruleset        (governance.ruleset)        : quorum/majority + result ratification

Each cycle a feedback controller proposes a resource policy (crop_fraction + O2 scrubbing); the colony
votes via the ruleset; a passing, ratified, resource-feasible proposal is applied. Invariants are checked
on the applied state every cycle. Stage A only (software + simulated electorate) -- human field-test
(Stage B) and formal verification (Stage C) are deferred per umbrella D1. Scale N=100..500 (D2).
"""
from __future__ import annotations

from dataclasses import dataclass

from models.resource_sim import oxygen_balance, per_capita_food_dry_kg
from governance.ruleset import evaluate_referendum
from prototypes.verify_mechanisms.mock_election import apply_tamper

# Food supply model (per-capita kg/day) = imported baseline + crop_fraction * crop yield.
IMPORTED_FOOD_PC = {"nominal": 0.35, "scarcity": 0.20, "famine": 0.05}
CROP_YIELD_PC = 0.45
CF_MIN, CF_MAX = 0.50, 1.00
INITIAL_CROP_FRACTION = 0.65


@dataclass(frozen=True)
class ColonyState:
    n: int
    crop_fraction: float
    scrubbing: bool


def food_demand_pc():
    return per_capita_food_dry_kg()


def food_supply_pc(crop_fraction, imported_pc):
    return imported_pc + crop_fraction * CROP_YIELD_PC


def feasible(crop_fraction, imported_pc):
    return food_supply_pc(crop_fraction, imported_pc) >= food_demand_pc()


def propose_policy(n, imported_pc):
    """Feedback controller: the smallest crop_fraction that feeds the colony; enable O2 scrubbing if
    that pushes the plant subsystem into over-production. Returns a ColonyState, or None if no
    crop_fraction in [CF_MIN, CF_MAX] is feasible (an honestly un-governable scarcity)."""
    cf = CF_MIN
    target = None
    while cf <= CF_MAX + 1e-9:
        cf_r = round(cf, 4)
        if feasible(cf_r, imported_pc):
            target = cf_r
            break
        cf += 0.01
    if target is None:
        return None
    scrub = oxygen_balance(n, target).overproduction
    return ColonyState(n=n, crop_fraction=target, scrubbing=scrub)


def _ballots_for(n, approve):
    """Deterministic synthetic ballots (1=yes, 0=no): ~85% yes when the proposal is feasible/approved,
    ~15% yes otherwise. Turnout = N (full participation in Stage-A sim)."""
    yes_target = int(round((0.85 if approve else 0.15) * n))
    return tuple(1 if i < yes_target else 0 for i in range(n))


def _check_invariants(state, imported_pc):
    v = []
    if not feasible(state.crop_fraction, imported_pc):
        v.append("starvation")
    if oxygen_balance(state.n, state.crop_fraction).overproduction and not state.scrubbing:
        v.append("o2-overproduction-unscrubbed")
    if not (CF_MIN <= state.crop_fraction <= CF_MAX):
        v.append("crop-fraction-out-of-bounds")
    return tuple(v)


@dataclass(frozen=True)
class CycleResult:
    cycle: int
    applied: bool
    state: ColonyState
    reasons: tuple
    invariants_ok: bool
    violations: tuple


def run_cycle(state, imported_pc, cycle, seed, tamper=False):
    proposal = propose_policy(state.n, imported_pc)
    if proposal is None:                       # no feasible policy -> nothing applied
        viol = _check_invariants(state, imported_pc)
        return CycleResult(cycle, False, state, ("infeasible",), len(viol) == 0, viol)

    approve = feasible(proposal.crop_fraction, imported_pc)
    true_ballots = _ballots_for(state.n, approve)
    published = true_ballots
    if tamper:
        published, _ = apply_tamper(true_ballots, n_flip=max(1, state.n // 10), seed=seed + 1)

    yes = sum(true_ballots)
    no = state.n - yes
    outcome = evaluate_referendum(yes=yes, no=no, turnout=state.n, eligible=state.n, kind="ordinary",
                                  true_ballots=true_ballots, published_ballots=published)
    new_state = proposal if outcome.passed else state   # only a passing, ratified proposal is applied
    viol = _check_invariants(new_state, imported_pc)
    return CycleResult(cycle, outcome.passed, new_state, outcome.reasons, len(viol) == 0, viol)


def run_sandbox(n, n_cycles=12, scenario="nominal", seed=0, tamper_cycle=None):
    """Run >=1 decision cycles. Returns a list[CycleResult]. Deterministic given (n, scenario, seed)."""
    if n <= 0:
        raise ValueError("n must be positive")
    if scenario not in IMPORTED_FOOD_PC:
        raise ValueError(f"unknown scenario: {scenario}")
    if n_cycles <= 0:
        raise ValueError("n_cycles must be positive")
    imported = IMPORTED_FOOD_PC[scenario]
    state = ColonyState(n=n, crop_fraction=INITIAL_CROP_FRACTION, scrubbing=False)
    results = []
    for c in range(n_cycles):
        tamper = tamper_cycle is not None and c == tamper_cycle
        r = run_cycle(state, imported, c, seed + c, tamper=tamper)
        state = r.state
        results.append(r)
    return results


# --------------------------------------------------------------------------- phase-2: AI-advised cycle
# Replaces the single-policy controller with an AI-curated MENU + approval disposal, gated by the
# diversity predicate + adversarial agenda-review (family mars-gov-ai-advisor). A menu that fails
# certification or is found to be steering is NOT applied; "none of these" -> caretaker (state unchanged).
@dataclass(frozen=True)
class AdvisedCycleResult:
    winner: object        # winning crop_fraction, or NONE_OF_THESE
    diversity_ok: bool
    steering_detected: bool            # ENDOGENOUS adversarial review (model-coherent only)
    exo_steering_detected: bool        # EXOGENOUS independent-preference audit (C2-b / D7)
    stages_ok: bool                    # M2 per-stage audit (menu disclosure + ballot collection)
    applied: bool
    ratified: bool        # passed the mechanism-aware binding-election contract (C1)
    caretaker_reason: str # "" when applied; else why refused + what the caretaker did (M1)
    state: ColonyState


def run_advised_cycle(state, scenario, n_voters, agenda=None):
    """AI-advised cycle, RATIFIED via the mechanism-aware binding-election contract (C1 resolved).

    The diversity predicate + adversarial review remain MODEL-COHERENT checks (endogenous to the same
    `_utility`/`optimal_cf` surface) -- "not omission-steering under the documented model", NOT governance
    validity (see docs/ai_advisor_spec.md "certification tiers"). The disposal is now ROUTED THROUGH
    `binding_elections.ratify(APPROVAL, ...)`: the AI proposes a menu, never owns the tally, and a menu is
    applied only if certified AND non-steering AND ratified (valid approval ballots, quorum, no tamper).
    The caretaker fallback still merely HOLDS state; the real invariant-checked min-survival transition is
    phase-2 (M1).
    """
    from governance.ai_advisor import (honest_agenda, option_diversity, adversarial_review,
                                       STATUS_QUO_CF, APPROVAL_TOL,
                                       stage_audit, state_invariants_ok, min_survival_policy)
    from governance.ruleset import NONE_OF_THESE
    from governance.binding_elections import APPROVAL, ratify
    # WHOLE-GRID variant (not the omitted-only exogenous_review): closes the dense-menu capture hole the
    # module documents -- a captor who puts the citizen optimum ON a dense ballot defeats the omitted-only
    # scan, but the whole-grid scan compares the winner against the best feasible policy regardless of
    # whether it sits on the menu. (Reproduced 2026-06-06: a dense menu elected cf=1.0, every gate passed.)
    from governance.exogenous_preferences import exogenous_review_full

    menu = agenda if agenda is not None else honest_agenda(scenario, state.n)
    div = option_diversity(menu, scenario, state.n)
    review = adversarial_review(menu, scenario, state.n)            # endogenous (model-coherent)

    # disposer: sincere approval ballots over the menu, ratified by the binding-election contract
    best_u = max(o.utility for o in menu)
    approved = frozenset(o.cf for o in menu if o.utility >= best_u - APPROVAL_TOL)
    ballots = [approved] * n_voters
    options = [o.cf for o in menu]

    # M2 per-stage audit: the advisor's power is UPSTREAM of the tally (menu disclosure + ballot
    # collection), so audit those stages, not only the final count.
    stages = stage_audit(menu, ballots, n_voters)

    rat = ratify(APPROVAL, ballots, ballots, options, status_quo=STATUS_QUO_CF,
                 eligible=n_voters, audit_fraction=1.0)
    winner = rat.winner

    # EXOGENOUS audit (C2-b / D7): score the elected winner against a structurally-INDEPENDENT
    # citizen-preference panel, NOT the advisor's own `_utility`. A captured advisor passes its own
    # (endogenous) review; this catches the steering the endogenous review structurally cannot.
    exo = exogenous_review_full(winner, scenario, state.n)

    # FEASIBILITY GUARD (integration-harness finding 2026-06-06): ratify checks ballots/quorum/tamper,
    # NOT option feasibility -- a menu whose elected option is infeasible under the pluralism gate would
    # otherwise apply a STARVING state. The winner must itself satisfy the survival invariants.
    winner_scrub = (oxygen_balance(state.n, winner).overproduction
                    if winner != NONE_OF_THESE else False)
    winner_safe = (winner != NONE_OF_THESE
                   and state_invariants_ok(winner, winner_scrub, scenario, state.n))

    applied = ((winner != NONE_OF_THESE) and div.ok and not review.steering_detected
               and not exo.steering_detected and stages.all_ok and rat.ok and winner_safe)
    if applied:
        new_state = ColonyState(n=state.n, crop_fraction=winner, scrubbing=winner_scrub)
        caretaker_reason = ""
    else:
        # M1 caretaker = a real invariant-checked min-survival TRANSITION, not a blind state-hold.
        # If the prior state is already invariant-safe, hold it; otherwise transition to the
        # least-effort feasible min-survival policy. If NO feasible policy exists, surface the famine.
        if state_invariants_ok(state.crop_fraction, state.scrubbing, scenario, state.n):
            new_state = state
            caretaker_reason = "refused-prior-state-safe-hold"
        else:
            surv = min_survival_policy(scenario, state.n)
            if surv is None:
                new_state = state
                caretaker_reason = "refused-no-feasible-survival-policy(famine)"
            else:
                cf, scrub = surv
                new_state = ColonyState(n=state.n, crop_fraction=cf, scrubbing=scrub)
                caretaker_reason = "refused-transitioned-to-min-survival"
    return AdvisedCycleResult(winner=winner, diversity_ok=div.ok,
                              steering_detected=review.steering_detected,
                              exo_steering_detected=exo.steering_detected,
                              stages_ok=stages.all_ok, applied=applied, ratified=rat.ok,
                              caretaker_reason=caretaker_reason, state=new_state)
