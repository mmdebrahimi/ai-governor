# Farm Season Report v1 — one governed replayed season (F16, Gate C)

Authored 2026-10-27, run `2026-10-27-1500-until-mvp-farm-governed-season`. Reproducible:
`aigov/farm_season.py::run_governed_season("Fontane", "lelystad", 2020)` — deterministic (pinned by
`tests/test_farm_governed_season.py::test_season_is_deterministic`).

> **PRIVACY — STANDING.** Public repo; public agronomic replay; no instance data.

## What was run

The full composition, day by day over the ratified reference season (Fontane @ Lelystad NL, 2020;
125 season days from 50% emergence 2020-05-22 to final harvest 2020-09-23):

- **World:** F14's `FarmTwin` (PCSE/WOFOST81 potential-production potato, validated ±10%/±20%
  contract — see `docs/farm_twin_world_spec.md` §5).
- **Decision loop:** F15's ratified instrument — Blitecast threshold-18 (certified), Smith Period
  (reported diagnostic) — over Estimate-wrapped ERA5 observations.
- **Kernel:** UNCHANGED `aigov.kernel.Governor`; every application through
  propose → ratify → certify → apply. The ratification seam is a **SIMULATED conventional-practice
  assembly** (a replay has no live family assembly — named, not hidden); self-referring ratifiers
  are still refused.
- **Cadence:** on-change proposals (design note in `aigov/farm_season.py` — resolves the F16
  ledger unknown), plus one on-the-record escalation when the rule nominally triggers under an
  ambiguous measurement.

## Season results (measured in THIS replay — not outcome claims)

| Arm | Sprays | Protection start | Protected days | Ambiguous days | Kernel escalations | Kernel refusals | Ungated applications | Unprotected full Smith Periods |
|---|---|---|---|---|---|---|---|---|
| governed-precision (honest ±3% RH error bars) | 0 | — | 0 | 61 | 1 (2020-09-09) | 0 | **0** | 2 |
| governed-nominal (sensitivity: sensor error → 0) | 1 | 2020-09-09 | 15 | 0 | 0 | 0 | **0** | 2 |
| calendar (weekly from emergence — convention) | 18 | 2020-05-22 | 125 | — | — | — | — | 0 |
| never-treat | 0 | — | 0 | — | — | — | — | 2 |

Season context: nominal Blitecast accumulation reached 18 on **2020-09-09** (exactly threshold at
season end: 18); **2 full Smith Periods** (first 2020-07-08) + 5 near-misses — the two rules
disagree by two months on this season, which is why the rule choice was a ratified decision, not a
default. Final tuber yield (model-coherent PP ceiling, identical across arms by construction —
there is NO disease in the world model): **18,589 kg/ha dry**.

## Findings

1. **The governed chain holds end-to-end: zero ungated applications across both governed arms**
   (H1 CONFIRMED). The one applied spray carries a ratification record + CERTIFY verdict; the one
   escalation is on the kernel record with its reason; 8 named adversarial attacks
   (`tests/test_adversarial_farm_instrument.py`) all end in detection, escalation, or refusal —
   including self-ratification, withheld-spray steering, premature-spray steering, truth-read
   injection, and the unbound-world fail-closed case.
2. **Honest error bars dominate this season's decisions.** With the published ±3% RH sensor error
   propagated, 61 of 125 days are measurement-ambiguous against the threshold and the loop's one
   kernel event is an ESCALATE to the accountable human — the governed system SURFACES precision
   instead of bluffing past it. Taken at nominal face value (how the published rule is operated in
   practice), the same chain certifies and applies exactly one spray, on the published trigger date.
3. **Spray economy (direction consistent with published validations):** governed-nominal used
   **1 spray vs the calendar arm's 18** on this dry season. Published Blitecast validations report
   25–70% spray reductions with yield preserved (Brazil, Ciência Rural lineage; F15 evidence row 3);
   2020 Lelystad was a low-pressure season, so the extreme reduction is plausible in direction and
   NOT generalizable as a number.
4. **H2 ("governed beats never-treat, ≈ matches calendar") is PARTIALLY evaluable in v1.** In
   risk-coverage terms: governed-nominal left 2 full Smith Periods unprotected (same as never-treat
   — both July periods precede the September Blitecast trigger) and the calendar arm left none. In
   yield terms the question is UNANSWERABLE in v1 — the PP world has no disease, so yield cannot
   separate the arms (labelled model-coherent-only per the F16 ledger's empirical-concerns flag).
   H2 verdict deferred to report v2 (see §registered-arm).

## Registered follow-on (cannot evaporate)

- **Arm (planned):** `van Oijen dynamic LAI damage coupling` on criterion "season-report-v2
  yield-denominated comparison" — the published mechanism (yield loss fully explained by green-LAI
  reduction; senescence ≤15%) exists; the exact functional form is paywalled.
- **Constraint (R9):** `van-oijen-coupling-paywall` — expiry: full text of van Oijen 1991/1992
  obtained. Until it lifts, yield columns stay model-coherent-only.
- Also out of v1 scope (named): post-first-spray interval rules (WSU/UMaine Table 2 — captured in
  `docs/blight_rules_provenance.md`); in-canopy vs ERA5 RH fidelity.

## Kill-condition evaluation (milestone 5 — written verdict, decompose doc §5)

**Condition:** the venture FREEZES (and F13 row-46's hobby decision is re-instated via R9) if
(a) the governed replay cannot reproduce the reference season within the F14 validation contract
after the bounded recovery budget, OR (b) fidelity requires authoring agronomy in-house. Capital
cap: $0 in season one.

**Verdict: NOT TRIPPED.**
(a) The F14 contract was met on the first validation run, inside bands, no recovery budget spent
(6/6 gating combos; Layer-1 worst +7.6% of ±10%; Layer-2 worst −7.4% of ±20%).
(b) No agronomy was authored in-house: the world is PCSE/WOFOST (external), the rules are
transcribed published tables/criteria pinned to published examples, the one coupling that WOULD
need in-house authorship was instead **deferred and registered** behind its paywall constraint —
the rail held precisely by refusing to improvise.
Capital spent in season one: **$0** (zero money-gated actions across all four runs — decompose,
F14, F15, F16; audit trails in `soraya_runs/`).

## The decision this report feeds (USER authority — recorded, not taken)

**Season-two go/no-go** (dirt, hardware, sensors, orchestration over bought machines) is the
user's call, gated on this report. The report's sharpest operational input: at reanalysis-grade RH
precision the governed loop escalates rather than decides through much of the season — **sensor
quality is the first real-world budget question**, because it is what converts escalations into
certified decisions.
