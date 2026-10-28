# F17 sensor-station spec — candidates for the ONE season-two purchase (2026-10-27)

**Status: PARKED AT THE MONEY GATE.** Nothing here is bought. This doc is the concrete spec+price
the money gate requires; the user approves a specific line item (with a live quoted price) or
declines (fallback: forecast-only season, F17 ledger candidate 3). Prices below are
search/estimate-grade and MUST be re-quoted at purchase time.

## The binding requirement (measured, season one)

At **±3% RH** error the Blitecast trigger becomes an escalation season (interval (−4, 40) around
threshold 18 — `docs/farm_season_report_v1.md`). So the purchase exists to buy **RH accuracy**, and
the spec bar is:

1. **Documented RH accuracy ≤ ±2.5%** across 40–100% RH (the Wallin/Smith operating region is ≥87%);
2. **Hourly (or finer) temp+RH logging with LOCAL programmatic export** (no cloud dependency for the
   decision path — an internet outage must not be a data outage);
3. Outdoor-rated in a **radiation shield** at canopy-ish height; runs unattended for a season;
4. Inside the private season-two cap (number off-repo).

Leaf wetness is OPTIONAL (Blitecast/Smith need RH+temp only); it is a nice-to-have add-on, not spec.

## Candidates

| # | Candidate | RH accuracy (evidence) | Local API (evidence) | Price class (verify at purchase) | Verdict vs spec |
|---|---|---|---|---|---|
| 1 | **Davis Vantage Pro2 (6152) + WeatherLink Live (6100)** | ±2–3% — Davis's published outdoor spec is ±2% on current SHT-generation sensors; a UColorado station page cites ±3% (older generation). CONFIRM the hygrometer spec on the exact quoted unit | YES — documented local API (GitHub `weatherlink-live-local-api`), PyPI client `weatherlink-live-local` reads it with no internet | HIGH (several hundred USD for station + WLL) | **MEETS spec** if the quoted unit's RH spec is ±2%; the reference instrument |
| 2 | **Ecowitt WS69/WS80 array + GW2000/GW3000 gateway** | ±5% per the GW3001 listing (per-array spec UNCONFIRMED — must verify before this candidate is eligible) | Practically yes — gateway serves local JSON (`get_livedata_info`; community clients ecowitt2mqtt/aioecowitt); official doc thin | LOW (~$112 search-confirmed for a GW2002 bundle) | **LIKELY FAILS the RH bar** (±5% is worse than the ±3% that caused the escalation season). Honest role: cheap practice/context station, NOT the precision instrument |
| 3 | **DIY: Sensirion SHT35 in a proper radiation shield + Raspberry Pi logger** | ±1.5% typical (Sensirion datasheet class) — the best RH-per-dollar available | Trivially — we write the logger, it IS the spine | LOW-MED (parts estimate well under candidate 1) | **MEETS the precision bar at low cost**; risk shifts to build quality (weatherproofing, shield quality, unattended reliability) — our labor replaces Davis's engineering |

## DRAFTED recommendation (ratify or redirect at the gate)

**Primary: candidate 1 (Davis VP2 + WeatherLink Live)** — the only option where a season of
unattended canopy-height RH at documented ±2% is someone else's solved engineering problem, which is
exactly what season two is scoring. **If the private cap says no: candidate 3 (SHT35 DIY)** — same
precision class, our reliability risk; the twin's data spine treats either identically.
Candidate 2 is DECLINED as the instrument on the measured RH bar, with a named revival condition: an
Ecowitt array whose per-model documented RH spec is ≤±2.5% re-opens it.

## What happens at purchase (the gate's shape)

1. User names the approved candidate; a live quote (price + exact model numbers) is fetched;
2. The money gate pauses on that concrete number for the user's explicit yes;
3. Post-purchase: stage-2 ingestion (station → `local/weather/livesite_*.csv` through the same
   contract `tests/test_farm_live_spine.py` pins) + a sensor-vs-free-source divergence log from day 1.

Sources: Davis WLL local-API spec + PyPI `weatherlink-live-local`; gpscentral.ca WLL spec sheet;
instrumentchoice.com.au WLL/VP2 listings; sundowner.colorado.edu PAOS station page (±3% cite);
shop.ecowitt.com GW2002/GW3001 listings (price, ±5% RH). Fetched 2026-10-27; all prices stale by design.
