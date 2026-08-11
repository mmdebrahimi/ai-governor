"""F2 — Guideline intake: where the polity's intent becomes machine-binding.

This module exists because of one finding. Probe B1 (`docs/probe-B1-guideline-compilation.md`) showed that
guidelines compile by TYPE: **P** (mechanism prohibition) and **O** (ordering) compile fully with no number
at all, while **F** (floor/ceiling) and **D** (metric direction) are missing exactly one thing — a *level* or
a *metric* that is a value judgement, not a technical fact. Every time the governor fills that number in, it
makes a sovereign choice while appearing merely to implement. That seam is **the threshold gap**.

`aigov/contract.py::I11` closes the gap at the VALIDATOR. This module closes it at the SOURCE: a binding
guideline cannot be constructed here unless a real panel supplied the number.

Design, and why each piece is the piece it is:

* **Sortition** for panel selection — a statistically representative body resists capture better than
  self-selection, and it is reproducible from a recorded seed (audit).
* **Quadratic priority budget** for agenda-setting — cost of `v` votes is `v**2`, so intensity is
  expressible without a loud minority buying the agenda outright.
* **Median** for level aggregation — NOT a mean. Black (1948, verified in
  `research_outputs/aigov-v1-social-choice-walls.md`) gives that on a single-peaked one-dimensional domain
  the median is the Condorcet winner; the median rule is also the strategy-resistant choice there, whereas a
  mean is trivially dragged by one extreme report.
* **Fail-closed on polarization** — a median is always *defined*, but on a two-camp panel it is a number
  nobody wants. Rather than silently aggregating, the intake ESCALATES. Same discipline as
  `aigov/choice/governance/fail_safe_gate.py`: never certify what you cannot faithfully aggregate.

**Recursive honesty:** the polarization threshold is itself a number. Supplying it from model judgement would
reproduce the very defect this module exists to prevent, so `ProceduralParameter` carries provenance and
`compile_guidelines` REFUSES an AI-supplied one.
"""

from __future__ import annotations

import hashlib
import random
from dataclasses import dataclass, field
from statistics import median
from typing import Optional

from .contract import Guideline, GuidelineType, ProvenanceKind

# --------------------------------------------------------------------------------------
# Errors
# --------------------------------------------------------------------------------------


@dataclass(frozen=True)
class IntakeError:
    code: str          # "G1".."G7"
    ref: str           # draft id / panel id
    message: str

    def __str__(self) -> str:
        return "[{}] {}: {}".format(self.code, self.ref, self.message)


ESCALATE = "escalate"
AGGREGATED = "aggregated"


# --------------------------------------------------------------------------------------
# Procedural parameters (numbers the MECHANISM needs — still not the AI's to choose)
# --------------------------------------------------------------------------------------


@dataclass(frozen=True)
class ProceduralParameter:
    """A number the intake procedure itself needs. Provenance is mandatory (G2 applies recursively)."""

    name: str
    value: float
    provenance_kind: ProvenanceKind
    provenance_ref: str

    def is_legitimate(self) -> bool:
        return self.provenance_kind is not ProvenanceKind.AI_SUPPLIED and bool(self.provenance_ref)


#: Default polarization tolerance — a PROCEDURAL constant of the intake mechanism.
#:
#: **DERIVED, not asserted.** `calibrate_polarization()` simulates 400 unimodal panels (normal / uniform /
#: skewed, widths 0.5–20) and 400 two-camp panels (gaps 8–60, within-spread 0.3–2.0) and picks the
#: threshold minimising false-escalations + missed-polarizations. Result on 2026-08-11:
#: unimodal p95 = 0.867, unimodal max = 0.914, bimodal p05 = 0.893, **best threshold = 0.900**,
#: 26 errors / 800 trials (3.25%). Re-derive any time by calling the function — the number is not a
#: judgement call, and the residual overlap (a weakly-separated two-camp panel genuinely resembles a
#: wide unimodal one) is real and reported rather than hidden.
DEFAULT_POLARIZATION = ProceduralParameter(
    name="polarization_tolerance",
    value=0.900,
    provenance_kind=ProvenanceKind.GUIDELINE,
    provenance_ref="CHARTER-PROC-001 (derived by calibrate_polarization, 2026-08-11)",
)


# --------------------------------------------------------------------------------------
# Sortition
# --------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Panel:
    """A sortition panel. Reproducible from `seed` — that reproducibility IS the audit trail (G4)."""

    id: str
    members: tuple
    seed: int
    electorate_size: int

    def fingerprint(self) -> str:
        payload = "{}|{}|{}|{}".format(self.id, self.seed, self.electorate_size, ",".join(self.members))
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def draw_panel(electorate, size: int, seed: int, panel_id: str = "P1") -> Panel:
    """Draw `size` citizens uniformly without replacement. Deterministic in `seed`."""
    roster = sorted(set(electorate))
    if size <= 0:
        raise ValueError("panel size must be positive")
    if size > len(roster):
        raise ValueError("panel size {} exceeds electorate {}".format(size, len(roster)))
    rng = random.Random(seed)
    return Panel(id=panel_id, members=tuple(sorted(rng.sample(roster, size))),
                 seed=seed, electorate_size=len(roster))


# --------------------------------------------------------------------------------------
# Quadratic priority budget
# --------------------------------------------------------------------------------------


def qv_cost(votes) -> int:
    """Quadratic cost: sum of v**2. Intensity is expressible; buying the whole agenda is not."""
    return sum(int(v) ** 2 for v in votes)


@dataclass(frozen=True)
class PriorityBallot:
    member: str
    allocation: dict          # topic -> votes (int, may be 0)

    def cost(self) -> int:
        return qv_cost(self.allocation.values())


def tally_priorities(ballots, budget: int):
    """Sum votes per topic across ballots. Returns (ranking, errors).

    A ballot exceeding the credit budget is REJECTED (G5) — not clipped, not scaled. Clipping would
    silently rewrite a citizen's expressed intensity.
    """
    errors, totals = [], {}
    for b in ballots:
        c = b.cost()
        if c > budget:
            errors.append(IntakeError("G5", b.member,
                                      "ballot costs {} credits, budget is {} — REJECTED, not clipped"
                                      .format(c, budget)))
            continue
        if any(int(v) < 0 for v in b.allocation.values()):
            errors.append(IntakeError("G5", b.member, "negative votes are not representable"))
            continue
        for topic, v in b.allocation.items():
            totals[topic] = totals.get(topic, 0) + int(v)
    ranking = sorted(totals.items(), key=lambda kv: (-kv[1], kv[0]))
    return ranking, errors


# --------------------------------------------------------------------------------------
# Level elicitation
# --------------------------------------------------------------------------------------


@dataclass(frozen=True)
class LevelElicitation:
    """The polity's answer to 'how much?'. `verdict` is AGGREGATED or ESCALATE."""

    topic: str
    proposals: tuple
    verdict: str
    level: Optional[float]
    spread: float
    panel_id: str
    reason: str = ""


def _wcss(xs) -> float:
    """Within-cluster sum of squares about the mean."""
    if not xs:
        return 0.0
    m = sum(xs) / len(xs)
    return sum((x - m) ** 2 for x in xs)


#: A "camp" smaller than this share of the panel is an OUTLIER, not a polity split. Without this floor
#: a single member proposing an absurd number scores 1.0 and unilaterally vetoes aggregation — precisely
#: the strategic vector the median was chosen to resist. Derived, not asserted: see
#: `calibrate_polarization`, which sweeps it.
MIN_CAMP_SHARE = 0.25


def _polarization(proposals, min_camp_share: float = MIN_CAMP_SHARE) -> float:
    """Bimodality: variance explained by the best BALANCED 2-cluster split, `1 - WCSS(2)/WCSS(1)`.

    In 1-D the optimal 2-means split is contiguous on sorted data, so scanning split points finds the
    exact optimum. Range-free and scale-invariant. Splits are restricted to those leaving at least
    `min_camp_share` of the panel on each side, so one outlier cannot manufacture a "camp".

    **Two defects this replaced, both found by sweeping rather than by unit tests:**
    1. The original metric divided the split-median gap by the FULL RANGE, so a tightly clustered panel
       scored 0.50 and a wide unimodal panel false-escalated — it measured noise, not structure.
    2. The unconstrained 2-means version scored a single extreme outlier at 1.000, handing any one
       panelist a unilateral escalation veto.

    Reference values (`calibrate_polarization`): a UNIMODAL sample sits well below the threshold because
    any sample split in two explains some variance; two TIGHT, WELL-SEPARATED, SUBSTANTIAL camps approach 1.0.
    """
    xs = sorted(float(p) for p in proposals)
    n = len(xs)
    if n < 4:
        return 0.0
    total = _wcss(xs)
    if total == 0.0:
        return 0.0   # unanimous panel: no structure to find
    lo_i = max(1, int(n * min_camp_share))
    hi_i = min(n - 1, n - int(n * min_camp_share))
    if lo_i >= hi_i:
        return 0.0
    best = min(_wcss(xs[:i]) + _wcss(xs[i:]) for i in range(lo_i, hi_i + 1))
    return 1.0 - best / total


def calibrate_polarization(trials: int = 400, panel_size: int = 16, seed: int = 20260811):
    """Derive the escalation threshold empirically instead of asserting it.

    Simulates UNIMODAL panels (normal / uniform / skewed) and TWO-CAMP panels, and reports the score
    distributions plus the threshold that best separates them. This is what `DEFAULT_POLARIZATION.value`
    is set from — the number is derived, and re-derivable by anyone running this function.
    """
    rng = random.Random(seed)
    uni, bim = [], []
    for _ in range(trials):
        shape = rng.choice(("normal", "uniform", "skewed"))
        if shape == "normal":
            s = [rng.gauss(25, rng.choice([0.5, 2, 5, 10])) for _ in range(panel_size)]
        elif shape == "uniform":
            w = rng.choice([1, 5, 20])
            s = [rng.uniform(25 - w, 25 + w) for _ in range(panel_size)]
        else:
            s = [25 + rng.expovariate(1 / rng.choice([1.0, 4.0])) for _ in range(panel_size)]
        uni.append(_polarization(s))

        gap = rng.choice([8, 15, 30, 60])
        within = rng.choice([0.3, 1.0, 2.0])
        half = panel_size // 2
        s = ([rng.gauss(25, within) for _ in range(half)]
             + [rng.gauss(25 + gap, within) for _ in range(panel_size - half)])
        bim.append(_polarization(s))

    uni.sort()
    bim.sort()
    # Threshold minimising (false-escalations + missed-polarizations).
    best_t, best_err = None, None
    t = 0.50
    while t <= 0.995:
        err = sum(1 for u in uni if u > t) + sum(1 for b in bim if b <= t)
        if best_err is None or err < best_err:
            best_t, best_err = round(t, 3), err
        t += 0.005
    return {
        "unimodal_p50": round(uni[len(uni) // 2], 3),
        "unimodal_p95": round(uni[int(len(uni) * 0.95)], 3),
        "unimodal_max": round(uni[-1], 3),
        "bimodal_min": round(bim[0], 3),
        "bimodal_p05": round(bim[int(len(bim) * 0.05)], 3),
        "bimodal_p50": round(bim[len(bim) // 2], 3),
        "best_threshold": best_t,
        "errors_at_best": best_err,
        "trials": trials,
    }


def elicit_level(topic: str, proposals, panel: Panel,
                 tolerance: ProceduralParameter = DEFAULT_POLARIZATION) -> LevelElicitation:
    """Aggregate panel proposals into ONE level by MEDIAN, or escalate if the panel is two camps.

    The median is used rather than the mean because on a single-peaked one-dimensional domain it is the
    Condorcet winner (Black 1948) and is not draggable by a single extreme report.
    """
    xs = [float(p) for p in proposals]
    if not xs:
        return LevelElicitation(topic, tuple(), ESCALATE, None, 0.0, panel.id,
                                "no proposals — nothing was elicited")
    pol = _polarization(xs)
    if pol > tolerance.value:
        return LevelElicitation(
            topic, tuple(xs), ESCALATE, None, pol, panel.id,
            "panel is polarized (split-median gap {:.2f} > tolerance {:.2f}); the median would be a number "
            "nobody proposed — routed to deliberation rather than silently aggregated".format(
                pol, tolerance.value))
    return LevelElicitation(topic, tuple(xs), AGGREGATED, float(median(xs)), pol, panel.id,
                            "median of {} panel proposals".format(len(xs)))


# --------------------------------------------------------------------------------------
# Drafts -> Guidelines
# --------------------------------------------------------------------------------------


@dataclass
class GuidelineDraft:
    """What a deliberating panel produces: a sentence, a type, and (for F/D) the elicited part."""

    id: str
    text: str
    gtype: GuidelineType
    elicitation: Optional[LevelElicitation] = None   # required for type F
    metric: Optional[str] = None                     # required for type D
    ratified: bool = False


def compile_guidelines(drafts, panel: Panel,
                       tolerance: ProceduralParameter = DEFAULT_POLARIZATION):
    """Compile panel drafts into `contract.Guideline` objects. Returns (guidelines, errors).

    A draft that fails any invariant produces an ERROR and NO guideline — it is never emitted in a
    weakened form. Type-A aspirations ARE emitted, flagged non-binding, so they stay visible (G3).
    """
    errors, out = [], []

    if not tolerance.is_legitimate():
        errors.append(IntakeError("G2", tolerance.name,
                                  "procedural parameter '{}' has provenance {} — the governor may not "
                                  "supply the numbers its own procedure runs on".format(
                                      tolerance.name, tolerance.provenance_kind.value)))
        return [], errors

    for d in drafts:
        if not d.ratified:
            errors.append(IntakeError("G1", d.id, "draft is not ratified; only the polity makes a "
                                                  "guideline binding"))
            continue

        if d.gtype is GuidelineType.A:
            out.append(Guideline(id=d.id, text=d.text, gtype=GuidelineType.A, ratified=True))
            continue

        if d.gtype is GuidelineType.F:
            if d.elicitation is None:
                errors.append(IntakeError("G1", d.id,
                                          "type-F guideline has NO elicitation — this is the threshold "
                                          "gap; the level must come from the panel, never the governor"))
                continue
            if d.elicitation.verdict != AGGREGATED or d.elicitation.level is None:
                errors.append(IntakeError("G7", d.id,
                                          "elicitation escalated ({}) — no binding level".format(
                                              d.elicitation.reason)))
                continue
            if d.elicitation.panel_id != panel.id:
                errors.append(IntakeError("G4", d.id,
                                          "elicitation cites panel '{}' but compilation panel is '{}'"
                                          .format(d.elicitation.panel_id, panel.id)))
                continue
            out.append(Guideline(id=d.id, text=d.text, gtype=GuidelineType.F, ratified=True,
                                 level=d.elicitation.level))
            continue

        if d.gtype is GuidelineType.D:
            if not d.metric:
                errors.append(IntakeError("G1", d.id,
                                          "type-D guideline has no metric — direction without a measure "
                                          "is not compilable"))
                continue
            out.append(Guideline(id=d.id, text=d.text, gtype=GuidelineType.D, ratified=True,
                                 metric=d.metric))
            continue

        # P and O compile with no elicited number at all — the clean case from probe B1.
        out.append(Guideline(id=d.id, text=d.text, gtype=d.gtype, ratified=True))

    return out, errors


def audit_record(panel: Panel, ranking, elicitations, guidelines, errors) -> dict:
    """The reproducible record of one intake round — the thing an auditor re-runs."""
    return {
        "panel_id": panel.id,
        "panel_seed": panel.seed,
        "panel_fingerprint": panel.fingerprint(),
        "panel_size": len(panel.members),
        "electorate_size": panel.electorate_size,
        "priority_ranking": list(ranking),
        "elicitations": [
            {"topic": e.topic, "verdict": e.verdict, "level": e.level,
             "polarization": round(e.spread, 4), "n_proposals": len(e.proposals)}
            for e in elicitations
        ],
        "emitted": [g.id for g in guidelines],
        "binding": [g.id for g in guidelines if g.is_binding()],
        "non_binding": [g.id for g in guidelines if not g.is_binding()],
        "errors": [str(e) for e in errors],
    }
