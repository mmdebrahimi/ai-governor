"""Validation suite for the AI-governor agenda layer (family mars-gov-ai-advisor). MVP gate.

Demonstrates the two falsifiable claims:
  H1 -- a measurable diversity predicate + adversarial agenda review keep agenda control CONTESTABLE:
        the predicate rejects a strawman (optimum-omitting) agenda, and the review detects steering when
        an honest omitted option would flip the winner -- but NOT for an honest spanning agenda.
  H2 -- simulator pluralism: two independent feasibility models surface boundary disagreement; an option
        is feasible only when both agree.
Bounded resource domain only. Deterministic (no RNG).
"""
import pytest

from governance.ruleset import NONE_OF_THESE, approval_winner
from governance.ai_advisor import (
    STATUS_QUO_CF,
    AgendaReview,
    adversarial_review,
    agenda_outcome,
    feasible_grid,
    honest_agenda,
    make_option,
    optimal_cf,
    option_diversity,
    strawman_agenda,
)

N = 200


# --- diversity predicate (H1) -----------------------------------------------
def test_honest_agenda_passes_diversity():
    v = option_diversity(honest_agenda("nominal", N), "nominal", N)
    assert v.ok is True and v.reasons == ()


def test_strawman_fails_diversity_by_omitting_optimum():
    v = option_diversity(strawman_agenda("nominal", N), "nominal", N)
    assert v.ok is False
    assert "omits-optimum" in v.reasons


def test_strawman_is_clustered():
    v = option_diversity(strawman_agenda("nominal", N), "nominal", N)
    assert "clustered-not-spanning" in v.reasons


def test_missing_status_quo_flagged():
    opts = tuple(o for o in honest_agenda("nominal", N) if abs(o.cf - STATUS_QUO_CF) > 1e-6)
    v = option_diversity(opts, "nominal", N)
    assert "missing-status-quo" in v.reasons


# --- adversarial agenda review (H1, the falsification test) ------------------
def test_honest_agenda_not_steering():
    r = adversarial_review(honest_agenda("nominal", N), "nominal", N)
    assert isinstance(r, AgendaReview)
    assert r.steering_detected is False


def test_strawman_steering_detected():
    r = adversarial_review(strawman_agenda("nominal", N), "nominal", N)
    assert r.steering_detected is True
    # inserting omitted options pulls the winner toward the true optimum
    opt = optimal_cf("nominal", N)
    assert abs(r.winner_with_omitted - opt) <= 0.05


def test_honest_winner_is_near_optimum():
    r = adversarial_review(honest_agenda("nominal", N), "nominal", N)
    assert abs(r.winner - optimal_cf("nominal", N)) <= 0.05


# --- pluralism (H2) ---------------------------------------------------------
def test_models_disagree_on_boundary_option():
    # ~0.61 is feasible under the optimistic model A but not the stricter model B (nominal)
    o = make_option(0.61, "nominal", N)
    assert o.model_disagreement is True
    assert o.feasible is False          # both must agree to count as feasible


def test_agreed_feasible_option():
    o = make_option(0.80, "nominal", N)
    assert o.feasible_A and o.feasible_B and o.feasible is True


def test_feasible_grid_nonempty_and_bounded():
    grid = feasible_grid("nominal", N)
    assert grid and all(0.5 <= cf <= 1.0 for cf in grid)


# --- multi-option primitive: approval + status-quo finalist ------------------
def test_none_of_these_when_no_option_beats_status_quo():
    # a non-SQ option tied with SQ must NOT win -> none-of-these
    w = approval_winner({STATUS_QUO_CF: 50, 0.70: 50}, status_quo_id=STATUS_QUO_CF,
                        tiebreak_order=[0.70, STATUS_QUO_CF])
    assert w == NONE_OF_THESE


def test_option_beats_status_quo_wins():
    w = approval_winner({STATUS_QUO_CF: 30, 0.70: 60}, status_quo_id=STATUS_QUO_CF)
    assert w == 0.70


def test_bullet_voting_can_shift_winner():
    # M1: a disciplined bloc bullet-voting an inferior option can beat the sincere winner
    opts = honest_agenda("nominal", N)
    sincere = agenda_outcome(opts, N).winner
    bloc = agenda_outcome(opts, N, extra_approvals={0.92: 5 * N}).winner
    assert sincere != 0.92
    assert bloc == 0.92


def test_agenda_requires_status_quo():
    opts = tuple(o for o in honest_agenda("nominal", N) if abs(o.cf - STATUS_QUO_CF) > 1e-6)
    with pytest.raises(ValueError):
        agenda_outcome(opts, N)


# --- guards -----------------------------------------------------------------
def test_unknown_scenario_rejected():
    with pytest.raises(ValueError):
        make_option(0.7, "apocalypse", N)


def test_determinism():
    a = adversarial_review(strawman_agenda("nominal", N), "nominal", N)
    b = adversarial_review(strawman_agenda("nominal", N), "nominal", N)
    assert (a.winner, a.winner_with_omitted, a.steering_detected) == \
           (b.winner, b.winner_with_omitted, b.steering_detected)
