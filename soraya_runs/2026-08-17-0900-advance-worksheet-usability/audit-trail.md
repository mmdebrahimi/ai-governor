# Audit trail — 2026-08-17-0900-advance-worksheet-usability

| # | step | gate | outcome |
|---|---|---|---|
| 1 | lock / run dir / `advance_ranker.rank` | auto | 1 eligible family |
| 2 | **Session board consulted before any plateau call** | auto | only `AI_Governor` row is this session's own — no foreign owner |
| 3 | Read the candidate-actions table | auto | **action #1 already done** — stale table driving the ranker |
| 4 | Read `Goal Hierarchy → Short-term` | auto | stale in the same way |
| 5 | Dependency check | auto | repo is stdlib-only (no requirements.txt / pyproject); py3.11.5 → `tomllib` available |
| 6 | Record forecast (E1) | auto | predicted: round trip reproduces the inventory on the first attempt |
| 7 | Write `aigov/answers.py` | auto | TOML intake, plain-language keys, in-repo refusal |
| 8 | Wire `--answers` / `--answers-template` / `--allow-answers-inside-repo` | auto | exit 2 on refusal |
| 9 | Write `tests/test_answers.py` | auto | 19 tests, round trip at the centre |
| 10 | **Run them** | auto | **19 passed first attempt** |
| 11 | **Real-surface check (R3):** emit template to a path outside the repo | auto | 646 lines, parses, answers nothing |
| 12 | **Real-surface check:** point `--answers` at an in-repo file | auto | REFUSED, **exit code 2 verified** |
| 13 | **Real-surface check:** run the CLI on a synthetic partial answers file | auto | 3 of 18 answered; E06 → HYBRID with a plain-English rationale; E17 → INTERNALIZE (no market); E01 marked compound → **verdict refused, told to split** |
| 14 | Full suite | auto | **429 passed** (410 → 429), 0 regressions |
| 15 | Score forecast **hit**; refresh both stale tables (direct-Edit + AC9 mirror) | auto | ranker now reads the real next action |
| 16 | 4 × `ce_ledger.append_action`; gitignore `*answers*.toml` | auto | rows 11–14 |
| 17 | Commit; push | irreversible (`reversible=True`) | rollback: `git push --force-with-lease origin <prior-sha>:main` |

## Verify-in-batch findings

Running the real CLI rather than trusting green tests surfaced three behaviours worth recording:

- **The compound refusal fires on the live path.** E01 was marked `one_decision = false` and the
  instrument declined to issue any verdict, telling the user to split it first. A verdict on a
  compound question is meaningless rather than approximate — that rail now demonstrably holds
  end to end, not just in a unit test.
- **The privacy refusal is real, not advisory.** Pointing `--answers` at a file inside the repo
  exits 2 with an actionable message. Checked by LOCATION rather than by `.gitignore`.
- **A freshly emitted template answers nothing.** Every field is commented out, because TOML has
  no "unanswered" scalar and an uncommented blank would be a lie. Pinned by test.

## Forecast

Predicted the round trip would reproduce the inventory on the first attempt — **HIT** (19/19 green
first run). Running calibration: 2 scored, 1 hit, 1 miss, 0.5.

## AC9 note

`### Candidate next actions` and `## Goal Hierarchy` have **no `/project-state` mutation op** (the
skill names `--refresh-goal-hierarchy` as a v0.5 candidate). Both were refreshed by the documented
direct-`Edit` + mirrored `--append-action --class edit-local-code` workaround. Both mirrors landed
(rows 12, 14) — no orphan.

## Named residual (still not diagnosed, third run running)

`resume_state --cwd .` from this root returns an unrelated DNA/FBA checkpoint. Flagged, ignored,
never acted on.
