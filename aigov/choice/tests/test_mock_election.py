"""Mock-election validation suite (family mars-gov-voting-verification). MVP gate criterion 3.

One parametrized suite over the two mechanisms (mirrors the resource-sim single-suite pattern).
Covers tamper detection, ballot-secrecy leak, eligibility, small-cell inference, the decision rule,
determinism, and edge cases. Selection is COMPUTED from documented parameters, never hardcoded.
"""
import pytest

from prototypes.verify_mechanisms.mock_election import (
    MECHANISMS,
    SECRECY_LEAK_MAX,
    TAMPER_DETECTION_MIN,
    MechanismScore,
    apply_tamper,
    channel_secrecy_leak,
    detect_tamper,
    generate_electorate,
    score_mechanism,
    select_mechanism,
    small_cell_inference_rate,
)


# --- secrecy channels -------------------------------------------------------
@pytest.mark.parametrize("mechanism", MECHANISMS)
def test_channel_leak_in_unit_range(mechanism):
    leak = channel_secrecy_leak(mechanism)
    assert 0.0 <= leak <= 1.0


def test_paper_leaks_less_than_e2e():
    assert channel_secrecy_leak("paper_rla") < channel_secrecy_leak("e2e_supervised")


def test_unknown_mechanism_rejected():
    with pytest.raises(ValueError):
        channel_secrecy_leak("blockchain_magic")


# --- synthetic electorate + small-cell inference ----------------------------
def test_electorate_is_seed_deterministic():
    a = generate_electorate(200, seed=7)
    b = generate_electorate(200, seed=7)
    assert a.ballots == b.ballots and a.bloc_of == b.bloc_of


def test_small_cell_n1_fully_leaks():
    assert small_cell_inference_rate(generate_electorate(1)) == 1.0


def test_full_cohesion_fully_leaks():
    # every bloc votes unanimously -> every member's vote inferable
    e = generate_electorate(100, cohesion=1.0, seed=3)
    assert small_cell_inference_rate(e) == 1.0


def test_small_cell_rate_in_unit_range():
    e = generate_electorate(300, cohesion=0.7, seed=11)
    assert 0.0 <= small_cell_inference_rate(e) <= 1.0


def test_generate_electorate_rejects_bad_inputs():
    with pytest.raises(ValueError):
        generate_electorate(0)
    with pytest.raises(ValueError):
        generate_electorate(10, n_choices=1)


# --- tamper detection (behavioral, deterministic) ---------------------------
@pytest.mark.parametrize("mechanism", MECHANISMS)
def test_no_tamper_not_flagged(mechanism):
    ballots = generate_electorate(120, seed=1).ballots
    assert detect_tamper(mechanism, ballots, ballots) is False


@pytest.mark.parametrize("mechanism", MECHANISMS)
def test_tamper_detected_under_full_audit(mechanism):
    true = generate_electorate(120, seed=1).ballots
    tampered, flipped = apply_tamper(true, n_flip=8, seed=2)
    assert flipped  # sanity: something was actually flipped
    assert detect_tamper(mechanism, true, tampered, audit_fraction=1.0, seed=3) is True


def test_e2e_detects_single_flip_without_audit():
    true = generate_electorate(120, seed=1).ballots
    tampered, _ = apply_tamper(true, n_flip=1, seed=4)
    # cryptographic verification catches any change regardless of audit fraction
    assert detect_tamper("e2e_supervised", true, tampered, audit_fraction=0.0) is True


# --- scoring + decision rule (the measured selection) -----------------------
@pytest.mark.parametrize("mechanism", MECHANISMS)
def test_score_shape(mechanism):
    s = score_mechanism(mechanism, generate_electorate(300, seed=5))
    assert s.mechanism == mechanism
    assert 0.0 <= s.secrecy_leak <= 1.0
    assert s.double_vote_block == 1.0


def test_selection_picks_paper_under_default_params():
    sel = select_mechanism(generate_electorate(300, seed=5))
    assert sel.winner == "paper_rla"
    eliminated = dict(sel.eliminated)
    assert "e2e_supervised" in eliminated
    assert "secrecy_leak" in eliminated["e2e_supervised"]


@pytest.mark.parametrize("n", [100, 500])
def test_selection_stable_across_scale_endpoints(n):
    assert select_mechanism(generate_electorate(n, seed=9)).winner == "paper_rla"


def test_selection_is_deterministic():
    a = select_mechanism(generate_electorate(250, seed=2))
    b = select_mechanism(generate_electorate(250, seed=2))
    assert a.winner == b.winner and a.scores == b.scores


def test_gate_reacts_to_dropped_tamper_detection():
    # a mechanism whose tamper-detection falls below the floor must fail the hard constraints
    weak = MechanismScore(
        mechanism="paper_rla", tamper_detection=TAMPER_DETECTION_MIN - 0.1,
        secrecy_leak=0.10, double_vote_block=1.0, roll_tamper_detection=1.0,
        understandability=0.9, small_cell_leak=0.0,
    )
    assert weak.passes_hard_constraints is False


def test_secrecy_ceiling_is_the_eliminator_for_e2e():
    assert channel_secrecy_leak("e2e_supervised") > SECRECY_LEAK_MAX
    assert channel_secrecy_leak("paper_rla") <= SECRECY_LEAK_MAX
