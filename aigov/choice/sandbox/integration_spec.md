# Integrated Governance Sandbox — Integration Spec (family `mars-gov-sandbox`)

Phase-1 deliverable: an Earth-side software sandbox that runs the full colony decision cycle —
**proposal → vote → resource-constrained outcome** — over ≥10 cycles, wiring the three built families.
Umbrella: `mars-governance`. Scale N = 100–500 (D2). Stage A only (umbrella D1).

## Wired interfaces
| Family | Module | Used for |
|---|---|---|
| mars-gov-resource-sim | `models.resource_sim` | `per_capita_food_dry_kg`, `oxygen_balance` — food feasibility + plant-O2 balance |
| mars-gov-voting-verification | `prototypes.verify_mechanisms.mock_election` | `apply_tamper` (+ selected `paper_rla` verification via the ruleset) |
| mars-gov-ruleset | `governance.ruleset` | `evaluate_referendum` — quorum + majority + ratification |

## The decision cycle (`run_cycle`)
1. **Propose** — a feedback controller (`propose_policy`) picks the smallest `crop_fraction` that feeds
   the colony, enabling O2 **scrubbing** if that pushes the plant subsystem into over-production.
2. **Vote** — a synthetic electorate (full turnout) votes; `evaluate_referendum` applies quorum (≥50%),
   ordinary majority (>50%), and ratification through the selected `paper_rla` mechanism.
3. **Outcome** — a *passing, ratified, resource-feasible* proposal is applied; otherwise the state is
   unchanged. A tampered tally yields `verification-failed` → never applied.

## Invariants (checked on the applied state every cycle)
- **no starvation** — food supply ≥ demand.
- **O2 managed** — plant-O2 over-production only allowed when scrubbing is on.
- **crop_fraction in [0.50, 1.00]**.
(Quorum + ratification are enforced upstream by the ruleset, so an applied decision is always quorate
and tamper-free.)

## Hypotheses demonstrated
- **H1** — nominal operation runs ≥10 cycles at N=100–500 with zero invariant violation.
- **H2** — under `scenario="scarcity"` the colony adapts (crop_fraction → ~0.93 + scrubbing on) and
  **converges to a stable, violation-free state**.

## Honest failure mode
`scenario="famine"` (imported food below what any crop_fraction can close) is **un-governable by policy
alone** — the sandbox flags `starvation` rather than pretending a vote fixes physics. This is a feature:
the rig detects when governance cannot save the colony.

## Deferred (Stage B / C, phase-2)
Human field-test with real participants (Stage B); formal verification of the cycle (Stage C); richer
proposals (multi-lever budgets, population policy); stochastic electorates; transient resource dynamics;
emergency-powers / recall flows in the loop.
