# Audit trail — 2026-08-31-0900-advance-encode-elicited-answers

| # | step | gate | outcome |
|---|---|---|---|
| 1 | Release stale lock from the banked `--until-mvp` run; open this run | auto | clean |
| 2 | `advance_ranker.rank` | auto | 1 eligible family; top action is user-gated |
| 3 | Read inventory + dossier state | auto | **1 of 24 answered**, 4 of 20 dossiers |
| 4 | Record forecast (E1) | auto | predicted ≥4 decisions answered + ≥1 non-UNDECIDABLE verdict |
| 5–6 | Encode 6 conversationally-given answers | auto | **bash heredoc failed twice on apostrophes** — switched to a written `.py` helper |
| 7 | **Run the inventory** | auto | **1 → 6 answered; FOUR real verdicts.** E19 and E21 **refused as compound** |
| 8–9 | Split E19 → E19a/E19b, E21 → E21a/E21b in the instance module | auto | 24 → 26 decisions, 0 unclassified |
| 10 | Rewrite the answers blocks for the split | auto | via a second `.py` helper |
| 11 | **Re-run and inspect** | auto | **8 verdicts.** See findings |
| 12 | Full suite | auto | **11 failed** — the guard test named all four missing ids in one message |
| 13 | Patch fixture | auto | **430 passed**, 0 regressions |
| 14 | Regenerate docs + docx | auto | 26 decisions |
| 15 | Score forecast **hit** | auto | calibration 0.7 over 5 |
| 16 | Ledger rows; commit; push | irreversible (`reversible=True`) | rollback: `git push --force-with-lease origin <prior-sha>:main` |

## What the instrument derived — first real output on elicited content

| Decision | Verdict | Why |
|---|---|---|
| **E01** jurisdiction screen | **HYBRID** | market cheaper, but turns on how rules got enforced where the family has developed |
| **E02b** will we build on a term of use | **INTERNALIZE** | **no external market — nobody sells a family its own risk appetite** |
| **E14** own instrumentation | **INTERNALIZE** | cheaper to own, *because the capability already exists in-house* |
| **E19a** tree species | **HYBRID** | turns on what the family wants standing there in 30 years |
| **E19b** livestock | **HYBRID** | turns on whether the family wants animals at all |
| **E20** hospitality | **HYBRID** | **it is the family home — an outsider cannot run a business inside it on our terms** |
| **E21a** where the family lives | **INTERNALIZE** | no market; nobody sells you where to live |
| **E21b** tax residence | **INTERNALIZE** | 50,000 to buy against 20,000/yr to hold |

**The compound refusal fired on real user content, twice.** E19 and E21 were both marked
`one_decision = false` from the user's own phrasing, and the instrument declined them a verdict
until split. That is the third historical defect's fix working on live data rather than a fixture.

**The assurance axis showed its independence.** E19a came back
*"permanent... reviewed by someone independent of the person making it. **This one is bought in, so
the reviewer must ALSO be independent of the supplier** — a supplier paid to do the work is not a
check on whether it should happen."* Sourcing and assurance are orthogonal, and the output proves it.

**One coupling question surfaced:** `E01 + E02b`, both turning on *"what we will actually tolerate
losing"*. Answering it yields the first ConfirmedCapability.

## Honest notes

- **Two bash heredocs failed on apostrophes** before I switched to written helper scripts. Wasted
  two steps; the lesson is to write the file rather than pipe prose through a shell.
- **Every number in the encoded answers is an ESTIMATE**, marked as such inline, under the standing
  2026-08-17 ratification. The verdicts inherit that quality.
- The `resume_state` checkpoint still returns unrelated robotics work when queried from this root —
  the same named residual, still not diagnosed, still ignored rather than acted on.
