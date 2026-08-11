# Department Ontology + the Department Contract

> Derived from `foundations-canon-map.md` (discovery-tier) + Beer's Viable System Model. This document answers
> two questions: **what departments must exist and why** (§1–2), and **what makes a department real rather than
> an essay** (§3, the contract). §3 is the load-bearing part — it is the scaling primitive that makes the other
> departments additive instead of bespoke. Date: 2026-08-11.

---

## 1. Derivation — departments are not a list, they are a functional partition

A polity must perform eight things or it ceases to exist as a polity:

| # | Function | Failure if absent |
|---|---|---|
| P1 | **Survive physically** — keep the closed loops closed | death |
| P2 | **Allocate scarce things** — who gets what, at what price | famine / capture |
| P3 | **Resolve disputes** — binding third-party judgment | feud |
| P4 | **Decide collectively** — convert plural preferences into one binding choice | paralysis / coup |
| P5 | **Reproduce socially** — transmit skills, norms, identity across cohorts | fragmentation |
| P6 | **Relate externally** — trade, dependence, defence | absorption / starvation |
| P7 | **Adapt** — learn, forecast, innovate, revise | ossification (Olson) then collapse (Tainter) |
| P8 | **Constrain its own power** — bind the ruler, including the machine | tyranny (Acemoglu–Robinson despotic Leviathan) |

Beer's VSM gives the *layering* that keeps those eight from collapsing into one blob: **S1** operations,
**S2** coordination (anti-oscillation between operations), **S3** control/audit (inside-and-now), **S4**
intelligence (outside-and-future), **S5** identity/policy (normative closure). Cybersyn is the one historical
attempt to run a state this way; it is a precedent to study, including its failure.

**Crucial asymmetry (from canon §4).** S1 departments are *not* equal in how centrally they may be run.
Departments governing a **hard closed physical loop** (D1) are legitimately central — few state variables,
measurable, causally tight, failure = death. Departments governing **dispersed tacit knowledge** (D2, D8, D9)
are subject to the Hayek wall and must be run as *rule-and-price setters*, never as allocators. Each department
below therefore carries a **central-legitimacy** rating; a department that exceeds its rating is a design defect,
not an ambition.

---

## 2. The departments

| ID | Department | VSM | Serves | Central-legitimacy | Reuse available today |
|---|---|---|---|---|---|
| **D0** | **Constitutional Core & Machine Limits** | S5 | P8 | n/a — it *is* the limit | `fail_safe_gate.py` (fail-closed escalation) |
| **D1** | **Life-Support & Resources** (O₂, water, power, thermal, pressure) | S1 | P1 | **HIGH** — closed loop, death-failure | `models/resource_sim.py`, `mars-gov-resource-sim` ledger |
| **D2** | **Economy & Fiscal** (money, prices, tax, budget) | S3 | P2 | **LOW** — Hayek wall; set rules + prices, do not allocate | — (new; K3 LVT-analogue is the leading candidate) |
| **D3** | **Collective Choice** (direct democracy, deliberation, ratification) | S5 | P4 | n/a — it *is* the sovereign channel | `binding_elections.py`, `ruleset.py`, `panel_agnostic.py`, `exogenous_preferences.py`, paper-RLA verification |
| **D4** | **Justice & Rule of Law** (adjudication, enforcement, rights) | S3 | P3 | MEDIUM — procedure central, judgment distributed | `docs/ruleset_predicates.md` (predicate rules) |
| **D5** | **External Relations & Trade** (resupply, dependence, law, defence posture) | S4 | P6 | MEDIUM | `governance/connection.py` (resupplier-as-coercer survival veto) |
| **D6** | **Health & Population** (medical capacity, demography, carrying capacity) | S1 | P1, P5 | MEDIUM — coupled to D1's ceiling | `resource_sim` population coupling |
| **D7** | **Education & Civic Formation** (skills, norms, shared identity) | S1/S5 | P5 | LOW — curriculum capture is a real risk | `governance/civic_education.py` (thin-unity/thick-pluralism + capture audit) |
| **D8** | **Innovation & Science** (R&D, IP regime, right to experiment) | S4 | P7 | **LOW** — discovery cannot be planned | — (new; prizes/AMC precedent exists in the capital module) |
| **D9** | **Labor, Housing & Social Insurance** (work, volume allocation, floor) | S1 | P2, P5 | LOW–MEDIUM | — (new; Harberger/COST candidate) |
| **D10** | **Infrastructure & Public Works** | S1 | P1, P2 | MEDIUM | — (new) |
| **D11** | **Security, Safety & Continuity** (internal safety, emergency, existential risk) | S1/S3 | P1, P8 | MEDIUM — but emergency power is D0-constrained | `fail_safe_gate.py` escalation path |
| **D12** | **Information Integrity & Public Record** (the ledger, the commons of fact) | S2/S3 | P4, P8 | MEDIUM | paper-RLA + tamper-evident log from `mars-gov-voting-verification` |
| **D13** | **Coordination & Arbitration** (inter-department conflict, scheduling, standards) | **S2** | all | HIGH by construction | — (new; the anti-oscillation organ) |
| **D14** | **Foresight & Simulation** (the digital twin, scenario analysis, early warning) | **S4** | P7 | n/a — advisory only | `resource_sim` + the twin to be built (F4) |
| **D15** | **Audit & Anti-Capture** (independent verification of the governor itself) | **S3\*** | P8 | n/a — must be *independent of* the governor | `panel_agnostic.py`, `exogenous_preferences.py`, `fail_safe_gate.py` |

**Count: 16 (D0–D15).** Ten of the sixteen already have a concrete, tested primitive in `Mars_Governance` —
which is why the reuse-first sequencing in the plan is not optimism.

### Separation-of-powers invariant (inherited, non-negotiable)

`mars-governance` already carries the flow-down requirement **generator ≠ tally ≠ verifier**. Generalized here:

> **No department may simultaneously (a) generate options, (b) execute the binding decision, and (c) verify that
> the decision was faithfully executed.** D14 generates. D3 decides. D15 verifies. D0 bounds all three.
> The AI Governor kernel may occupy **at most one** of those roles per decision.

### The three departments that do NOT exist and must not be invented

- A "Ministry of Truth" — D12 governs the *record's integrity*, never the content of belief.
- A "Ministry of Preferences" — the governor never models what citizens *should* want (W1, Fork 1).
- A "Ministry of Optimization" — there is no scalar to optimize (K2); D13 arbitrates declared trade-offs, it does
  not maximize a welfare function.

---

## 3. The Department Contract (F3) — the anti-theater primitive

A department is **real** iff it can fill this contract and its falsification test executes. This is a Python
dataclass + validator, not a doc convention — `validate(spec)` returns errors, and an invalid spec cannot be
loaded by the kernel.

```
DepartmentSpec
  id                    : str                      # D0..D15
  vsm_layer             : {S1,S2,S3,S4,S5}
  central_legitimacy    : {HIGH, MEDIUM, LOW}      # from §2; bounds allowed instrument classes
  state_vars            : [ StateVar ]
  instruments           : [ Instrument ]
  objectives_received   : [ ObjectiveRef ]         # GIVEN by a ratified guideline; never self-authored
  hard_constraints      : [ Constraint ]
  couplings             : [ Coupling ]
  metrics               : [ Metric ]
  failure_modes         : [ FailureMode ]
  falsification_test    : ExecutablePredicate      # must run and must be able to FAIL
  sunset_cycles         : int                      # rules expire unless re-ratified (W12)

StateVar    : name, unit, observability ∈ {direct, estimated, latent}, owner_dept
Instrument  : name, domain, bounds, latency_cycles, reversibility ∈ {reversible, costly, irreversible}, cost
ObjectiveRef: guideline_id, direction ∈ {raise, lower, hold_within}, priority_source
Constraint  : predicate, source ∈ {constitution, physics, law}, on_violation = FAIL_CLOSED
Coupling    : other_dept, shared_var, direction ∈ {reads, writes, contends}, arbiter = D13
Metric      : name, formula, gaming_model, rotation_policy          # W9 Goodhart
FailureMode : name, detector, escalation_target
```

### Validator invariants (each is a test)

| # | Invariant | Wall / critique it closes |
|---|---|---|
| I1 | Every `ObjectiveRef.guideline_id` resolves to a **ratified** guideline. A self-authored objective is a validation error. | Fork 1 — the AI never chooses the objective (W1, W3) |
| I2 | Every `Instrument` declares reversibility; `irreversible` instruments require a supermajority ratification class. | W11, W12; Soraya's own gate philosophy |
| I3 | Couplings are **bilateral**: if A declares `contends` with B on var v, B must declare it too, or validation fails. | Critique 4 — silent inter-department fights (A1) |
| I4 | Every `Metric` declares a `gaming_model`. No gaming model ⇒ error. | W9 Goodhart/Campbell |
| I5 | Every `Constraint` has `on_violation = FAIL_CLOSED`. Optimizing through a hard constraint is unrepresentable. | W11; `fail_safe_gate` precedent |
| I6 | `falsification_test` must execute **and** be demonstrated to fail on a mutated spec (a test that cannot fail is not a test). | Anti-theater (critique 3) |
| I7 | `sunset_cycles > 0`. Every rule expires; continuation requires an affirmative act. | W12 Tainter |
| I8 | `central_legitimacy = LOW` ⇒ instruments restricted to *rule/price setting*; direct quantity allocation is a validation error. | W8 Hayek; the subsidiarity engine |
| I9 | No department declares itself in ≥2 of {generate, decide, verify}. | Separation-of-powers invariant |
| I10 | Every rule emitted by a department passes the **Fuller linter** (8 desiderata of legality). | L5 / V4 |
| **I11** | **No `Constraint` or `ObjectiveRef` may carry a numeric threshold whose provenance is not a ratified guideline or a physical constant.** An AI-supplied threshold is a validation error. | **The threshold gap** — discovered empirically by probe B1 (`probe-B1-guideline-compilation.md`) |

**I8, I10 and I11 are the three invariants that make this project structurally different from a technocratic
optimizer.** I8 mechanically enforces subsidiarity: a department that cannot centrally know cannot centrally
allocate. I10 mechanically enforces legality on machine-generated rules. **I11 mechanically enforces Fork 1** —
it closes the seam where an advisory AI silently becomes a sovereign one by filling in the numbers a vague
guideline omitted. Every compiled guideline additionally carries its **type** (`P` mechanism-prohibition ·
`O` ordering · `F` floor/ceiling · `D` metric-direction · `A` aspiration) so type-`A` guidelines are visibly
non-binding rather than quietly dropped.

---

## 4. Build order implied by the ontology

1. **D0** (constitutional core) — nothing else may be built before the limits exist.
2. **The contract** (§3) — before any department instance.
3. **D14** (twin) — departments must have a world to act on before they can be falsified.
4. **First three department instances**, chosen to span the *hard cases* rather than the easy ones:
   - **D1 Life-Support** (`HIGH` legitimacy, closed physical loop, reuse of `resource_sim`) — the case where
     central planning is *justified*;
   - **D2 Economy/Fiscal** (`LOW` legitimacy, Hayek wall, LVT-analogue) — the case where it is *forbidden*;
   - **D3 Collective Choice** (the sovereign channel, ~193 tests of reuse) — the case that *legitimates* the rest.
   Together they exercise all three central-legitimacy ratings, all three separation-of-powers roles, and the
   coupling machinery (D1↔D2 contend on volume/power; D3 ratifies both).
5. **D15 audit + D13 arbitration** — the checks, built *with* the first departments, never after.
6. Remaining departments — additive under the contract, one per increment.

**Anything that reverses this order (a department before the contract, an instrument before D0) is the failure
mode this document exists to prevent.**
