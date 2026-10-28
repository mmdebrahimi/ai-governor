"""F17 off-repo sensor-site configuration (season-two privacy rail).

The live sensor site's coordinates NEVER enter this public repo. They live in a gitignored local
file (``local/farm_site.json`` by default) that the ingestion spine reads at run time. In-repo
artifacts refer to the site only by its SHAPE key (``livesite``), the same off-repo pattern as the
season-two capital-cap number.

Tests use the already-public Lelystad fixture coordinates (``aigov.farm_weather.SITES``), never a
private config.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

#: SHAPE-only key under which the live site's caches are written (``livesite_daily.csv`` etc.).
LIVE_SITE_KEY = "livesite"

_EXAMPLE = {
    "latitude": 52.52,
    "longitude": 5.47,
    "timezone": "UTC",
    "_comment": (
        "Replace latitude/longitude with the real sensor site's coordinates. This file is "
        "gitignored (local/) and must NEVER be committed - the repo is public."
    ),
}


@dataclass(frozen=True)
class SiteConfig:
    latitude: float
    longitude: float
    timezone: str = "UTC"
    site_key: str = LIVE_SITE_KEY


def default_config_path(repo_root: Path | None = None) -> Path:
    root = repo_root if repo_root is not None else Path(__file__).resolve().parent.parent
    return root / "local" / "farm_site.json"


def write_example(path: Path | None = None) -> Path:
    """Write a template config for the user to fill in. Never overwrites an existing file."""
    path = path if path is not None else default_config_path()
    if path.exists():
        raise FileExistsError(f"refusing to overwrite existing site config: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_EXAMPLE, indent=2), encoding="utf-8")
    return path


def load_site_config(path: Path | None = None) -> SiteConfig:
    """Load the off-repo site config. Raises with a fill-me-in message when absent."""
    path = path if path is not None else default_config_path()
    if not path.exists():
        raise FileNotFoundError(
            f"off-repo site config missing: {path}. Create it with "
            f"`python -c \"from aigov.farm_site_config import write_example; write_example()\"` "
            f"and fill in the real coordinates. It is gitignored on purpose (public repo)."
        )
    raw = json.loads(path.read_text(encoding="utf-8"))
    lat = float(raw["latitude"])
    lon = float(raw["longitude"])
    if not (-90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0):
        raise ValueError(f"site config has out-of-range coordinates: lat={lat}, lon={lon}")
    if abs(lat - _EXAMPLE["latitude"]) < 1e-9 and abs(lon - _EXAMPLE["longitude"]) < 1e-9:
        raise ValueError(
            "site config still carries the example (Lelystad fixture) coordinates - fill in the "
            "real sensor site before building a live cache, or pass coordinates explicitly."
        )
    return SiteConfig(latitude=lat, longitude=lon, timezone=str(raw.get("timezone", "UTC")))
