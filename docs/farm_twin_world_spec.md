# Farm-Twin World Spec (F14) — PCSE/WOFOST potato world + validation contract

Authored 2026-10-27, **before the first validation run** (contract-first discipline, per
`aigov/choice/docs/resource_sim_spec.md` pattern). Soraya run
`2026-10-27-1100-until-mvp-farm-twin-world`.

> **PRIVACY — STANDING.** Public repo. The reference region-season below is a PUBLIC agronomic choice
> (published field trials), not a statement about where anything will be bought or operated.

## 1. What the world is

The F14 world model is **PCSE 6.0.13 / WOFOST 8.1 potential-production potato** (`Wofost81_PP`),
wrapped as a day-steppable twin. The independent-author rail holds end-to-end:

- **Engine + parameters:** PCSE ships the potato parameter sets calibrated in **ten Den, van de Wiel,
  de Wit, van Evert, van Ittersum & Reidsma (2022), "Modelling potential potato yields: Accounting for
  experimental differences in modern cultivars", European Journal of Agronomy 137:126510**
  (de Wit authors PCSE itself). Verified by running, not assumed: the shipped `Fontane` variety carries
  the paper's calibrated `TSUMEM = 255 °Cd` and the paper's introduced `REALLOC_*` reallocation
  parameters, and all five trial cultivars (`Innovator`, `Fontane`, `Markies`, `Premiere`, `Festien`)
  are present in `YAMLCropDataProvider(model=Wofost81_PP)`.
- **Scope honesty (inherited D7):** `Wofost81_PP` simulates POTENTIAL growth — no water, nutrient,
  pest or disease limitation. TWSO is a model-coherent ceiling, never an outcome claim. Late blight is
  NOT in this model; the venture's twin is a COMPOSITION (this growth world + weather-driven risk rules
  + damage coupling, F15's surface).

## 2. Reference region-season (pending decision 1 — resolved, draft-then-ratify)

**Chosen: the ten Den et al. 2022 trial site-seasons** — Lelystad, NL (52.52°N, 5.47°E, clay) and
Vredepeel, NL (51.54°N, 5.88°E, sand), seasons 2019 and 2020, near-potential treatment (optimal
irrigation + fertilisation arm).

Why this beats the earlier draft ("a regional yield statistic"): a regional average is
management-limited and incomparable to a PP simulation, while these are **published field-measured
yields under near-potential management for the exact cultivars the engine ships** — same cultivar,
same site, same season, with the paper's own simulated values alongside. Public criteria only. The
region is also late-blight country (satisfies Gate B's need for a blight-relevant climate), and NASA
POWER + open-meteo both cover the coordinates.

### Agromanagement derivation (public, from the paper)

| Site-year | Planting | Crop start (emergence) | Crop end (final harvest) |
|---|---|---|---|
| Lelystad 2019 | 25/04/2019 | planting + Table-5 interval | 02/10/2019 |
| Lelystad 2020 | 20/04/2020 | planting + Table-5 interval | 23/09/2020 |
| Vredepeel 2019 | 18/04/2019 | planting + Table-5 interval | 25/09/2019 |
| Vredepeel 2020 | **24/04/2020** (inference, see below) | planting + Table-5 interval | 24/09/2020 |

Emergence intervals (paper Table 5, 2020; days planting→80% emergence): Premiere 29, Innovator 31,
Fontane V 31, Fontane L 32, Markies 32, Festien 28. For 2019 the same per-cultivar intervals are used
(the paper reports the 2019 range as 28–33 days; per-cultivar 2019 dates are not tabulated in the
main text). Crop end type = harvest at the final destructive-harvest date (Table 3); max_duration 250.

**Named data defect (documented inference):** the paper's Table 1 prints Vredepeel 2020 planting as
`24/09/2020`, which is impossible (the FINAL harvest was 24/09/2020 and every other planting is
mid-to-late April). Treated as a 04↔09 digit swap → **24/04/2020**. Sensitivity: a ±1-week planting
error shifts PP final yield by a few percent; the Layer-1 band (±10%) absorbs it, and the replay
report states Vredepeel-2020 results carry this caveat.

### Weather deviation (named)

The paper used on-farm stations + KNMI (irradiation: Lelystad Airport / Volkel). The replay uses
**NASA POWER** (daily, agroclimatology) — a deliberate substitution so the data spine is globally
reusable. This is the main source of reproduction error and is priced into the Layer-1 band.
Hourly RH for Gate B's Smith-Period rules comes from **open-meteo archive** (ERA5) — cached, not used
by this growth world.

## 3. Data spine (milestone 2)

- `data/farm_twin/weather/` holds the cached season weather as PCSE-readable CSV exported once from
  NASA POWER (daily, both sites, 2019+2020) and open-meteo (hourly RH, both sites, 2019+2020).
- Re-runs load the repo cache (no network). The validation test fails LOUDLY if the cache is missing
  and cannot be rebuilt — never a silent skip.
- Provenance header in each CSV: source, coordinates, fetch date, variable mapping.

## 4. Twin disciplines (milestone 3)

`FarmTwin` (new module `aigov/farm_twin.py`) wraps the PCSE season and honors the three ColonyTwin
disciplines, adapted:

1. **Coverage** — `check_state_coverage` / `check_reverse_coverage` between the twin's declared state
   vector (DVS, LAI, TWSO, TAGP, day) and what the wrapper actually exposes; a declared-but-unreadable
   or readable-but-undeclared variable is a test failure.
2. **Observability-enforced reads** — every read goes through the twin's `read(name)`: DIRECT state
   returns the value; anything not in the declared observable set is REFUSED (raises), never silently
   served. (The Estimate-wrapped sensor layer with error bars is F15's surface — this world exposes
   truth; F15 degrades it.)
3. **Per-tick physical bounds** — each `tick()` asserts: DVS non-decreasing; TWSO non-decreasing;
   LAI within (0, 10); daily TWSO increment within a published-plausible envelope (≤ 400 kg DM/ha/day;
   generous ceiling above reported NL maxima) — a violation halts the twin (bounds are tripwires, not
   clamps).

## 5. Validation contract (milestone 4) — FROZEN BEFORE FIRST RUN

**Replay set (gating):** the **2020 season** (the paper's calibration year), all six cultivar-site
combos — Lelystad: Innovator, Fontane L, Markies; Vredepeel: Premiere, Fontane V, Festien — PP mode,
NASA POWER weather, agromanagement per §2.

**Published anchors (ten Den 2022, Table 6; final tuber yield, t/ha DRY):**

| Combo | Observed ± sd | Paper-simulated |
|---|---|---|
| Premiere (V) | 18.3 ± 1.16 | 17.2 |
| Innovator (L) | 16.1 ± 1.40 | 16.0 |
| Fontane L | 18.2 ± 0.94 | 17.5 |
| Fontane V | 19.1 ± 1.97 | 17.6 |
| Markies (L) | 16.4 ± 1.03 | 15.5 |
| Festien (V) | 18.0 ± 1.85 | 16.5 |

**Layer 1 — Reproduction (gating):** for every 2020 combo,
`|sim_TWSO − paper_sim| / paper_sim ≤ 0.10`.
Rationale: same engine lineage + same parameter sets; the residual is the weather substitution (NASA
POWER vs on-farm/KNMI) + agromanagement approximation. ±10% is the house band (resource_sim pattern).

**Layer 2 — Fidelity (gating):** for every 2020 combo,
`|sim_TWSO − observed| / observed ≤ 0.20`.
Rationale: the paper's own 2020 errors run 0.3–8.5%; ±20% adds the weather + setup margin on top of
the worst case. Band width stated here, before any validation run.

**2019 replay (reported, NOT gating):** same six combos against Table 9 (Premiere 15.3 obs/17.7 sim;
Innovator 14.7/17.9; Fontane L 16.5/18.3; Fontane V 21.3/18.5; Markies 16.0/16.4; Festien 18.3/17.6).
The paper itself drifts to −15.3% in this evaluation year, so it tests generalization, not wrapper
correctness; numbers are recorded in the replay report either way.

**Sanity anchors (context, non-gating):** NL ware potato actual average ≈ 51.3 t/ha FRESH; NL
potential ≈ 72 t/ha FRESH (Silva et al. 2017, cited in ten Den 2022). At Fontane's measured DM% of
22.5 (paper, 2020), a PP sim of ~17.5 t/ha dry ≈ 78 t/ha fresh — above actual, near published
potential, as a potential-mode output must be.

**Verdict discipline:** the contract evaluates to a recorded verdict either way. A Layer-1 failure
means the wrapped engine is NOT reproducing its published source (wrapper/setup defect — fix and
re-run, each diagnosis spending a recovery attempt). A Layer-1 pass + Layer-2 failure is a FIDELITY
finding recorded in the ledger — the bar fails honestly; no band widening after the fact (any band
change is a user-ratified contract amendment, logged as a Decision).

## 6. MVP criteria mapping

| Criterion | This spec |
|---|---|
| Smoke green | pre-existing (`tests/test_farm_twin_smoke.py`) |
| Spec exists | this document |
| Validation contract evaluated | `tests/test_farm_twin_validation.py` implements §5 verbatim |
