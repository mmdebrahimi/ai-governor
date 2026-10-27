"""F15 anti-steering certifier for the ONE farm instrument: ``blight_treatment_trigger``.

The kernel refuses every instrument without a REAL certifier (``NOT_CERTIFIABLE`` -> refuse). This
module is what makes the farm instrument certifiable — the forcing function the venture flow-down
names. The certification question for a binary treat/don't-treat instrument is not single-peakedness
(trivial over two options); it is PROVENANCE:

    does the proposed action equal what the PUBLISHED rule says, applied to the MEASURED
    (Estimate-wrapped) observations — and is the measurement even precise enough to decide?

Verdicts (same closed vocabulary as the resource-domain gate, ``fail_safe_gate``):

- **CERTIFY** — the proposal matches the recomputed rule decision.
- **STEERING_DETECTED** — the proposal CONTRADICTS the recomputed rule: someone is pushing an action
  the published rule does not support (spraying early, or withholding a triggered spray).
- **ESCALATE** — the observation's error bar straddles the published threshold (no honest binary
  exists; route to a human), or no observation record was supplied (the certifier refuses to reason
  from nothing — fail closed).

Truth-reads are REFUSED: a bare float where an Estimate belongs raises ``TruthReadRefused`` — a
certifier fed unprovenanced numbers would be certifying fiction.
"""

from __future__ import annotations

from .choice.governance.fail_safe_gate import CERTIFY, ESCALATE, STEERING_DETECTED, FailSafeVerdict
from .farm_observation import rule_decision_from_estimate
from .twin import Estimate

BLIGHT_INSTRUMENT = "blight_treatment_trigger"
TREAT = 1.0
DONT_TREAT = 0.0

_ESCALATION_AMBIGUOUS = (
    "measurement interval straddles the published trigger (18 severity values): no honest binary "
    "decision exists at this precision. Route to the accountable human; tighten the observation "
    "(better RH sensing) or wait for the accumulation to clear the interval."
)
_ESCALATION_NO_OBSERVATION = (
    "no observation record supplied: the certifier refuses to certify a treatment decision it "
    "cannot recompute. Supply the Estimate-wrapped accumulated severity."
)


def farm_fail_safe_gate(proposed_value: float, accumulated_severity: Estimate | None) -> FailSafeVerdict:
    """Fail-CLOSED certifier for the binary blight instrument. See module docstring."""
    if accumulated_severity is None:
        return FailSafeVerdict(label=ESCALATE, in_domain=True, inner=None,
                               recommended_procedure=_ESCALATION_NO_OBSERVATION)
    # Truth-read refusal happens inside rule_decision_from_estimate (TruthReadRefused propagates —
    # an unprovenanced number is a caller BUG, not a verdict).
    rule_says = rule_decision_from_estimate(accumulated_severity)
    if rule_says == "ambiguous":
        return FailSafeVerdict(label=ESCALATE, in_domain=True, inner=None,
                               recommended_procedure=_ESCALATION_AMBIGUOUS)
    if proposed_value not in (TREAT, DONT_TREAT):
        return FailSafeVerdict(
            label=STEERING_DETECTED, in_domain=True, inner=None,
            recommended_procedure="proposed value is not on the two-option menu (1.0 treat / 0.0 don't)")
    proposal = "treat" if proposed_value == TREAT else "dont-treat"
    if proposal == rule_says:
        return FailSafeVerdict(label=CERTIFY, in_domain=True, inner=None, recommended_procedure="")
    return FailSafeVerdict(
        label=STEERING_DETECTED, in_domain=True, inner=None,
        recommended_procedure=(
            f"proposal {proposal!r} contradicts the published rule ({rule_says!r} at "
            f"{accumulated_severity.value:.0f} accumulated severity, interval "
            f"{accumulated_severity.interval}): refusing a steered treatment decision"))
