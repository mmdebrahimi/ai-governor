"""F14 farm-twin-world — MVP criterion 1: the world model is day-steppable on THIS host.

Pins the verified surface from the 2026-10-27 decompose run (see
``docs/farm-season-twin-decompose-2026-10-27.md`` §0): PCSE 6.x / WOFOST 8.1 potato advances ONE
day per ``run(days=1)``, exposes state mid-run via ``get_variable`` (the property the governed loop
requires and DSSAT's batch surface lacks), and completes a replayed real season (Wageningen 2006,
NASA POWER weather) with agronomically-shaped outputs.

Honest scope: this is a STEPPABILITY smoke, not a fidelity validation. The validation contract
(F14 milestone 4) is a separate, written-first artifact. Potential-production (PP) mode is the
unstressed ceiling — TWSO here is model-coherent only, never an outcome claim (inherited D7).

Network note: first run downloads crop parameters (GitHub) and weather (NASA POWER); both cache
under ``~/.pcse``. Subsequent runs are offline. A network failure surfaces as an ERROR, never a
silent skip — a skipping MVP criterion would be a vacuous pass.
"""

import textwrap

import pytest
import yaml

pcse = pytest.importorskip("pcse", reason="pcse not installed (F14 dependency; pip install pcse)")

from pcse.base import ParameterProvider  # noqa: E402
from pcse.input import (  # noqa: E402
    DummySoilDataProvider,
    NASAPowerWeatherDataProvider,
    WOFOST81SiteDataProvider_Classic,
    YAMLCropDataProvider,
)
from pcse.models import Wofost81_PP  # noqa: E402

#: The replayed reference run — public, concept-level (Wageningen is PCSE's home turf, chosen for
#: provider reliability; the venture's REAL reference region-season is F14 pending decision 1).
LAT, LON = 52.0, 5.5
AGRO_YAML = textwrap.dedent(
    """
    - 2006-03-31:
        CropCalendar:
            crop_name: potato
            variety_name: Fontane
            crop_start_date: 2006-04-10
            crop_start_type: emergence
            crop_end_date: 2006-09-20
            crop_end_type: harvest
            max_duration: 200
        TimedEvents: null
        StateEvents: null
    """
)


@pytest.fixture(scope="module")
def season():
    crop = YAMLCropDataProvider(model=Wofost81_PP)
    crop.set_active_crop("potato", "Fontane")
    site = WOFOST81SiteDataProvider_Classic(WAV=100, CO2=400, NAVAILI=80)
    params = ParameterProvider(cropdata=crop, sitedata=site, soildata=DummySoilDataProvider())
    weather = NASAPowerWeatherDataProvider(latitude=LAT, longitude=LON)
    sim = Wofost81_PP(params, weather, yaml.safe_load(AGRO_YAML))

    steps = 0
    midrun = []
    for day in range(220):
        sim.run(days=1)
        steps += 1
        if day in (10, 60, 110):
            midrun.append(
                {
                    "day": sim.day,
                    "DVS": sim.get_variable("DVS"),
                    "LAI": sim.get_variable("LAI"),
                    "TWSO": sim.get_variable("TWSO"),
                }
            )
        if sim.flag_terminate:
            break
    return {"sim": sim, "steps": steps, "midrun": midrun}


def test_advances_one_day_per_run_call(season):
    # A full season consumed >100 individual daily ticks — the governed loop's required cadence.
    assert season["steps"] > 100
    assert season["sim"].flag_terminate


def test_state_is_readable_mid_run(season):
    # The property DSSAT's batch surface lacks: state BETWEEN ticks, not only end-of-run output.
    for reading in season["midrun"]:
        assert reading["DVS"] is not None
        assert reading["LAI"] is not None and reading["LAI"] > 0


def test_mid_run_state_evolves_monotonically_where_biology_says_so(season):
    # DVS (phenological stage) and TWSO (tuber weight) are non-decreasing across the season.
    dvs = [r["DVS"] for r in season["midrun"]]
    assert dvs == sorted(dvs)
    twso = [r["TWSO"] or 0.0 for r in season["midrun"]]
    assert twso == sorted(twso)


def test_season_outputs_are_agronomically_shaped(season):
    # Shape bounds only (PP mode is a ceiling): dry tuber yield in a broad plausible band,
    # LAImax where a closed potato canopy lives. NOT a fidelity claim — that is milestone 4's
    # written validation contract.
    summary = season["sim"].get_summary_output()[0]
    assert 5_000 < summary["TWSO"] < 35_000, "dry tuber kg/ha outside any plausible band"
    assert 2.0 < summary["LAIMAX"] < 8.0
