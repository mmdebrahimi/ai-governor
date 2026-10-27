"""F15 observation layer: the decision loop reads ESTIMATES, never truth.

The F14 world serves truth (its own state); a real farm serves SENSOR READINGS. This layer turns the
cached hourly weather (``data/farm_twin/weather/<site>_hourly_rh.csv``, open-meteo ERA5) into
``Estimate`` values (``aigov.twin.Estimate``: value + method + error bar) so every number entering
the governed decision carries HOW it was measured and how wrong it could be.

Error-bar provenance (derived, not invented): capacitive RH sensors carry about ±3% RH error even
well-calibrated (Litschmann et al. 2012, as cited in Litschmann et al. 2020, JPPR 60(2)) — and the
blight rules THRESHOLD on RH (>= 90%), so the honest interval on any hours-count or severity total
is obtained by RECOUNTING at RH >= 87% and RH >= 93%. The interval is the recount spread; no error
number is invented for temperature (named limitation: the interval covers RH-threshold sensitivity
only).
"""

from __future__ import annotations

import csv
import datetime
from collections import defaultdict
from pathlib import Path

from .blight_rules import (
    BLITECAST_SEVERITY_THRESHOLD,
    HourlyWeather,
    daily_severity,
)
from .farm_weather import default_weather_dir
from .twin import Estimate

RH_SENSOR_ERROR_PCT = 3.0  # Litschmann et al. 2012 via Litschmann et al. 2020 (±3% RH)


class TruthReadRefused(TypeError):
    """Raised when the decision loop is handed a bare number where an Estimate is required."""


def _require_estimate(value, name: str) -> Estimate:
    if not isinstance(value, Estimate):
        raise TruthReadRefused(
            f"{name} must be an Estimate (method + error bar), got {type(value).__name__}: "
            f"a bare number is a truth-read and the decision loop refuses it"
        )
    return value


class FarmObservation:
    """Estimate-wrapped reads over one site's cached hourly weather. Offline; cache-missing raises."""

    def __init__(self, site: str, weather_dir: Path | None = None):
        self.site = site
        path = (weather_dir or default_weather_dir()) / f"{site}_hourly_rh.csv"
        if not path.exists():
            raise FileNotFoundError(
                f"hourly weather cache missing: {path} (build with `python -m aigov.farm_weather`)"
            )
        self._by_day: dict[datetime.date, list[HourlyWeather]] = defaultdict(list)
        with path.open(encoding="utf-8") as fh:
            next(fh)  # provenance comment line
            for row in csv.DictReader(fh):
                t = datetime.datetime.fromisoformat(row["time_utc"])
                self._by_day[t.date()].append(
                    HourlyWeather(
                        time=t,
                        rh_pct=float(row["relative_humidity_2m_pct"]),
                        temp_c=float(row["temperature_2m_c"]),
                    )
                )

    # ------------------------------------------------------------------ reads

    def hours(self, day: datetime.date) -> list[HourlyWeather]:
        if day not in self._by_day:
            raise KeyError(f"no cached hours for {self.site} on {day}")
        return self._by_day[day]

    def accumulated_severity(
        self,
        emergence_50pct: datetime.date,
        through: datetime.date,
    ) -> Estimate:
        """Blitecast severity total from 50% emergence through ``through``, as an Estimate.

        value  = total with the published RH >= 90% threshold;
        interval = recounts at RH >= 93% (low bound) and RH >= 87% (high bound) — the ±3% RH sensor
        error pushed through the threshold, the only error source this layer claims to cover.
        """
        totals = {}
        for thr in (90.0, 93.0, 87.0):
            totals[thr] = sum(
                daily_severity(self._by_day[d], rh_threshold=thr)
                for d in sorted(self._by_day)
                if emergence_50pct <= d <= through
            )
        value = float(totals[90.0])
        lo, hi = float(totals[93.0]), float(totals[87.0])
        # rel_error chosen so Estimate.interval covers the WIDER recount deviation.
        spread = max(value - lo, hi - value, 0.0)
        rel = spread / value if value > 0 else (1.0 if spread > 0 else 0.0)
        return Estimate(
            name=f"blitecast_accumulated_severity[{self.site}]",
            value=value,
            method=(
                f"Wallin daily SV over ERA5 hourly RH/temp, summed {emergence_50pct}..{through}; "
                f"interval = recount at RH>=93/87 (±{RH_SENSOR_ERROR_PCT:.0f}% RH sensor error, "
                f"Litschmann 2012/2020); temp error NOT covered (named limitation)"
            ),
            rel_error=rel,
        )


def rule_decision_from_estimate(acc: Estimate, threshold: int = BLITECAST_SEVERITY_THRESHOLD) -> str:
    """What the published rule says, given a MEASURED severity total: 'treat' / 'dont-treat' /
    'ambiguous' (the error bar straddles the published threshold — no honest binary exists)."""
    acc = _require_estimate(acc, "accumulated severity")
    lo, hi = acc.interval
    if lo >= threshold:
        return "treat"
    if hi < threshold:
        return "dont-treat"
    return "ambiguous"
