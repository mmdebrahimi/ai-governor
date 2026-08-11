"""Closed-loop ECLSS resource model for a Mars colony (population x food x oxygen).

Family: mars-gov-resource-sim (umbrella: mars-governance).

Per-capita O2/CO2 are derived FROM FIRST PRINCIPLES (metabolic energy expenditure +
respiratory quotient) and validated against NASA BVAD-style analog references within
+/-10%. Food (dry mass) is energy-derived with a caloric density calibrated to the BVAD
dry-food basis; water is requirement-based with a metabolic-water credit. The plant
subsystem reproduces the bioregenerative O2 OVER-production hazard that sank the Mars One
life-support design (full photosynthetic food closure fixes more carbon than the crew
metabolizes, so it over-produces O2 relative to respiration).

References: V-HAB / HERITAGE crew models; Marspedia "Life support"; NSS "Towards Closed
ECLSS for Space Habitats" Part I. Crew metabolic rate 136.7 W/person, RQ 0.87 (analog source).
Scale contract: validated for crew sizes N = 10 .. 1000 (umbrella decision D2).
"""
from dataclasses import dataclass

# --- physical constants ---
SECONDS_PER_DAY = 86_400
J_PER_KJ = 1_000
KJ_PER_KCAL = 4.184
MOLAR_VOLUME_STP_L = 22.414       # L/mol at STP
O2_MOLAR_MASS_G = 32.0
CO2_MOLAR_MASS_G = 44.0

# --- crew metabolic baseline (analog-sourced) ---
METABOLIC_RATE_W = 136.7          # W/person (average), NSS ECLSS analog data
RESPIRATORY_QUOTIENT = 0.87       # molar CO2 produced / O2 consumed
O2_CALORIC_EQUIV_KJ_PER_L = 20.4  # kJ released per L O2 at RQ ~0.87
FOOD_ENERGY_DENSITY_KCAL_PER_G = 4.57  # calibrated to the BVAD dry-food basis
WATER_INTAKE_KG_PER_DAY = 3.6     # potable + food-rehydration + hygiene (requirement)
METABOLIC_WATER_KG_PER_DAY = 0.30

# --- validation references (NASA BVAD-style, per person per day) ---
O2_REF_KG = 0.835
CO2_REF_KG = 1.040
FOOD_DRY_REF_KG = 0.617

# --- plant / bioregenerative subsystem ---
# Full photosynthetic food closure fixes more carbon than the crew metabolizes, so it
# OVER-produces O2 relative to respiration -> documented Mars One oxygen-poisoning failure mode.
PLANT_O2_OVERPRODUCTION_FACTOR = 1.5


def _crew_energy_kj_per_day(metabolic_rate_w=METABOLIC_RATE_W):
    return metabolic_rate_w * SECONDS_PER_DAY / J_PER_KJ


def per_capita_o2_kg(metabolic_rate_w=METABOLIC_RATE_W,
                     o2_kj_per_l=O2_CALORIC_EQUIV_KJ_PER_L):
    """O2 consumed per person per day (kg), derived from metabolic energy expenditure."""
    energy_kj = _crew_energy_kj_per_day(metabolic_rate_w)
    o2_liters = energy_kj / o2_kj_per_l
    o2_mol = o2_liters / MOLAR_VOLUME_STP_L
    return o2_mol * O2_MOLAR_MASS_G / 1000.0


def per_capita_co2_kg(metabolic_rate_w=METABOLIC_RATE_W,
                      rq=RESPIRATORY_QUOTIENT,
                      o2_kj_per_l=O2_CALORIC_EQUIV_KJ_PER_L):
    """CO2 produced per person per day (kg) = RQ * molar O2 consumption."""
    energy_kj = _crew_energy_kj_per_day(metabolic_rate_w)
    o2_mol = (energy_kj / o2_kj_per_l) / MOLAR_VOLUME_STP_L
    co2_mol = o2_mol * rq
    return co2_mol * CO2_MOLAR_MASS_G / 1000.0


def per_capita_food_dry_kg(metabolic_rate_w=METABOLIC_RATE_W,
                           density_kcal_per_g=FOOD_ENERGY_DENSITY_KCAL_PER_G):
    """Dry food mass per person per day (kg), from caloric need / energy density."""
    energy_kcal = _crew_energy_kj_per_day(metabolic_rate_w) / KJ_PER_KCAL
    return energy_kcal / density_kcal_per_g / 1000.0


def per_capita_water_kg(intake=WATER_INTAKE_KG_PER_DAY,
                        metabolic_credit=METABOLIC_WATER_KG_PER_DAY):
    """Net potable water demand per person per day (intake minus metabolic water)."""
    return intake - metabolic_credit


@dataclass(frozen=True)
class ResourceTotals:
    n_crew: int
    days: int
    o2_kg: float
    co2_kg: float
    food_dry_kg: float
    water_kg: float

    @property
    def per_capita_day(self):
        """Re-normalize totals back to one person for one day (scale-invariance check)."""
        denom = self.n_crew * self.days
        return ResourceTotals(1, 1,
                              self.o2_kg / denom, self.co2_kg / denom,
                              self.food_dry_kg / denom, self.water_kg / denom)


def simulate(n_crew, days=1):
    """Aggregate closed-loop crew resource demand over `days` for `n_crew` people."""
    if n_crew <= 0 or days <= 0:
        raise ValueError("n_crew and days must be positive")
    scale = n_crew * days
    return ResourceTotals(
        n_crew=n_crew, days=days,
        o2_kg=per_capita_o2_kg() * scale,
        co2_kg=per_capita_co2_kg() * scale,
        food_dry_kg=per_capita_food_dry_kg() * scale,
        water_kg=per_capita_water_kg() * scale,
    )


@dataclass(frozen=True)
class OxygenBalance:
    n_crew: int
    crop_fraction: float
    crew_o2_kg: float
    plant_o2_kg: float

    @property
    def net_o2_kg(self):
        return self.plant_o2_kg - self.crew_o2_kg

    @property
    def overproduction(self):
        return self.net_o2_kg > 0


def oxygen_balance(n_crew, crop_fraction=1.0,
                   overproduction_factor=PLANT_O2_OVERPRODUCTION_FACTOR):
    """Closed-loop O2 balance: photosynthetic plant O2 vs crew O2 demand.

    `crop_fraction` in [0, 1] is the share of crew calories grown photosynthetically.
    Full closure (1.0) OVER-produces O2 (net > 0) -> the Mars One oxygen-poisoning hazard;
    break-even is at crop_fraction = 1 / overproduction_factor.
    """
    if n_crew <= 0:
        raise ValueError("n_crew must be positive")
    if not 0.0 <= crop_fraction <= 1.0:
        raise ValueError("crop_fraction must be in [0, 1]")
    crew_o2 = per_capita_o2_kg() * n_crew
    plant_o2 = crew_o2 * overproduction_factor * crop_fraction
    return OxygenBalance(n_crew, crop_fraction, crew_o2, plant_o2)
