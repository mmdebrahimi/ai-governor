# Audit trail - soraya --advance, 2026-08-12

Gate mode: money-only. Every step classified `auto` by `action_gate` (in-cwd edits, local tests).
Pre-planned ~35 steps; ran ~58 with one self-extension into spillover, noted below.

## Target selection

`advance_ranker` returned all 7 families `eligible`, all `terminal_met`. The `next_action` cells are
stale seeding-era entries ("Draft clause list", which shipped as C01-C38), so code owned eligibility
and the fine-grained pick was model judgment - as the honesty rail requires.

Picked the `decisions.py` remediation: the only place in the repo with a CONFIRMED defect producing
wrong answers right now, with a 4-item sequence already ratified by the prior `/brainstorm`, and
nothing about it gated.

| # | Step | Outcome |
|---|---|---|
| 1 | Lock + run dir | acquired |
| 2 | `advance_ranker` | 7 eligible, 0 blocked, 0 degraded |
| 3 | Classify batch through `action_gate` | 7/7 `auto` |
| 4 | Rewrite the derivation section of `aigov/decisions.py` | affirmed-pair grouping + completeness rail |
| 5 | Rewrite `tests/test_decisions.py` | deleted `test_clustering_is_transitive`, added the refusal guard |
| 6 | Caught my own vacuous assertion | `... or True` in a test I had just written - fixed |
| 7 | Run on the defect scenario | FIXTURE WRONG (Coase direction backwards); corrected, re-ran |
| 8 | Mutation proof | completeness check disabled -> 2 tests RED; restored byte-identical |
| 9 | Spillover -> item 5 (assurance) | `reversibility` finally drives a verdict |
| 10 | Spillover -> item 7 (atomicity) | a compound decision now gets NO verdict |
| 11 | Protocol doc rewritten | fact kinds, coupling question, assurance, atomicity, withdrawn insight |
| 12 | Full suites | 383 root / 193 organ, 0 regressions |

## Self-extension (auditable, not silent)

Estimated ~35 steps for items 1-4. On finishing them the terminal checklist did not hold - items 5
and 7 were adjacent, reversible, ungated and high-VOI - so the run continued into them under the
spillover default, ending near 58 steps. Well inside the ~100-step self-budget.

## Two of my own errors this run

1. A test assertion ending `... or True`, which made it vacuous - exactly the "green on words, not
   behaviour" failure. Caught by reading what I wrote, not by the suite.
2. The verification fixture had internal cost 20000 against external 6000, making every decision
   MARKET, so the first real run proved nothing. SECOND time this session I have had the Coase
   direction backwards. Corrected; the re-run is what actually demonstrated the fix.

## Judgment call recorded

Item 6 (decision specificity, advisory-only) was DROPPED rather than built. An elicited field that
feeds no verdict is the precise defect shape already found twice in this module -
`private_information` before HYBRID existed, `reversibility` before assurance did. Adding a third
deliberately, and labelling it advisory, would be repeating a known mistake.

## Terminal

Item 8 (coverage lenses) is blocked on a criterion the two-seat panel found insufficient earlier in
this session. The remaining frontier is the user-bound inventory session and a design problem that
just failed review and needs fresh thinking, not another reflexive pass.

**terminal_reason:** decisions.py frontier exhausted of code-closable work; remainder is
user-input-bound or needs a redesign that should not be attempted reflexively.
**budget_verdict:** within self-budget (~58 of ~100).
