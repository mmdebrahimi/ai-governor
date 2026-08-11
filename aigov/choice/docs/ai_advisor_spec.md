# AI-Governor Agenda Layer — Spec (family `mars-gov-ai-advisor`)

Phase-1, **resource domain only**. A proposer/disposer design: an AI proposer generates a curated,
analyzed option set; humans dispose via approval voting. Built per the 2026-06-05 brainstorm/review.
Umbrella: `mars-governance`. Code: `governance/ai_advisor.py` (+ `approval_winner` in `governance/ruleset.py`).

## The honest claim (T1 — narrowed)
> Positive agenda rights are a **necessary** anti-agenda-control mechanism for AI-assisted governance, and
> become **testable only in bounded domains with formal option spaces**. They make agenda control
> **contestable, not solved.**

This is NOT general-governance certification. It is resource-allocation agenda certification.

## Decisions (T1–T4 defaults; ratify or redirect)
- **T1** narrowed headline (above).
- **T2** multi-option rule = **approval voting + status-quo finalist** (`approval_winner`): a non-status-quo
  option must strictly beat the status quo's approvals, else `NONE_OF_THESE`. Simple, paper/RLA-compatible,
  no ranking (blunts automation bias). Known failure mode (M1): disciplined bullet-voting — surfaced by
  `test_bullet_voting_can_shift_winner`; full mitigation (published distributions, runoff) is phase-2.
- **T3** `NONE_OF_THESE` → a binding interim state: a citizen-drafting window opens; the **urgent-cycle
  default is a minimum-survival caretaker policy** (no decision must not be a silent dangerous decision).
  *(Procedure modeled as the outcome value here; the drafting-window workflow is phase-2.)*
- **T4** simulator **pluralism**: two independent feasibility models (`FeasibilityModel` A/B, different
  yield assumptions). An option is feasible only if **both agree**; boundary disagreement is surfaced
  (`Option.model_disagreement`) — defends against the simulator-as-single-point-of-capture risk (C3).

## Formal option space (what makes diversity measurable — C2)
Option lever = `crop_fraction`; `scrubbing` is a derived O2 label; the import assumption sets the scenario.
`_utility` encodes the genuine tension (food-deficit catastrophic; |O2 net| and farming effort are costs),
giving an interior optimum near the plant-O2 break-even (cf ≈ 0.667), distinct from the inefficient
status quo (cf = 0.85).

## Option-diversity predicate (`option_diversity`)
A ballot's option set is certified iff: **status quo present** + **≥2 feasible options** + **spans** the
feasible lever range (≥50% of the grid range) + **does not omit the optimum** (a feasible option within
`OPTIMUM_TOL` of `optimal_cf`). A strawman that clusters around the status quo fails on `omits-optimum`
and `clustered-not-spanning`.

## Adversarial agenda review (`adversarial_review`) — the falsification test (M3)
Insert every omitted feasible grid option and re-tally. **Steering is detected** if the winner flips to
`NONE_OF_THESE` or its utility shifts beyond `STEERING_UTILITY_THRESHOLD`. This is a **falsification
regime, not a proof** — the feasible space is not exhaustively enumerable (denominator problem). An honest
spanning agenda shows no steering; a strawman does.

## Pipeline fit + certification tiers (corrected 2026-06-06 review)
Generates analyzed options → `approval_winner` (this family, extends ruleset) → **model-disposal result**.
**The advised path is NOT yet ratified.** `paper_rla` ratifies the SINGLE-CHOICE referendum path only;
approval ballots are *sets* per voter and need their own paper-compatible audit (phase-2, C1). Do not read
`run_advised_cycle`'s output as a binding, verified decision.

Two-tier certification language — use precisely:
- **MODEL-COHERENT** — "under the documented utility model + constants, the menu is not omission-steering
  by this metric." This is ALL the diversity predicate + adversarial review establish; the certification is
  ENDOGENOUS to the same `_utility`/`optimal_cf` surface it scores against. The ledger "confirmed" markers
  mean **model-coherent, NOT governance validity**.
- **GOVERNANCE-VALIDATED** — reserved for claims backed by STRUCTURALLY INDEPENDENT evidence (a second,
  independently-authored utility model; human comprehension / preference elicitation; public contestation).
  **Nothing in Stage A is governance-validated.**

### Known gaps → phase-2 (2026-06-06 review)
- **C1** mechanism-aware binding-election contract (ballot schema · validity · tally · margin · tamper ·
  audit/ratification *per mechanism*); approval gets its own paper-compatible audit. Advisor proposes a
  menu, never a privileged tally channel.
- **C2-b** a structurally INDEPENDENT non-steering check (2nd utility model / human elicitation) — relabeling
  is necessary but NOT sufficient.
- **M1** caretaker = a real min-survival governance transition (recomputed feasible allocation,
  invariant-checked, authority-defined, time-limited/auto-expiring, logged, review-triggered) — today it
  merely holds state.
- **M2** per-stage audit (menu generation · disclosure · ballot collection · tally · ratification ·
  application) — the advisor's power is UPSTREAM of the tally.
- **Stage B** priority order: comprehension → framing-sensitivity → agenda-trust/contestation → coercion/abstention.
- **Stage C** scope: the FULL state machine (cert · disposal · ratification · fallback · invariants ·
  caretaker), not just pure predicates.

## Deferred (phase-2)
Multi-lever options (labor/energy/storage/risk-tolerance); citizen agenda-injection + spam bounds; the
citizen-drafting-window workflow; published approval distributions + runoff (full M1 fix); model
calibration against real outcomes; general (non-resource) agenda certification; AI-vs-citizen option
labeling decision; emergency-powers bypass predicate.
