# Binding-Election Contract — Spec (family `mars-gov-binding-elections`)

Resolves **C1** (2026-06-06 review): the advised cycle was applying an approval winner with no
ratification, and `paper_rla` (single-choice) is not a drop-in for approval ballots (sets per voter).
This family defines a **mechanism-aware binding-election contract** so each voting mechanism owns its
own ballot schema, tally, winner, and audit. Code: `governance/binding_elections.py`.

## Contract (`MechanismContract`)
Each mechanism provides: `validate(ballots, options)` · `tally(ballots, options)` ·
`winner(tally, status_quo, options)` · `audit(true, published, audit_fraction, seed) -> tamper?`.

`ratify(mechanism, true_ballots, published_ballots, options, status_quo, eligible, quorum=0.5, ...)`
returns `Ratification(ok, winner, reasons)`. **ok iff** ballots valid AND quorum met AND audit finds no
tamper. The status quo is mandatory (an option).

## Mechanisms
- **SINGLE_CHOICE** — paper + risk-limiting audit; one choice per voter; reuses the single-choice tamper
  model (`mock_election.detect_tamper`). Winner = plurality (ties → status quo if tied, else first).
- **APPROVAL** — sets per voter; tally = approval counts; winner = `approval_winner` + **status-quo
  finalist** (a non-SQ option must strictly beat SQ, else `none-of-these`). Audit = an **approval-specific
  comparison RLA**: sample voters, tamper detected iff a sampled voter's published approval-*set* differs
  from the true set (a length mismatch is structural tamper).

## Why approval needs its own audit
Single-choice audits compare categorical choices; approval ballots are sets, so margins, overstatement,
and sampling differ. Reusing the single-choice audit on approval ballots would manufacture a false
ratification signal — hence the distinct `_ap_audit`.

## Integration (makes the advised cycle honest end-to-end)
`sandbox/governance_sandbox.py:run_advised_cycle` now builds sincere approval ballots over the AI menu and
routes them through `ratify(APPROVAL, ...)`; a menu is **applied only if** diversity-certified AND
non-steering AND **ratified**. The AI advisor proposes the menu; it never owns the tally.

## Deferred (phase-2)
Per-stage audit (menu disclosure / ballot collection) [M2]; coercion-resistant ballot privacy; real RLA
risk-limit math (sample size from margin); paper-compatible approval ballot encoding; multi-winner /
proportional mechanisms.
