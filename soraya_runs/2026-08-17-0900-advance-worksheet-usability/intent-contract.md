# Intent contract — 2026-08-17-0900-advance-worksheet-usability

**Mode:** `/soraya --advance`, bound to the `AI_Governor` project root (invoking cwd has no `project_state/`).
**Eligibility gate:** 1 eligible family — `aigov-land-enterprise`. Mars F0–F12 frozen.
**Session board (R4/B):** the only row naming `AI_Governor` is this same session's own. No foreign
owner, no handoff owed, no collision risk.

**What the gate surfaced.** The ranker returned candidate action #1 — *"Run the decision-inventory
session, Claude drafting the candidate list"* — which was COMPLETED five days ago. The table was
stale, so every future `--advance` would keep picking finished work. Downstream, action #3
("encode the corrected list as DecisionRecords") named a capability that did not exist: there was
no path from the user's answers back into the instrument.

**Picked work (two things, both reversible):**
1. Build the answers-intake path — the missing half of the inventory.
2. Refresh the two stale planning tables so the ranker points at reality.

**Planned estimate:** ~14 steps. **Actual:** 17.

**Standing constraints honored:** the repo is PUBLIC, so the intake is designed to keep answers
OUT of it — `load_answers` refuses an in-repo path by location (not by `.gitignore`, which is one
`git add -f` from meaning nothing). No jurisdiction, amount or person written anywhere.

**Gates:** none hit. No money, no destructive-local, no genuinely-irreversible-outward action.
