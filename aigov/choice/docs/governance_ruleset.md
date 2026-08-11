# Mars Colony Governance Ruleset v0.1 (family `mars-gov-ruleset`)

A direct-democracy governance ruleset for a 100–500-person Mars colony, expressed so every rule is a
**falsifiable, machine-checkable predicate** (`docs/ruleset_predicates.md`, `governance/ruleset.py`) and
enforced through the **selected verification mechanism** (`paper_rla` + risk-limiting audit + public
bulletin board, from `mars-gov-voting-verification`). Umbrella: `mars-governance`. Scale: N = 100–500 (D2).

## Decision instruments
- **Ordinary referendum** — simple majority of valid votes (`yes-share > 50%`), quorum ≥ 50% of eligible.
- **Constitutional amendment** — supermajority (`yes-share ≥ 2/3`), quorum ≥ 50%, plus a ≥7-day
  deliberation window and a 90-day re-proposal cooldown after a failed amendment.
- **Recall** — a petition signed by ≥40% of eligible triggers a recall referendum (then ordinary rules).

## Eligibility (binding to voting family)
Eligibility, credentialing, and the registry root-of-trust are owned by `mars-gov-voting-verification`
(threat-model doc). A ballot counts only if cast by an eligible, credentialed colonist who has not already
voted; the ruleset consumes that mechanism's eligibility + tamper verdicts rather than re-implementing them.

## Result ratification
No result is binding until the selected mechanism **ratifies** it: `result_ratifiable(...)` runs the
paper+RLA verification and rejects any tampered tally (`verification-failed`). This couples governance
legitimacy directly to the measured-best verification layer.

## Dispute resolution
Disputes (eligibility challenges, result challenges) must be resolved within a **14-day SLA**
(`dispute_within_sla`). The resolution *procedure* (who adjudicates, appeal path) is deferred to phase-2;
only the SLA is pinned and checkable now.

## What "TESTED" means here (umbrella D1, staged)
- **Stage A (now):** the predicate suite passes — rules are machine-checkable and enforceable in software.
- **Stage B (phase-2):** the integrated sandbox (`mars-gov-sandbox`) runs the ruleset over ≥10 decision
  cycles with a simulated population.
- **Stage C (phase-2):** formal verification of the predicates.

## Open / deferred (phase-2)
Trustee-board change-approval workflow; dispute-resolution procedure + appeals; weighted/liquid democracy;
multi-option ballots; emergency-powers rules; constitutional entrenchment (rules that need a higher bar to
change); legitimacy/understandability instrument. These do not block the Stage-A predicate MVP.
