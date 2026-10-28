# Farm venture SEASON TWO — decompose + requirements flow-down (2026-10-27)

Soraya decompose run, per the RATIFIED anchor `docs/idea-anchor-prompt-farm-season-two-2026-10-27.md`
(user verbatim 2026-10-27: "ratify the anchor" — all seven forks at their drafted positions, including
the no-farm revision: real sensors + real local weather + VIRTUAL crop, nothing planted).

> **PRIVACY — STANDING (inherited verbatim).** Public repo. Family composition, ages, names, capital
> position, amounts, property holdings and specific locations NEVER enter this file or any other file
> in this repo. The sensor site is recorded as a SHAPE ("a reachable sensor site"), never a location.
> The season-two capital cap EXISTS in-repo as a fact + category list; its NUMBER stays off-repo.

## 0. What season two is (one line)

The season-one brain, fed by REALITY's weather for the first time: one real sensor station streaming
into the validated twin (virtual potato crop on live local weather), the governed loop deciding daily
in shadow mode, scored on what real sensor precision buys over the ERA5 reanalysis baseline.

## 1. Project-family decomposition

| # | Family (slug) | Scope (one line) | Why a distinct family |
|---|---|---|---|
| F17 | `farm-live-sensor-spine` | The live data spine: sensor-station selection (spec+price → money gate), ingestion of real station data + real local forecast/reanalysis weather into the season-one cache format, gap/outage handling | Its falsifier is DATA-quality (completeness, units, divergence vs reanalysis) — independent of any decision logic; it also owns the ONE money action |
| F18 | `farm-virtual-shadow-season` | The live loop: twin grows the virtual crop on live local weather day by day in real time; governed loop (same rules, certifier, kernel) decides daily on the REAL station's observations; decision record accumulates all season | Its falsifier is the governed loop's behavior under REAL measurement error and REAL time (one tick per real day, outages, drift) — season one proved it only on replayed clean history |
| F19 | `farm-season-two-report` | Season-two terminal: scoring (escalation rate at real sensor precision vs ERA5 baseline; sensor-vs-reanalysis divergence; sim-twin parallel-run drift), kill-condition evaluation, real-plot go/no-go for season three | The venture gate holder — same shape as F16 was for season one; keeps scoring independent of the loop that is being scored |

Robots/swarm: OUT of scope (anchor fork 6). Real plot + real crop: season three, gated by F19's
go/no-go (anchor fork 3).

## 2. Requirements flow-down + dependency graph

| Family | Binding requirement | Depends on | Critical-path position | Cheapest next test |
|---|---|---|---|---|
| `farm-live-sensor-spine` | Station must measure the Blitecast/Smith inputs (RH, temp — hourly) at adequate precision; data lands in the F14 cache format so the twin + rules consume it UNCHANGED; the purchase pauses at the money gate with spec+price | F14 (cache format), F15 (which inputs the rules need) — both MET | Gate A | BEFORE any purchase: build the spine against a FREE live source (open-meteo current-conditions for the sensor site's locale) — proves ingestion end-to-end at $0 and sharpens the sensor spec |
| `farm-virtual-shadow-season` | One governed decision per REAL day, all season, surviving outages (recovery budget); zero ungated applications (nothing to actuate, but the refusal chain still runs); parallel twin tick for calibration (anchor fork 7) | `farm-live-sensor-spine` | Gate B | a 7-day live dry-run on the free-source spine: does the daily loop run unattended-by-the-loop (user-attended) for a week with a scoreable record? |
| `farm-season-two-report` | Scoring definitions FROZEN before the season starts (same authored-first contract discipline as F14 §5); kill condition: no scoreable decision record (outage/data loss beyond recovery budget) OR cap breach → pause + re-plan | `farm-virtual-shadow-season` | Gate C — venture terminal | write the scoring contract NOW (it needs no hardware and freezes the bar before any data could tempt it) |

**Critical path:** `Gate A {F17 free-source spine → sensor spec+price → MONEY GATE → station live}` →
`Gate B {F18 live shadow loop}` → `Gate C {F19 report + go/no-go}`. F19's scoring contract is
cross-cutting and can be authored in parallel with Gate A (authored-first discipline).

**Season-one assets transferred unchanged:** `aigov/farm_twin.py` (world), `aigov/blight_rules.py` +
`aigov/farm_observation.py` + `aigov/farm_certifier.py` (instrument), `aigov/kernel.py` (governed
loop), `aigov/farm_weather.py` (cache format = the integration contract F17 targets).

## 3. VOI-ranked first moves

1. **F17: free-source live spine** (high progress + high info, $0) — proves the whole ingestion path
   and quantifies the reanalysis baseline BEFORE any money moves; the sensor purchase then buys a
   measured delta, not a hope.
2. **F19: freeze the scoring contract** (cheap, retires bar-drift risk) — authored-first, parallel.
3. **F17: sensor-station spec + price candidates** → money gate (user decision with a concrete ask).
4. **F18: 7-day dry-run** on the free spine (needs 1).

## 4. `/project-init` seeding

Self-invoked this run (v1.2), announced inline: `farm-live-sensor-spine`, `farm-virtual-shadow-season`,
`farm-season-two-report`. Self-init account after: 15 live / 25 ceiling.

## 5. Terminal condition (season two)

Mechanical assert when F17+F18+F19 meet their recorded MVP criteria AND one complete live season's
decision record exists with the report's three scores + an explicit real-plot go/no-go DRAFTED.
The go/no-go DECISION is the user's (same authority shape as the season-two GO). Kill condition as in
the anchor: unscoreable season (data loss beyond recovery budget) or cap breach → pause + re-plan.
