"""F18 shadow-loop tests — offline via the refresh=False seam (prebuilt caches, simulated today)."""

from __future__ import annotations

import datetime as dt

import pytest

from aigov.choice.governance.fail_safe_gate import CERTIFY, ESCALATE
from aigov.farm_live_weather import write_hourly_csv
from aigov.farm_shadow_season import load_records, run_daily_tick, season_summary
from aigov.farm_site_config import LIVE_SITE_KEY, SiteConfig

START = dt.date(2026, 11, 1)
CFG = SiteConfig(latitude=52.52, longitude=5.47)  # public fixture coords; refresh=False → never fetched


def _day_rows(day: dt.date, *, rh=70.0, temp=12.0, hours=range(24)):
    return [(f"{day.isoformat()}T{h:02d}:00", rh, temp) for h in hours]


def _write_cache(tmp_path, days: dict[dt.date, list]):
    rows = [r for d in sorted(days) for r in days[d]]
    write_hourly_csv(tmp_path / f"{LIVE_SITE_KEY}_hourly_rh.csv", LIVE_SITE_KEY, rows, "fixture")


def _tick(tmp_path, today: dt.date):
    return run_daily_tick(
        season_start=START, today=today, cfg=CFG,
        weather_dir=tmp_path, state_dir=tmp_path / "state", refresh=False,
    )


def test_clean_dry_day_certifies_dont_treat(tmp_path):
    day = dt.date(2026, 11, 3)
    _write_cache(tmp_path, {d: _day_rows(d) for d in (dt.date(2026, 11, 1), dt.date(2026, 11, 2), day)})
    rec = _tick(tmp_path, today=day + dt.timedelta(days=1))
    assert rec.date == day.isoformat()
    assert rec.coverage == "ok" and rec.present_hours == 24
    assert rec.acc_value == 0.0 and rec.rule_decision == "dont-treat"
    assert rec.proposal == "dont-treat" and rec.verdict == CERTIFY


def test_humid_run_straddles_and_escalates(tmp_path):
    # RH 91 all day at 15 C (59 F, Wallin 54-59 band): SV(90%)=4/day but SV(93%)=0 — five such days
    # put the value at 20 (past threshold 18) with the low recount at 0: straddle -> ESCALATE.
    days = {
        START + dt.timedelta(days=i): _day_rows(START + dt.timedelta(days=i), rh=91.0, temp=15.0)
        for i in range(5)
    }
    _write_cache(tmp_path, days)
    rec = _tick(tmp_path, today=START + dt.timedelta(days=5))
    assert rec.acc_value == pytest.approx(20.0)
    assert rec.acc_lo == pytest.approx(0.0)
    assert rec.rule_decision == "ambiguous"
    assert rec.proposal == "treat" and rec.verdict == ESCALATE
    assert rec.note  # the escalation carries its routed procedure


def test_degraded_day_classified(tmp_path):
    day = dt.date(2026, 11, 2)
    days = {dt.date(2026, 11, 1): _day_rows(dt.date(2026, 11, 1)), day: _day_rows(day, hours=range(5, 24))}
    _write_cache(tmp_path, days)  # 19 present hours -> 5 missing -> degraded
    rec = _tick(tmp_path, today=day + dt.timedelta(days=1))
    assert rec.coverage == "degraded" and rec.present_hours == 19


def test_absent_day_escalates_without_fabrication(tmp_path):
    _write_cache(tmp_path, {dt.date(2026, 11, 1): _day_rows(dt.date(2026, 11, 1))})
    rec = _tick(tmp_path, today=dt.date(2026, 11, 3))  # decides 11-02, absent from cache
    assert rec.coverage == "no-data" and rec.verdict == ESCALATE
    assert rec.acc_value is None and "never interpolated" in rec.note


def test_rerun_same_day_is_idempotent_and_summary_counts(tmp_path):
    day = dt.date(2026, 11, 2)
    _write_cache(tmp_path, {dt.date(2026, 11, 1): _day_rows(dt.date(2026, 11, 1)), day: _day_rows(day)})
    _tick(tmp_path, today=day + dt.timedelta(days=1))
    _tick(tmp_path, today=day + dt.timedelta(days=1))  # same decided day again
    recs = load_records(tmp_path / "state")
    assert len(recs) == 1
    s = season_summary(tmp_path / "state")
    assert s["ticks"] == 1 and s["verdicts"] == {CERTIFY: 1}


def test_decision_before_season_start_refused(tmp_path):
    with pytest.raises(ValueError, match="precedes season start"):
        _tick(tmp_path, today=START)
