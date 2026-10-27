"""F14 farm-twin data spine: repo-owned weather cache for the reference region-season.

Builds and loads the cached season weather named in ``docs/farm_twin_world_spec.md`` §3:

- Daily meteorology per trial site (NASA POWER agroclimatology), exported ONCE to a PCSE-readable
  CSV under ``data/farm_twin/weather/`` so every later run is offline and byte-stable.
- Hourly relative humidity + temperature per site (open-meteo ERA5 archive), cached as plain CSV —
  Gate B's Smith-Period inputs; NOT consumed by the growth world.

Provenance is written into each file's header. A loader that finds no cache raises — a missing data
spine must never degrade into a silent re-download inside a test that claims to be offline.
"""

from __future__ import annotations

import csv
import datetime as _dt
from pathlib import Path

#: The ten Den et al. 2022 trial sites (public coordinates, spec §2).
SITES = {
    "lelystad": {"lat": 52.52, "lon": 5.47},
    "vredepeel": {"lat": 51.54, "lon": 5.88},
}

YEARS = (2019, 2020)

_PCSE_CSV_HEADER = """## Site Characteristics
Country     = 'Netherlands'
Station     = '{station}'
Description = 'NASA POWER agroclimatology replay cache for the ten Den et al. 2022 trial site'
Source      = 'power.larc.nasa.gov via pcse.input.NASAPowerWeatherDataProvider (fetched {fetched})'
Contact     = 'n/a (public data)'
Longitude = {lon}; Latitude = {lat}; Elevation = {elev}; AngstromA = {anga}; AngstromB = {angb}; HasSunshine = False
## Daily weather observations (missing values are NaN)
"""


def default_weather_dir(repo_root: Path | None = None) -> Path:
    root = repo_root if repo_root is not None else Path(__file__).resolve().parent.parent
    return root / "data" / "farm_twin" / "weather"


def _daily_csv_path(weather_dir: Path, site: str) -> Path:
    return weather_dir / f"{site}_daily.csv"


def _hourly_csv_path(weather_dir: Path, site: str) -> Path:
    return weather_dir / f"{site}_hourly_rh.csv"


def build_daily_cache(site: str, weather_dir: Path, years=YEARS) -> Path:
    """Fetch NASA POWER once for ``site`` and export the given years as a PCSE CSV. Network."""
    from pcse.input import NASAPowerWeatherDataProvider

    coords = SITES[site]
    wdp = NASAPowerWeatherDataProvider(latitude=coords["lat"], longitude=coords["lon"])
    records = [
        r
        for r in wdp.export()
        if r["DAY"].year in years
    ]
    if not records:
        raise RuntimeError(f"NASA POWER returned no records for {site} in {years}")

    weather_dir.mkdir(parents=True, exist_ok=True)
    out = _daily_csv_path(weather_dir, site)
    header = _PCSE_CSV_HEADER.format(
        station=site,
        fetched=_dt.date.today().isoformat(),
        lon=coords["lon"],
        lat=coords["lat"],
        elev=wdp.elevation,
        anga=getattr(wdp, "angstA", 0.25),
        angb=getattr(wdp, "angstB", 0.5),
    )
    with out.open("w", newline="", encoding="utf-8") as fh:
        fh.write(header)
        fh.write("DAY,IRRAD,TMIN,TMAX,VAP,WIND,RAIN,SNOWDEPTH\n")
        for r in sorted(records, key=lambda x: x["DAY"]):
            # PCSE-internal -> CSV units: IRRAD J/m2/d -> kJ; VAP hPa -> kPa; RAIN cm -> mm.
            fh.write(
                "{day},{irrad:.1f},{tmin:.2f},{tmax:.2f},{vap:.3f},{wind:.2f},{rain:.2f},NaN\n".format(
                    day=r["DAY"].strftime("%Y%m%d"),
                    irrad=r["IRRAD"] / 1000.0,
                    tmin=r["TMIN"],
                    tmax=r["TMAX"],
                    vap=r["VAP"] / 10.0,
                    wind=r["WIND"],
                    rain=r["RAIN"] * 10.0,
                )
            )
    return out


def build_hourly_rh_cache(site: str, weather_dir: Path, years=YEARS) -> Path:
    """Fetch open-meteo ERA5 hourly RH + temperature for the site-years. Network."""
    import requests

    coords = SITES[site]
    weather_dir.mkdir(parents=True, exist_ok=True)
    out = _hourly_csv_path(weather_dir, site)
    rows: list[tuple[str, float, float]] = []
    for year in years:
        resp = requests.get(
            "https://archive-api.open-meteo.com/v1/archive",
            params={
                "latitude": coords["lat"],
                "longitude": coords["lon"],
                "start_date": f"{year}-01-01",
                "end_date": f"{year}-12-31",
                "hourly": "relative_humidity_2m,temperature_2m",
                "timezone": "UTC",
            },
            timeout=120,
        )
        resp.raise_for_status()
        payload = resp.json()["hourly"]
        rows.extend(zip(payload["time"], payload["relative_humidity_2m"], payload["temperature_2m"]))
    with out.open("w", newline="", encoding="utf-8") as fh:
        fh.write(
            f"# open-meteo ERA5 archive, {site} ({coords['lat']},{coords['lon']}), "
            f"years {years}, fetched {_dt.date.today().isoformat()}, UTC\n"
        )
        writer = csv.writer(fh)
        writer.writerow(["time_utc", "relative_humidity_2m_pct", "temperature_2m_c"])
        writer.writerows(rows)
    return out


def build_all(weather_dir: Path | None = None) -> list[Path]:
    weather_dir = weather_dir if weather_dir is not None else default_weather_dir()
    built = []
    for site in SITES:
        built.append(build_daily_cache(site, weather_dir))
        built.append(build_hourly_rh_cache(site, weather_dir))
    return built


def load_daily_weather(site: str, weather_dir: Path | None = None):
    """Load the cached PCSE weather for ``site``. Offline; raises if the cache is absent."""
    from pcse.input import CSVWeatherDataProvider

    weather_dir = weather_dir if weather_dir is not None else default_weather_dir()
    path = _daily_csv_path(weather_dir, site)
    if not path.exists():
        raise FileNotFoundError(
            f"Farm-twin weather cache missing: {path}. Build it once (network) with "
            f"`python -m aigov.farm_weather` — tests never rebuild it silently."
        )
    return CSVWeatherDataProvider(str(path))


if __name__ == "__main__":
    for p in build_all():
        print("built:", p)
