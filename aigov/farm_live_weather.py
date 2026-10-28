"""F17 live sensor-data spine, stage 1 (free source, $0).

Pulls REAL recent weather for the off-repo sensor site from open-meteo (no key, no cost) and writes
it in EXACTLY the two season-one cache formats (``aigov.farm_weather``), so the validated twin
(PCSE ``CSVWeatherDataProvider``) and the blight rules (``FarmObservation``) consume live data
UNCHANGED. Stage 2 (the physical station, money-gated) will feed the same two files.

Spine policies (decided 2026-10-27, F17 ledger):

- **Actuals only.** ``end`` defaults to *yesterday* (UTC): forecast rows are never written to the
  cache — the governed loop decides on observed weather, and PCSE must never grow a crop on a
  forecast that later changes.
- **Off-repo output.** The live site's caches carry coordinates (the PCSE header needs them), so
  they live under the gitignored ``local/weather/`` — never under the committed ``data/`` tree.
  SHAPE-only key ``livesite`` names the files (privacy rail).
- **Null hours are OMITTED, counted, and classified** — never interpolated, never fabricated
  (honesty rail: the loop escalates under missing data exactly as under ambiguity). A day missing
  more than ``MAX_MISSING_HOURS_FOR_DAILY`` hours is omitted from the DAILY file entirely: the
  twin's failed tick on that day IS the outage signal F18 handles.
- Derivations are provenanced: VAP via Tetens over hourly dew point; 10 m -> 2 m wind via the
  FAO-56 log-profile factor 0.748; IRRAD = sum of hourly shortwave radiation (W/m^2 avg -> J/m^2/h).

Day-coverage classification (derived in ``docs/farm_live_spine_recovery_budget.md``):
``ok`` (<= 2 missing hours) / ``degraded`` (3-12) / ``unscoreable`` (> 12).
"""

from __future__ import annotations

import csv
import datetime as _dt
import math
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from .farm_site_config import LIVE_SITE_KEY, SiteConfig

#: FAO-56 wind log-profile conversion, 10 m measurement height -> 2 m (u2 = u10 * 4.87/ln(67.8*10-5.42)).
WIND_10M_TO_2M = 0.748

#: A day missing more than this many hours is omitted from the DAILY cache (outage day).
MAX_MISSING_HOURS_FOR_DAILY = 4

#: Day-coverage classes for the hourly (rules) cache - thresholds derived in the recovery-budget doc.
COVERAGE_OK_MAX_MISSING = 2
COVERAGE_DEGRADED_MAX_MISSING = 12

_HOURLY_VARS = (
    "relative_humidity_2m,temperature_2m,dew_point_2m,precipitation,"
    "shortwave_radiation,wind_speed_10m"
)

#: open-meteo forecast API serves roughly the last 92 days; cut over to the ERA5 archive before that
#: (with margin). The archive lags ~5 days behind real time, so recent days MUST come from forecast.
_FORECAST_PAST_LIMIT_DAYS = 80


def default_live_weather_dir(repo_root: Path | None = None) -> Path:
    root = repo_root if repo_root is not None else Path(__file__).resolve().parent.parent
    return root / "local" / "weather"


# --------------------------------------------------------------------------- pure derivations


def vap_hpa_from_dewpoint_c(dewpoint_c: float) -> float:
    """Actual vapour pressure (hPa) from dew point via Tetens (as used for PCSE VAP)."""
    return 6.108 * math.exp(17.27 * dewpoint_c / (dewpoint_c + 237.3))


def wind2m_from_10m(wind10_ms: float) -> float:
    return wind10_ms * WIND_10M_TO_2M


def classify_day(missing_hours: int) -> str:
    """Day-coverage class for the rules cache (see recovery-budget doc for the derivation)."""
    if missing_hours <= COVERAGE_OK_MAX_MISSING:
        return "ok"
    if missing_hours <= COVERAGE_DEGRADED_MAX_MISSING:
        return "degraded"
    return "unscoreable"


@dataclass
class DailyDerived:
    day: _dt.date
    irrad_kj: float
    tmin_c: float
    tmax_c: float
    vap_kpa: float
    wind2m_ms: float
    rain_mm: float
    present_hours: int


@dataclass
class LiveSpineReport:
    site_key: str
    start: _dt.date
    end: _dt.date
    hourly_rows_written: int
    missing_hours_total: int
    daily_rows_written: int
    days_omitted: list[str] = field(default_factory=list)
    day_coverage: dict[str, str] = field(default_factory=dict)
    sources: list[str] = field(default_factory=list)


def derive_daily(hours_by_day: dict[_dt.date, list[dict]]) -> list[DailyDerived]:
    """Derive PCSE daily rows from present hourly records; omit days too degraded to summarize."""
    out: list[DailyDerived] = []
    for day in sorted(hours_by_day):
        rows = [r for r in hours_by_day[day] if _complete(r)]
        if 24 - len(rows) > MAX_MISSING_HOURS_FOR_DAILY:
            continue
        temps = [r["temperature_2m"] for r in rows]
        vap_hpa = sum(vap_hpa_from_dewpoint_c(r["dew_point_2m"]) for r in rows) / len(rows)
        out.append(
            DailyDerived(
                day=day,
                # shortwave_radiation is the hour's mean W/m^2 -> J/m^2/h = *3600; sum -> J/m^2/d -> /1000 kJ
                irrad_kj=sum(r["shortwave_radiation"] * 3600.0 for r in rows) / 1000.0,
                tmin_c=min(temps),
                tmax_c=max(temps),
                vap_kpa=vap_hpa / 10.0,
                wind2m_ms=wind2m_from_10m(sum(r["wind_speed_10m"] for r in rows) / len(rows)),
                rain_mm=sum(r["precipitation"] for r in rows),
                present_hours=len(rows),
            )
        )
    return out


def _complete(r: dict) -> bool:
    return all(
        r.get(k) is not None
        for k in (
            "relative_humidity_2m",
            "temperature_2m",
            "dew_point_2m",
            "precipitation",
            "shortwave_radiation",
            "wind_speed_10m",
        )
    )


# --------------------------------------------------------------------------- cache writers

_DAILY_HEADER = """## Site Characteristics
Country     = 'n/a'
Station     = '{station}'
Description = 'F17 live spine cache (actuals only - forecast rows never written)'
Source      = 'open-meteo ({sources}) fetched {fetched} - derivations per aigov/farm_live_weather.py'
Contact     = 'n/a'
Longitude = {lon}; Latitude = {lat}; Elevation = {elev}; AngstromA = 0.25; AngstromB = 0.5; HasSunshine = False
## Daily weather observations (missing values are NaN)
"""


def write_daily_csv(
    path: Path, station: str, lat: float, lon: float, elev: float, rows: list[DailyDerived], sources: str
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        fh.write(
            _DAILY_HEADER.format(
                station=station, sources=sources, fetched=_dt.date.today().isoformat(),
                lon=lon, lat=lat, elev=elev,
            )
        )
        fh.write("DAY,IRRAD,TMIN,TMAX,VAP,WIND,RAIN,SNOWDEPTH\n")
        for r in rows:
            fh.write(
                "{day},{irrad:.1f},{tmin:.2f},{tmax:.2f},{vap:.3f},{wind:.2f},{rain:.2f},NaN\n".format(
                    day=r.day.strftime("%Y%m%d"), irrad=r.irrad_kj, tmin=r.tmin_c, tmax=r.tmax_c,
                    vap=r.vap_kpa, wind=r.wind2m_ms, rain=r.rain_mm,
                )
            )


def write_hourly_csv(path: Path, station: str, rows: list[tuple[str, float, float]], sources: str) -> None:
    """Same shape FarmObservation reads: one provenance line, then time_utc/rh/temp. Null hours omitted."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        fh.write(
            f"# F17 live spine ({station}), open-meteo ({sources}), actuals only, "
            f"fetched {_dt.date.today().isoformat()}, UTC; null hours omitted (never interpolated)\n"
        )
        writer = csv.writer(fh)
        writer.writerow(["time_utc", "relative_humidity_2m_pct", "temperature_2m_c"])
        writer.writerows(rows)


# --------------------------------------------------------------------------- fetch + build


def _fetch_hourly(lat: float, lon: float, start: _dt.date, end: _dt.date) -> tuple[list[dict], float, list[str]]:
    """Fetch hourly records [start, end] as a list of dicts with a 'time' key. Network."""
    import requests

    today = _dt.date.today()
    spans: list[tuple[str, _dt.date, _dt.date]] = []
    cutover = today - _dt.timedelta(days=_FORECAST_PAST_LIMIT_DAYS)
    if start < cutover:
        spans.append(("archive", start, min(end, cutover - _dt.timedelta(days=1))))
    if end >= cutover:
        spans.append(("forecast", max(start, cutover), end))

    records: list[dict] = []
    elevation = float("nan")
    sources: list[str] = []
    for kind, s, e in spans:
        url = (
            "https://archive-api.open-meteo.com/v1/archive"
            if kind == "archive"
            else "https://api.open-meteo.com/v1/forecast"
        )
        resp = requests.get(
            url,
            params={
                "latitude": lat, "longitude": lon,
                "start_date": s.isoformat(), "end_date": e.isoformat(),
                "hourly": _HOURLY_VARS, "timezone": "UTC",
            },
            timeout=120,
        )
        resp.raise_for_status()
        payload = resp.json()
        elevation = float(payload.get("elevation", elevation))
        hourly = payload["hourly"]
        keys = [k for k in hourly if k != "time"]
        for i, t in enumerate(hourly["time"]):
            records.append({"time": t, **{k: hourly[k][i] for k in keys}})
        sources.append(f"{kind} {s}..{e}")
    return records, elevation, sources


def build_live_caches(
    cfg: SiteConfig,
    start: _dt.date,
    end: _dt.date | None = None,
    weather_dir: Path | None = None,
) -> LiveSpineReport:
    """Fetch actuals for [start, end] and write BOTH season-one-format caches. Network.

    ``end`` defaults to YESTERDAY (UTC) - today is still accumulating and forecast rows are policy-
    excluded. Idempotent by construction: each run rewrites the full requested window from source.
    """
    end = end if end is not None else _dt.date.today() - _dt.timedelta(days=1)
    if end >= _dt.date.today():
        raise ValueError("live cache carries ACTUALS only: end must be before today (UTC)")
    weather_dir = weather_dir if weather_dir is not None else default_live_weather_dir()

    records, elevation, sources = _fetch_hourly(cfg.latitude, cfg.longitude, start, end)
    src = " + ".join(sources)  # no ';' — PCSE's header parser splits on it

    hours_by_day: dict[_dt.date, list[dict]] = defaultdict(list)
    hourly_rows: list[tuple[str, float, float]] = []
    missing = 0
    for r in records:
        day = _dt.datetime.fromisoformat(r["time"]).date()
        hours_by_day[day].append(r)
        if r.get("relative_humidity_2m") is None or r.get("temperature_2m") is None:
            missing += 1
        else:
            hourly_rows.append((r["time"], r["relative_humidity_2m"], r["temperature_2m"]))

    daily = derive_daily(hours_by_day)
    site = cfg.site_key or LIVE_SITE_KEY
    write_daily_csv(
        weather_dir / f"{site}_daily.csv", site, cfg.latitude, cfg.longitude, elevation, daily, src
    )
    write_hourly_csv(weather_dir / f"{site}_hourly_rh.csv", site, hourly_rows, src)

    written_days = {d.day for d in daily}
    coverage = {
        day.isoformat(): classify_day(
            24 - sum(1 for r in hours_by_day[day]
                     if r.get("relative_humidity_2m") is not None and r.get("temperature_2m") is not None)
        )
        for day in sorted(hours_by_day)
    }
    return LiveSpineReport(
        site_key=site, start=start, end=end,
        hourly_rows_written=len(hourly_rows), missing_hours_total=missing,
        daily_rows_written=len(daily),
        days_omitted=[d.isoformat() for d in sorted(hours_by_day) if d not in written_days],
        day_coverage=coverage, sources=sources,
    )


if __name__ == "__main__":
    from .farm_site_config import load_site_config

    cfg = load_site_config()
    report = build_live_caches(cfg, start=_dt.date.today() - _dt.timedelta(days=14))
    print(report)
