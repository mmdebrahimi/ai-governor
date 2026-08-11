# AI Government F6 — Collective Choice (D3): the sovereign channel
<!-- project-schema: 0.1 -->

> Initialized 2026-08-11. Project ID: aigov-collective-choice. Originating goal (verbatim): "Integrate the existing Mars_Governance collective-choice organ into the AI Government as department D3 with ZERO test loss, so the sovereign channel (ratify-gates-execution, fail-closed escalation, anti-steering) is the AI Governor's decision seam rather than something rebuilt."
> Seeded by Soraya `--advance` spillover (2026-08-11), `/project-init` protocol executed by hand. Parent umbrella: `aigov`. Self-init recorded 5/25.

## Project Context
- **Project ID:** aigov-collective-choice
- **Project root:** C:\Users\Farshad\PythonProjects\Skill_Development\AI_Governor
- **Captured:** 2026-08-11
- **Originating goal:** (see verbatim above)
- **Refined goal (if 3c produced one):** Vendor the Mars_Governance organ (`governance/`, `models/`, `sandbox/`, `prototypes/`, `tests/`, `docs/`, `results/`) into `aigov/choice/` as a self-contained subtree whose own suite passes at full strength from the new root, WITHOUT modifying the source tree; then bind `fail_safe_gate` as the implemented invariant behind charter clause C15.
- **Role:** FAMILY ledger under umbrella `aigov`. Critical-path position: **Gate B — the sovereign channel (D3).**
- **Horizon (months):** 3
- **Schema:** project-schema 0.1

## Empirical Concerns
- **Verdict:** PASS
- **Check status:** attempted
- **Provisional:** NO
- **Findings:** The goal's factual claim ("the existing organ passes its suite") was checked by DIRECT EXECUTION, twice, and the check surfaced a provenance fact that corrects an earlier claim of this project. **Committed HEAD of `Space_Reflectors_Project` carries 132 tests across 11 test files** (measured in an isolated detached `git worktree` at HEAD, then removed). **The working tree carries 193 tests across 17 test files.** The 61-test difference is ~6 weeks of UNCOMMITTED work (8 modified + 16 untracked entries, mtimes 2026-06-27/28), including `governance/civic_education.py`, `governance/connection.py`, `tests/test_caretaker_and_stages.py`, `tests/test_civic_education.py`. **The `132` figure in `results/innovation_governance_failsafe_2026-06-08.md` is therefore CORRECT for HEAD and was wrongly called "stale" by this project on 2026-08-11 — corrected here and on the session board.**

## Project vs Research-Program
- **Verdict:** PASS
- **Provisional:** NO
- **Classification:** project
- **Rationale:** Bounded (one vendoring operation + an import fix + a charter binding), mechanically measurable (test count preserved exactly), horizon 3 ≤ 12.

## Refinement Candidates
- **Verdict:** PASS
- **Provisional:** NO
- **Refined-from:** originating-goal
- **Candidates:** C1 (= refined goal, EXECUTED): vendor as a self-contained subtree with its own conftest. C2: rewrite imports to make the organ a true `aigov.choice.*` package — cleaner long-term, higher risk of silent behaviour change during the move, DEFERRED until the kernel actually needs the namespace. C3: depend on the sibling repo by path instead of vendoring — REJECTED, it would couple this project to another session's uncommitted working tree.

## MVP Criteria
<!-- attempt-budget: 3 -->
- file-exists aigov/choice/governance/fail_safe_gate.py
- file-exists aigov/choice/conftest.py
- test-exit-0 python -m pytest aigov/choice/tests -q
- project-state-row project_state/aigov.md:F6-organ-vendored-zero-test-loss
<!-- project-state:end:mvp-criteria -->

> **Bar status: PROPOSED (draft-then-ratify)** under the v1.12 execute-mode exception. Not user-confirmed.
> Note the `project-state-row` predicate targets the UMBRELLA, not this ledger — per the 2026-08-11
> self-satisfying-predicate rule.

## Goal Hierarchy
### Long-term (12+ months tier)
A sovereign channel the AI Governor cannot bypass: options are ratified before they apply, results that cannot be faithfully audited are escalated rather than certified, and the tally is independent of the generator.

### Mid-term (3-12 months)
| # | Milestone | Success Criterion | Horizon |
|---|---|---|---|
| 1 | Organ vendored, suite at full strength | 193/193 from the new root; source tree byte-unchanged | ≤1 mo |
| 2 | C15 bound to a real invariant | charter `enforced_by` resolves; PENDING → ENFORCED | ≤1 mo |
| 3 | Kernel binding (`ratify()` gates apply) | no action applies without ratified ∧ certified ∧ constraint-satisfying | ≤2 mo (needs F5) |
| 4 | Namespace migration (C2) | organ importable as `aigov.choice.*` with 0 test loss | ≤3 mo |

### Short-term (≤1 month)
| # | Action | Class | Owner | Horizon |
|---|---|---|---|---|
| 1 | Bind ratify() into the kernel decision seam | edit-local-code | claude | ≤4 wk |
| 2 | Namespace migration to aigov.choice.* (C2) | edit-local-code | claude | ≤4 wk |
| 3 | Wire the vendored suite into the root pytest run (two conftests currently kept separate) | run-tests | claude | ≤2 wk |
| 4 | Re-vendor if the source session commits its 6-week backlog | propose | claude | ≤4 wk |

## State Snapshot
### Assumptions
- The vendored subtree is a faithful copy of the organ's behaviour — confidence: high (suite re-run at full strength)
- Vendoring a working-tree state (not a commit) is acceptable provenance if recorded — confidence: medium
- The organ's semantics transfer to a 16-department government unchanged — confidence: medium (untested until F5)
### Evidence
| # | Claim | Source | Confidence | Captured |
|---|---|---|---|---|
| 1 | Vendored organ passes 193/193 from the AI_Governor root | `cd aigov/choice && python -m pytest tests/ -q` → 193 passed in 23.55s | high | 2026-08-11 |
| 2 | Committed HEAD carries only 132 tests / 11 files; working tree 193 / 17 | isolated detached `git worktree` at HEAD, run then removed | high | 2026-08-11 |
| 3 | 24 uncommitted entries in Mars_Governance (8 modified, 16 untracked), mtimes 2026-06-27/28 | `git status --short -- Mars_Governance` | high | 2026-08-11 |
| 4 | Source tree unchanged by this run (24 status entries before and after) | `git status` before/after; worktree removed + pruned | high | 2026-08-11 |
<!-- project-state:end:evidence -->
### Unknowns
- Whether the source session intends to commit its 6-week backlog, and whether the vendored copy should then be refreshed
- Whether the organ's single-peakedness domain check transfers to multi-department decisions (not just crop_fraction)
- Whether two conftests can coexist in one pytest run without path interference
### Hypotheses (Active)
| ID | Statement | Status (open/under-investigation/falsified/confirmed) | Last-tested |
|---|---|---|---|
| H1 | The organ vendors with zero test loss | confirmed | 2026-08-11 |
| H2 | The organ's fail-closed escalation generalizes beyond the resource domain to arbitrary department decisions | open | - |
| H3 | The vendored copy stays behaviourally identical to the source under future source changes | open | - |
<!-- project-state:end:hypotheses -->
### Decisions Made
| Decision | Date | Notes |
|---|---|---|
| DV1 — VENDOR, do not path-depend | 2026-08-11 | C3 rejected: depending on the sibling path would couple this project to another session's UNCOMMITTED working tree. Vendoring pins a known-good state and leaves the source untouched (R4). |
| DV2 — Provenance is a working-tree state, recorded not hidden | 2026-08-11 | The vendored copy captures 6 weeks of uncommitted source work. Honest label: "vendored from the Mars_Governance WORKING TREE at 2026-08-11", never "from HEAD". |
| DV3 — Namespace migration (C2) DEFERRED | 2026-08-11 | Rewriting imports during a move risks silent behaviour change; the self-contained-subtree form preserves the suite exactly. Revisit when F5 needs the namespace. |
<!-- project-state:end:decisions-made -->
### Pending Decisions
| Decision | Proposer | Blocker | Notes |
|---|---|---|---|
| Should the 6-week uncommitted Mars_Governance backlog be committed by its owner? | claude | owner/user authority | NOT Soraya's call — a different project's repo. Surfaced as a risk, not acted on. |
| Merge the vendored suite into the root pytest run vs keep separate | claude | none | separate for now; two conftests both insert sys.path |
<!-- project-state:end:pending-decisions -->

## Bellman-Inspired Decision Frame
### Current state (one-line summary)
Organ vendored to `aigov/choice/` (32+ .py files incl. `prototypes/`, initially missed and caught by a collection error); 193/193 from the new root; source tree byte-unchanged; charter C15 flipped PENDING → ENFORCED, raising the measured checkable fraction 0.68 → 0.72.

### Target state / terminal condition
See ## MVP Criteria — vendored organ at full strength plus the C15 binding, with the umbrella carrying the zero-test-loss record.

### Progress proxy
- **MVP bar:** 4 / 4 criteria met (see `## MVP Criteria`) — bar REACHED 2026-08-11
- **v0.1 metric:** `unknowns-retired` count + `gates-passed` count

### Candidate next actions
| # | Action | Class | Expected progress | Expected info gain | Uncertainty | Cost |
|---|---|---|---|---|---|---|
| 1 | Bind ratify() into the kernel decision seam | edit-local-code | high | high | medium | med |
| 2 | Namespace migration to aigov.choice.* | edit-local-code | med | low | medium | med |
| 3 | Merge vendored suite into the root pytest run | run-tests | low | med | low | low |
<!-- project-state:end:candidate-actions -->

### Re-evaluation trigger
- **Default:** re-run `/project-state` after any action class fires
- **Manual override:** `/project-state aigov-collective-choice`

## Allowed Action Classes (v0.2 placeholder — not enforced in v0.1)
- `propose` · `research` · `write-plan` · `edit-local-code` (requires approval) · `run-tests` · `ask-user` · `stop`

## Action Log
| # | Date | Action class | Description | Outcome |
|---|---|---|---|---|
| 1 | 2026-08-11 | propose | /project-init protocol executed by hand (family seed, --advance spillover) | ledger created; self-init 5/25 |
| 2 | 2026-08-11 | edit-local-code | Vendored governance/models/sandbox/tests/docs/results into aigov/choice/ | first pass MISSED prototypes/ — 14 collection errors, ModuleNotFoundError: prototypes |
| 3 | 2026-08-11 | edit-local-code | Vendored the missing prototypes/ package | 193 passed in 23.32s from the new root |
| 4 | 2026-08-11 | run-tests | Isolated detached git worktree at HEAD to separate committed from working-tree state | HEAD = 132 tests / 11 files; working tree = 193 / 17; worktree removed + pruned |
| 5 | 2026-08-11 | edit-local-code | Flipped charter C15 PENDING -> ENFORCED; added fail_safe_gate to IMPLEMENTED_INVARIANTS | checkable fraction 0.68 -> 0.72; pin updated with reason |
| 6 | 2026-08-11 | run-tests | Rewrote test_pending_is_not_counted_as_enforcement to test the MECHANISM not the inventory | it had hard-coded C15 and broke when C15 landed; 89 root + 193 organ = 282 green |
<!-- project-state:end:action-log -->

## Open Questions for User
- **Risk surfaced, not acted on:** `Space_Reflectors_Project/Mars_Governance` has ~6 weeks of uncommitted governance work (24 entries; 61 tests' worth). That is a different project's repo and committing it is not Soraya's call. The vendored copy in `aigov/choice/` now incidentally preserves that state.
- MVP bar is PROPOSED under the execute-mode exception, not confirmed.

## Last Evaluation (v0.2 placeholder — not enforced in v0.1)
- **Date:** 2026-08-11
- **Progress signal:** bar reached 4/4; H1 confirmed; 2 unknowns retired (vendoring fidelity, committed-vs-working provenance); 1 earlier project claim corrected (the "132 is stale" claim)
