"""F14 MVP criterion 3: the validation contract of ``docs/farm_twin_world_spec.md`` §5, verbatim.

Contract authored 2026-10-27 BEFORE the first validation run (written-first discipline). Anchors are
ten Den et al. (2022), EJA 137:126510, Tables 6 (2020, GATING) and 9 (2019, REPORTED non-gating).

- Layer 1 (reproduction, gating): each 2020 combo within ±10% of the PAPER'S OWN simulated yield.
- Layer 2 (fidelity, gating): each 2020 combo within ±20% of the OBSERVED trial yield.
- 2019 replay: reported, never gating (the paper itself drifts to −15.3% in its evaluation year).

Offline by construction: weather comes from the repo cache (``data/farm_twin/weather/``); a missing
cache is an ERROR, never a silent skip.
"""

import pytest

pytest.importorskip("pcse", reason="pcse not installed (F14 dependency; pip install pcse)")

from aigov.farm_twin import FarmTwin  # noqa: E402

#: (cultivar, site) -> (observed t/ha dry, paper-simulated t/ha dry) — ten Den 2022 Table 6 (2020).
ANCHORS_2020 = {
    ("Premiere", "vredepeel"): (18.3, 17.2),
    ("Innovator", "lelystad"): (16.1, 16.0),
    ("Fontane", "lelystad"): (18.2, 17.5),
    ("Fontane", "vredepeel"): (19.1, 17.6),
    ("Markies", "lelystad"): (16.4, 15.5),
    ("Festien", "vredepeel"): (18.0, 16.5),
}

#: Table 9 (2019, evaluation year) — REPORTED only.
ANCHORS_2019 = {
    ("Premiere", "vredepeel"): (15.3, 17.7),
    ("Innovator", "lelystad"): (14.7, 17.9),
    ("Fontane", "lelystad"): (16.5, 18.3),
    ("Fontane", "vredepeel"): (21.3, 18.5),
    ("Markies", "lelystad"): (16.0, 16.4),
    ("Festien", "vredepeel"): (18.3, 17.6),
}

LAYER1_BAND = 0.10
LAYER2_BAND = 0.20


@pytest.fixture(scope="module")
def replay_2020():
    results = {}
    for cultivar, site in ANCHORS_2020:
        summary = FarmTwin(cultivar, site, 2020).run_season()
        results[(cultivar, site)] = summary["TWSO"] / 1000.0  # kg/ha -> t/ha dry
    return results


@pytest.mark.parametrize("combo", sorted(ANCHORS_2020), ids=lambda c: f"{c[0]}@{c[1]}")
def test_layer1_reproduction_within_10pct_of_published_simulation(replay_2020, combo):
    _, paper_sim = ANCHORS_2020[combo]
    sim = replay_2020[combo]
    rel = abs(sim - paper_sim) / paper_sim
    assert rel <= LAYER1_BAND, (
        f"{combo}: replay {sim:.2f} vs paper-sim {paper_sim:.1f} t/ha dry -> {rel:.1%} "
        f"(band {LAYER1_BAND:.0%}) — the wrapped engine is NOT reproducing its published source"
    )


@pytest.mark.parametrize("combo", sorted(ANCHORS_2020), ids=lambda c: f"{c[0]}@{c[1]}")
def test_layer2_fidelity_within_20pct_of_observed_trial_yield(replay_2020, combo):
    observed, _ = ANCHORS_2020[combo]
    sim = replay_2020[combo]
    rel = abs(sim - observed) / observed
    assert rel <= LAYER2_BAND, (
        f"{combo}: replay {sim:.2f} vs observed {observed:.1f} t/ha dry -> {rel:.1%} "
        f"(band {LAYER2_BAND:.0%}) — fidelity finding; record in the F14 ledger, do NOT widen the band"
    )


def test_2019_evaluation_year_is_replayed_and_reported(capsys):
    # Non-gating by contract: the paper's own evaluation-year error reaches −15.3%. The replay must
    # COMPLETE for every combo and the numbers are printed into the test report (run pytest -s/-rA).
    lines = ["2019 evaluation-year replay (REPORTED, non-gating; obs / paper-sim / replay, t/ha dry):"]
    for (cultivar, site), (observed, paper_sim) in sorted(ANCHORS_2019.items()):
        summary = FarmTwin(cultivar, site, 2019).run_season()
        sim = summary["TWSO"] / 1000.0
        lines.append(
            f"  {cultivar}@{site}: obs {observed:.1f} / paper-sim {paper_sim:.1f} / replay {sim:.2f} "
            f"(vs obs {(sim - observed) / observed:+.1%}, vs paper-sim {(sim - paper_sim) / paper_sim:+.1%})"
        )
        assert sim > 0.0
    print("\n".join(lines))
