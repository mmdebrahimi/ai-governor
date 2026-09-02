# Result — total tax + two buildings

Directive: `/soraya do it` — execute the three recommendations from `gate-change-2026-09.md`.

## What was executed

| # | Recommendation | Status |
|---|---|---|
| 1 | Run the total-tax comparison | **DONE** — model built, defect found, re-run, 4 sensitivities |
| 2 | Check the two-buildings rule (Uruguay + Chile) | **DONE** — both researched, plus Spain as the constraint case |
| 3 | Surface the coupling question | **SURFACED** — needs one sentence from the user; not answerable by me |

## Findings

**Uruguay costs ~1/4 of Chile in lifetime tax, and wins in every scenario tested (3.8x-5.3x).**
Base case USD 2.089M holding / USD 300k foreign income / 20 yrs: Uruguay 359,000 vs Chile 1,767,199.

**My forecast f6 was WRONG and is scored MISS.** I predicted annual land tax would reorder the top
two. It did not: Uruguay was already first and stayed first (no flip), and the mechanism was
falsified — income tax drove the gap 6:1 over land tax (1,206,000 vs 202,199). The driver is
holiday length (Chile 3-6 yrs vs Uruguay 11) and the rate after it (~30% worldwide vs 12% on
foreign capital income only).

**Chile's inheritance tax is the largest single unmodelled line** — up to 25%, USD 522,250 on this
holding, against Uruguay's zero. Material for an enterprise built to pass to the next generation.

**Two buildings: permitted in both**, same shape — family dwelling easy, guest building gated.
Uruguay's Colonia local plan expressly allows 2 dwelling units per plot plus tourist uses.
**Spain (Andalucía) is the real constraint**: one dwelling per rural plot, 1% footprint cap.

## Defect found and fixed mid-run

The first model run showed **Chile cheaper than Uruguay**. Chile's post-holiday foreign-income rate
was left at 0.0, silently granting a permanent exemption. Fixing it inverted the answer. Caught by
inspecting the numbers against the caveats rather than reporting the exit-0 output.

Second presentation defect: the UAE row ranked first at USD 0, which is meaningless — the UAE
cannot hold farmland. Excluded from the ranking with the reason printed inline.

## Calibration

f6 scored MISS. Ledger now n=6, hit-rate 0.58 (was 0.70).
**`research`-class forecasts sit at 0.25 over 2 samples** — a visible tendency to over-predict that
research will overturn a ranking. Below MIN_SAMPLE, so directional only.

## Open

- Coupling question: do E01 and E02b need the same decision-maker? (user, one sentence)
- Is the family's foreign income **earned or passive**? Moves Uruguay's income line to zero if earned.
- Chile's article 7-bis surcharge is unmodelled — Chile is understated.
- Canadian departure tax unmodelled (owed regardless of destination, so ranking-neutral).

## Artifacts

- `D:\land_enterprise_private\total_tax_model.py`
- `D:\land_enterprise_private\total-tax-and-two-buildings-2026-09.md`
- `D:\land_enterprise_private\total-tax-and-two-buildings-2026-09_Bombardier.docx`
