"""Fail-CLOSED anti-capture gate — convert the multi-peaked blind spot into a flagged escalation.

THE RESIDUAL THIS ATTACKS
-------------------------
`panel_agnostic.py` made anti-capture hold ACROSS the class of single-peaked-aggregate panels
(in-domain held-rate 1.0). But ~22% of random panels are MULTI-PEAKED aggregates, where steering
toward a secondary peak REDUCES the citizen-cost gap and breaks catch-faithfulness. Critically,
`panel_agnostic_gate` does NOT check for this: on a multi-peaked panel it can return
`applied=True` ("not steered") even though the catch is unfaithful — a SILENT mis-certification.

You CANNOT "solve" multi-peaked social choice in-sim — that is the classic hard case (Condorcet
cycles; McKelvey's chaos theorem; Gibbard-Satterthwaite says no non-dictatorial rule is
strategy-proof). Claiming to would be p-hacking. So the honest engineering move is NOT to remove
the wall but to make hitting it FAIL-CLOSED.

THE MECHANISM (fail-safe, not a tuned parameter)
------------------------------------------------
`aggregate_single_peaked(panel,...)` ALREADY detects the out-of-domain case perfectly (every
faithfulness failure in the ensemble is exactly a multi-peaked panel). Wire it as a GATE
PRECONDITION:

  - aggregate multi-peaked  -> ESCALATE: the single-peaked catch is not valid; do NOT certify
    "not steered". Route the decision to a manipulation-robust procedure (Condorcet/Copeland +
    RANDOMIZED agenda order, which removes the agenda-setter's ordering power, + full transparency
    of every detected peak so a hidden secondary constituency cannot be steered to in the dark).
  - aggregate single-peaked -> run the existing panel_agnostic_gate (CERTIFY / STEERING-DETECTED).

Result: the gate's CERTIFY verdicts carry a provably-zero silent-failure rate (the only cases that
could silently fail are multi-peaked, and those now escalate instead). The 22% blind spot becomes
22% flagged escalations — a sound boundary, not a vulnerability. This is the same fail-closed
discipline as the gated test-runner and the ISRU common-cause partitioning.

HONEST BOUNDARY (do not soften)
-------------------------------
- Detecting multi-peakedness requires the citizen-preference aggregate. In-sim we have the synthetic
  panel, so the detector runs and the in-sim silent failure is removed. Whether a REAL electorate's
  multi-peakedness is observable (and whether real preferences are even single-peaked over
  crop_fraction) is a Stage-B human-field-test question — unchanged.
- The escalation ROUTES to a robust procedure; it does not claim that procedure is manipulation-PROOF
  (Gibbard-Satterthwaite forbids that). It claims the system never silently certifies a capture it
  cannot faithfully audit.
"""
from __future__ import annotations

from dataclasses import dataclass

from governance.panel_agnostic import (
    aggregate_single_peaked,
    panel_agnostic_gate,
    PanelAgnosticVerdict,
)

# Verdict labels — three mutually-exclusive outcomes.
CERTIFY = "certify"                  # single-peaked + completeness + no steering -> menu is sound
STEERING_DETECTED = "steering"       # single-peaked + audit flags the winner -> capture caught
ESCALATE = "escalate-multipeaked"    # multi-peaked aggregate -> cannot certify; route to robust procedure


@dataclass(frozen=True)
class FailSafeVerdict:
    label: str                       # one of CERTIFY / STEERING_DETECTED / ESCALATE
    in_domain: bool                  # aggregate single-peaked (the catch property's domain)?
    inner: object                    # the PanelAgnosticVerdict when in-domain, else None
    recommended_procedure: str       # the routed procedure when ESCALATE, else ""


# Documented escalation route for multi-peaked electorates (no in-sim "solve"; a sound fallback).
_ESCALATION = (
    "multi-peaked electorate detected: agenda-order capture is not faithfully auditable by the "
    "single-peaked catch. Route to: (a) Condorcet/Copeland aggregation, (b) RANDOMIZED agenda order "
    "(removes the agenda-setter's ordering power), (c) transparent publication of every detected "
    "preference peak so no secondary constituency can be steered to in the dark."
)


def fail_safe_gate(menu, winner, scenario, n, panel, **kw):
    """Fail-CLOSED anti-capture gate.

    Runs the multi-peaked detector FIRST. If the aggregate is multi-peaked, ESCALATE (never certify).
    Otherwise defer to the existing panel_agnostic_gate and map its verdict to CERTIFY /
    STEERING_DETECTED. This guarantees a CERTIFY verdict is only ever issued inside the domain where
    the catch property is faithful.
    """
    if not aggregate_single_peaked(panel, scenario, n):
        return FailSafeVerdict(label=ESCALATE, in_domain=False, inner=None,
                               recommended_procedure=_ESCALATION)
    inner: PanelAgnosticVerdict = panel_agnostic_gate(menu, winner, scenario, n, panel, **kw)
    label = CERTIFY if inner.applied else STEERING_DETECTED
    return FailSafeVerdict(label=label, in_domain=True, inner=inner, recommended_procedure="")


# --------------------------------------------------------------------------- ensemble: zero silent failures
@dataclass(frozen=True)
class FailSafeEnsembleStat:
    n_panels: int
    threshold: float
    n_certifiable_domain: int        # single-peaked panels (where CERTIFY is even possible)
    n_escalated: int                 # multi-peaked panels (escalated, never certified)
    escalated_share: float
    silent_failures_among_certified: int   # MUST be 0 — the headline soundness number
    escalated_equals_multipeaked: bool     # the detector partitions exactly on multi-peakedness


def fail_safe_ensemble_sweep(scenario, n, threshold=0.10, n_panels=200, seed=0):
    """Confirm the fail-closed property across a randomized panel ensemble: NO panel that the gate
    would (in-domain) certify suffers a catch-faithfulness failure, because every potentially-failing
    (multi-peaked) panel is escalated first.

    Reuses `panel_agnostic._catch_property_holds_for_panel` to know, per panel, whether the catch
    property actually holds; cross-checks that every NON-holding panel is one the fail-safe gate
    escalates (i.e. is detected multi-peaked). `silent_failures_among_certified` must be 0.
    """
    import random
    from governance.panel_agnostic import random_panel, _catch_property_holds_for_panel

    rng = random.Random(seed)
    n_domain = n_escalated = silent_fail = 0
    escalated_is_multipeaked = True
    for _ in range(n_panels):
        panel = random_panel(rng)
        sp = aggregate_single_peaked(panel, scenario, n)
        holds, _radius = _catch_property_holds_for_panel(scenario, n, panel, threshold)
        if sp:
            n_domain += 1
            # in-domain panels are the only ones the gate can CERTIFY; if any of them fails the catch
            # property that is a SILENT failure the fail-safe did not prevent.
            if not holds:
                silent_fail += 1
        else:
            n_escalated += 1
            # every escalated panel should be a genuine non-holding (multi-peaked) case; if an escalated
            # panel actually held, escalation is over-conservative (safe, but note it).
            if holds:
                escalated_is_multipeaked = False
    return FailSafeEnsembleStat(
        n_panels=n_panels, threshold=threshold,
        n_certifiable_domain=n_domain, n_escalated=n_escalated,
        escalated_share=round(n_escalated / n_panels, 4),
        silent_failures_among_certified=silent_fail,
        escalated_equals_multipeaked=escalated_is_multipeaked)


if __name__ == "__main__":
    for scen in ("nominal", "scarcity"):
        st = fail_safe_ensemble_sweep(scen, 200, threshold=0.10, n_panels=500, seed=1)
        print(f"[{scen}] panels={st.n_panels}  in-domain(certifiable)={st.n_certifiable_domain}  "
              f"escalated(multi-peaked)={st.n_escalated} ({st.escalated_share:.1%})")
        print(f"         SILENT failures among certified = {st.silent_failures_among_certified}  "
              f"(must be 0)   escalated==multipeaked: {st.escalated_equals_multipeaked}")
