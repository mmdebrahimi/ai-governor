# Blight-rules provenance record (F15) — every number, its source

Authored 2026-10-27 (run `2026-10-27-1300-until-mvp-farm-twin-decision-loop`). I11 discipline: no
invented numbers anywhere in the decision chain. Implementation: `aigov/blight_rules.py`,
`aigov/farm_observation.py`, `aigov/farm_certifier.py`; pins: `tests/test_blight_rules.py`,
`tests/test_farm_instrument_certifier.py`.

| # | Number / rule | Value as implemented | Source | Tier |
|---|---|---|---|---|
| 1 | Wallin severity table — hour thresholds per band | SV1/2/3/4 at ≥16/19/22/25 h (cool band), ≥13/16/19/22 h (mid), ≥10/13/16/19 h (warm) | WSU TB65E Table 1 ("adapted from IPM WISDOM, 1995"), text-extracted; **cross-checked cell-for-cell against UMaine Bulletin #2418 (Johnson) — identical** | published, two independent sources |
| 2 | Temperature band edges | 45–53 / 54–59 / 60–80 °F | WSU TB65E. **Named variant:** UMaine prints 45–54 / 55–59 / 60–81 °F — a 1°F edge disagreement between published sources; WSU implemented, variant recorded here | published, sources disagree at the edge |
| 3 | Outside-band severity = 0 | <45 °F or >80 °F → SV 0 | UMaine #2418 published worked examples (18 h at 40 °F or 85 °F → 0 SV) | published |
| 4 | Published worked examples (unit-test pins) | 18 h RH≥90% → SV 3 @65 °F, 2 @56 °F, 1 @50 °F, 0 @40/85 °F | UMaine Bulletin #2418 | published |
| 5 | RH threshold for a "humid hour" | ≥ 90% | All sources (Wallin 1962 lineage; "90 percent relative humidity criteria") | published |
| 6 | BLITECAST first-spray trigger | 18 accumulated severity values | Krause, Massie & Hyre 1975 (Plant Disease Reporter 59:95–98, primary citation) via OSU Malheur 1998-22 + WSU TB65E ("7 to 14 days after 18 DSV") + UMaine ("7–10 days after 18") | published (primary paywalled; three concurring secondary) |
| 7 | Accumulation start | 50% crop emergence | Litschmann et al. 2020, JPPR 60(2):440; UMaine NoBlight description concurs | published |
| 8 | Smith Period | 2 consecutive days: min temp ≥10 °C AND ≥11 h RH≥90% each day | Smith 1956 (Plant Pathology 5, primary paywalled) as stated verbatim in the Hutton-supervised GB 2003–2014 Smith Period review (Dancey; Cooke/Skelsey/Birch) | published |
| 9 | Smith near-miss | 10 h instead of 11 on one/both days | same review ("only 10 hours of humidity above 90%") | published |
| 10 | RH sensor error (observation interval) | ±3% RH → severity interval = recount at RH≥87% / RH≥93% | Litschmann et al. 2012, cited in Litschmann et al. 2020 | published error, DERIVED interval |
| 11 | Certifier threshold semantics | treat iff interval-low ≥ 18; don't iff interval-high < 18; else ESCALATE | derivation from #6 + #10 (no new number) | derived |

## Implementation conventions (named, not sourced — they are choices, not claims)

- **Daily aggregation:** a "day" is the calendar-day (UTC) bucket of cached hourly data; the humid
  period is that day's hours with RH ≥ 90% and the table temperature is the mean of exactly those
  hours. The sources describe humid *periods*; daily bucketing is the common operational reading and
  caps hours at 24, which makes UMaine's above-top-bucket continuation formulas unreachable (not
  implemented).
- **Weather source:** open-meteo ERA5 reanalysis hourly RH/temp (the F14 cached spine), not canopy
  sensors. ERA5 grid RH ≠ in-canopy RH — a named fidelity gap for F16's season report, same class as
  the paper-vs-NASA-POWER deviation in F14.

## Measured finding (recorded 2026-10-27, Lelystad 2020 replay — not a rule, an observation)

With the ±3% RH sensor error honestly propagated, the season-end severity estimate is 18 with
interval (−4, 40): **the Blitecast trigger is measurement-limited near its own threshold** on
reanalysis-grade RH. Consequence: the certifier ESCALATEs rather than certifies through much of the
accumulation window — the governed loop surfaces precision, it does not bluff past it. Nominal-run
numbers for context: first-spray date 2020-09-09 (threshold reached exactly at 18), 2 full Smith
Periods (first 2020-07-08) + 5 near-misses in the Fontane-L window. These are replay observations,
not published validations.

## Still open (named)

- The Wallin/BLITECAST **primary texts** (Wallin 1962; Krause et al. 1975) remain paywalled; the
  table rests on two concurring extension publications. Fetch-if-ever-accessible.
- **Damage coupling** (untreated risk → yield loss): no verified published function yet — decides
  whether F16's bar stays yield-denominated (F15 candidate action 4).
- **Spray-interval rules after the first spray** (WSU Table 2 / UMaine Table 2): captured in sources,
  not implemented — season-one scope is the FIRST-spray trigger instrument only.
