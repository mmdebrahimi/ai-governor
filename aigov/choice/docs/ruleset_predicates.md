# Governance Ruleset — Predicate Specification (family `mars-gov-ruleset`)

Every governance rule is reduced to a **machine-checkable predicate** (`governance/ruleset.py`). This is
the operational contract H1 asserts: a direct-democracy ruleset *expressible as predicates, enforceable by
the selected verification mechanism*. Thresholds below are the documented constants.

## Threshold rules
| Rule | Predicate | Threshold | Notes |
|---|---|---|---|
| Quorum | `quorum_met(turnout, eligible)` | turnout/eligible ≥ **0.50** | any vote invalid below quorum |
| Ordinary majority | `simple_majority(yes, no)` | yes-share **> 0.50** | strict; a tie fails |
| Amendment supermajority | `supermajority(yes, no)` | yes-share ≥ **2/3** | constitutional changes |
| Recall petition | `recall_petition_valid(sigs, eligible)` | sigs/eligible ≥ **0.40** | triggers a recall vote |

## Timing rules
| Rule | Predicate | Threshold | Notes |
|---|---|---|---|
| Deliberation latency | `amendment_latency_ok(proposed, vote)` | vote − proposed ≥ **7 days** | min deliberation window |
| Amendment cooldown | `amendment_cooldown_ok(last_failed, new)` | gap ≥ **90 days** | re-proposal cooldown after failure |
| Dispute SLA | `dispute_within_sla(raised, resolved)` | resolved − raised ≤ **14 days** | unresolved ⇒ breach |

## Mechanism binding (the enforceability claim)
`result_ratifiable(true_ballots, published_ballots)` calls the **selected verification mechanism**
(`paper_rla`, from `mars-gov-voting-verification`) via `detect_tamper(..., audit_fraction=1.0)`. A result
is ratifiable iff the mechanism finds **no tamper**. This is what makes H1 concrete rather than abstract:
the ruleset does not merely *describe* rules, it executes them against the chosen verification layer.

## Composition
`evaluate_referendum(yes, no, turnout, eligible, kind, [ballots])` composes quorum + the kind-appropriate
threshold + (when ballots supplied) ratifiability, returning a frozen `Outcome(passed, reasons)` where
`reasons` enumerates violations (`quorum-not-met`, `threshold-not-met`, `verification-failed`).

## Falsifiability
All predicates are pure and total; bad inputs raise `ValueError`. The suite
`tests/test_ruleset_predicates.py` pins each boundary (tie fails, 2/3 boundary, 7-day latency, 14-day SLA,
tamper blocks ratification). Change a threshold constant and the corresponding boundary test must move.

## Deferred to phase-2
Weighted/quadratic voting, delegation/liquid-democracy, multi-option (non-binary) ballots, the full RLA
risk-limit computation, trustee-board change-approval workflow, and dispute-resolution *procedure* (only
its SLA is pinned here).
