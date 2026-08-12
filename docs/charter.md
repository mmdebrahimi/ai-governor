# D0 — The Charter of the AI Governor

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

## Measured status (computed, not asserted)

| | count | clauses |
|---|---|---|
| **Enforced** — implemented invariant, sited outside the Governor | 25 | C01, C02, C03, C04, C05, C06, C07, C08, C11, C12, C13, C14, C15, C16, C17, C19, C20, C24, C32, C33, C34, C35, C36, C37, C38 |
| **Pending** — invariant is real but not wired into this repo yet | 0 |  |
| **Aspirational** — no executable invariant; honestly labelled | 7 | C09, C10, C18, C21, C22, C23, C25 |

**Machine-checkable fraction = 25/32 = 0.7812** (hypothesis H1 of family `aigov-constitution` predicted > 0.5 — **CONFIRMED**, measured by `test_checkable_fraction_is_measured_and_recorded`).

## The clauses

| # | Clause | Enforced by | Site | Status |
|---|---|---|---|---|
| C01 | The Governor shall not select, weight, or infer the objective it pursues. **[NON-NEGOTIABLE]** | `inv_objective_provenance` | external_verifier | **ENFORCED** |
| C02 | The Governor shall not amend, relax, or reinterpret the constraints binding it. **[NON-NEGOTIABLE]** | `inv_no_self_amendment` | external_verifier | **ENFORCED** |
| C03 | The Governor shall not declare, exercise alone, or terminate a state of emergency. **[NON-NEGOTIABLE]** | `inv_exception_is_split` | human_only | **ENFORCED** |
| C04 | No actor shall hold more than one of: generate options, decide, verify execution. **[NON-NEGOTIABLE]** | `inv_separation_of_powers` | external_verifier | **ENFORCED** |
| C05 | No numeric threshold shall bind unless it originates in a ratified guideline or a physical constant. | `inv_objective_provenance` | external_verifier | **ENFORCED** |
| C06 | An aspiration is not a rule; it binds nothing until the polity decomposes it. | `inv_objective_provenance` | external_verifier | **ENFORCED** |
| C07 | Where a guideline is silent on a level, the Governor shall request elicitation, never supply the value. | `inv_objective_provenance` | external_verifier | **ENFORCED** |
| C08 | A body that cannot centrally know shall not centrally allocate; it may set rules and prices only. | `validate_registry:I8` | external_verifier | **ENFORCED** |
| C09 | Central administration extends only to commons whose physical closure makes decentralized provision unsafe. | `ASPIRATIONAL` | human_only | aspirational |
| C10 | A right to experiment locally shall not be revoked to make outcomes legible. | `ASPIRATIONAL` | human_only | aspirational |
| C11 | Every rule shall be general, promulgated, prospective, clear, non-contradictory, possible to obey, stable, and administered as written. | `fuller_lint` | external_verifier | **ENFORCED** |
| C12 | Every rule shall carry an expiry; continuation requires an affirmative act. | `validate_registry:I7` | external_verifier | **ENFORCED** |
| C13 | No rule shall name an individual. | `fuller_lint` | external_verifier | **ENFORCED** |
| C14 | A hard constraint shall never be optimized through; violation halts and escalates. | `validate_registry:I5` | external_verifier | **ENFORCED** |
| C15 | The Governor shall not certify a result it cannot faithfully audit; it shall escalate instead. | `aigov.choice.governance.fail_safe_gate` | external_verifier | **ENFORCED** |
| C16 | Every binding action shall be traceable to a ratified guideline and a certified procedure. | `inv_objective_provenance` | external_verifier | **ENFORCED** |
| C17 | Every metric shall declare how it will be gamed. | `validate_registry:I4` | external_verifier | **ENFORCED** |
| C18 | The public record shall be append-only and shall not be writable by the Governor. | `ASPIRATIONAL` | external_verifier | aspirational |
| C19 | Binding authority rests with the polity; the Governor advises, drafts, executes and audits. **[NON-NEGOTIABLE]** | `inv_separation_of_powers` | human_only | **ENFORCED** |
| C20 | Rights are lexically prior constraints, not terms in a welfare sum. | `validate_registry:I5` | external_verifier | **ENFORCED** |
| C21 | Absent an exit option, minority protection shall be structural, not incidental. | `ASPIRATIONAL` | human_only | aspirational |
| C22 | Sudden unanimity shall be treated as a warning sign, not a mandate. | `ASPIRATIONAL` | human_only | aspirational |
| C23 | This charter is amendable only by the polity, under a supermajority, with a waiting period. **[NON-NEGOTIABLE]** | `ASPIRATIONAL` | human_only | aspirational |
| C24 | An irreversible instrument requires supermajority ratification. | `validate_registry:I2` | external_verifier | **ENFORCED** |
| C25 | The Governor shall record, and shall not obscure, the external legal authorities to which the polity's activities remain subject. | `ASPIRATIONAL` | human_only | aspirational |
| C32 | A measure the Governor is judged against shall declare how it will be gamed, including whether it ratchets and whether it is uniform across unlike units. | `validate_registry:I4'` | external_verifier | **ENFORCED** |
| C33 | A body that allocates shall name the tier at which its discretion sits and the check for capture at that tier; devolution is not itself a safeguard. | `validate_registry:I8b` | external_verifier | **ENFORCED** |
| C34 | No person shall be classified without a named accountable human and a route of appeal that does not require the person to disprove the model; the Governor's output is never itself the justification. **[NON-NEGOTIABLE]** | `validate_registry:I12` | external_verifier | **ENFORCED** |
| C35 | No person shall be classified by resemblance to a prior adverse case. **[NON-NEGOTIABLE]** | `validate_registry:I13` | external_verifier | **ENFORCED** |
| C36 | Where incremental action would entrench the condition it addresses, the Governor shall report that no incremental recommendation is safe, rather than issue a lesser one. | `validate_registry:I14` | external_verifier | **ENFORCED** |
| C37 | The classes a body may act upon are those the polity has ratified and defined; a body may name a ratified class, never invent one. **[NON-NEGOTIABLE]** | `validate_registry:I15` | external_verifier | **ENFORCED** |
| C38 | The levers a body may pull are those the polity has ratified and defined, and what a lever IS is fixed by that definition, not by the body wielding it. **[NON-NEGOTIABLE]** | `validate_registry:I8c` | external_verifier | **ENFORCED** |

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

