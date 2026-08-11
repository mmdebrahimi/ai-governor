"""Civic-education / shared-identity model (family mars-gov-civic-education).

Operationalizes the "thin unity, thick pluralism" design (docs/civic_education_identity.md): a NARROW
mandatory civic core (survival interdependence, rule of law, the governance system, a common language, a
shared factual baseline) + WIDE freedom on everything else (origin culture, religion, personal values).

KEY STRUCTURAL INSIGHT (reuse, not new): a curriculum that "instills values" IS agenda-setting at the
identity level — structurally identical to the AI advisor curating a policy menu. So the SAME anti-capture
primitives apply: the curriculum-capture audit here is the value-domain analogue of
governance.exogenous_preferences.exogenous_review — it detects whether one source (founder/faction) has
captured the mandatory core, INDEPENDENTLY of cohesion (so high cohesion cannot mask capture — the
"Company Town" failure mode). Deterministic; no RNG.

Two failure modes, both divisions:
  - FRAGMENTATION ("Little Earths") — too little shared identity; cohesion below floor.
  - MONOCULTURE  ("Company Town")  — too much enforced sameness OR a captured core; pluralism/dissent lost.
A HEALTHY curriculum avoids both.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

CORE_MAX = 5            # "thin core": at most this many mandatory civic modules
COH_MIN = 0.60          # cohesion floor (below -> fragmentation)
PLU_MIN = 0.50          # pluralism floor (below -> monoculture)
CAPTURE_THRESHOLD = 0.50  # >this share of the CORE from one source -> capture (company-town)
TARGET_TRADITIONS = 4   # elective breadth that saturates the pluralism score
COERCION_THRESHOLD = 0.60  # employer/resource dependence above this VOIDS formal dissent (2026-06-06 review)

HEALTHY = "healthy"
FRAGMENTATION = "fragmentation"
MONOCULTURE = "monoculture"


@dataclass(frozen=True)
class CivicCurriculum:
    core_modules: tuple        # ((topic, source), ...) -- the MANDATORY thin core
    elective_traditions: int   # distinct origin-traditions represented in electives (pluralism breadth)
    dissent_allowed: bool      # is dissent FORMALLY permitted (no de-jure penalty)?
    cross_cutting: float       # 0..1 — degree work/housing mixes origin groups (contact theory)
    economic_dependence: float = 0.0  # 0..1 — voter dependence on a single employer/resource gatekeeper.
    #   COERCION CHANNEL (2026-06-06 review): in a company town, formal dissent can be socially/economically
    #   FALSE. High dependence voids `dissent_allowed` -> see `effective_dissent`.
    practically_required: tuple = ()  # ((topic, source), ...) — FORMALLY elective but required in practice
    #   (credential/employment/status gate). CONTROL-SURFACE channel (2026-06-06 review issue 1): capture
    #   can be laundered through required-electives/rituals even when the declared core looks diverse.

    def __post_init__(self):
        if not 0.0 <= self.cross_cutting <= 1.0:
            raise ValueError("cross_cutting must be in [0,1]")
        if not 0.0 <= self.economic_dependence <= 1.0:
            raise ValueError("economic_dependence must be in [0,1]")
        if self.elective_traditions < 0:
            raise ValueError("elective_traditions must be non-negative")
        if not isinstance(self.practically_required, tuple):
            raise ValueError("practically_required must be a tuple")

    @property
    def core_size(self):
        return len(self.core_modules)

    @property
    def core_present(self):
        return self.core_size > 0

    @property
    def effective_dissent(self):
        """Dissent is real only if FORMALLY allowed AND not economically coerced. A company-town with
        high employer/resource dependence makes formally-permitted dissent practically false."""
        return self.dissent_allowed and self.economic_dependence < COERCION_THRESHOLD


def cohesion_index(curr):
    """Shared-identity strength: a present core + cross-cutting ties (contact theory). 0..1."""
    return (0.5 if curr.core_present else 0.0) + 0.5 * curr.cross_cutting


def pluralism_index(curr):
    """Retained diversity: elective breadth x dissent, penalized when a THICK mandated core crowds out
    electives (the over-mandation that pushes toward monoculture). 0..1."""
    breadth = min(1.0, curr.elective_traditions / TARGET_TRADITIONS)
    dissent = 1.0 if curr.effective_dissent else 0.4   # EFFECTIVE (coercion-aware), not merely formal
    overmandation = max(0.0, 1.0 - 0.2 * max(0, curr.core_size - CORE_MAX))
    return breadth * dissent * overmandation


def core_source_concentration(curr):
    """Max share of the mandatory core authored by any single source. 0 when no core."""
    if not curr.core_present:
        return 0.0
    counts = Counter(src for _, src in curr.core_modules)
    return max(counts.values()) / curr.core_size


def control_surface(curr):
    """The FULL mandatory-in-practice surface: the declared core PLUS practically-required modules
    (formally elective but required for credential/employment/status). 2026-06-06 review issue 1."""
    return tuple(curr.core_modules) + tuple(curr.practically_required)


def control_surface_concentration(curr):
    """Max single-source share of the whole control surface. 0 when the surface is empty."""
    surface = control_surface(curr)
    if not surface:
        return 0.0
    counts = Counter(src for _, src in surface)
    return max(counts.values()) / len(surface)


def capture_detected(curr):
    """Curriculum-capture audit (value-domain analogue of exogenous_review's WHOLE-GRID fix): one source
    dominating the CONTROL SURFACE (core + practically-required), NOT just the declared core, is capture —
    checked INDEPENDENTLY of cohesion so high cohesion cannot mask it, and INDEPENDENTLY of a clean-looking
    core so ideology laundered through required-electives/rituals is still caught."""
    surface = control_surface(curr)
    return bool(surface) and control_surface_concentration(curr) > CAPTURE_THRESHOLD


@dataclass(frozen=True)
class CivicAssessment:
    cohesion: float
    pluralism: float
    captured: bool
    classification: str


def classify(curr):
    """Order matters: capture (insidious, cohesion-masked) checked FIRST, then fragmentation, then the
    thick-mandation/dissent monoculture."""
    coh, plu, cap = cohesion_index(curr), pluralism_index(curr), capture_detected(curr)
    if cap:
        cls = MONOCULTURE                       # company-town capture, even if cohesion is high
    elif coh < COH_MIN:
        cls = FRAGMENTATION
    elif plu < PLU_MIN or not curr.effective_dissent:
        cls = MONOCULTURE                       # incl. coerced dissent (economic company-town)
    else:
        cls = HEALTHY
    return CivicAssessment(cohesion=coh, pluralism=plu, captured=cap, classification=cls)


def robust_healthy(curr):
    """Sensitivity check (2026-06-06 review alt 2): HEALTHY is fragile if a small perturbation (one fewer
    elective tradition, 0.1 less cross-cutting, +0.1 economic dependence) tips it out of HEALTHY. Returns
    True only for ROBUST-healthy curricula — guards against single-point-classification false confidence."""
    import dataclasses
    if classify(curr).classification != HEALTHY:
        return False
    perturbed = dataclasses.replace(
        curr,
        elective_traditions=max(0, curr.elective_traditions - 1),
        cross_cutting=max(0.0, curr.cross_cutting - 0.1),
        economic_dependence=min(1.0, curr.economic_dependence + 0.1),
    )
    return classify(perturbed).classification == HEALTHY


def division_risk(curr, scarcity=0.0):
    """0..1 risk of social division. Structural risk rises with low cohesion (fragmentation), low
    pluralism, and capture; SCARCITY amplifies it (couples to the resource/connection families — the
    import-dependent era is the highest-division-risk window). Capture raises risk even at high cohesion."""
    if not 0.0 <= scarcity <= 1.0:
        raise ValueError("scarcity must be in [0,1]")
    coh, plu = cohesion_index(curr), pluralism_index(curr)
    structural = 0.4 * (1.0 - coh) + 0.3 * (1.0 - plu) + 0.3 * (1.0 if capture_detected(curr) else 0.0)
    return min(1.0, structural * (1.0 + scarcity))
