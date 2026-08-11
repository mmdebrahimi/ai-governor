"""Mock-election rig: evidence-based voting-mechanism selection (family mars-gov-voting-verification).

Phase-1 Earth-test prototype. Compares TWO complete voting systems for a small (N=100-500),
high-coercion-risk, no-external-authority colony electorate:
  - paper_rla:       paper private casting + risk-limiting audit + public bulletin board
  - e2e_supervised:  in-person E2E-verifiable voting on supervised private terminals

Each mechanism is scored against the documented threat model (docs/voting_threat_model.md):
tamper-evidence, ballot secrecy (controllable leakage channels), and eligibility. A documented
decision rule (hard-constraint elimination -> tiebreak) selects the winner. Tamper detection and
small-cell inference are exercised by REAL deterministic functions so the gate is not decorative.

CONSTRUCT-VALIDITY CAVEAT: the per-channel attack-success-rates below are MODELED parameter
estimates from the threat-model doc, NOT empirical field measurements. They are the falsifiability
levers -- change them and re-run; the selection may flip. The Earth rig represents mechanism
*attack-surface* differences, not the Mars-specific environment. See docs/voting_threat_model.md.
"""
from __future__ import annotations

import random
from collections import Counter
from dataclasses import dataclass

# --- threat-model parameters (modeled attack-success-rate in [0,1]; lower = better secrecy) ---
# Per-mechanism CONTROLLABLE ballot-secrecy leakage channels. Documented in the threat-model doc.
PAPER_RLA_CHANNELS = {
    "insider_logs": 0.00,         # no electronic record of the vote exists
    "device_compromise": 0.00,    # no voter devices in the casting path
    "coercer_receipt": 0.00,      # no vote-revealing receipt is produced
    "physical_observation": 0.15, # booth / line observation in close quarters (private booth mitigates)
    "timing": 0.02,
}
E2E_SUPERVISED_CHANNELS = {
    "insider_logs": 0.05,         # ballots encrypted; residual metadata risk
    "device_compromise": 0.20,    # a supervised terminal is still compromisable
    "coercer_receipt": 0.10,      # receipt is non-transferable but observable / photographable
    "physical_observation": 0.10, # supervisor presence
    "timing": 0.05,
}
_CHANNELS = {"paper_rla": PAPER_RLA_CHANNELS, "e2e_supervised": E2E_SUPERVISED_CHANNELS}

# Tamper-detection / eligibility are near-parity; modeled per mechanism.
TAMPER_DETECTION = {"paper_rla": 0.99, "e2e_supervised": 1.00}      # RLA risk-limit vs cryptographic
DOUBLE_VOTE_BLOCK = {"paper_rla": 1.00, "e2e_supervised": 1.00}     # both registry-bound credentials
ROLL_TAMPER_DETECTION = {"paper_rla": 1.00, "e2e_supervised": 1.00} # public change-log + challenge period
UNDERSTANDABILITY = {"paper_rla": 0.90, "e2e_supervised": 0.50}     # tiebreak (deferred-qualitative)

# Decision-rule thresholds (docs/voting_threat_model.md).
SECRECY_LEAK_MAX = 0.30       # hard constraint: controllable channel leak must be <= this
TAMPER_DETECTION_MIN = 0.99   # hard constraint
DOUBLE_VOTE_BLOCK_MIN = 1.00  # hard constraint (zero tolerance for double voting)

MECHANISMS = ("paper_rla", "e2e_supervised")


# --------------------------------------------------------------------------- secrecy channels
def channel_secrecy_leak(mechanism):
    """P(at least one controllable channel leaks a voter-vote link); channels assumed independent."""
    if mechanism not in _CHANNELS:
        raise ValueError(f"unknown mechanism: {mechanism}")
    p_safe = 1.0
    for rate in _CHANNELS[mechanism].values():
        p_safe *= (1.0 - rate)
    return 1.0 - p_safe


# --------------------------------------------------------------------------- synthetic electorate
@dataclass(frozen=True)
class Electorate:
    n: int
    ballots: tuple   # choice index per voter
    bloc_of: tuple   # social-bloc id per voter (the attacker's social-graph knowledge)


def generate_electorate(n, n_blocs=5, cohesion=0.85, n_choices=2, seed=0):
    """Seeded synthetic electorate: voters belong to social blocs with correlated preferences.

    `cohesion` = probability a voter follows their bloc's preference (else votes randomly).
    The bloc map is what a social-graph-aware attacker uses for small-cell inference.
    """
    if n <= 0:
        raise ValueError("n must be positive")
    if n_choices < 2:
        raise ValueError("n_choices must be >= 2")
    rng = random.Random(seed)
    nb = max(1, min(n_blocs, n))
    bloc_pref = [rng.randrange(n_choices) for _ in range(nb)]
    ballots, bloc_of = [], []
    for v in range(n):
        b = v % nb
        bloc_of.append(b)
        ballots.append(bloc_pref[b] if rng.random() < cohesion else rng.randrange(n_choices))
    return Electorate(n=n, ballots=tuple(ballots), bloc_of=tuple(bloc_of))


def small_cell_inference_rate(electorate):
    """SHARED (mechanism-independent) secrecy risk: fraction of voters whose vote is inferable from a
    published bloc-level tally because their bloc voted unanimously. N=1 -> 1.0. Mitigation
    (result aggregation / minimum cell size) is deferred to phase-2 and noted in the threat model."""
    by_bloc = {}
    for choice, b in zip(electorate.ballots, electorate.bloc_of):
        by_bloc.setdefault(b, []).append(choice)
    inferable = sum(len(v) for v in by_bloc.values() if len(set(v)) == 1)
    return inferable / electorate.n


# --------------------------------------------------------------------------- tamper (real, deterministic)
def tally(ballots):
    return dict(Counter(ballots))


def apply_tamper(ballots, n_flip, n_choices=2, seed=0):
    """Flip `n_flip` distinct ballots to a different choice. Returns (tampered_ballots, flipped_indices)."""
    n = len(ballots)
    n_flip = max(0, min(n_flip, n))
    rng = random.Random(seed)
    idx = set(rng.sample(range(n), n_flip)) if n_flip else set()
    tampered = tuple((c + 1) % n_choices if i in idx else c for i, c in enumerate(ballots))
    return tampered, frozenset(idx)


def detect_tamper(mechanism, true_ballots, tampered_ballots, audit_fraction=1.0, seed=0):
    """Behavioral tamper detection. E2E: cryptographic verification catches ANY alteration.
    paper_rla: a risk-limiting audit samples `audit_fraction` of ballots and detects iff the sample
    intersects a flipped ballot. Both are deterministic given the seed."""
    if mechanism not in MECHANISMS:
        raise ValueError(f"unknown mechanism: {mechanism}")
    flipped = {i for i in range(len(true_ballots)) if true_ballots[i] != tampered_ballots[i]}
    if not flipped:
        return False  # nothing was tampered
    if mechanism == "e2e_supervised":
        return True   # any altered ballot fails its proof
    n = len(true_ballots)
    k = max(1, min(int(round(audit_fraction * n)), n))
    sample = random.Random(seed).sample(range(n), k)
    return any(i in flipped for i in sample)


# --------------------------------------------------------------------------- scoring + decision rule
@dataclass(frozen=True)
class MechanismScore:
    mechanism: str
    tamper_detection: float
    secrecy_leak: float          # controllable-channel leak (the differentiator)
    double_vote_block: float
    roll_tamper_detection: float
    understandability: float
    small_cell_leak: float       # shared contextual risk (reported, not a differentiator)

    @property
    def passes_hard_constraints(self):
        return (self.secrecy_leak <= SECRECY_LEAK_MAX
                and self.tamper_detection >= TAMPER_DETECTION_MIN
                and self.double_vote_block >= DOUBLE_VOTE_BLOCK_MIN)


def score_mechanism(mechanism, electorate):
    if mechanism not in MECHANISMS:
        raise ValueError(f"unknown mechanism: {mechanism}")
    return MechanismScore(
        mechanism=mechanism,
        tamper_detection=TAMPER_DETECTION[mechanism],
        secrecy_leak=channel_secrecy_leak(mechanism),
        double_vote_block=DOUBLE_VOTE_BLOCK[mechanism],
        roll_tamper_detection=ROLL_TAMPER_DETECTION[mechanism],
        understandability=UNDERSTANDABILITY[mechanism],
        small_cell_leak=small_cell_inference_rate(electorate),
    )


@dataclass(frozen=True)
class Selection:
    winner: str                  # selected mechanism, or "" if all eliminated
    scores: tuple
    eliminated: tuple            # ((mechanism, reason), ...)


def select_mechanism(electorate, mechanisms=MECHANISMS):
    """Documented decision rule: eliminate any mechanism failing a hard constraint, then tiebreak
    survivors by (lower secrecy_leak, higher understandability)."""
    scores = [score_mechanism(m, electorate) for m in mechanisms]
    survivors, eliminated = [], []
    for s in scores:
        if s.passes_hard_constraints:
            survivors.append(s)
            continue
        reasons = []
        if s.secrecy_leak > SECRECY_LEAK_MAX:
            reasons.append(f"secrecy_leak {s.secrecy_leak:.3f} > {SECRECY_LEAK_MAX}")
        if s.tamper_detection < TAMPER_DETECTION_MIN:
            reasons.append(f"tamper_detection {s.tamper_detection:.3f} < {TAMPER_DETECTION_MIN}")
        if s.double_vote_block < DOUBLE_VOTE_BLOCK_MIN:
            reasons.append("double_vote_block below floor")
        eliminated.append((s.mechanism, "; ".join(reasons)))
    winner = ""
    if survivors:
        survivors.sort(key=lambda s: (s.secrecy_leak, -s.understandability))
        winner = survivors[0].mechanism
    return Selection(winner=winner, scores=tuple(scores), eliminated=tuple(eliminated))
