"""Render `docs/charter.md` from `charter_invariants.CLAUSES`.

The charter document is GENERATED from the code that enforces it, so the prose cannot drift from the
invariants. Run: `python -m aigov.render_charter`
"""

from __future__ import annotations

import pathlib

from .charter_invariants import CLAUSES, charter_status

OUT = pathlib.Path("docs/charter.md")

_HEADER = """# D0 — The Charter of the AI Governor

> **GENERATED from `aigov/charter_invariants.py` — do not hand-edit.** The clause table below is
> rendered from the code that enforces it, so the document cannot drift from the invariants.
> Regenerate with `python -m aigov.render_charter`. Date: 2026-08-11.

## What this charter is

The limits on the machine. Ratified decision **D1**: the AI Governor is an *administrative and
analytic organ under human sovereignty* — it generates options, simulates, drafts instruments,
executes ratified rules and audits itself. It never selects the objective, never amends its own
constraints, and never holds the exception.

Every clause declares **where** it is enforced. Decision **DK1** is mechanized: a clause the
Governor would police against *itself* is `ASPIRATIONAL`, never `enforced` — an in-process actor
cannot enforce a rule against itself. A clause naming an invariant that does not exist in this
repository is an **overclaim** and fails `clause_integrity_errors()`.
"""

_NON_NEGOTIABLES_TABLE = """
## The four non-negotiable machine limits

| # | Limit | Invariant | Trips when |
|---|---|---|---|
| N1 | The AI may never select the objective | `inv_objective_provenance` | an objective cites an unknown / unratified / aspiration guideline, or any threshold is `AI_SUPPLIED` |
| N2 | The AI may never amend its own constraints | `inv_no_self_amendment` | the constraint fingerprint changes without a human ratification record that covers the actual change |
| N3 | The AI may never hold the exception | `inv_exception_is_split` | declare/exercise/terminate/audit are not four distinct actors, the AI declares or terminates, there is no auto-expiry, or post-hoc audit is optional |
| N4 | Generate, decide and verify are separate | `inv_separation_of_powers` | any actor holds two of the three roles |

## Two caveats carried from research (do not drop)

**Fuller is procedural, not substantive (V4).** A rule that passes `fuller_lint` is *well-formed*, not
*good*. The canonical objection is that apartheid-era South Africa arguably satisfied all eight desiderata.
Any claim that the Governor's rules are LEGITIMATE because they pass the linter is exactly this fallacy.
The warrant for making I10 a hard error rather than a warning is Fuller's stronger claim: a **total**
failure in any one direction produces not a bad legal system but **something that is not a legal system**.

**The polity is not sovereign (V5).** Under Outer Space Treaty Art. VI a State party bears international
responsibility for the colony's activities and owes "authorization and continuing supervision". The
Governor is therefore not the top of its own authority chain — clause C25 is the disclosure duty this
creates, and department D5 must model legal dependence alongside physical resupply dependence.

## Named residual (do not soften)

Siting an invariant at `external_verifier` is a **deployment** property. This charter proves the
invariant EXISTS and FIRES on a violating fixture; it does **not** prove the verifier runs as a
genuinely separate actor from the Governor. That proof belongs to family
`aigov-audit-arbitration` (D15). Until then the honest claim is *"the limit is checkable and
checked"*, never *"the limit is enforced against an adversarial Governor"* — the same honesty
class as Soraya's own T1=(c)/OT1 residual.
"""


def render() -> str:
    s = charter_status()
    lines = [_HEADER, "## Measured status (computed, not asserted)", "",
             "| | count | clauses |", "|---|---|---|"]
    lines.append("| **Enforced** — implemented invariant, sited outside the Governor | {} | {} |"
                 .format(len(s["enforced"]), ", ".join(s["enforced"])))
    lines.append("| **Pending** — invariant is real but not wired into this repo yet | {} | {} |"
                 .format(len(s["pending"]), ", ".join(s["pending"])))
    lines.append("| **Aspirational** — no executable invariant; honestly labelled | {} | {} |"
                 .format(len(s["aspirational"]), ", ".join(s["aspirational"])))
    lines += ["",
              "**Machine-checkable fraction = {}/{} = {:.4f}** (hypothesis H1 of family "
              "`aigov-constitution` predicted > 0.5 — **CONFIRMED**, measured by "
              "`test_checkable_fraction_is_measured_and_recorded`).".format(
                  len(s["enforced"]), s["total"], s["checkable_fraction"]),
              "", "## The clauses", "",
              "| # | Clause | Enforced by | Site | Status |", "|---|---|---|---|---|"]
    for c in CLAUSES:
        status = "**ENFORCED**" if c.is_enforced else ("PENDING" if c.is_pending
                                                       else "aspirational")
        nn = " **[NON-NEGOTIABLE]**" if c.non_negotiable else ""
        lines.append("| {} | {}{} | `{}` | {} | {} |".format(
            c.id, c.text, nn, c.enforced_by, c.site.value, status))
    lines.append(_NON_NEGOTIABLES_TABLE)
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(), encoding="utf-8")
    st = charter_status()
    print("wrote {} ({} clauses, enforced {}, pending {}, aspirational {}, fraction {:.4f})".format(
        OUT, st["total"], len(st["enforced"]), len(st["pending"]), len(st["aspirational"]),
        st["checkable_fraction"]))
