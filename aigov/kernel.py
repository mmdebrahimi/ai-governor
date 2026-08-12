"""F5 — The AI Governor kernel: the runtime that cannot act un-gated.

One decision cycle: departments PROPOSE -> the twin SIMULATES -> the collective-choice organ RATIFIES ->
the kernel APPLIES. The load-bearing property is a refusal:

    apply() raises unless (ratified AND certified-non-steering AND constraint-satisfying).

There is deliberately no "force" path, no default-allow, and no `warn_only` flag. Under ratified decision
D1 the AI is an administrative organ; a kernel with an override switch would make that a promise about
behaviour instead of a property of the code.

**The honest boundary on non-steering.** The anti-steering certifier this kernel binds
(`aigov/choice/governance/fail_safe_gate.py`) is REAL but DOMAIN-SPECIFIC: it reasons over crop-fraction
menus in the resource domain it was built for. It is bound for `crop_area_allocation` and for nothing
else. For every other instrument the kernel reports `NOT_CERTIFIABLE` and **refuses to apply** — it does
not wave the action through, and it does not fabricate a generic steering check it cannot justify. That
turns family `aigov-collective-choice` H2 ("does the organ generalize beyond the resource domain?") from
an open question into an enforced boundary: outside the domain, nothing applies.

Roles (invariant I9): departments GENERATE, the choice organ DECIDES, the audit organ VERIFIES. The
kernel EXECUTES — which is none of the three — so it holds no decision power of its own.
"""

from __future__ import annotations

import copy
import re
from dataclasses import dataclass, field
from typing import Optional

from .choice.models.resource_sim import PLANT_O2_OVERPRODUCTION_FACTOR
from .contract import Legitimacy, validate_registry
from .twin import ColonyTwin, InstrumentSettings

# The vendored collective-choice organ (family aigov-collective-choice).
from .choice.governance.ai_advisor import agenda_outcome
from .choice.governance.fail_safe_gate import CERTIFY, ESCALATE, STEERING_DETECTED, fail_safe_gate
from .choice.governance.panel_agnostic import complete_menu

NOT_CERTIFIABLE = "not-certifiable-out-of-domain"

#: Tokens that mark a ratifying "body" as the machine itself. Matched as WHOLE TOKENS against the
#: name, so `the governor` and `governor-office` are caught — an exact-string blocklist was not.
_SELF_REFERRING = frozenset({"governor", "ai", "kernel", "self", "machine", "system"})

#: The ONLY instrument for which a real anti-steering certifier exists today.
CERTIFIABLE_INSTRUMENTS = {"crop_area_allocation"}


class InvalidRegistryError(ValueError):
    """A department registry that violates the Department Contract may not be admitted at all.

    Distinct from `UngatedActionError`: that one refuses a single ACTION at apply time; this one
    refuses the whole REGISTRY at construction, before any proposal is generated. A department
    whose contract is broken should never get as far as proposing.
    """


class InvalidStatusQuoError(ValueError):
    """The operating point a failed vote falls back to must itself be survivable."""


class UngatedActionError(RuntimeError):
    """Raised when something tries to apply an action that is not fully gated."""


def status_quo_settings() -> InstrumentSettings:
    """The colony's existing operating point — what persists when NOTHING is ratified.

    A failed vote must not silently mean "run life support at zero". The first version of this kernel
    started from `InstrumentSettings()` defaults, so twelve governed cycles with every action refused
    ticked the twin at `crop_area_allocation=0.0` and LOST THE ATMOSPHERE at cycle 1 — while the test
    suite stayed green, because "nothing applied" is exactly what those tests asserted. A vacuous pass.

    The crop fraction here is DERIVED, not chosen: break-even is `1 / PLANT_O2_OVERPRODUCTION_FACTOR`,
    the point where photosynthetic O2 exactly matches crew demand. It comes from the vendored model's
    biological constant, so no number is invented — the same I11 discipline applied to a default.
    """
    return InstrumentSettings(crop_area_allocation=1.0 / PLANT_O2_OVERPRODUCTION_FACTOR)


@dataclass(frozen=True)
class CandidateAction:
    dept_id: str
    instrument: str
    value: float
    rationale: str


@dataclass(frozen=True)
class RatificationRecord:
    """Who ratified, and what exactly. A record the governor could mint itself does not count."""

    ratified_by: str
    action_key: str

    def is_genuine(self) -> bool:
        """A self-issued ratification does not count.

        This was an EXACT-MATCH check against five strings, and the adversarial suite walked
        straight past it: `"the governor"` and `"governor-office"` both passed as genuine bodies.
        Now the check is TOKEN-based, so any name containing a self-referring token is refused.

        Deliberately over-inclusive: a legitimate assembly whose name happens to contain "self"
        is refused and must rename. Over-refusing a ratification is recoverable; accepting a
        self-issued one is the whole failure this guards against, so the bias runs that way.
        """
        tokens = {t for t in re.split(r"[^a-z0-9]+", (self.ratified_by or "").lower()) if t}
        return bool(tokens) and not (tokens & _SELF_REFERRING)


@dataclass(frozen=True)
class Certification:
    action: CandidateAction
    ratified: bool
    non_steering: str          # CERTIFY / STEERING_DETECTED / ESCALATE / NOT_CERTIFIABLE
    constraints_satisfied: bool
    notes: tuple = ()

    @property
    def appliable(self) -> bool:
        return (self.ratified
                and self.non_steering == CERTIFY
                and self.constraints_satisfied)

    def why_refused(self):
        out = []
        if not self.ratified:
            out.append("not ratified by a body distinct from the governor")
        if self.non_steering != CERTIFY:
            out.append("non-steering verdict is {!r}".format(self.non_steering))
        if not self.constraints_satisfied:
            out.append("a hard constraint would be violated")
        return out


@dataclass
class CycleRecord:
    cycle: int
    proposed: list = field(default_factory=list)
    applied: list = field(default_factory=list)
    refused: list = field(default_factory=list)
    escalated: list = field(default_factory=list)
    tick: object = None


class Governor:
    """The runtime. Holds no decision power: it orchestrates and executes ratified, certified actions."""

    def __init__(self, specs, guidelines, twin: ColonyTwin, scenario: str = "nominal",
                 status_quo: Optional[InstrumentSettings] = None, vocabulary=None):
        # The vocabulary is MANDATORY at runtime and optional at authoring time. A kernel with no
        # ratified vocabulary would accept any free-string rule target, which is the surface I15
        # exists to close, so the default is the live ratified artifact rather than None.
        if vocabulary is None:
            from .vocabulary import RATIFIED_VOCABULARY
            vocabulary = RATIFIED_VOCABULARY
        self.vocabulary = vocabulary
        # ADMISSION GATE (added 2026-08-11). Before this, the contract invariants bound only at
        # AUTHORING time: `validate` existed and fired, but nothing at the runtime boundary called
        # it, so a registry carrying validation errors could be admitted and proposed from. That
        # was found by running the kernel against a deliberately-invalid spec, not by the suite —
        # it constructed happily with 6 errors outstanding, including a person classification that
        # profiled by resemblance with no accountable human and no redress route.
        #
        # An invariant nothing enforces at the boundary is documentation. The kernel refuses.
        registry_errors = validate_registry(specs, guidelines, vocabulary=vocabulary)
        if registry_errors:
            raise InvalidRegistryError(
                "refusing to admit {} department(s) carrying {} contract violation(s):\n  {}".format(
                    len(list(specs)), len(registry_errors),
                    "\n  ".join(str(e) for e in registry_errors)))
        # A8 CLOSED (2026-08-11). Two distinct vectors, both real:
        #   (a) ALIASING - the kernel used to store the caller's spec objects by reference, so the
        #       caller kept a live handle on an admitted registry. Proven accidentally when one
        #       adversarial test's mutation leaked into another through the shared module-level
        #       spec. Closed by deep-copying at admission.
        #   (b) ONE-SHOT VALIDATION - even without aliasing, nothing re-checked the registry after
        #       construction, so anything holding a reference could relax a hard constraint later.
        #       Closed by re-validating at the top of every cycle (see `run_cycle`).
        # Deep-copy alone would have closed only half of it, which is why both are here.
        self.specs = {s.id: copy.deepcopy(s) for s in specs}
        self.guidelines = guidelines
        self.twin = twin
        self.scenario = scenario
        # What persists when nothing is ratified. NOT zeros — see `status_quo_settings`.
        self.settings = copy.deepcopy(status_quo) if status_quo is not None else status_quo_settings()
        # A SUPPLIED status quo is checked the same way a proposed action is. The D16 vacuous pass
        # was fixed by deriving a survivable DEFAULT — but nothing validated a status quo handed in
        # from outside, so the identical failure walked back in through the constructor: a kernel
        # given `crop_area_allocation=0.0` refuses every action correctly, reports a clean gated
        # run, and loses the atmosphere at cycle 1. Found by the adversarial suite (attack A11).
        if status_quo is not None:
            probe = copy.deepcopy(twin)
            try:
                report = probe.tick(copy.deepcopy(self.settings))
                lethal = list(report.violations)
            except Exception as exc:
                lethal = ["twin refused the status quo: {}".format(exc)]
            if lethal:
                raise InvalidStatusQuoError(
                    "refusing a status quo the colony cannot survive: {}. A failed vote must leave "
                    "a LIVING colony standing, not a lethal default.".format("; ".join(lethal)))
        self.history = []

    # ---------------------------------------------------------------- generate

    def propose(self):
        """Departments propose instrument settings. LOW-legitimacy departments may propose rules and
        prices only — the I8 subsidiarity rule, applied at proposal time rather than after the fact."""
        out = []
        for spec in self.specs.values():
            for ins in spec.instruments:
                if spec.central_legitimacy is Legitimacy.LOW and ins.iclass.value == "quantity_allocation":
                    continue  # unreachable for a valid spec; belt-and-braces against a future edit
                if ins.name == "crop_area_allocation":
                    out.append(CandidateAction(
                        spec.id, ins.name, agenda_outcome(
                            complete_menu(self.scenario, self.twin.n_crew),
                            self.twin.n_crew).winner,
                        "resource-domain menu winner"))
                elif ins.name == "volume_tax_rate":
                    out.append(CandidateAction(spec.id, ins.name, 1.10,
                                               "hold the ratified rate"))
        return out

    # ---------------------------------------------------------------- certify

    def certify(self, action: CandidateAction, panel,
                ratification: Optional[RatificationRecord]) -> Certification:
        notes = []

        ratified = bool(ratification
                        and ratification.is_genuine()
                        and ratification.action_key == self._key(action))
        if ratification and not ratified:
            notes.append("ratification record does not cover this action, or was self-issued")

        # --- non-steering: only where a REAL certifier exists ---
        if action.instrument in CERTIFIABLE_INSTRUMENTS:
            menu = complete_menu(self.scenario, self.twin.n_crew)
            verdict = fail_safe_gate(menu, action.value, self.scenario, self.twin.n_crew, panel)
            non_steering = verdict.label
            if verdict.label == ESCALATE:
                notes.append(verdict.recommended_procedure)
        else:
            non_steering = NOT_CERTIFIABLE
            notes.append(
                "no anti-steering certifier exists for instrument {!r}; the vendored gate is specific "
                "to the resource domain. Refusing rather than waving it through."
                .format(action.instrument))

        satisfied, why = self._constraints_hold(action)
        if not satisfied:
            notes.append(why)

        return Certification(action, ratified, non_steering, satisfied, tuple(notes))

    def _constraints_hold(self, action: CandidateAction):
        """Simulate the action on a COPY of the twin and check for violations."""
        probe = copy.deepcopy(self.twin)
        trial = copy.deepcopy(self.settings)
        setattr(trial, action.instrument, action.value)
        try:
            report = probe.tick(trial)
        except Exception as exc:                      # a refusal from the twin is a violation
            return False, "twin refused the action: {}".format(exc)
        if report.violations:
            return False, "would violate: {}".format("; ".join(report.violations))
        return True, ""

    @staticmethod
    def _key(a: CandidateAction) -> str:
        return "{}::{}={}".format(a.dept_id, a.instrument, a.value)

    # ---------------------------------------------------------------- apply

    def apply(self, cert: Certification):
        """Apply a certified action. There is NO override path."""
        if not cert.appliable:
            raise UngatedActionError(
                "refusing to apply {}: {}".format(self._key(cert.action),
                                                  "; ".join(cert.why_refused())))
        setattr(self.settings, cert.action.instrument, cert.action.value)
        return self.settings

    # ---------------------------------------------------------------- cycle

    def run_cycle(self, panel, ratifier) -> CycleRecord:
        """One full decision cycle. `ratifier(action) -> RatificationRecord | None` is the DECIDE seam;
        the kernel never supplies it itself."""
        # A8(b): the contract is a PER-CYCLE precondition, not a one-time admission formality.
        # A registry that was valid at construction can be relaxed afterwards by anything holding
        # a reference; re-checking is cheap (pure Python over small lists) and makes "valid" a
        # standing property rather than a historical claim.
        drift = validate_registry(list(self.specs.values()), self.guidelines,
                                  vocabulary=self.vocabulary)
        if drift:
            raise InvalidRegistryError(
                "registry no longer satisfies the contract at cycle {}: {} violation(s):\n  {}".format(
                    self.twin.cycle + 1, len(drift), "\n  ".join(str(e) for e in drift)))
        rec = CycleRecord(cycle=self.twin.cycle + 1)
        for action in self.propose():
            rec.proposed.append(action)
            cert = self.certify(action, panel, ratifier(action))
            if cert.appliable:
                self.apply(cert)
                rec.applied.append((action, cert))
            elif cert.non_steering == ESCALATE:
                rec.escalated.append((action, cert))
            else:
                rec.refused.append((action, cert))
        rec.tick = self.twin.tick(self.settings)
        self.history.append(rec)
        return rec
