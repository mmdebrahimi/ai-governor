"""AI-governor agenda layer (family mars-gov-ai-advisor) -- phase-1 RESOURCE domain only.

Proposer/disposer split: an AI proposer GENERATES a curated, analyzed option set; humans DISPOSE via
approval voting (+ status-quo finalist + none-of-these, from governance.ruleset). Agenda control is kept
CONTESTABLE -- never claimed "solved" -- by three measurable mechanisms:

  1. a MEASURABLE option-diversity predicate (mandatory status-quo + spans the feasible lever range +
     does not omit the optimum) -- testable because the resource option space is formal;
  2. simulator PLURALISM -- >=2 INDEPENDENT feasibility models; an option counts as feasible only if
     both agree, and boundary disagreement is surfaced (defends against simulator capture, C3);
  3. an ADVERSARIAL AGENDA-REVIEW falsification test -- insert omitted-but-feasible options and check
     whether the winner shifts beyond an audit threshold (outcome-sensitivity-to-omitted-options, M3).

BOUNDED-DOMAIN CLAIM ONLY (docs/ai_advisor_spec.md): this is resource-allocation agenda certification,
NOT general-governance certification. Positive agenda rights make agenda control CONTESTABLE, not solved.
Option lever = crop_fraction (scrubbing is a derived label; import assumption sets the scenario).
"""
from __future__ import annotations

from dataclasses import dataclass

from models.resource_sim import oxygen_balance, per_capita_food_dry_kg
from governance.ruleset import NONE_OF_THESE, approval_winner

CROP_YIELD_PC = 0.45
STATUS_QUO_CF = 0.85          # current (inefficient, O2-over-producing) policy -- far from the optimum
FARMING_COST = 0.10           # labor/energy cost per unit crop_fraction
STARVATION_PENALTY = 10.0     # food deficit is catastrophic
APPROVAL_TOL = 0.02           # sincere voters approve options within this utility band of the best
OPTIMUM_TOL = 0.05            # an agenda "contains the optimum" if a feasible option is this close
MATERIAL_DISTINCT_EPS = 0.03
STEERING_UTILITY_THRESHOLD = 0.10  # winner-utility shift beyond this on omitted-insertion = steering
CF_MIN, CF_MAX = 0.50, 1.00


@dataclass(frozen=True)
class FeasibilityModel:
    name: str
    imported_pc: float
    crop_yield_pc: float = CROP_YIELD_PC

    def supply_pc(self, cf):
        return self.imported_pc + cf * self.crop_yield_pc

    def margin(self, cf):
        return self.supply_pc(cf) - per_capita_food_dry_kg()

    def feasible(self, cf):
        return self.margin(cf) >= 0


def models_for(scenario):
    """Pluralism (T4): two INDEPENDENT feasibility models with different yield assumptions."""
    imported = {"nominal": 0.35, "scarcity": 0.20}.get(scenario)
    if imported is None:
        raise ValueError(f"unknown scenario: {scenario}")
    return FeasibilityModel("A", imported, 0.45), FeasibilityModel("B", imported, 0.42)


@dataclass(frozen=True)
class Option:
    cf: float
    feasible_A: bool
    feasible_B: bool
    scrubbing: bool
    utility: float

    @property
    def feasible(self):                 # feasible only if BOTH models agree (pluralism gate)
        return self.feasible_A and self.feasible_B

    @property
    def model_disagreement(self):
        return self.feasible_A != self.feasible_B


def _utility(cf, model, n):
    """Tension between food security and O2 balance: deficit is catastrophic; |O2 net| (over/under
    production) and farming effort are costs. Interior optimum near the O2 break-even (cf=0.667)."""
    margin = model.margin(cf)
    o2_net = abs(1.5 * cf - 1.0)        # 0 at the plant-O2 break-even crop_fraction
    starve = STARVATION_PENALTY * max(0.0, -margin)
    return -starve - o2_net - FARMING_COST * cf


def make_option(cf, scenario, n):
    a, b = models_for(scenario)
    cf = round(cf, 4)
    return Option(cf=cf, feasible_A=a.feasible(cf), feasible_B=b.feasible(cf),
                  scrubbing=oxygen_balance(n, cf).overproduction,
                  utility=round(_utility(cf, a, n), 5))


def feasible_grid(scenario, n, step=0.01):
    a, b = models_for(scenario)
    out, cf = [], CF_MIN
    while cf <= CF_MAX + 1e-9:
        r = round(cf, 4)
        if a.feasible(r) and b.feasible(r):
            out.append(r)
        cf += step
    return out


def optimal_cf(scenario, n):
    grid = feasible_grid(scenario, n)
    if not grid:
        return None
    a, _ = models_for(scenario)
    return max(grid, key=lambda cf: _utility(cf, a, n))


# --------------------------------------------------------------------------- option generators
def honest_agenda(scenario, n):
    """A diversity-passing agenda: spans the feasible lever range, includes the status quo + the optimum."""
    cfs = sorted({0.65, 0.70, 0.78, STATUS_QUO_CF, 0.92})
    return tuple(make_option(cf, scenario, n) for cf in cfs)


def strawman_agenda(scenario, n, preferred_cf=STATUS_QUO_CF):
    """Manufactured consensus: cluster options around the status quo, OMIT the optimum (no real change)."""
    cfs = sorted({preferred_cf, preferred_cf - 0.05, preferred_cf + 0.05})
    return tuple(make_option(cf, scenario, n) for cf in cfs)


# --------------------------------------------------------------------------- diversity predicate
@dataclass(frozen=True)
class DiversityVerdict:
    ok: bool
    reasons: tuple


def option_diversity(options, scenario, n):
    reasons = []
    if not any(abs(o.cf - STATUS_QUO_CF) < 1e-6 for o in options):
        reasons.append("missing-status-quo")
    feas = [o for o in options if o.feasible]
    if len(feas) < 2:
        reasons.append("insufficient-feasible-options")
    else:
        grid = feasible_grid(scenario, n)
        cfs = sorted(o.cf for o in feas)
        if grid:
            span = (cfs[-1] - cfs[0]) / (max(grid) - min(grid) + 1e-9)
            if span < 0.5:
                reasons.append("clustered-not-spanning")
        opt = optimal_cf(scenario, n)
        if opt is not None and not any(abs(o.cf - opt) <= OPTIMUM_TOL for o in feas):
            reasons.append("omits-optimum")
    return DiversityVerdict(ok=(len(reasons) == 0), reasons=tuple(reasons))


# --------------------------------------------------------------------------- disposer: approval outcome
@dataclass(frozen=True)
class AgendaOutcome:
    winner: object   # winning crop_fraction, or NONE_OF_THESE
    approvals: tuple


def agenda_outcome(options, n_voters, extra_approvals=None):
    """Sincere approval vote (+ status-quo finalist). Each voter approves options within APPROVAL_TOL of
    the best utility. `extra_approvals` injects bloc/bullet votes for a specific option (for M1 tests)."""
    if not any(abs(o.cf - STATUS_QUO_CF) < 1e-6 for o in options):
        raise ValueError("agenda must include the status-quo option")
    best_u = max(o.utility for o in options)
    approvals = {o.cf: (n_voters if o.utility >= best_u - APPROVAL_TOL else 0) for o in options}
    for cf, c in (extra_approvals or {}).items():
        approvals[cf] = approvals.get(cf, 0) + c
    order = [o.cf for o in sorted(options, key=lambda x: -x.utility)]
    winner = approval_winner(approvals, status_quo_id=STATUS_QUO_CF, tiebreak_order=order)
    return AgendaOutcome(winner=winner, approvals=tuple(sorted(approvals.items())))


# --------------------------------------------------------------------------- adversarial agenda review
@dataclass(frozen=True)
class AgendaReview:
    winner: object
    winner_with_omitted: object
    steering_detected: bool
    diversity: DiversityVerdict


def _winner_utility(winner, scenario, n):
    if winner == NONE_OF_THESE:
        return None
    a, _ = models_for(scenario)
    return _utility(winner, a, n)


def adversarial_review(options, scenario, n):
    """Falsification test (M3): insert every omitted feasible grid option and re-tally. Steering is
    detected if the winner flips to none-of-these OR the winner's utility shifts beyond the audit
    threshold -- i.e. the original curation was steering the outcome by omission.

    ENDOGENOUS: scores against the SAME `_utility` surface that built the options, so a captured menu
    whose options carry an attacker's utility can fool it (the winner doesn't move). The exogenous
    check below (C2-b) is the structurally independent backstop."""
    div = option_diversity(options, scenario, n)
    out1 = agenda_outcome(options, n)
    existing = [o.cf for o in options]
    omitted = [make_option(cf, scenario, n) for cf in feasible_grid(scenario, n)
               if all(abs(cf - e) > MATERIAL_DISTINCT_EPS for e in existing)]
    out2 = agenda_outcome(tuple(options) + tuple(omitted), n)
    if out1.winner == out2.winner:
        steering = False
    else:
        u1, u2 = _winner_utility(out1.winner, scenario, n), _winner_utility(out2.winner, scenario, n)
        steering = (u1 is None or u2 is None) or abs(u2 - u1) > STEERING_UTILITY_THRESHOLD
    return AgendaReview(winner=out1.winner, winner_with_omitted=out2.winner,
                        steering_detected=steering, diversity=div)


# --------------------------------------------------------------------------- M1: min-survival caretaker
def state_invariants_ok(cf, scrubbing, scenario, n):
    """A colony state is safe iff BOTH feasibility models feed everyone AND O2 over-production is
    scrubbed. Used to decide whether the caretaker may HOLD the prior state or must transition."""
    a, b = models_for(scenario)
    feasible = a.feasible(cf) and b.feasible(cf)
    o2_over = oxygen_balance(n, cf).overproduction
    return feasible and (not o2_over or scrubbing)


def min_survival_policy(scenario, n):
    """The least-effort feasible crop_fraction (both models agree) with O2 scrubbing enabled as needed.
    Returns (cf, scrubbing) or None when NO feasible policy exists (an honestly un-governable famine)."""
    grid = feasible_grid(scenario, n)
    if not grid:
        return None
    cf = min(grid)  # smallest crop_fraction that still feeds everyone -> minimal labor/energy burden
    return cf, oxygen_balance(n, cf).overproduction


# --------------------------------------------------------------------------- M2: per-stage audit
@dataclass(frozen=True)
class StageAudit:
    menu_disclosure: bool   # every option carries feasibility labels + the menu is non-trivial
    ballot_collection: bool  # one valid approval ballot per voter, over the menu's options
    reasons: tuple

    @property
    def all_ok(self):
        return self.menu_disclosure and self.ballot_collection


def stage_audit(menu, ballots, n_voters):
    """Audit the pipeline UPSTREAM of the tally (the advisor's real power, 2026-06-06 review M2)."""
    reasons = []
    disclosure = len(menu) >= 2 and all(
        hasattr(o, "feasible_A") and hasattr(o, "feasible_B") for o in menu)
    if not disclosure:
        reasons.append("menu-disclosure-incomplete")
    cfs = {o.cf for o in menu}
    collection = len(ballots) == n_voters and all(
        isinstance(b, (set, frozenset)) and set(b) <= cfs for b in ballots)
    if not collection:
        reasons.append("ballot-collection-invalid")
    return StageAudit(disclosure, collection, tuple(reasons))
