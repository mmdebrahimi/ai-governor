"""F18 virtual-shadow season loop — one governed decision per REAL day, shadow mode.

Season two never actuates anything: each daily tick RECOMMENDS-AND-LOGS. The loop is:

    refresh live caches (F17 spine) -> read yesterday (the last complete UTC day) -> accumulate
    Blitecast severity as an Estimate -> propose the nominal action -> run the real certifier gate
    -> append one TickRecord.

Dry-run scope (winter 2026/27): exactly the above — no crop is growing, so the PCSE twin does not
tick. The LIVE season (virtual planting on the real calendar, ~Apr 2027) adds the twin in lockstep
per ``docs/farm_shadow_season_protocol.md``.

State lives OFF-REPO under ``local/shadow_season/`` (daily records carry the real locale's
weather-derived values; the privacy rail keeps per-day live-site data out of the public tree).
Restart safety: the record file is the only state — severity is recomputed from the cache on every
tick, so a crashed or skipped day costs nothing but that day's coverage.

Honesty rails carried over from season one: missing data is never interpolated (an absent day goes
through the certifier as ``None`` and comes back ESCALATE); the proposal is gated by the SAME
``farm_fail_safe_gate`` the replayed season used; records are idempotent by date.
"""

from __future__ import annotations

import datetime as _dt
import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .choice.governance.fail_safe_gate import ESCALATE
from .farm_certifier import DONT_TREAT, TREAT, farm_fail_safe_gate
from .farm_live_weather import build_live_caches, classify_day, default_live_weather_dir
from .farm_observation import FarmObservation, rule_decision_from_estimate
from .farm_site_config import LIVE_SITE_KEY, SiteConfig
from .blight_rules import BLITECAST_SEVERITY_THRESHOLD


def default_state_dir(repo_root: Path | None = None) -> Path:
    root = repo_root if repo_root is not None else Path(__file__).resolve().parent.parent
    return root / "local" / "shadow_season"


@dataclass(frozen=True)
class TickRecord:
    date: str                 # the decided day (ISO)
    coverage: str             # ok / degraded / unscoreable / no-data
    present_hours: int
    acc_value: float | None   # Blitecast accumulated severity (Estimate.value), None on no-data
    acc_lo: float | None
    acc_hi: float | None
    rule_decision: str        # treat / dont-treat / ambiguous / no-data
    proposal: str             # the nominal shadow proposal that was gated
    verdict: str              # fail_safe_gate labels: certify / steering-detected / escalate-multipeaked
    note: str = ""


def _records_path(state_dir: Path) -> Path:
    return state_dir / "records.jsonl"


def load_records(state_dir: Path | None = None) -> list[TickRecord]:
    path = _records_path(state_dir if state_dir is not None else default_state_dir())
    if not path.exists():
        return []
    return [TickRecord(**json.loads(line)) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _append_record(state_dir: Path, rec: TickRecord) -> None:
    """Idempotent by date: a re-run of the same day replaces that day's record."""
    state_dir.mkdir(parents=True, exist_ok=True)
    existing = [r for r in load_records(state_dir) if r.date != rec.date]
    existing.append(rec)
    existing.sort(key=lambda r: r.date)
    _records_path(state_dir).write_text(
        "\n".join(json.dumps(asdict(r)) for r in existing) + "\n", encoding="utf-8"
    )


def run_daily_tick(
    *,
    season_start: _dt.date,
    today: _dt.date | None = None,
    cfg: SiteConfig | None = None,
    weather_dir: Path | None = None,
    state_dir: Path | None = None,
    refresh: bool = True,
) -> TickRecord:
    """One shadow tick: decide YESTERDAY (the last complete UTC day) and log the gated verdict.

    ``refresh=False`` skips the network pull and reads the existing caches (the test seam, and the
    recovery path when open-meteo is down: yesterday's decision then runs on the cache as-is).
    """
    today = today if today is not None else _dt.date.today()
    decision_day = today - _dt.timedelta(days=1)
    if decision_day < season_start:
        raise ValueError(f"decision day {decision_day} precedes season start {season_start}")
    weather_dir = weather_dir if weather_dir is not None else default_live_weather_dir()
    state_dir = state_dir if state_dir is not None else default_state_dir()

    if refresh:
        if cfg is None:
            from .farm_site_config import load_site_config

            cfg = load_site_config()
        build_live_caches(cfg, start=season_start, end=decision_day, weather_dir=weather_dir)

    site = (cfg.site_key if cfg is not None else LIVE_SITE_KEY) or LIVE_SITE_KEY
    obs = FarmObservation(site, weather_dir=weather_dir)

    try:
        hours = obs.hours(decision_day)
    except KeyError:
        # The day is wholly absent from the cache: the certifier is given nothing and says so.
        verdict = farm_fail_safe_gate(DONT_TREAT, None)
        rec = TickRecord(
            date=decision_day.isoformat(), coverage="no-data", present_hours=0,
            acc_value=None, acc_lo=None, acc_hi=None, rule_decision="no-data",
            proposal="dont-treat", verdict=verdict.label,
            note="day absent from cache - escalated, never interpolated",
        )
        _append_record(state_dir, rec)
        return rec

    acc = obs.accumulated_severity(season_start, decision_day)
    lo, hi = acc.interval  # property on Estimate
    rule = rule_decision_from_estimate(acc)
    nominal = TREAT if acc.value >= BLITECAST_SEVERITY_THRESHOLD else DONT_TREAT
    verdict = farm_fail_safe_gate(nominal, acc)
    rec = TickRecord(
        date=decision_day.isoformat(),
        coverage=classify_day(24 - len(hours)),
        present_hours=len(hours),
        acc_value=acc.value, acc_lo=lo, acc_hi=hi,
        rule_decision=rule,
        proposal="treat" if nominal == TREAT else "dont-treat",
        verdict=verdict.label,
        note=verdict.recommended_procedure[:160] if verdict.label == ESCALATE else "",
    )
    _append_record(state_dir, rec)
    return rec


def season_summary(state_dir: Path | None = None) -> dict:
    """Aggregate counts for the dry-run / season report (SHAPE-safe: no per-day weather values)."""
    recs = load_records(state_dir)
    out = {
        "ticks": len(recs),
        "first": recs[0].date if recs else None,
        "last": recs[-1].date if recs else None,
        "verdicts": {}, "coverage": {}, "decisions": {},
    }
    for r in recs:
        out["verdicts"][r.verdict] = out["verdicts"].get(r.verdict, 0) + 1
        out["coverage"][r.coverage] = out["coverage"].get(r.coverage, 0) + 1
        out["decisions"][r.rule_decision] = out["decisions"].get(r.rule_decision, 0) + 1
    return out


if __name__ == "__main__":
    import sys

    start = _dt.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else _dt.date.today() - _dt.timedelta(days=7)
    print(run_daily_tick(season_start=start))
    print(season_summary())
