"""Registry compositions — because a coupling is relative to WHICH colony you are running.

I3 makes every coupling bilateral: if D3 contends with D1 for power, D1 must say so too. That is
the right rule (a one-sided declaration is exactly how one department plans around a resource
another is quietly consuming), but it has a consequence that only appeared once a third department
existed: a spec's coupling list is not a property of the department alone, it is a property of the
department IN A COMPOSITION.

A D1 that names D3 is invalid in a colony without D3 — I3 rejects a reference to an absent
department. A D1 that does not name D3 is invalid in a colony with one. Both are correct; they are
answers to different questions. So the composition, not the module-level constant, is the unit, and
this module is where compositions are built.

The two-department registry is kept because it is a real (interim) colony and most of the kernel
and adversarial tests are written against it. `phase1_registry()` is the three-department world the
phase-1 terminal actually asks for: HIGH, MEDIUM and LOW central legitimacy in one colony.
"""

from __future__ import annotations

from dataclasses import replace

from .contract import Coupling, CouplingDirection
from .specs.d1_lifesupport import SPEC as _D1
from .specs.d2_economy import SPEC as _D2
from .specs.d3_fabrication import SPEC as _D3

#: Shared variables D3's machines genuinely contend for. Fabrication draws power life-support is
#: allocating, and occupies pressurized volume both other departments already contend over.
_D3_CONTENTIONS = ("power_kw", "pressurized_volume_m3")


def two_department_registry() -> list:
    """D1 (HIGH) + D2 (LOW). The interim colony; no MEDIUM-legitimacy department."""
    return [_D1, _D2]


def phase1_registry() -> list:
    """D1 (HIGH) + D2 (LOW) + D3 (MEDIUM) — the composition the phase-1 terminal requires.

    D1 is rebuilt with the mirror couplings D3's presence obliges it to declare. Built here rather
    than hard-coded into the D1 module so the two-department colony stays valid.
    """
    d1 = replace(_D1, couplings=list(_D1.couplings) + [
        Coupling("D3", var, CouplingDirection.CONTENDS) for var in _D3_CONTENTIONS
    ])
    return [d1, _D2, _D3]


def legitimacy_span(specs) -> set:
    """The set of central-legitimacy levels a registry spans. The terminal asks for all three."""
    return {s.central_legitimacy for s in specs}
