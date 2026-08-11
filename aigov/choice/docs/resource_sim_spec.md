# Resource Simulator — Spec (family `mars-gov-resource-sim`)

Closed-loop ECLSS resource model: population × food × oxygen for a Mars colony, validated on Earth
against published analog figures. Umbrella: `mars-governance`. Scale contract: crew N = 10..1000 (D2).

## Purpose
Provide the resource-constraint engine the governance sandbox (`mars-gov-sandbox`) consumes: given a
crew size, return steady-state O2/CO2/food/water demand and the closed-loop O2 balance, and surface the
bioregenerative over-production hazard so governance decisions can be stress-tested against scarcity.

## Model

### Crew metabolic baseline (first-principles)
- Metabolic rate **136.7 W/person**, respiratory quotient **0.87** (NSS ECLSS analog data).
- Daily energy expenditure = 136.7 W × 86 400 s = **11.81 MJ/day ≈ 2822 kcal/day**.
- **O2 consumption** derived via the caloric equivalent of O2 (20.4 kJ/L at RQ 0.87):
  `energy_kJ / 20.4 → L O2 → mol → kg` ⇒ **≈ 0.827 kg O2/person/day**.
- **CO2 production** = RQ × molar O2 ⇒ **≈ 0.99 kg CO2/person/day**.
- **Food (dry)** = caloric need / energy density (4.57 kcal/g, calibrated to BVAD dry-food basis)
  ⇒ **≈ 0.62 kg/person/day**.
- **Water** = intake (3.6 kg/day potable+hygiene+rehydration) − metabolic credit (0.30) = **3.3 kg/day**.

### Plant / bioregenerative subsystem
- `crop_fraction ∈ [0,1]` = share of crew calories grown photosynthetically.
- Plant O2 = crew_O2 × **1.5** × crop_fraction (over-production factor: full food closure fixes more
  carbon than the crew metabolizes).
- **Net O2 = plant_O2 − crew_O2**; `overproduction = net > 0`. Break-even at crop_fraction = 1/1.5 ≈ 0.667.
- Reproduces the **Mars One** failure mode: full food closure over-produces O2 → oxygen-poisoning risk;
  partial closure needs supplemental O2.

## Validation contract (MVP)
Reference values (NASA BVAD-style, per person per day): O2 = 0.835 kg, CO2 = 1.040 kg, food_dry = 0.617 kg.
The model passes if each derived per-capita value is **within ±10%** of its reference, demand scales
**linearly** across N=10..1000, per-capita values are **population-invariant**, and the plant subsystem
flags over-production at full closure / supplemental need at partial closure. See
`tests/test_resource_sim_validation.py`.

## API
- `per_capita_o2_kg()`, `per_capita_co2_kg()`, `per_capita_food_dry_kg()`, `per_capita_water_kg()`
- `simulate(n_crew, days=1) -> ResourceTotals` (`.per_capita_day` re-normalizes)
- `oxygen_balance(n_crew, crop_fraction=1.0) -> OxygenBalance` (`.net_o2_kg`, `.overproduction`)

## Limitations / future work
- Static "average adult" crew (V-HAB limitation); no demographic mix or activity variation yet.
- Water/food are requirement-based, not fully mass-balanced recycling loops.
- Over-production factor is a single literature-informed constant, not a crop-by-crop photosynthesis model.
- No transient dynamics (steady-state only); HERITAGE-style time-varying response is future work.
