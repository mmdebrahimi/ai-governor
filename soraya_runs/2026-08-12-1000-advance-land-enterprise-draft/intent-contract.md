# Intent contract — 2026-08-12-1000-advance-land-enterprise-draft

**Mode:** `/soraya --advance` (no explicit caps; dynamic self-budget)
**Invoked from:** `C:\Users\Farshad\PythonProjects\scientific_research`
**Bound to project root:** `C:\Users\Farshad\PythonProjects\Skill_Development\AI_Governor`
(the invoking cwd holds no `project_state/`, so every AC9 write would have parked there)

**Umbrella:** `project_state/aigov.md`
**Eligibility gate** (`scripts/advance_ranker.py`) returned exactly one eligible family:

| family | eligibility | bucket | blocked_by | terminal_met |
|---|---|---|---|---|
| `aigov-land-enterprise` | eligible | high | — | unknown |

The Mars families F0–F12 are FROZEN by user decision of 2026-08-12 and were not candidates.

**Picked action:** candidate #1 — *"Run the decision-inventory session, Claude drafting the
candidate list for the user to correct"* (`ask-user`, high progress, highest info gain).

**Split of the action.** The elicitation itself is the user's and cannot be executed for them.
The DRAFTING half is Soraya's and is what this run performs, so the session becomes correction
rather than composition.

**Standing constraints honored:**
- PRIVACY — public repo (`github.com/mmdebrahimi/ai-governor`): shapes only, roles-as-slots, no
  jurisdiction / amount / holding / person. Machine-scanned before commit.
- NO INVENTED NUMBERS — every elicited field left unanswered rather than drafted. The instrument
  exists to refuse exactly the guesses a drafter would be tempted to supply.
- NO PROPOSED STRUCTURE — the list is flat; grouping is computed from affirmed couplings only.

**Planned step estimate:** ~14. **Actual:** 17 (one self-corrected run-dir misplacement, one
added `--candidate-list` mode).

**Gates encountered:** none. No money, no destructive-local, no genuinely-irreversible-outward
action was reached. `git push` classified `irreversible` + `reversible=True` → ran un-gated under
the money-only default with a rollback note recorded.
