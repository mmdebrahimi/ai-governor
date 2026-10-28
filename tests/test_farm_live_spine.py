"""F17 live spine tests — offline (fixtures); the real-surface fetch is run + inspected in the
Soraya batch that built this (R3), not here, so the suite stays deterministic."""

from __future__ import annotations

import datetime as dt
import math
from pathlib import Path

import pytest

from aigov.farm_live_weather import (
    COVERAGE_DEGRADED_MAX_MISSING,
    COVERAGE_OK_MAX_MISSING,
    MAX_MISSING_HOURS_FOR_DAILY,
    DailyDerived,
    build_live_caches,
    classify_day,
    derive_daily,
    vap_hpa_from_dewpoint_c,
    wind2m_from_10m,
    write_daily_csv,
    write_hourly_csv,
)
from aigov.farm_site_config import (
    LIVE_SITE_KEY,
    SiteConfig,
    default_config_path,
    load_site_config,
    write_example,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


def _hour(day: dt.date, h: int, *, rh=85.0, temp=14.0, dew=11.0, precip=0.0, swrad=120.0, wind=3.0):
    return {
        "time": f"{day.isoformat()}T{h:02d}:00",
        "relative_humidity_2m": rh,
        "temperature_2m": temp,
        "dew_point_2m": dew,
        "precipitation": precip,
        "shortwave_radiation": swrad,
        "wind_speed_10m": wind,
    }


def _full_day(day: dt.date, **kw) -> list[dict]:
    return [_hour(day, h, **kw) for h in range(24)]


# --------------------------------------------------------------------- privacy rail


def test_local_dir_is_gitignored():
    gitignore = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
    assert "local/" in gitignore.splitlines()


def test_missing_site_config_raises_with_instructions(tmp_path):
    with pytest.raises(FileNotFoundError, match="gitignored on purpose"):
        load_site_config(tmp_path / "farm_site.json")


def test_default_config_path_is_under_gitignored_local():
    assert default_config_path().parent.name == "local"


def test_example_config_roundtrip_refused_until_real_coords(tmp_path):
    p = write_example(tmp_path / "farm_site.json")
    with pytest.raises(ValueError, match="example"):
        load_site_config(p)  # fixture coords must be replaced, never silently used as the site
    with pytest.raises(FileExistsError):
        write_example(p)


def test_out_of_range_coords_refused(tmp_path):
    p = tmp_path / "farm_site.json"
    p.write_text('{"latitude": 95.0, "longitude": 5.0}', encoding="utf-8")
    with pytest.raises(ValueError, match="out-of-range"):
        load_site_config(p)


# --------------------------------------------------------------------- derivations


def test_vap_tetens_at_known_point():
    # Tetens at Td=11.0 C: 6.108*exp(17.27*11/(11+237.3)) = 13.126... hPa (hand-computed)
    assert vap_hpa_from_dewpoint_c(11.0) == pytest.approx(13.127, abs=0.01)


def test_wind_profile_factor():
    assert wind2m_from_10m(4.0) == pytest.approx(2.992, abs=0.001)


def test_derive_daily_units_and_values():
    day = dt.date(2026, 10, 20)
    rows = derive_daily({day: _full_day(day, swrad=120.0, precip=0.5, temp=14.0, wind=4.0)})
    assert len(rows) == 1
    r = rows[0]
    # 120 W/m^2 avg * 3600 s * 24 h / 1000 = 10368 kJ/m^2/d
    assert r.irrad_kj == pytest.approx(10368.0)
    assert r.rain_mm == pytest.approx(12.0)  # 0.5 mm * 24
    assert r.tmin_c == r.tmax_c == 14.0
    assert r.vap_kpa == pytest.approx(1.3127, abs=0.001)  # 13.127 hPa -> kPa
    assert r.wind2m_ms == pytest.approx(2.992, abs=0.001)
    assert r.present_hours == 24


def test_derive_daily_omits_day_beyond_missing_budget():
    day = dt.date(2026, 10, 20)
    hours = _full_day(day)
    for h in range(MAX_MISSING_HOURS_FOR_DAILY + 1):  # 5 null hours > budget of 4
        hours[h]["temperature_2m"] = None
    assert derive_daily({day: hours}) == []


def test_derive_daily_tolerates_small_gaps():
    day = dt.date(2026, 10, 20)
    hours = _full_day(day)
    hours[3]["temperature_2m"] = None  # 1 missing hour <= budget
    rows = derive_daily({day: hours})
    assert len(rows) == 1 and rows[0].present_hours == 23


# --------------------------------------------------------------------- coverage classes


def test_classify_day_thresholds():
    assert classify_day(0) == "ok"
    assert classify_day(COVERAGE_OK_MAX_MISSING) == "ok"
    assert classify_day(COVERAGE_OK_MAX_MISSING + 1) == "degraded"
    assert classify_day(COVERAGE_DEGRADED_MAX_MISSING) == "degraded"
    assert classify_day(COVERAGE_DEGRADED_MAX_MISSING + 1) == "unscoreable"


# --------------------------------------------------------------------- contract round-trips


def test_daily_csv_loads_through_pcse_unchanged(tmp_path):
    """The twin's own provider (CSVWeatherDataProvider) must read the live cache as-is."""
    from pcse.input import CSVWeatherDataProvider

    days = [dt.date(2026, 10, 18) + dt.timedelta(days=i) for i in range(3)]
    rows = derive_daily({d: _full_day(d, precip=0.5) for d in days})
    out = tmp_path / f"{LIVE_SITE_KEY}_daily.csv"
    write_daily_csv(out, LIVE_SITE_KEY, 52.52, 5.47, 0.0, rows, "fixture")
    wdp = CSVWeatherDataProvider(str(out))
    rec = wdp(days[1])
    assert rec.TMIN == pytest.approx(14.0)
    assert rec.IRRAD == pytest.approx(10368.0 * 1000.0)  # PCSE re-converts kJ -> J internally
    assert rec.RAIN == pytest.approx(1.2)  # 12 mm -> cm internally


def test_hourly_csv_loads_through_farm_observation_unchanged(tmp_path):
    """The rules' own reader (FarmObservation) must read the live cache as-is."""
    from aigov.farm_observation import FarmObservation

    day = dt.date(2026, 10, 20)
    rows = [(f"{day.isoformat()}T{h:02d}:00", 91.0, 12.0) for h in range(24)]
    write_hourly_csv(tmp_path / f"{LIVE_SITE_KEY}_hourly_rh.csv", LIVE_SITE_KEY, rows, "fixture")
    obs = FarmObservation(LIVE_SITE_KEY, weather_dir=tmp_path)
    assert len(obs.hours(day)) == 24
    assert obs.hours(day)[0].rh_pct == 91.0


def test_build_live_caches_refuses_future_end():
    cfg = SiteConfig(latitude=52.52, longitude=5.47)
    with pytest.raises(ValueError, match="ACTUALS only"):
        build_live_caches(cfg, start=dt.date.today(), end=dt.date.today())
