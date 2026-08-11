# Governance multi-peaked residual — converted to a FAIL-CLOSED escalation (no silent mis-certification)

**Date:** 2026-06-08 (Soraya --advance, top-VOI family mars-governance)
**Type:** fail-safe reliability mechanism (NOT an attempt to "solve" multi-peaked social choice — that would be p-hacking)
**Builds on:** `innovation_governance_2026-06-08.md` (the panel-agnostic completeness proof)
**Model:** `governance/fail_safe_gate.py`; tests `tests/test_fail_safe_gate.py` (5, pass); full governance suite 132 passed (was 127), 0 regressions.

## The residual this closes

The panel-agnostic proof made anti-capture hold ACROSS the class of single-peaked-aggregate panels (in-domain held-rate 1.0). But ~22% of random panels are **multi-peaked** aggregates, where steering toward a secondary peak *reduces* the citizen-cost gap and breaks catch-faithfulness. The danger was not the wall itself — it is that `panel_agnostic_gate` **did not check for it**: on a multi-peaked panel it could return `applied=True` ("not steered") even when the catch was unfaithful — a **silent mis-certification** of a real capture.

Multi-peaked electorates are the classic hard case in social choice (Condorcet cycles; McKelvey's chaos theorem; Gibbard-Satterthwaite forbids any non-dictatorial strategy-proof rule). You **cannot** solve them in-sim, and claiming to would be exactly the kind of fabrication this project refuses.

## The mechanism (fail-closed, not a tuned parameter)

`aggregate_single_peaked(panel,...)` already detects the out-of-domain case **perfectly** — every faithfulness failure in the ensemble is exactly a multi-peaked panel. Wire it as a **gate precondition**:

- **aggregate multi-peaked → ESCALATE.** Do not certify "not steered." Route to a manipulation-robust procedure: (a) Condorcet/Copeland aggregation, (b) **randomized agenda order** (removes the agenda-setter's ordering power — the lever McKelvey chaos exploits), (c) transparent publication of every detected preference peak (so a hidden secondary constituency cannot be steered to in the dark).
- **aggregate single-peaked → run the existing panel-agnostic gate** (CERTIFY / STEERING-DETECTED).

A CERTIFY verdict is therefore only ever issued inside the domain where the catch property is faithful. The 22% blind spot is converted from *silent catch failures* into *flagged escalations* — a sound boundary, not a vulnerability. Same fail-closed discipline as the gated test-runner and the ISRU common-cause partitioning.

## Result (ensemble, 500 random panels/scenario, deterministic)

| Scenario | In-domain (certifiable) | Escalated (multi-peaked) | **Silent failures among certified** | Escalated == multi-peaked |
|---|---|---|---|---|
| nominal | 388 | 112 (22.4%) | **0** | yes |
| scarcity | 500 | 0 (0.0%) | **0** | yes |

- **Zero silent failures among certified verdicts** — the headline soundness number. The gate never certifies a capture it cannot faithfully audit.
- **Escalation is targeted, not blanket** — it fires on exactly the multi-peaked panels (112/500 in nominal), and on none in scarcity (whose aggregates are always single-peaked). No valid panel is needlessly escalated.

## What this changes for the module

The governance anti-capture story is now: **"in software, the mechanism either certifies a sound result or refuses and routes to a robust procedure — it never silently passes a capture it cannot audit."** The multi-peaked theorem-wall is preserved and handled honestly (fail-closed), rather than papered over.

## Honest boundaries (do not soften)
- **Detection needs the citizen-preference aggregate.** In-sim we have the synthetic panel, so the detector runs and the in-sim silent failure is removed. Whether a REAL electorate's multi-peakedness is observable — and whether real preferences over crop_fraction are single-peaked at all — is a Stage-B human-field-test question, unchanged.
- **The escalation ROUTES, it does not claim a manipulation-PROOF procedure** — Gibbard-Satterthwaite forbids that. It claims the system never silently certifies an unauditable capture, and hands multi-peaked cases to a procedure that removes the agenda-setter's ordering power.
- Still **synthetic** panels only; the human axis remains the real gate (`docs/governance_field_test_design.md`).

## Reproduce
```bash
cd Mars_Governance
python -m pytest tests/test_fail_safe_gate.py -q
python -m governance.fail_safe_gate
```
