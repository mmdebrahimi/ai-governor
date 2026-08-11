# Stage C — Formal Verification Plan (family `mars-gov-stage-bc-plan`)

Stage A = tested by example (142 passing unit tests). Stage C raises the bar to **proof over the full
state machine** — the 2026-06-06 review was explicit: "the governance risk lives in the *transitions*
(agenda certification · voter choice · approval disposal · ratification · fallback · caretaker · invariant
preservation), not the pure predicates. The dangerous failures are integration failures." This is a
**plan** (class-e); some of it is code-closable in-model, some needs a real verification toolchain.

## Scope — the WHOLE state machine, not just predicates
| Layer | Artifact | Property to prove |
|---|---|---|
| Predicates | `governance/ruleset.py` | each threshold rule total + monotone at its boundary |
| Election | `governance/binding_elections.py` | `ratify` ⇒ (valid ∧ quorum ∧ no-tamper); per-mechanism audit soundness |
| Agenda | `governance/ai_advisor.py` + `exogenous_preferences.py` | diversity-pass ∧ ¬endogenous-steer ∧ ¬exogenous-steer ⇒ winner within bounded citizen-cost of the optimum |
| Cycle | `sandbox/governance_sandbox.py:run_advised_cycle` | **the integration theorem (below)** |

## The integration theorem (the load-bearing claim)
> **For every reachable cycle: the applied state always satisfies the survival invariants**
> (no-starvation ∧ O2-managed ∧ crop ∈ [0.5,1.0]), AND **no tampered / unratified / steered menu is ever
> applied**, AND **on any refusal the caretaker transition itself preserves the invariants** (or honestly
> flags famine).

Sub-obligations:
- **Safety:** `applied ⇒ ratified ∧ diversity_ok ∧ ¬steer ∧ ¬exo_steer ∧ stages_ok` (already a conjunction
  in code — prove no path sets `applied` otherwise).
- **Caretaker liveness:** `¬applied ⇒ state_invariants_ok(new_state)` ∨ `caretaker_reason = famine`.
- **No-regression:** an applied state never violates an invariant a prior applied state held.

## Method (staged, cheapest first)
1. **Property-based testing (code-closable NOW):** Hypothesis-style generators over (scenario, menu,
   ballots, prior-state) asserting the integration theorem on thousands of random cycles. Closes the
   "integration failure" gap cheaply before heavyweight proof. *This is the recommended next in-model step.*
2. **Model checking (external tooling):** encode the cycle as a finite transition system (TLA+ / a model
   checker) over a discretized crop_fraction lattice; check the safety + caretaker invariants exhaustively.
3. **Mechanized proof (external, heaviest):** the predicate algebra + the safety conjunction in a proof
   assistant (Lean/Coq) for the parts that don't depend on the (modeled) utility surface.

## Honest boundaries
- Stage C proves the machine does **what the code says** — it does **not** validate the **modeled
  parameters** (utility weights, attack-rates, steering threshold). Those are Stage-B/empirical, not
  provable. A proof of a captured-utility machine still steers; Stage C + the exogenous check together
  bound that, they don't eliminate it.
- **Code-closable now:** the property-based-testing layer (1). **External wall:** the model-checker / proof-
  assistant toolchains (2,3) need real tools + expertise the agent can scaffold but not fully run in-loop.

## Recommended next move
Build the **property-based integration-test harness** (method 1) as a real family — it's the single
highest-value, fully in-model step, and it directly attacks the "integration failures are the dangerous
ones" finding without waiting on external verification tooling.
