# F18 virtual-shadow season protocol (2026-10-27)

How season two's live loop runs, frozen before it runs. Companion to
`docs/farm_live_spine_recovery_budget.md` (outage tolerances) and the F19 scoring contract (to be
frozen before the live season). Code: `aigov/farm_shadow_season.py`.

## Cadence and the decided day

One tick per real day. A tick decides **yesterday** (the last complete UTC day): refresh the F17
caches (actuals only) → accumulate Blitecast severity from the season anchor date as an Estimate
(±3% RH recount interval) → propose the nominal action (treat iff value ≥ 18) → gate it through the
SAME `farm_fail_safe_gate` the replayed season used → append one `TickRecord`. **Nothing actuates in
season two** — every verdict is recommend-and-log.

A missed tick costs nothing but that day's latency: severity is recomputed from the cache each tick
(restart-safe by recomputation — resolves the F18 state-store unknown: rules recompute, no
checkpoint; in the live season the twin re-simulates from planting each tick, ~11 s at day 125 in
season one, hypothesis H1 of the F18 ledger watches that number live). Records are idempotent by
date; the record file under off-repo `local/shadow_season/` is the only state.

## Outage behavior (inherits the derived recovery budget)

Day coverage classes from `classify_day`: ok ≤2 / degraded 3–12 / unscoreable >12 missing hours. A
day wholly absent from the cache goes through the certifier as `None` and returns the escalate
verdict — missing data is never interpolated, and a free-source gap may be backfilled from the ERA5
archive after its ~5-day lag (reanalysis-grade; sensor gaps are NOT sensor data when bridged).

## Dry-run (winter 2026/27) — MVP criterion 3

≥ 7 consecutive real days of live ticks on the free-source spine (no crop grows in winter, so the
twin does not tick; the loop's season anchor is the dry-run start date). Deliverable:
`docs/farm_shadow_dryrun_report.md` — tick count, verdict/coverage histograms (`season_summary`),
gaps and latencies observed, and any contract surprises. The dry-run is a rehearsal: its verdicts
are not scored against the F19 contract.

## Live season (~Apr–Sep 2027)

- **Virtual planting** on a public agronomic rule for the locale's climate zone (rule in-repo,
  locale parameters from the off-repo config); 50% emergence per the season-one EMERGENCE_DAYS
  handling. The anchor date for severity accumulation is 50% emergence (Blitecast convention,
  season one).
- **The twin joins the loop**: PCSE grows the virtual crop on the live daily cache in lockstep
  (re-simulated from planting each tick), serving the governed loop's constraint probe exactly as in
  the replayed season.
- **Three arms, side by side, every day** (the F19 scoring subjects): governed-precision (interval
  semantics, escalates on straddle), governed-nominal (point value), ERA5-baseline (same rules on
  reanalysis data for the same locale — quantifies what the sensor bought). Plus the calendar and
  never-treat reference counters from season one.
- **Stage-2 sensor data** (post money-gate) replaces/augments the free source through the unchanged
  cache contract, with a daily sensor-vs-reanalysis divergence log from day one.

## Known fidelity question (named, not papered over)

The Wallin table's integer-°F bands leave gaps at band edges (e.g. 53.6 °F falls between the 45–53
and 54–59 rows and scores 0 — found by this protocol's own test fixtures). Season one computed the
same way, so comparisons are internally consistent; whether the PUBLISHED table intends contiguous
bands (rounding vs half-open intervals) is an F19 contract question to resolve against the primary
sources (WSU TB65E / UMaine #2418) BEFORE the live season scores real days near band edges.
