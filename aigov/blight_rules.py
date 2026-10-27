"""F15 published spray-decision rules for potato late blight. ZERO invented numbers (I11).

Every threshold in this module is transcribed from a published source and pinned by
``tests/test_blight_rules.py``; the number-by-number provenance record is
``docs/blight_rules_provenance.md``.

Two rule families:

1. **Wallin severity values + BLITECAST first-spray trigger** (Wallin 1962; Krause, Massie & Hyre
   1975, Plant Disease Reporter 59:95-98). Daily "disease severity values" (SV 0-4) from hours of
   relative humidity >= 90% and the average temperature during those hours; accumulation starts at
   50% crop emergence; late blight is forecast — and the first protectant spray recommended — once
   the running total reaches 18. The SV table is transcribed from WSU TB65E (IPM WISDOM 1995),
   cross-checked cell-for-cell against UMaine Bulletin #2418 (hour thresholds identical; the two
   sources' temperature band EDGES differ by 1°F — the WSU edges are implemented, the variant is
   recorded in the provenance doc).
2. **Smith Period** (L.P. Smith, 1956, refining the Beaumont criteria): two consecutive days where
   the minimum temperature does not fall below 10°C AND each day has at least 11 hours with relative
   humidity >= 90%. A "near miss" = the two-day shape holds but one or both days reach only 10 such
   hours. Definition as stated in the Hutton-supervised GB 2003-2014 Smith Period review (Dancey).

Scope honesty: these are RISK-FORECAST rules, not a disease model. WOFOST (the F14 world) grows the
crop; these rules read the same replayed weather and flag spray-decision days. The damage coupling
(untreated risk -> yield loss) is NOT here — it is F15/F16's named open question.
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import Iterable, Sequence

# --------------------------------------------------------------------------------------
# Wallin severity-value table (WSU TB65E Table 1, "adapted from IPM WISDOM, 1995")
# --------------------------------------------------------------------------------------

#: Temperature bands in °F (WSU edges; UMaine prints 45-54 / 55-59 / 60-81 — same hour cells).
#: Outside every band (below 45°F or above 80°F) the severity is 0 — pinned by UMaine's published
#: examples (18 h of RH>=90% at 40°F or 85°F accumulates 0 SV).
#: Each band maps to the MINIMUM hours of RH>=90% needed for SV 1, 2, 3, 4. Hours at or below the
#: SV-1 minimum minus one give 0 ("<15 hrs scores 0" per UMaine; the WSU 0-column prints 15/12/9
#: as the top of the zero bucket).
WALLIN_TABLE_F = (
    # (temp_lo_f, temp_hi_f, (min hours for SV1, SV2, SV3, SV4))
    (45.0, 53.0, (16, 19, 22, 25)),
    (54.0, 59.0, (13, 16, 19, 22)),
    (60.0, 80.0, (10, 13, 16, 19)),
)

#: BLITECAST: late blight forecast + first protectant spray once accumulated SV reaches this.
BLITECAST_SEVERITY_THRESHOLD = 18

#: Accumulation starts at 50% crop emergence (Litschmann et al. 2020; UMaine NoBlight description).
BLITECAST_ACCUMULATION_START = "50% crop emergence"

RH_THRESHOLD_PCT = 90.0


def c_to_f(temp_c: float) -> float:
    return temp_c * 9.0 / 5.0 + 32.0


def wallin_severity(avg_temp_f: float, rh90_hours: float) -> int:
    """Severity value (0-4) for ONE day: hours of RH>=90% and the avg temp during those hours."""
    for lo, hi, mins in WALLIN_TABLE_F:
        if lo <= avg_temp_f <= hi:
            sv = 0
            for level, min_hours in enumerate(mins, start=1):
                if rh90_hours >= min_hours:
                    sv = level
            return sv
    return 0  # outside every band (UMaine examples: 40°F -> 0, 85°F -> 0)


@dataclass(frozen=True)
class HourlyWeather:
    """One hour: UTC timestamp, relative humidity (%), temperature (°C)."""

    time: datetime.datetime
    rh_pct: float
    temp_c: float


def daily_severity(hours: Sequence[HourlyWeather], rh_threshold: float = RH_THRESHOLD_PCT) -> int:
    """Wallin SV for one calendar day of hourly weather.

    Convention (implementation, not source): a 'day' is the calendar-day bucket of the supplied
    hours; the humid period is the set of hours with RH >= threshold and the temperature entering
    the table is the mean °C of exactly those hours, converted to °F. With 24-hour days the
    above-top-bucket continuation formulas (UMaine) are unreachable and are not implemented.
    """
    humid = [h for h in hours if h.rh_pct >= rh_threshold]
    if not humid:
        return 0
    avg_temp_f = c_to_f(sum(h.temp_c for h in humid) / len(humid))
    return wallin_severity(avg_temp_f, len(humid))


def blitecast_first_spray_date(
    days: Iterable[tuple[datetime.date, int]],
    emergence_50pct: datetime.date,
    threshold: int = BLITECAST_SEVERITY_THRESHOLD,
):
    """First date the accumulated SV (from 50% emergence, inclusive) reaches ``threshold``.

    ``days`` is (date, daily severity value), any order. Returns (date | None, final_total).
    """
    total = 0
    for day, sv in sorted(days):
        if day < emergence_50pct:
            continue
        total += int(sv)
        if total >= threshold:
            return day, total
    return None, total


# --------------------------------------------------------------------------------------
# Smith Period (Smith 1956)
# --------------------------------------------------------------------------------------

SMITH_MIN_TEMP_C = 10.0
SMITH_RH_HOURS_FULL = 11
SMITH_RH_HOURS_NEAR_MISS = 10


@dataclass(frozen=True)
class SmithDay:
    date: datetime.date
    min_temp_c: float
    rh90_hours: int


@dataclass(frozen=True)
class SmithPeriod:
    start: datetime.date       # first of the two consecutive days
    full: bool                 # True = full Smith Period; False = near miss


def smith_day(date: datetime.date, hours: Sequence[HourlyWeather],
              rh_threshold: float = RH_THRESHOLD_PCT) -> SmithDay:
    """Reduce one calendar day of hourly weather to the two Smith quantities."""
    if not hours:
        raise ValueError(f"no hourly weather supplied for {date}")
    return SmithDay(
        date=date,
        min_temp_c=min(h.temp_c for h in hours),
        rh90_hours=sum(1 for h in hours if h.rh_pct >= rh_threshold),
    )


def smith_periods(days: Sequence[SmithDay]) -> list[SmithPeriod]:
    """All (full + near-miss) Smith Periods in a date-ordered day sequence.

    Full: two CONSECUTIVE days, each with min temp >= 10°C and >= 11 h of RH >= 90%.
    Near miss: both days clear the temperature floor and >= 10 h, but at least one day is below 11 h
    (the review's "one or both ... has only 10 hours" allowance).
    """
    out = []
    ordered = sorted(days, key=lambda d: d.date)
    for a, b in zip(ordered, ordered[1:]):
        if (b.date - a.date).days != 1:
            continue
        if a.min_temp_c < SMITH_MIN_TEMP_C or b.min_temp_c < SMITH_MIN_TEMP_C:
            continue
        if a.rh90_hours >= SMITH_RH_HOURS_FULL and b.rh90_hours >= SMITH_RH_HOURS_FULL:
            out.append(SmithPeriod(start=a.date, full=True))
        elif a.rh90_hours >= SMITH_RH_HOURS_NEAR_MISS and b.rh90_hours >= SMITH_RH_HOURS_NEAR_MISS:
            out.append(SmithPeriod(start=a.date, full=False))
    return out
