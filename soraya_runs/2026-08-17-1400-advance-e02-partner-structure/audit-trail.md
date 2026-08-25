# Audit trail — 2026-08-17-1400-advance-e02-partner-structure

| # | step | gate | outcome |
|---|---|---|---|
| 1 | lock / run dir / rank | auto | 1 eligible family; 1 of 18 answered |
| 2 | Record 2 forecasts (E1) | auto | f3 treaty-flip, f4 split-is-answerable |
| 3–4 | Search: Canada–Indonesia treaty; Canada BITs with Ethiopia/Laos | auto | Indonesia CEPA signed 24 Sep 2025 with ISDS, ratification expected 2026 |
| 5 | WebFetch Global Affairs FIPA page | auto | wrong page — 2021 model text, no country list |
| 6 | WebFetch travel.gc.ca/destinations/mongolia | auto | **"take normal security precautions"** — lowest level, confirmed |
| 7 | WebFetch trade-agreements index | auto | 301 redirect; followed it rather than guessing |
| 8 | WebFetch travel.gc.ca/destinations/indonesia | auto | **high degree of caution + Papua avoid-non-essential** — my earlier inference was WRONG |
| 9 | WebFetch investment-agreements register | auto | **authoritative list obtained** — see findings |
| 10–13 | Split E02 → E02a/E02b in the instance module | auto | factual/authority seam; `SUSPECTED_COMPOUND_IDS` drops E02, keeps E15 |
| 14 | Verify module loads, phases classified | auto | 19 decisions, 0 UNCLASSIFIED |
| 15 | Patch both test fixtures | auto | **3 failed** |
| 16 | Diagnose | auto | see below — one was the instrument being right |
| 17 | Fix, re-run | auto | 429 passed, 0 regressions |
| 18 | **Inspect the derivation**, correct the bundle, regenerate 3 docx | auto | verified numbers replace estimates |
| 19 | Score forecasts; commit; push | irreversible (`reversible=True`) | rollback: `git push --force-with-lease origin <prior-sha>:main` |

## Verified findings (authoritative: Global Affairs Canada, travel.gc.ca, 2026-08-17)

| Country | Instrument | Status |
|---|---|---|
| Thailand | FIPA | **in force 24 Sep 1998** |
| China | FIPA | in force 1 Oct 2014 |
| Mongolia | FIPA | in force 24 Feb 2017 |
| Vietnam | CPTPP ch.9 ISDS | in force 14 Jan 2019 |
| Malaysia | CPTPP ch.9 ISDS | in force 29 Nov 2022 |
| Indonesia | CEPA investment chapter, ISDS | signed 24 Sep 2025, ratification expected 2026 |
| Laos | — | **none, confirmed** |
| Ethiopia | — | **none, confirmed** |
| Kazakhstan | FIPA | exploratory discussions only |

Three corrections to the earlier bundle, all of which changed a conclusion:

- **Thailand's FIPA is real and dates to 1998.** Drafted as "verify". Thailand therefore has
  *stronger* formal protection than Vietnam or Malaysia, which rely on CPTPP.
- **Indonesia's advisory was inferred wrong** — high caution with Papua at avoid-non-essential, not
  normal precautions. It was flagged unconfirmed in the draft, which is why it got caught.
- **Laos and Ethiopia have no treaty recourse, confirmed absent** rather than merely unfound. That
  is a stronger and worse statement than the draft made.

## The failure worth recording

Patching the fixture for the split produced 3 failures. Two were mine (a stale pinned count, a
literal `[E02]` id). The third was **the instrument being right and my fixture being wrong**: I gave
E02b both TOLERANCE and PARTNER_READ, which bridged two coupling cliques into one component whose
internal pairs were not all affirmed — so `derive_capabilities` correctly refused to confirm ANY
capability. That is the transitive-clustering refusal, one of the three historical defects this
module was rebuilt to prevent, firing on live data.

Fixed by making E02b turn on TOLERANCE only, which is also the semantically correct answer: whether
the family will build on a term-of-use turns on risk appetite, not on how it reads a counterparty.

After the fix the derivation is cleaner than before the split:
`{E02a, E06, E07, E13}` (counterparty judgement) and `{E01, E02b, E10}` (risk tolerance).

## Forecasts

- **f3** — predicted a country would flip from none-found to a real **in-force** treaty. Indonesia
  flipped to *signed, not yet in force*; Thailand's "verify" resolved to in-force. Neither is
  precisely the predicted flip. Scored **partial**, not hit.
- **f4** — predicted the factual half of E02 would be answerable from the bundle without the user.
  Scored **hit**.

Running calibration: 4 scored, 2 hits, 1 miss, 1 partial, 0.625.
