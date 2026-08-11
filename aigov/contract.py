"""The Department Contract — the AI Government's anti-theater primitive.

A department is REAL iff it can fill `DepartmentSpec` and its falsification test executes.
`validate()` turns each invariant I1-I11 (`docs/department-ontology.md` section 3) into a distinct,
individually-triggerable error, so "a department" is a checked artifact rather than an essay.

Three invariants carry the project's structural commitments:

    I8  subsidiarity  - a LOW-central-legitimacy department may not allocate quantities, only set
                        rules and prices (Hayek's knowledge problem, made mechanical)
    I9  separation    - no actor is in two of {generate, decide, verify}
    I11 threshold provenance - no numeric threshold may originate with the AI (ratified D1:
                        the AI never selects the objective). This is the seam probe B1 found where
                        an advisory AI silently becomes a sovereign one.

Ratified decisions this module encodes: D1 (AI = administrative organ), D2 (colony scale),
D3 (runnable simulation). See project_state/aigov.md.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Optional


# --------------------------------------------------------------------------------------
# Enumerations
# --------------------------------------------------------------------------------------


class VSMLayer(Enum):
    S1 = "S1"  # operations
    S2 = "S2"  # coordination
    S3 = "S3"  # control / audit
    S4 = "S4"  # intelligence
    S5 = "S5"  # identity / policy


class Legitimacy(Enum):
    """How much central administration is defensible for this department.

    HIGH   - a hard closed physical loop (few state vars, measurable, failure = death)
    MEDIUM - procedure central, judgment distributed
    LOW    - dispersed tacit knowledge; the Hayek wall applies (see I8)
    """

    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class Observability(Enum):
    DIRECT = "direct"
    ESTIMATED = "estimated"
    LATENT = "latent"


class InstrumentClass(Enum):
    RULE = "rule"
    PRICE = "price"
    QUANTITY_ALLOCATION = "quantity_allocation"


class Reversibility(Enum):
    REVERSIBLE = "reversible"
    COSTLY = "costly"
    IRREVERSIBLE = "irreversible"


class RatificationClass(Enum):
    SIMPLE = "simple"
    SUPERMAJORITY = "supermajority"


class OnViolation(Enum):
    FAIL_CLOSED = "fail_closed"
    OPTIMIZE_THROUGH = "optimize_through"  # representable only so I5 can reject it


class ConstraintSource(Enum):
    CONSTITUTION = "constitution"
    PHYSICS = "physics"
    LAW = "law"


class CouplingDirection(Enum):
    READS = "reads"
    WRITES = "writes"
    CONTENDS = "contends"


class Role(Enum):
    GENERATE = "generate"
    DECIDE = "decide"
    VERIFY = "verify"


class GuidelineType(Enum):
    """The compilability partition found by probe B1.

    P - mechanism prohibition  ("the state may not do X")        -> compiles fully
    O - ordering / monotonicity ("more A implies more B")        -> compiles fully
    F - floor / ceiling with a level                             -> needs an ELICITED level
    D - direction on a metric                                    -> needs a metric + gaming model
    A - aspiration                                               -> never binding
    """

    P = "P"
    O = "O"
    F = "F"
    D = "D"
    A = "A"


class ProvenanceKind(Enum):
    GUIDELINE = "guideline"
    PHYSICAL_CONSTANT = "physical_constant"
    AI_SUPPLIED = "ai_supplied"  # representable only so I11 can reject it


class Direction(Enum):
    RAISE = "raise"
    LOWER = "lower"
    HOLD_WITHIN = "hold_within"


# --------------------------------------------------------------------------------------
# Value types
# --------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Provenance:
    kind: ProvenanceKind
    ref: str  # guideline id, or the name of the physical constant


@dataclass(frozen=True)
class Guideline:
    """A guideline produced by the polity. `level` / `metric` are the ELICITED parts.

    The intake mechanism must supply `level` for type F and `metric` for type D, because those are
    the values an AI would otherwise fill in — which is exactly the threshold gap (probe B1).
    """

    id: str
    text: str
    gtype: GuidelineType
    ratified: bool = False
    level: Optional[float] = None
    metric: Optional[str] = None

    def is_binding(self) -> bool:
        return self.ratified and self.gtype is not GuidelineType.A

    def elicitation_complete(self) -> bool:
        if self.gtype is GuidelineType.F:
            return self.level is not None
        if self.gtype is GuidelineType.D:
            return bool(self.metric)
        return True


@dataclass(frozen=True)
class StateVar:
    name: str
    unit: str
    observability: Observability
    owner_dept: str


@dataclass(frozen=True)
class Instrument:
    name: str
    iclass: InstrumentClass
    bounds: tuple
    latency_cycles: int
    reversibility: Reversibility
    ratification_class: RatificationClass


@dataclass(frozen=True)
class ObjectiveRef:
    """An objective the department is GIVEN. It never authors one (D1 / I1)."""

    guideline_id: str
    metric: str
    direction: Direction
    threshold: Optional[float] = None
    threshold_provenance: Optional[Provenance] = None


@dataclass(frozen=True)
class Constraint:
    name: str
    predicate: str
    source: ConstraintSource
    on_violation: OnViolation = OnViolation.FAIL_CLOSED
    threshold: Optional[float] = None
    threshold_provenance: Optional[Provenance] = None
    guideline_id: Optional[str] = None


@dataclass(frozen=True)
class Coupling:
    other_dept: str
    shared_var: str
    direction: CouplingDirection
    arbiter: str = "D13"


@dataclass(frozen=True)
class Metric:
    name: str
    formula: str
    gaming_model: str  # I4: how this metric will be gamed. Empty => validation error.
    rotation_policy: str


@dataclass(frozen=True)
class FailureMode:
    name: str
    detector: str
    escalation_target: str


@dataclass(frozen=True)
class Rule:
    """A machine-emitted rule, linted against Fuller's eight desiderata of legality (I10)."""

    id: str
    applies_to_class: str  # a class of persons/situations, not a named individual
    published: bool
    effective_cycle: int
    predicate: str
    enforcement_ref: str
    sunset_cycles: int


@dataclass
class DepartmentSpec:
    id: str
    vsm_layer: VSMLayer
    central_legitimacy: Legitimacy
    state_vars: list = field(default_factory=list)
    instruments: list = field(default_factory=list)
    objectives_received: list = field(default_factory=list)
    hard_constraints: list = field(default_factory=list)
    couplings: list = field(default_factory=list)
    metrics: list = field(default_factory=list)
    failure_modes: list = field(default_factory=list)
    rules: list = field(default_factory=list)
    falsification_test: Optional[Callable[[], bool]] = None
    sunset_cycles: int = 0
    roles: frozenset = frozenset()


@dataclass(frozen=True)
class Error:
    code: str  # "I1".."I11", or "FULLER-<n>"
    dept: str
    message: str

    def __str__(self) -> str:
        return "[{}] {}: {}".format(self.code, self.dept, self.message)


# --------------------------------------------------------------------------------------
# Fuller's eight desiderata of legality (I10)
# --------------------------------------------------------------------------------------

#: Which Fuller checks are genuinely mechanical vs. structurally shallow. Recorded so the
#: guarantee is never overstated: checks 2, 3, 5, 7, 8 are real structural properties of the
#: Rule record; checks 1, 4, 6 are SHALLOW (they test the shape of a declaration, not its content)
#: and are marked so a reader does not mistake them for semantic verification.
FULLER_DEPTH = {
    1: "shallow",   # generality      - we can only check it names a class, not that the class is general
    2: "mechanical",  # promulgation
    3: "mechanical",  # non-retroactivity
    4: "shallow",   # clarity         - non-empty predicate; not a semantic clarity judgment
    5: "mechanical",  # non-contradiction (registry-level, pairwise)
    6: "shallow",   # possibility of compliance - rejects only literally-unsatisfiable predicates
    7: "mechanical",  # constancy (sunset > 0)
    8: "mechanical",  # congruence (an enforcement reference exists)
}

_UNSATISFIABLE = {"false", "0 == 1", "never"}


def fuller_lint(rule: Rule, current_cycle: int = 0, dept: str = "?") -> list:
    """Lint one Rule against Fuller's eight desiderata. Returns a list of Error."""
    errs = []
    if not rule.applies_to_class or rule.applies_to_class.startswith("person:"):
        errs.append(Error("FULLER-1", dept,
                          "rule {} is not general (targets a named individual)".format(rule.id)))
    if not rule.published:
        errs.append(Error("FULLER-2", dept, "rule {} is not promulgated".format(rule.id)))
    if rule.effective_cycle < current_cycle:
        errs.append(Error("FULLER-3", dept,
                          "rule {} is retroactive (effective {} < current {})".format(
                              rule.id, rule.effective_cycle, current_cycle)))
    if not rule.predicate.strip():
        errs.append(Error("FULLER-4", dept, "rule {} has no predicate (unclear)".format(rule.id)))
    if rule.predicate.strip().lower() in _UNSATISFIABLE:
        errs.append(Error("FULLER-6", dept,
                          "rule {} cannot possibly be complied with".format(rule.id)))
    if rule.sunset_cycles <= 0:
        errs.append(Error("FULLER-7", dept,
                          "rule {} has no sunset (not constant/revisable)".format(rule.id)))
    if not rule.enforcement_ref.strip():
        errs.append(Error("FULLER-8", dept,
                          "rule {} has no enforcement reference (incongruent)".format(rule.id)))
    return errs


# --------------------------------------------------------------------------------------
# Invariants I1-I11 (single-spec)
# --------------------------------------------------------------------------------------


def _check_threshold_provenance(dept, label, threshold, prov, guidelines):
    """I11: a numeric threshold must come from a ratified guideline or a physical constant."""
    errs = []
    if threshold is None:
        return errs
    if prov is None:
        errs.append(Error("I11", dept,
                          "{} carries threshold {} with NO provenance (AI-supplied thresholds are "
                          "how an advisory AI becomes sovereign)".format(label, threshold)))
        return errs
    if prov.kind is ProvenanceKind.AI_SUPPLIED:
        errs.append(Error("I11", dept,
                          "{} threshold {} is AI_SUPPLIED; only a ratified guideline or a physical "
                          "constant may set a value".format(label, threshold)))
    elif prov.kind is ProvenanceKind.GUIDELINE:
        g = guidelines.get(prov.ref)
        if g is None or not g.is_binding():
            errs.append(Error("I11", dept,
                              "{} threshold {} cites guideline '{}' which is not a binding ratified "
                              "guideline".format(label, threshold, prov.ref)))
        elif g.level is not None and g.level != threshold:
            errs.append(Error("I11", dept,
                              "{} threshold {} does not match the elicited level {} of guideline "
                              "'{}'".format(label, threshold, g.level, prov.ref)))
    return errs


def validate(spec: DepartmentSpec, guidelines) -> list:
    """Validate one DepartmentSpec. Returns a list of Error (empty == valid).

    `guidelines` is a mapping {guideline_id: Guideline} of the ratified guideline set.
    I3 (bilateral coupling) and cross-department contradiction are registry-level; see
    `validate_registry`.
    """
    if not isinstance(guidelines, dict):
        guidelines = {g.id: g for g in guidelines}
    d = spec.id
    errs = []

    # I1 - objective provenance: every objective traces to a BINDING ratified guideline.
    for obj in spec.objectives_received:
        g = guidelines.get(obj.guideline_id)
        if g is None:
            errs.append(Error("I1", d, "objective on '{}' cites unknown guideline '{}'".format(
                obj.metric, obj.guideline_id)))
        elif not g.ratified:
            errs.append(Error("I1", d, "objective on '{}' cites UNRATIFIED guideline '{}' - the AI "
                                       "may not author its own objective".format(obj.metric, g.id)))
        elif g.gtype is GuidelineType.A:
            errs.append(Error("I1", d, "objective on '{}' cites type-A (aspiration) guideline '{}'; "
                                       "aspirations are never binding".format(obj.metric, g.id)))
        elif not g.elicitation_complete():
            errs.append(Error("I1", d, "guideline '{}' is type {} but its level/metric was never "
                                       "elicited from the polity".format(g.id, g.gtype.value)))

    # I2 - reversibility declared; irreversible instruments need supermajority ratification.
    for ins in spec.instruments:
        if ins.reversibility is Reversibility.IRREVERSIBLE and \
                ins.ratification_class is not RatificationClass.SUPERMAJORITY:
            errs.append(Error("I2", d, "irreversible instrument '{}' is only SIMPLE-ratified".format(
                ins.name)))

    # I4 - every metric declares a gaming model (Goodhart).
    for m in spec.metrics:
        if not m.gaming_model.strip():
            errs.append(Error("I4", d, "metric '{}' declares no gaming model".format(m.name)))

    # I5 - hard constraints fail closed; optimizing through one is unrepresentable.
    for c in spec.hard_constraints:
        if c.on_violation is not OnViolation.FAIL_CLOSED:
            errs.append(Error("I5", d, "constraint '{}' does not fail closed".format(c.name)))

    # I6 - a falsification test exists (the mutation-proof lives in the test suite).
    if spec.falsification_test is None or not callable(spec.falsification_test):
        errs.append(Error("I6", d, "no executable falsification_test"))

    # I7 - every department sunsets.
    if spec.sunset_cycles <= 0:
        errs.append(Error("I7", d, "sunset_cycles must be > 0 (rules expire unless re-ratified)"))

    # I8 - SUBSIDIARITY: a LOW-legitimacy department may set rules and prices, never allocate.
    if spec.central_legitimacy is Legitimacy.LOW:
        for ins in spec.instruments:
            if ins.iclass is InstrumentClass.QUANTITY_ALLOCATION:
                errs.append(Error("I8", d,
                                  "LOW central-legitimacy department may not use "
                                  "QUANTITY_ALLOCATION instrument '{}' - it cannot centrally know "
                                  "what it would centrally allocate".format(ins.name)))

    # I9 - separation of powers: at most one of {generate, decide, verify}.
    if len(spec.roles) > 1:
        errs.append(Error("I9", d, "declares {} roles {} - generate/decide/verify must be "
                                   "separate".format(len(spec.roles),
                                                     sorted(r.value for r in spec.roles))))

    # I10 - Fuller legality linter on every emitted rule.
    for r in spec.rules:
        errs.extend(fuller_lint(r, current_cycle=0, dept=d))

    # I11 - threshold provenance on objectives and constraints.
    for obj in spec.objectives_received:
        errs.extend(_check_threshold_provenance(
            d, "objective '{}'".format(obj.metric), obj.threshold, obj.threshold_provenance,
            guidelines))
    for c in spec.hard_constraints:
        errs.extend(_check_threshold_provenance(
            d, "constraint '{}'".format(c.name), c.threshold, c.threshold_provenance, guidelines))

    return errs


# --------------------------------------------------------------------------------------
# Registry-level invariants (need more than one spec)
# --------------------------------------------------------------------------------------


def validate_registry(specs, guidelines) -> list:
    """Validate a set of specs together: per-spec invariants plus I3 and cross-dept contradiction."""
    if not isinstance(guidelines, dict):
        guidelines = {g.id: g for g in guidelines}
    by_id = {s.id: s for s in specs}
    errs = []
    for s in specs:
        errs.extend(validate(s, guidelines))

    # I3 - couplings are BILATERAL. A one-sided declaration is how departments silently fight.
    for s in specs:
        for cp in s.couplings:
            other = by_id.get(cp.other_dept)
            if other is None:
                errs.append(Error("I3", s.id, "coupling references unknown department '{}'".format(
                    cp.other_dept)))
                continue
            mirrored = any(o.other_dept == s.id and o.shared_var == cp.shared_var
                           and o.direction is cp.direction
                           for o in other.couplings)
            if not mirrored:
                errs.append(Error("I3", s.id,
                                  "coupling ({} on '{}' with {}) is not mirrored by {}".format(
                                      cp.direction.value, cp.shared_var, cp.other_dept,
                                      cp.other_dept)))

    # FULLER-5 - non-contradiction across all emitted rules (pairwise, registry-level).
    seen = {}
    for s in specs:
        for r in s.rules:
            key = (r.applies_to_class, r.predicate)
            neg = (r.applies_to_class, _negate(r.predicate))
            if neg in seen:
                errs.append(Error("FULLER-5", s.id,
                                  "rule {} contradicts rule {} on class '{}'".format(
                                      r.id, seen[neg], r.applies_to_class)))
            seen[key] = r.id
    return errs


def _negate(predicate: str) -> str:
    p = predicate.strip()
    if p.startswith("NOT "):
        return p[4:]
    return "NOT " + p


__all__ = [n for n in dir() if not n.startswith("_")]
