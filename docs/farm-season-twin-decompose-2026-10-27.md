# Farm-season-twin venture — decompose + requirements flow-down (2026-10-27)

> Soraya `decompose` output (run `2026-10-27-0900-decompose-plan-farm-season-twin`). Subject per the
> ratified `/idea-anchor` (2026-10-26) + `/probe farm-season-twin` (2026-10-27): standalone venture,
> season one is a SIMULATION TWIN only, one instrument deep, external world-model author, $0 capital
> (sim-only — the money gate IS the cap), kill condition encoded in the terminal family's bar.

## 0. Verified external surfaces (resolved this run — the probe's flip condition)

| Surface | Verdict | Evidence |
|---|---|---|
| Steppable crop simulator | **PCSE/WOFOST (Wageningen)** — pure Python, EUPL 1.2, `run()` advances ONE day, `get_variable()` reads state mid-run, `NASAPowerWeatherDataProvider` built in | pcse.readthedocs.io user guide |
| Potato parameters | `Potato_701`–`Potato_704` via `YAMLCropDataProvider` (WOFOST_crop_parameters repo, version-pinned branches) | github.com/ajwdewit/WOFOST_crop_parameters |
| DSSAT alternative | SUBSTOR-Potato is daily but py-dssattools is BATCH-oriented (run_treatment → read outputs); no steppable surface found | py-dssattools docs; dssat.net |
| Spray-decision provenance | **Published decision rules exist**: Blitecast severity-value threshold 18 (Wisconsin-derived; Brazilian trials: −25–70% sprays, yield preserved); UK Smith Period (2 consecutive days min temp ≥10°C + ≥11h RH ≥90%) | OSU Malheur reports 1998/2001; EuroBlight 2013 (Skelsey); Ciência Rural 2024 |
| Weather replay | NASA POWER agroclimatology API — free, daily, global ~0.5°; `pynasapower` client; hourly RH (Smith needs ≥11h RH≥90%) available from open-meteo historical as fallback | power.larc.nasa.gov; pypi pynasapower |

**Named fidelity gap (honest, load-bearing):** WOFOST simulates crop GROWTH (potential/water-limited
production). It does NOT simulate late blight. The twin is therefore a composition: WOFOST (growth) +
weather-driven risk rules (Blitecast/Smith) + a DAMAGE COUPLING (untreated high-risk periods → yield
loss). The damage coupling is where invented numbers would creep in; it requires a published yield-loss
relationship, and if none survives scrutiny, the season-one bar reframes from "yield outcome" to
"risk-rule compliance" — stated now so it cannot drift in silently.

## 1. Project-family decomposition

| # | Family (slug) | Scope (one line) | Why a distinct family |
|---|---|---|---|
| F14 | `farm-twin-world` | The ground-truth world: PCSE/WOFOST-potato wrapped as a twin honoring the ColonyTwin disciplines (coverage, observability, per-tick bounds), fed by a replayed real historical season | Evidence base is AGRONOMIC fidelity (external model + external weather vs published yields) — falsified by validation-contract miss |
| F15 | `farm-twin-decision-loop` | The governed instrument: observation layer (Estimate-wrapped), the ONE instrument (late-blight treat/don't-treat), its anti-steering certifier, externally-provenanced thresholds + status quo | Evidence base is GOVERNANCE mechanics (provenance, certifiability, fail-closed) — falsified by the adversarial suite |
| F16 | `farm-governed-season` | Integration terminal: the kernel runs one full replayed season end-to-end, every action gated, season report + kill-condition evaluation | Evidence base is the COMPOSED loop — falsified only by running the whole thing (the ledger's own lesson: running the real thing finds what green suites cannot) |

## 2. Requirements flow-down + dependency graph

| Family | Binding requirement | Depends on | Critical-path position | Cheapest next test |
|---|---|---|---|---|
| `farm-twin-world` | Day-steppable, mid-run-readable potato world validated against a REAL season (external author: PCSE + NASA POWER), honoring coverage/observability/bounds | — | **Gate A** | `pip install pcse` + a day-step smoke on Python 3.14 (RETIRED THIS RUN if smoke passes) |
| `farm-twin-decision-loop` | Every threshold carries EXTERNAL provenance (Blitecast 18 / Smith Period); the instrument has a real certifier (kernel refuses otherwise); observation is Estimate-wrapped, never truth-read | farm-twin-world (input shapes) | **Gate B** | Unit-test Smith/Blitecast rules against published example values |
| `farm-governed-season` | `apply()` executes ONLY ratified+certified actions across a full replayed season; season report emitted; kill condition evaluated; adversarial suite extended to the new instrument | farm-twin-world, farm-twin-decision-loop | **Gate C — venture terminal** | One governed tick end-to-end (1 sim day through kernel) |

**Critical path:** `Gate A {farm-twin-world} → Gate B {farm-twin-decision-loop} → Gate C {farm-governed-season}`.
Cross-cutting (no own family): the privacy rail (public repo, concept-level only — nothing here names
family specifics) and the adversarial-suite pattern (`tests/test_adversarial_kernel.py`), folded into F16.

## 3. VOI-ranked first moves

1. **PCSE day-step smoke on this host** — retires the venture's biggest unknown (steppability × Python 3.14) for the cost of one install + one script. *(Executed this run.)*
2. **Weather replay provider** — one region-season of NASA POWER daily data cached locally; turns "external data spine" from unowned to owned.
3. **Smith/Blitecast rule module with published-value unit tests** — the provenance anchor for every threshold downstream.
4. **Damage-coupling literature check** — find a published late-blight yield-loss relationship; this decides whether F16's bar is yield-denominated or compliance-denominated.

## 4. `/project-init` commands (self-invoked this run, per Soraya v1.2)

```
/project-init "Build the ground-truth world for the farm-season twin: wrap PCSE/WOFOST potato as a day-steppable twin honoring coverage, observability and per-tick bounds, fed by a replayed real historical season and validated against published regional yields" --project-id farm-twin-world --horizon 2
/project-init "Build the governed decision loop for the farm-season twin: an Estimate-wrapped observation layer, one instrument (late-blight treat/don't-treat) with externally-provenanced thresholds (Blitecast/Smith), a real anti-steering certifier, and an externally-provenanced status quo" --project-id farm-twin-decision-loop --horizon 3
/project-init "Run one full replayed historical potato season end-to-end under the aigov kernel with every action gated, emit a season report, extend the adversarial suite to the new instrument, and evaluate the venture kill condition" --project-id farm-governed-season --horizon 4
```

## 5. Terminal condition

The venture's season-one terminal is F16's bar (full governed replayed season + report + kill-condition
evaluation). Soraya asserts mechanically when all three families meet their recorded criteria; the
"season two goes to dirt/hardware" judgment is ALWAYS the user's — explicit sign-off, never auto-closed.

**Kill condition (user-ratified "supersede, bounded"):** if the governed replay cannot reproduce the
reference season within the F14 validation contract after the bounded recovery budget, OR fidelity turns
out to require authoring agronomy in-house (breaking the independent-author rail), the venture FREEZES at
its honest state and the F13 "automation = hobby" decision is re-instated with a constraint-expiry entry
(R9) naming what would reopen it. Capital cap: $0 in season one — sim only; any step requiring spend
parks at the money gate by construction.
