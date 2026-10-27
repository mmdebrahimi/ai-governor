"""F15 MVP criterion 1: the spray-decision rules reproduce PUBLISHED values.

Anchors (full provenance: ``docs/blight_rules_provenance.md``):
- Wallin severity table: WSU TB65E Table 1 (IPM WISDOM 1995), cross-checked against UMaine
  Bulletin #2418 — hour thresholds identical in both.
- Published worked examples (UMaine #2418): an 18-hour RH>=90% period yields SV 3 at 65°F,
  2 at 56°F, 1 at 50°F, and 0 at 40°F or 85°F.
- BLITECAST: first spray at 18 accumulated SV (Krause/Massie/Hyre 1975 via OSU Malheur 1998-22,
  WSU TB65E); accumulation starts at 50% emergence (Litschmann et al. 2020).
- Smith Period (Smith 1956, via the Hutton-supervised GB 2003-2014 review): 2 consecutive days,
  min temp >= 10°C, >= 11 h RH >= 90% each day; near miss at 10 h.
"""

import datetime

import pytest

from aigov.blight_rules import (
    BLITECAST_SEVERITY_THRESHOLD,
    HourlyWeather,
    SmithDay,
    blitecast_first_spray_date,
    c_to_f,
    daily_severity,
    smith_day,
    smith_periods,
    wallin_severity,
)

D = datetime.date
T = lambda d, h: datetime.datetime(d.year, d.month, d.day, h)  # noqa: E731


# ------------------------------------------------------------------ Wallin table

@pytest.mark.parametrize(
    "temp_f,expected", [(65, 3), (56, 2), (50, 1), (40, 0), (85, 0)],
    ids=["65F", "56F", "50F", "40F", "85F"],
)
def test_published_umaine_examples_18h(temp_f, expected):
    assert wallin_severity(temp_f, 18) == expected


@pytest.mark.parametrize(
    "temp_f,cells",
    [
        # WSU TB65E Table 1: (hours, expected SV) at each bucket boundary.
        (50, [(15, 0), (16, 1), (18, 1), (19, 2), (21, 2), (22, 3), (24, 3), (25, 4), (27, 4)]),
        (57, [(12, 0), (13, 1), (15, 1), (16, 2), (18, 2), (19, 3), (21, 3), (22, 4), (24, 4)]),
        (70, [(9, 0), (10, 1), (12, 1), (13, 2), (15, 2), (16, 3), (18, 3), (19, 4), (21, 4)]),
    ],
    ids=["45-53F", "54-59F", "60-80F"],
)
def test_wallin_table_bucket_boundaries(temp_f, cells):
    for hours, expected in cells:
        assert wallin_severity(temp_f, hours) == expected, (temp_f, hours)


def test_outside_bands_is_zero_severity():
    for temp_f in (40.0, 44.9, 80.1, 85.0):
        assert wallin_severity(temp_f, 24) == 0


def test_daily_severity_uses_avg_temp_of_humid_hours_only():
    # 18 humid hours at 18.3°C (65°F) + 6 dry freezing hours: the dry hours must not drag the
    # band down — published example says SV 3.
    day = D(2020, 7, 1)
    hours = [HourlyWeather(T(day, h), 95.0, 18.3) for h in range(18)]
    hours += [HourlyWeather(T(day, 18 + h), 50.0, -5.0) for h in range(6)]
    assert daily_severity(hours) == 3
    assert round(c_to_f(18.3)) == 65


# ------------------------------------------------------------------ BLITECAST accumulation

def test_blitecast_triggers_at_18_and_not_before():
    em = D(2020, 5, 22)
    days = [(em + datetime.timedelta(days=i), 2) for i in range(9)]  # 2 SV/day -> 18 on day 9
    dt, total = blitecast_first_spray_date(days, em)
    assert dt == em + datetime.timedelta(days=8)
    assert total == BLITECAST_SEVERITY_THRESHOLD
    dt_short, total_short = blitecast_first_spray_date(days[:-1], em)
    assert dt_short is None and total_short == 16


def test_blitecast_ignores_severity_before_50pct_emergence():
    em = D(2020, 5, 22)
    before = [(em - datetime.timedelta(days=i), 4) for i in range(1, 6)]  # 20 SV pre-emergence
    dt, total = blitecast_first_spray_date(before, em)
    assert dt is None and total == 0


# ------------------------------------------------------------------ Smith Period

def _smith(dates_temps_hours):
    return [SmithDay(d, t, h) for d, t, h in dates_temps_hours]


def test_full_smith_period_detected():
    days = _smith([(D(2020, 7, 8), 11.0, 12), (D(2020, 7, 9), 10.0, 11)])
    periods = smith_periods(days)
    assert len(periods) == 1 and periods[0].full and periods[0].start == D(2020, 7, 8)


def test_near_miss_at_10_hours():
    days = _smith([(D(2020, 7, 8), 11.0, 10), (D(2020, 7, 9), 12.0, 11)])
    periods = smith_periods(days)
    assert len(periods) == 1 and not periods[0].full


@pytest.mark.parametrize(
    "days",
    [
        [(D(2020, 7, 8), 9.9, 12), (D(2020, 7, 9), 12.0, 12)],   # temp floor broken
        [(D(2020, 7, 8), 11.0, 9), (D(2020, 7, 9), 12.0, 12)],   # below near-miss hours
        [(D(2020, 7, 8), 11.0, 12), (D(2020, 7, 10), 12.0, 12)],  # not consecutive
    ],
    ids=["cold-day", "too-few-hours", "gap-day"],
)
def test_no_smith_period(days):
    assert smith_periods(_smith(days)) == []


def test_smith_day_reduction():
    day = D(2020, 7, 8)
    hours = [HourlyWeather(T(day, h), 95.0 if h < 11 else 60.0, 10.0 + h * 0.1) for h in range(24)]
    sd = smith_day(day, hours)
    assert sd.rh90_hours == 11
    assert sd.min_temp_c == 10.0


# ------------------------------------------------------------------ real cached season (structural)

def test_rules_run_on_the_cached_reference_season():
    # Structural only — no published per-season classification exists to pin against, so no yield
    # of this test is a fidelity claim. It pins: the cache feeds the rules end-to-end, severity is
    # a valid SV every day, and accumulation is monotone.
    from aigov.farm_observation import FarmObservation

    obs = FarmObservation("lelystad")
    em, end = D(2020, 5, 22), D(2020, 9, 23)
    days = [d for d in sorted(obs._by_day) if em <= d <= end]
    assert len(days) > 100
    svs = [daily_severity(obs.hours(d)) for d in days]
    assert all(sv in (0, 1, 2, 3, 4) for sv in svs)
    totals = [sum(svs[: i + 1]) for i in range(len(svs))]
    assert totals == sorted(totals)
