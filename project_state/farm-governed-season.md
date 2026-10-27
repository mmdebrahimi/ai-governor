# Farm-Season Twin — Governed Season Integration (F16)

<!-- project-schema: 0.1 -->

> Initialized 2026-10-27 (Soraya self-init, run `2026-10-27-0900-decompose-plan-farm-season-twin`).
> Project ID: farm-governed-season. Originating goal (verbatim): "Run one full replayed historical
> potato season end-to-end under the aigov kernel with every action gated, emit a season report,
> extend the adversarial suite to the new instrument, and evaluate the venture kill condition".

> **PRIVACY — STANDING.** Public repo. Concept-level only.

## Project Context
- **Project ID:** farm-governed-season
- **Project root:** C:\Users\Farshad\PythonProjects\Skill_Development\AI_Governor
- **Captured:** 2026-10-27
- **Originating goal:** (verbatim above)
- **Refined goal (3c top candidate):** One governed replayed season: F14's world ticked day-by-day,
  F15's instrument proposed/ratified/certified/applied through the UNCHANGED kernel, a season report
  comparing governed vs status-quo vs never-treat runs, ≥3 new named adversarial attacks on the farm
  instrument all ending in detection or escalation, and a written kill-condition evaluation.
- **Horizon (months):** 4
- **Relationship to portfolio:** Gate C — the venture terminal. Depends on F14 + F15. The explicit
  NON-GOAL: a permanent farm-operations loop (unbounded operating state — the F13 init carved this
  out and the same carve-out binds here). Season two (dirt/hardware/orchestration over bought
  machines) is a USER decision gated on this family's season report.

## Empirical Concerns
- **Verdict:** FLAG
- **Check status:** inherited
- **Findings:** Inherits F14's composition-fidelity flag and F15's damage-coupling flag. Adds its own:
  a season report whose yield comparison rests on an unverified damage coupling must label those
  numbers model-coherent-only (the Mars twin's own honesty class), never outcome claims.

## Project vs Research-Program
- **Verdict:** FAIL → hybrid
- **Rationale:** BOUNDED: the replayed season, the report, the adversarial extension, the kill
  evaluation. UNBOUNDED: "govern the farm" — explicitly out, recorded as what the project makes
  possible, not what it delivers (same shape as F13's carve-out).

## Goal Hierarchy

### Mid-term (≤4 months)
| # | Milestone | Success Criterion |
|---|---|---|
| 1 | One governed tick | a single sim day flows propose→ratify→certify→apply with zero bypasses |
| 2 | Full governed season | replayed season completes; every applied action carries a RatificationRecord + certification |
| 3 | Season report | governed vs status-quo vs never-treat comparison, honesty-labelled |
| 4 | Adversarial extension | ≥3 named attacks on the farm instrument; all end in detection or escalation |
| 5 | Kill condition evaluated | written verdict against the decompose doc §5 condition, either way |

## MVP Criteria
| Criterion | Kind | Predicate |
|---|---|---|
| Governed season test green | test-exit-0 | `python -m pytest tests/test_farm_governed_season.py -q` |
| Season report exists | file-exists | `docs/farm_season_report_v1.md` |
| Adversarial extension green | test-exit-0 | `python -m pytest tests/test_adversarial_farm_instrument.py -q` |

## State Snapshot

### Assumptions
- The kernel's cycle machinery needs no fork to drive a 365-tick season — confidence: **medium**
- Season-scale determinism (seeded) is achievable so the report is reproducible — confidence: **high**

### Evidence
| # | Claim | Source | Confidence | Captured |
|---|---|---|---|---|
| 1 | Running the composed loop finds defects green suites cannot (kernel lost-atmosphere incident; decisions.py 3 defects) | this repo's own record | high | 2026-10-27 |
<!-- project-state:end:evidence -->

### Unknowns
- Whether kernel cycle cadence (propose each tick vs propose on rule-change) fits a 150-day season
- What the season report's denominator is (yield vs compliance — F15 action 4 decides)

### Hypotheses (Active)
| ID | Statement | Status | Last-tested |
|---|---|---|---|
| H1 | The governed season completes with zero ungated applications | open | never |
| H2 | Governed run beats never-treat and ≈ matches status-quo calendar on the replayed season's risk profile | open | never |
<!-- project-state:end:hypotheses -->

### Decisions Made
| Decision | Date | Notes |
|---|---|---|
| Venture kill condition + $0 season-one capital cap encoded here (user-ratified "supersede, bounded") | 2026-10-27 | See decompose doc §5; failing it re-instates F13 row 46's hobby decision with an R9 constraint-expiry entry |
<!-- project-state:end:decisions-made -->

### Pending Decisions
| Decision | Proposer | Blocker | Notes |
|---|---|---|---|
| Season-two go/no-go (dirt, hardware, orchestration over bought machines) | user | milestone 5 | AUTHORITY — never Soraya's |
<!-- project-state:end:pending-decisions -->

## Bellman-Inspired Decision Frame

### Current state (one-line summary)
Seeded 2026-10-27. Blocked on F14 + F15 by design; first unblocked action is the one-governed-tick
spike as soon as F14's wrapper and F15's rules exist in any walking form.

### Target state / terminal condition
All five milestones met and the kill condition evaluated in writing. The unbounded operating state is
explicitly NOT the terminal.

### Candidate next actions
| # | Action | Class | Expected progress | Expected info gain | Uncertainty | Cost |
|---|---|---|---|---|---|---|
| 1 | One-governed-tick spike (earliest possible integration) | run-tests | high | highest | medium | 1 day once F14/F15 walk |
| 2 | Season-cadence design note (propose-per-tick vs on-change) | write-plan | medium | medium | low | 2 hrs |
<!-- project-state:end:candidate-actions -->

### Re-evaluation trigger
- after any action; immediately when F14 milestone 1 + F15 milestone 1 both land (unblocks the spike)

## Allowed Action Classes (v0.2 placeholder)
- `propose` / `research` / `write-plan` / `run-tests` / `ask-user` / `stop` — auto
- `edit-local-code` — auto in-cwd

## Action Log
| # | Date | Action class | Description | Outcome |
|---|---|---|---|---|
| 1 | 2026-10-27 | propose | /project-init protocol executed by hand (Soraya self-init, decompose mode) | ledger created |
<!-- project-state:end:action-log -->

## Open Questions for User
- Season-two go/no-go is yours, gated on milestone 5 — recorded now so it cannot drift into an autonomous call.

## Last Evaluation
- **Date:** 2026-10-27
- **Progress signal:** (init only)
