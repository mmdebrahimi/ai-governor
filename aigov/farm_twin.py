"""F14 FarmTwin: the PCSE/WOFOST potato world wrapped in the twin disciplines.

The world model for the farm-season twin (``docs/farm_twin_world_spec.md``). It wraps
``Wofost81_PP`` — carrying the ten Den et al. (2022) cultivar calibrations PCSE ships — as a
day-steppable twin with the three ColonyTwin disciplines (``aigov/twin.py`` is the template):

1. **Coverage** — ``SERVED`` declares every variable this twin serves; ``check_coverage`` fails on a
   declared-but-unreadable or readable-but-undeclared variable.
2. **Observability-enforced reads** — ``read()`` serves DIRECT names only and REFUSES anything
   undeclared. (This world exposes truth; F15's sensor layer degrades it into ``Estimate``\\ s.)
3. **Per-tick physical bounds** — tripwires, not clamps: a violated bound HALTS the twin. A world
   reporting impossible state would be telling the decision loop a comfortable fiction.

Scope honesty (inherited D7): potential-production mode — no water/nutrient/pest/disease limitation.
TWSO is a model-coherent ceiling, never an outcome claim. Late blight is NOT in this model.
"""

from __future__ import annotations

import datetime
import textwrap
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from .contract import Observability
from .farm_weather import load_daily_weather

# --------------------------------------------------------------------------------------
# The reference region-season (spec §2 — ten Den et al. 2022 trials, public data)
# --------------------------------------------------------------------------------------

#: Planting + final-harvest dates per trial site-year (paper Tables 1 + 3).
#: Vredepeel 2020 planting is a DOCUMENTED INFERENCE (the paper prints the impossible 24/09/2020;
#: treated as a 04<->09 digit swap — see spec §2).
TRIALS = {
    ("lelystad", 2019): {"planting": datetime.date(2019, 4, 25), "crop_end": datetime.date(2019, 10, 2)},
    ("lelystad", 2020): {"planting": datetime.date(2020, 4, 20), "crop_end": datetime.date(2020, 9, 23)},
    ("vredepeel", 2019): {"planting": datetime.date(2019, 4, 18), "crop_end": datetime.date(2019, 9, 25)},
    ("vredepeel", 2020): {"planting": datetime.date(2020, 4, 24), "crop_end": datetime.date(2020, 9, 24)},
}

#: Days from planting to 80% emergence per cultivar-site (paper Table 5, 2020; reused for 2019,
#: whose per-cultivar dates are not tabulated — the paper reports the 2019 range as 28–33 d).
EMERGENCE_DAYS = {
    ("Innovator", "lelystad"): 31,
    ("Fontane", "lelystad"): 32,
    ("Markies", "lelystad"): 32,
    ("Premiere", "vredepeel"): 29,
    ("Fontane", "vredepeel"): 31,
    ("Festien", "vredepeel"): 28,
}

#: The six gating 2020 combos (spec §5) as (cultivar, site) pairs.
COMBOS_2020 = [(c, s) for (c, s) in EMERGENCE_DAYS]


# --------------------------------------------------------------------------------------
# Discipline errors
# --------------------------------------------------------------------------------------


class ObservabilityRefused(LookupError):
    """Raised when something reads a variable this twin does not declare as served."""


class FarmTwinHalted(RuntimeError):
    """Raised when a per-tick physical bound trips. The twin refuses to serve impossible state."""


@dataclass
class FarmTickReport:
    day: datetime.date
    dvs: float
    lai: float
    twso_kg_ha: float
    violations: list = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.violations


# --------------------------------------------------------------------------------------
# The twin
# --------------------------------------------------------------------------------------

#: Generous ceiling on daily tuber dry-matter gain (kg DM/ha/day), above reported NL maxima —
#: a tripwire against a non-physical integration step, not an agronomic claim.
MAX_DAILY_TWSO_GAIN_KG_HA = 400.0
MAX_PLAUSIBLE_LAI = 10.0


class FarmTwin:
    """One replayed cultivar-site-season potato world, day-steppable, discipline-enforcing."""

    SERVED = {
        "dvs": Observability.DIRECT,
        "lai": Observability.DIRECT,
        "twso_kg_ha": Observability.DIRECT,
        "tagp_kg_ha": Observability.DIRECT,
        "day": Observability.DIRECT,
    }

    #: PCSE output names behind each served variable.
    _PCSE_NAMES = {"dvs": "DVS", "lai": "LAI", "twso_kg_ha": "TWSO", "tagp_kg_ha": "TAGP"}

    def __init__(self, cultivar: str, site: str, year: int, weather_dir: Path | None = None):
        from pcse.base import ParameterProvider
        from pcse.input import (
            DummySoilDataProvider,
            WOFOST81SiteDataProvider_Classic,
            YAMLCropDataProvider,
        )
        from pcse.models import Wofost81_PP

        if (cultivar, site) not in EMERGENCE_DAYS:
            raise ValueError(f"unknown trial combo: {cultivar} at {site}")
        trial = TRIALS[(site, year)]
        self.cultivar, self.site, self.year = cultivar, site, year
        self.planting = trial["planting"]
        self.emergence = self.planting + datetime.timedelta(days=EMERGENCE_DAYS[(cultivar, site)])
        self.crop_end = trial["crop_end"]

        crop = YAMLCropDataProvider(model=Wofost81_PP)
        crop.set_active_crop("potato", cultivar)
        site_params = WOFOST81SiteDataProvider_Classic(WAV=100, CO2=400, NAVAILI=80)
        params = ParameterProvider(
            cropdata=crop, sitedata=site_params, soildata=DummySoilDataProvider()
        )
        agromanagement = yaml.safe_load(
            textwrap.dedent(
                f"""
                - {self.planting.isoformat()}:
                    CropCalendar:
                        crop_name: potato
                        variety_name: {cultivar}
                        crop_start_date: {self.emergence.isoformat()}
                        crop_start_type: emergence
                        crop_end_date: {self.crop_end.isoformat()}
                        crop_end_type: harvest
                        max_duration: 250
                    TimedEvents: null
                    StateEvents: null
                """
            )
        )
        self._sim = Wofost81_PP(params, load_daily_weather(site, weather_dir), agromanagement)
        self._prev = {"dvs": None, "twso_kg_ha": None}
        self.ticks = 0

    # ---------------------------------------------------------------- reads

    def read(self, name: str) -> float | datetime.date:
        """Read a DIRECT variable. Refuses anything this twin does not declare as served."""
        if name not in self.SERVED:
            raise ObservabilityRefused(
                f"'{name}' is not a variable this twin serves; declared: {sorted(self.SERVED)}"
            )
        if name == "day":
            return self._sim.day
        value = self._sim.get_variable(self._PCSE_NAMES[name])
        return 0.0 if value is None else float(value)

    @property
    def terminated(self) -> bool:
        return bool(self._sim.flag_terminate)

    # ---------------------------------------------------------------- dynamics

    def tick(self) -> FarmTickReport:
        """Advance one day; enforce the per-tick bounds as tripwires (violation HALTS)."""
        if self.terminated:
            raise FarmTwinHalted(f"season already terminated on {self._sim.day}; nothing to advance")
        self._sim.run(days=1)
        self.ticks += 1
        if self.terminated and self._sim.get_variable("DVS") is None:
            # Harvest day: PCSE removes the crop object, so live reads return None. That is
            # bookkeeping, not a physical collapse — serve the last pre-harvest state, no bounds.
            return FarmTickReport(
                day=self._sim.day,
                dvs=self._prev["dvs"] or 0.0,
                lai=0.0,
                twso_kg_ha=self._prev["twso_kg_ha"] or 0.0,
            )
        report = FarmTickReport(
            day=self._sim.day,
            dvs=self.read("dvs"),
            lai=self.read("lai"),
            twso_kg_ha=self.read("twso_kg_ha"),
        )
        prev_dvs, prev_twso = self._prev["dvs"], self._prev["twso_kg_ha"]
        if prev_dvs is not None and report.dvs < prev_dvs:
            report.violations.append(f"DVS decreased: {prev_dvs} -> {report.dvs}")
        if prev_twso is not None:
            if report.twso_kg_ha < prev_twso:
                report.violations.append(f"TWSO decreased: {prev_twso} -> {report.twso_kg_ha}")
            if report.twso_kg_ha - prev_twso > MAX_DAILY_TWSO_GAIN_KG_HA:
                report.violations.append(
                    f"TWSO gained {report.twso_kg_ha - prev_twso:.0f} kg/ha in one day "
                    f"(> {MAX_DAILY_TWSO_GAIN_KG_HA:.0f})"
                )
        if not 0.0 <= report.lai <= MAX_PLAUSIBLE_LAI:
            report.violations.append(f"LAI outside (0, {MAX_PLAUSIBLE_LAI}): {report.lai}")
        self._prev = {"dvs": report.dvs, "twso_kg_ha": report.twso_kg_ha}
        if report.violations:
            raise FarmTwinHalted(
                f"{self.cultivar}@{self.site} {self.year} tripped physical bounds on "
                f"{report.day}: {report.violations}"
            )
        return report

    def run_season(self, max_days: int = 250) -> dict:
        """Tick to termination; return the season summary (final TWSO etc.)."""
        while not self.terminated and self.ticks < max_days:
            self.tick()
        if not self.terminated:
            raise FarmTwinHalted(f"season did not terminate within {max_days} daily ticks")
        summary = self._sim.get_summary_output()[0]
        summary["ticks"] = self.ticks
        return summary


# --------------------------------------------------------------------------------------
# Coverage checks (discipline 1)
# --------------------------------------------------------------------------------------


def check_coverage(twin: FarmTwin) -> list[str]:
    """Forward + reverse coverage: every SERVED name reads; no obvious unserved read succeeds.

    Returns a list of violations (empty = covered). Forward: a declared variable that raises on
    ``read()`` is a lie in SERVED. Reverse is enforced structurally by ``read()`` refusing
    undeclared names — probed here with a canary.
    """
    violations = []
    for name in twin.SERVED:
        try:
            twin.read(name)
        except Exception as exc:  # noqa: BLE001 — any failure to serve a declared name is the finding
            violations.append(f"declared-but-unreadable: {name} ({exc})")
    try:
        twin.read("soil_moisture")  # a plausible-sounding variable this PP world does NOT have
        violations.append("undeclared read served: soil_moisture")
    except ObservabilityRefused:
        pass
    return violations
