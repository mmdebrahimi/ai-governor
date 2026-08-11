# verify_mechanisms — voting-mechanism mock-election rig

Phase-1 Earth-test prototype for family `mars-gov-voting-verification` (umbrella `mars-governance`).
Evidence-based selection between **two complete voting systems** for a 100–500-person, high-coercion-risk,
no-external-authority colony electorate. Falsification target: the front-runner hypothesis H2 that
**paper private-casting + risk-limiting audit beats in-person E2E-verifiable voting** on the combined
threat-model score.

## Candidates (two, per recorded hypothesis H2)
- `paper_rla` — paper private casting + risk-limiting audit + public bulletin board.
- `e2e_supervised` — in-person E2E-verifiable voting on supervised private terminals.

(Blockchain is deferred — it collapses to an append-only bulletin-board *substrate* inside a complete
system, not a third complete candidate. Drop criterion is in `docs/voting_threat_model.md`.)

## What the rig measures
Per mechanism, against the threat model (tamper-evidence | ballot secrecy | eligibility):
- **tamper-detection** — `detect_tamper(...)` runs a real, deterministic check (E2E cryptographic
  verification catches any alteration; paper RLA detects iff its audit sample hits a flipped ballot).
- **ballot-secrecy leak** — `channel_secrecy_leak(...)` aggregates per-mechanism controllable channels
  (insider logs, device compromise, coercer receipt, physical observation, timing).
- **small-cell inference** — `small_cell_inference_rate(...)`, a *shared* social-graph risk derived from
  the synthetic electorate (unanimous blocs leak every member's vote). Mechanism-independent; reported,
  not a differentiator.
- eligibility (double-vote-block, roll-tamper detection) and understandability (deferred-qualitative
  tiebreak constant).

## Decision rule (`select_mechanism`)
Eliminate any mechanism failing a **hard constraint** (`secrecy_leak <= 0.30`, `tamper_detection >= 0.99`,
`double_vote_block == 1.0`), then tiebreak survivors by `(lower secrecy_leak, higher understandability)`.

## Falsifiability (construct-validity caveat)
The per-channel attack-success-rates in `mock_election.py` are **modeled parameter estimates**, not field
data. They are the levers: raise paper's `physical_observation` or lower `SECRECY_LEAK_MAX` and paper can
lose. The current default parameters select **`paper_rla`** (E2E is eliminated on the secrecy hard
constraint, ~0.42 > 0.30). This confirms H2 *conditional on the documented parameters* — change them and
re-run to falsify.

## Run
```bash
python -m pytest tests/test_mock_election.py -q
```
The suite is the MVP gate (criterion 3). It parametrizes over both mechanisms; adding a third candidate is
a one-line change to `MECHANISMS`.
