# F17 live-spine recovery budget — derived outage tolerances (2026-10-27)

What a missing hour / missing day COSTS, derived from the rules' own math — not asserted. Constants
live in `aigov/farm_live_weather.py`; the season-level numbers below are DRAFT until F19's frozen
scoring contract adopts or amends them (authored-first discipline: this doc precedes any live season).

## 1. What an outage does to the RULES (hourly cache)

The Wallin daily severity (`aigov/blight_rules.py`) counts consecutive RH≥90% hours and maps the
count to a severity value **SV ∈ [0, 4]** through hour-boundaries spaced **3 hours apart** (e.g.
10/13/16/19 h in the 60–80 °F band; same spacing in every band). Blitecast then ACCUMULATES daily
SVs from 50% emergence against threshold 18 — an accumulated quantity never forgets a bad day.

A missing hour can at worst extend or break one RH≥90 run by one hour, so **k missing hours in a
day shift that day's SV by at most ceil(k/3), capped at 4** (crossing one 3-h boundary per 3 missing
hours; 4 is the table's maximum). This bound is band-independent and does not require knowing the
missing hours' temperature.

| missing hours k | max ΔSV (ceil(k/3), cap 4) | class (`classify_day`) |
|---|---|---|
| 0–2 | ≤ 1 | `ok` — within the noise the ±3% RH sensor error already imposes |
| 3–12 | ≤ 4 | `degraded` — day carried as an SV interval, same recount pattern as the RH-error Estimate |
| 13–24 | > 4 ⇒ cap, info content gone | `unscoreable` — the day's severity is unknowable to within a full max day |

Missing hours are **omitted, never interpolated** (honesty rail: the loop escalates under missing
data exactly as under ambiguity; a fabricated humid hour could manufacture a spray trigger).

## 2. What an outage does to the WORLD (daily cache)

PCSE's daily row wants TMIN/TMAX (extremes — robust to a few missing hours), VAP + WIND (means —
robust), RAIN + IRRAD (SUMS — these under-count linearly with missing hours). With
`MAX_MISSING_HOURS_FOR_DAILY = 4`: extremes/means come from ≥20 of 24 hours; the worst-case sum
under-count is 4/24 ≈ 17% of one day's radiation/rain — small against season totals, and
`DailyDerived.present_hours` records it per day. **Beyond 4 missing hours the day is omitted from
the daily file entirely**: the twin's failed tick on a missing day IS the outage signal F18's
protocol handles (escalate, never fabricate weather).

## 3. Season-level budget (DRAFT — F19's contract freezes the final numbers)

- Each `degraded`/`unscoreable` day adds its ΔSV bound to an **outage-induced interval width**
  W_out on the accumulated severity (the same interval algebra `FarmObservation.accumulated_severity`
  uses for sensor error). The season's decision record stays scoreable while W_out stays small
  against threshold 18.
- **DRAFT kill-condition input:** season unscoreable when **W_out > 8** (two full max days of pure
  outage uncertainty) before the season's treat/don't-treat question resolves, OR when **> 3
  consecutive days** are omitted from the daily file (the twin cannot tick — virtual crop state
  undefined beyond a replayable gap).
- **Backfill asymmetry (recorded, not optional):** free-source gaps can be RETROACTIVELY filled from
  the ERA5 archive once its ~5-day lag passes — reanalysis-grade repair. A real SENSOR's outage is
  NOT fillable by reanalysis without destroying exactly what the sensor was bought to measure
  (local precision vs reanalysis is season two's scored question); a sensor gap may be bridged by
  the free source but the bridged hours are scored as reanalysis-grade, never as sensor hours.

## 4. Where the thresholds live

`aigov/farm_live_weather.py`: `COVERAGE_OK_MAX_MISSING = 2`, `COVERAGE_DEGRADED_MAX_MISSING = 12`,
`MAX_MISSING_HOURS_FOR_DAILY = 4`; pinned by `tests/test_farm_live_spine.py::test_classify_day_thresholds`.
Changing any of them is a logged contract amendment, not a tweak.
