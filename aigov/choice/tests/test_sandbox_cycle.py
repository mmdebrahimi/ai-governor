"""Integrated-sandbox validation suite (family mars-gov-sandbox). MVP gate.

Demonstrates H1 (>=10 cycles, N=100-500, zero invariant violation in Stage A) and H2 (direct-democracy
stable under resource-scarcity stress). Also pins the end-to-end verification binding: a tampered tally
is never applied. One flat suite mirroring the resource-sim pattern.
"""
import pytest

from sandbox.governance_sandbox import ColonyState, run_sandbox


# --- H1: nominal operation, zero violations over >=10 cycles ----------------
def test_h1_nominal_zero_violations():
    results = run_sandbox(300, n_cycles=12, scenario="nominal")
    assert len(results) >= 10
    assert all(r.invariants_ok for r in results)
    assert all(not r.violations for r in results)


@pytest.mark.parametrize("n", [100, 500])
def test_h1_scale_endpoints(n):
    results = run_sandbox(n, n_cycles=10, scenario="nominal")
    assert all(r.invariants_ok for r in results)


# --- H2: stability under resource-scarcity stress ---------------------------
def test_h2_scarcity_stays_stable():
    results = run_sandbox(300, n_cycles=12, scenario="scarcity")
    assert all(r.invariants_ok for r in results)
    # converged: the last several applied states are identical
    tail = [r.state for r in results[-4:]]
    assert all(s == tail[0] for s in tail)


def test_h2_scarcity_enables_scrubbing():
    final = run_sandbox(300, n_cycles=12, scenario="scarcity")[-1].state
    # scarcity forces crop_fraction up into plant-O2 over-production -> scrubbing must be on
    assert final.crop_fraction > 0.9
    assert final.scrubbing is True


def test_nominal_no_scrubbing_needed():
    final = run_sandbox(300, n_cycles=12, scenario="nominal")[-1].state
    assert final.scrubbing is False


# --- end-to-end verification binding ----------------------------------------
def test_tampered_decision_is_not_applied():
    results = run_sandbox(200, n_cycles=12, scenario="nominal", tamper_cycle=3)
    tcyc = results[3]
    assert tcyc.applied is False
    assert "verification-failed" in tcyc.reasons
    # the tampered cycle leaves the prior (clean) state unchanged and violation-free
    assert tcyc.invariants_ok is True
    assert tcyc.state == results[2].state


# --- honest failure detection: un-governable famine flags starvation --------
def test_famine_flags_starvation():
    results = run_sandbox(300, n_cycles=10, scenario="famine")
    assert any("starvation" in r.violations for r in results)
    assert any(not r.invariants_ok for r in results)


# --- determinism + guards ---------------------------------------------------
def test_determinism():
    a = run_sandbox(250, n_cycles=10, scenario="scarcity", seed=2)
    b = run_sandbox(250, n_cycles=10, scenario="scarcity", seed=2)
    assert [r.state for r in a] == [r.state for r in b]
    assert [r.applied for r in a] == [r.applied for r in b]


@pytest.mark.parametrize("kwargs", [
    {"n": 0},
    {"n": 100, "scenario": "bogus"},
    {"n": 100, "n_cycles": 0},
])
def test_invalid_inputs(kwargs):
    with pytest.raises(ValueError):
        run_sandbox(**kwargs)


def test_state_is_frozen():
    s = run_sandbox(100, n_cycles=10)[0].state
    assert isinstance(s, ColonyState)
    with pytest.raises(Exception):
        s.crop_fraction = 0.99
