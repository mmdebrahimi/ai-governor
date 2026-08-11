"""Earth<->Mars connection model (family mars-gov-connection-model).

Parameterizes the connection as governance-sim INPUTS (docs/earth_mars_connection_scenarios.md):
  - latency  : round-trip light-time (6..44 min) -- no real-time control, ever.
  - blackout : ~2-week comms outage every ~26 cycles at solar conjunction -> governance must complete
               decision cycles with ZERO Earth contact (the caretaker/min-survival primitive, M1).
  - resupply : transfer windows every ~26 cycles; import food per capita ramps DOWN as local crop
               capacity grows (umbilical -> tether -> handshake).

The load-bearing output is `resupplier_veto_survivable`: while the colony cannot feed itself from local
crop capacity, whoever controls resupply holds a SURVIVAL VETO over governance (the resupplier-as-coercer
adversary, docs/voting_threat_model.md). The veto is LIVE during the import-dependent phase and VOID once
self-sufficient. All physics-grounded constants; deterministic (no RNG).
"""
from __future__ import annotations

import math
from dataclasses import dataclass

from models.resource_sim import per_capita_food_dry_kg

SYNODIC_CYCLES = 26              # resupply-window + conjunction cadence (~26 months)
BLACKOUT_DURATION = 2           # conjunction comms outage length (cycles)
LATENCY_MIN_MIN = 6.0           # round-trip light-time at closest approach
LATENCY_MAX_MIN = 44.0          # round-trip light-time at farthest

BASE_CROP_CAPACITY_PC = 0.30    # early local food production per capita (below demand)
CAPACITY_GROWTH_PER_CYCLE = 0.02  # greenhouse buildout: local capacity grows over time
BASE_IMPORT_PC = 0.35           # Earth resupply food per capita when fully import-dependent


def demand_pc():
    return per_capita_food_dry_kg()


def is_blackout(cycle, every=SYNODIC_CYCLES, duration=BLACKOUT_DURATION):
    """True during the conjunction comms outage -> NO Earth contact this cycle."""
    if cycle < 0:
        raise ValueError("cycle must be non-negative")
    return (cycle % every) < duration


def round_trip_latency_min(cycle):
    """Round-trip light-time oscillating 6..44 min over the synodic cycle (closest..farthest)."""
    if cycle < 0:
        raise ValueError("cycle must be non-negative")
    phase = (cycle % SYNODIC_CYCLES) / SYNODIC_CYCLES
    swing = 0.5 - 0.5 * math.cos(2 * math.pi * phase)     # 0..1..0
    return LATENCY_MIN_MIN + (LATENCY_MAX_MIN - LATENCY_MIN_MIN) * swing


def crop_capacity_pc(cycle, growth=CAPACITY_GROWTH_PER_CYCLE, base=BASE_CROP_CAPACITY_PC):
    """Local food production per capita, growing as the colony builds out greenhouses."""
    if cycle < 0:
        raise ValueError("cycle must be non-negative")
    return base * (1.0 + growth * cycle)


def import_needed_pc(cycle, **kw):
    """Food per capita that MUST come from Earth this cycle (0 once self-sufficient)."""
    return max(0.0, demand_pc() - crop_capacity_pc(cycle, **kw))


def imported_food_pc(cycle, withheld=False, base_import=BASE_IMPORT_PC, **kw):
    """Food per capita actually delivered. `withheld=True` models the resupplier exercising the veto."""
    if withheld:
        return 0.0
    return min(base_import, import_needed_pc(cycle, **kw)) if import_needed_pc(cycle, **kw) > 0 else 0.0


def self_sufficient(cycle, **kw):
    """True iff local crop capacity alone meets demand (import-independent)."""
    return crop_capacity_pc(cycle, **kw) >= demand_pc()


def self_sufficiency_cycle(growth=CAPACITY_GROWTH_PER_CYCLE, base=BASE_CROP_CAPACITY_PC):
    """The first cycle at which the colony becomes self-sufficient (crop capacity >= demand)."""
    if base >= demand_pc():
        return 0
    if growth <= 0:
        return None                                       # never closes the loop
    return math.ceil((demand_pc() / base - 1.0) / growth)


def resupplier_veto_survivable(cycle, **kw):
    """Can the colony survive a WITHHELD resupply this cycle? Survivable iff self-sufficient. While
    NOT survivable, the resupplier holds a live survival veto over governance (resupplier-as-coercer)."""
    return self_sufficient(cycle, **kw)


@dataclass(frozen=True)
class ConnectionState:
    cycle: int
    earth_contact: bool          # False during conjunction blackout
    round_trip_latency_min: float
    resupply_window: bool        # a transfer window is open this cycle
    import_needed_pc: float
    self_sufficient: bool
    veto_survivable: bool        # = self_sufficient

    @property
    def phase(self):
        if self.self_sufficient:
            return "handshake"
        return "tether" if self.cycle > 0 else "umbilical"


def connection_at(cycle, **kw):
    if cycle < 0:
        raise ValueError("cycle must be non-negative")
    return ConnectionState(
        cycle=cycle,
        earth_contact=not is_blackout(cycle),
        round_trip_latency_min=round_trip_latency_min(cycle),
        resupply_window=(cycle % SYNODIC_CYCLES == 0),
        import_needed_pc=import_needed_pc(cycle, **kw),
        self_sufficient=self_sufficient(cycle, **kw),
        veto_survivable=resupplier_veto_survivable(cycle, **kw),
    )


def timeline(n_cycles, **kw):
    if n_cycles <= 0:
        raise ValueError("n_cycles must be positive")
    return [connection_at(c, **kw) for c in range(n_cycles)]
