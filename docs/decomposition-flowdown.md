# AI Government — Decomposition, Requirements Flow-down, Critical Path

> Soraya `decompose` output, per `~/.claude/skills/soraya/references/decompose-flowdown-template.md`.
> Date: 2026-08-11. Umbrella: `aigov` (ledger `project_state/aigov.md`).
> Upstream framing: `idea-anchor-DRAFT-2026-08-11.md` (**3 forks awaiting ratification**),
> `foundations-canon-map.md`, `department-ontology.md`.

---

## 1. Project-family decomposition

| # | Family (slug) | Scope (one line) | Why a distinct family (its own falsifier) | Class |
|---|---|---|---|---|
| F0 | `aigov-foundations` | Verify the canon map's 12 load-bearing claims (V1–V12) into audit-tier memos | Falsified by: a wall/result being mis-stated such that the charter's bound is wrong | research-only (e) |
| F1 | `aigov-constitution` | D0 — the machine's charter: what the AI may never do, encoded as machine-checkable invariants | Falsified by: an invariant that prose asserts but no test can check | new capability (a) |
| F2 | `aigov-guideline-intake` | How a population produces guidelines precise enough to *bind* a machine (sortition + QV priorities) | Falsified by: guidelines that cannot compile to constraints ⇒ the governor is decorative (**crux A2**) | cross-cutting (d) |
| F3 | `aigov-dept-contract` | `DepartmentSpec` + validator invariants I1–I10 (the department SDK) | Falsified by: two real departments that cannot both be expressed without shared mutable state (**A1**) | new capability (a) |
| F4 | `aigov-twin` | D14 — the colony digital twin departments act on (extends `resource_sim` to population + economy) | Falsified by: twin outputs that don't reproduce the reused ECLSS/analog baselines | cross-cutting (d) |
| F5 | `aigov-kernel` | The AI Governor runtime: guideline → options → simulate → menu → ratify → apply → audit → next cycle | Falsified by: a cycle that applies an unratified or uncertified action | cross-cutting (d) |
| F6 | `aigov-collective-choice` | D3 — integrate the existing `Mars_Governance` organ (193 tests) as the sovereign channel | Falsified by: the port losing any of the 193 tests or the ratify-gate semantics | refactor (c) |
| F7 | `aigov-dept-lifesupport` | D1 instance — the `HIGH` central-legitimacy case (closed physical loop) | Falsified by: a loop that closes in sim but violates a physical bound | new capability (a) |
| F8 | `aigov-dept-economy` | D2 instance — the `LOW` central-legitimacy case: volume/area LVT-analogue + Pigouvian O₂/water pricing | Falsified by: I8 violation (a `LOW` dept allocating quantities) or a fiscal instrument that cannot fund the public-goods bill | new capability (a) |
| F9 | `aigov-audit-arbitration` | D15 (independent audit) + D13 (inter-department arbitration) | Falsified by: an audit that certifies a capture it cannot faithfully detect (the silent-mis-certification bug already closed once) | new capability (a) |
| F10 | `aigov-adversarial` | Red team: agenda manipulation (W5), metric gaming (W9), preference falsification (Kuran), emergency-power abuse, capture | Falsified by: an attack the system passes silently rather than escalating | cross-cutting (d) |
| F11 | `aigov-integration` | End-to-end governed run: ≥12 cycles, ≥3 departments, on the twin, under adversarial load | This IS the phase-1 mission terminal | cross-cutting (d) |
| F12 | `aigov-scale-gates` | **DEFERRED to phase 2.** Colony→city→nation phase-change gates (attention budget, enforcement distance, exit collapse) | — | research-only (e) |

**Seeding policy (deliberate, anti-sprawl).** Only the **unblocked** families get `/project-init` ledgers now
(umbrella + F0 + F1 + F3). Downstream families are *proposed here* and seeded when their predecessor gate clears
— which is exactly the eligibility rule `scripts/advance_ranker.py` enforces (a family whose predecessor isn't
machine-checkably done is `blocked:predecessor` and cannot be worked anyway). Seeding twelve ledgers today would
produce ten stale artifacts and burn ten slots of the best-effort self-init population cap.

---

## 2. Requirements flow-down + dependency graph

| Family | Binding requirement (the one constraint that gates it) | Depends on | Critical-path position | Cheapest next test |
|---|---|---|---|---|
| F0 | V1–V12 promoted to audit-tier; contested set confirmed contested | — | **Gate A** | `/research` on V1 (the five walls) — one memo |
| F1 | Every charter clause has a machine-checkable invariant or is labelled *aspirational* | F0 (V1, V4) | **Gate A** | Write the clause list; count how many are checkable |
| F2 | A guideline artifact that **compiles** to `ObjectiveRef` + `Constraint` without a human rewriting it | F0 (V6), F1 | Gate B | Hand-compile 3 real guideline sentences; see what breaks |
| F3 | I1–I10 all expressible as validator errors; I6 demonstrated by a mutation that fails | F1 | **Gate B — the scaling primitive** | Write `DepartmentSpec` + `validate()`; mutate a spec; assert failure |
| F6 | Zero test loss (193/193) + ratify-gate semantics preserved | F1 | Gate B (parallel, reuse) | Run the suite from the new root |
| F4 | Twin reproduces the reused ECLSS/analog baselines within stated tolerance | F3 | Gate C | Wire `resource_sim` behind the contract's `StateVar` interface |
| F5 | No action applies without (ratified ∧ certified-non-steering ∧ within constraints) | F2, F3, F4, F6 | **Gate D — the kernel** | One cycle, one department, one guideline, end to end |
| F7 | Closed loop respects physical bounds under the roadmap's Gate-2/Gate-5 envelope | F3, F4 | Gate D | Port `resource_sim` into a `DepartmentSpec` |
| F8 | Fiscal instrument funds the public-goods bill **and** passes I8 (no quantity allocation) | F3, F4 | Gate D | Compute LVT-analogue yield on the twin's volume/area inventory |
| F9 | Never certifies what it cannot faithfully audit; escalates instead | F5 | Gate E | Reuse `fail_safe_gate` domain-check pattern on a second domain |
| F10 | Every named attack ends in *escalation or detection*, never silent success | F5, F7, F8, F9 | Gate E | Run W5 agenda-reordering attack against the kernel's menu |
| F11 | ≥12 cycles · ≥3 departments · adversarial load · reproducible via `pytest` | all above | **Gate F — terminal** | — |

### Cross-family flow-down (requirements that travel)

| From | To | Requirement that flows |
|---|---|---|
| Fork 1 (ratified) | **all** | The AI never selects the objective, amends its own constraints, or holds the exception |
| Fork 2 (ratified) | all | Scale = colony 100–1000; anything nation-scale is out of V1 scope |
| F0/V1 (walls) | F1, F5, F9 | Fail-closed boundaries: certify only inside the domain where the property is faithful |
| F0/V4 (Fuller) | F3 (I10), F5 | Every machine-emitted rule passes the legality linter |
| F0/V2 (Henry George) | F8 | The fiscal base and its efficiency claim |
| F0/V5 (space law) | F8, F5(D5 later) | Property regime must survive OST Art. II — usufruct + self-assessment (K7) |
| F1 | F3 | `Constraint.source = constitution` entries come from the charter, not the department |
| F3 (I8) | F7, F8, all depts | `LOW` legitimacy ⇒ rule/price instruments only. **This is the subsidiarity engine.** |
| F3 (I3) | F7↔F8 | Bilateral coupling declaration (both contend on pressurized volume + power) |
| F3 (I9) | F5, F9, F14 | Separation of powers: generate ≠ decide ≠ verify, ≤1 role per actor per decision |
| F6 | F5 | `ratify()` **gates** apply — a menu applies only if certified ∧ non-steering ∧ ratified |
| F6 | F9 | paper-RLA tamper audit is reused as the verification primitive |
| F2 | F5 | The compiled guideline set is the kernel's only source of objectives |
| F4 | F7, F8, F10 | Shared world-state; departments may not hold private copies of shared vars |
| `mars-governance` (D7) | **all** | Every "confirmed" result is MODEL-COHERENT, not governance-validated |
| roadmap Gates 2/5 | F4, F7 | Power and life-support-closure envelopes bound what the twin may assume |

**Critical path:**
`Gate A {F0 ∥ F1} → Gate B {F3 ∥ F2 ∥ F6} → Gate C {F4} → Gate D {F5 ∥ F7 ∥ F8} → Gate E {F9 → F10} → Gate F {F11}`
Cross-cutting throughout: **F10** (adversarial) should run *early and repeatedly*, not only at Gate E — every
gate emits an attack surface, and a red-team pass at each gate is cheaper than one at the end.
Deferred: **F12**.

---

## 3. VOI-ranked first moves

Ranked by (expected progress + expected info gain) / cost. Coarse buckets only — no fabricated numeric score
(the Cost column in a real ledger is free-form; `advance_ranker` deliberately computes no number).

| Rank | Move | Progress | Info gain | Cost | Why |
|---|---|---|---|---|---|
| 1 | **Ratify the 3 idea-anchor forks** | high | high | ~0 | Blocks nothing technical, but the wrong answer to Fork 1 invalidates every downstream artifact. Authority decision — user only. |
| 2 | **F3 contract + validator** | high | high | low | The scaling primitive. Everything after it is additive; without it every department is bespoke. Also the cheapest anti-theater guarantee. |
| 3 | **F1 charter clause list** | high | high | low | Cheap to draft, and it exposes immediately how many clauses are actually checkable vs aspirational — a real measurement, not a doc. |
| 4 | **F0 V1 research memo** (the five walls) | medium | high | medium | Retires the largest correctness risk in the whole framing at one shot. |
| 5 | **F6 reuse port** | high | low | low | 193 tests of value for near-zero effort; but low info gain — we already know it works. |
| 6 | **F2 hand-compile 3 guidelines** | medium | **highest** | low | Directly probes crux A2. If guidelines don't compile, the project's shape changes — better to learn in hour 1 than week 3. |

Note the rank-2/rank-6 tension: **F2's information value is the highest of any technical move** because it tests
the assumption most likely to be false. Recommendation: do F3 and F2's cheap probe *together* in the first
increment — the probe is one hour and could reshape the contract.

---

## 4. `/project-init` seeding

Seeded now (unblocked):

```
/project-init "<umbrella goal>" --project-id aigov --horizon 12
/project-init "<F0 goal>"       --project-id aigov-foundations   --horizon 3
/project-init "<F1 goal>"       --project-id aigov-constitution  --horizon 3
/project-init "<F3 goal>"       --project-id aigov-dept-contract --horizon 3
```

Seeded on gate clearance (not now): `aigov-guideline-intake`, `aigov-collective-choice`, `aigov-twin`,
`aigov-kernel`, `aigov-dept-lifesupport`, `aigov-dept-economy`, `aigov-audit-arbitration`, `aigov-adversarial`,
`aigov-integration`. Deferred: `aigov-scale-gates`.

---

## 5. Terminal condition

**Phase-1 (this ledger's) terminal — mechanically assertable:**

> The AI Governor kernel, on the colony digital twin at electorate 100–1000, consumes a ratified guideline set
> and runs **≥12 decision cycles across ≥3 departments spanning all three central-legitimacy ratings**, where
> **every binding action is (ratified ∧ certified-non-steering ∧ constraint-satisfying) or fail-closed
> escalated**, under the F10 adversarial suite, reproducibly via `pytest`.

**The program terminal is NOT mechanical.** "AI government capable of running a colony/city/nation/world" is an
open-world goal with no mechanical closure. Soraya asserts phase-1 completion mechanically and then **requests
explicit user sign-off**; the judgment that no further families are needed is always the user's. Per the
inherited `mars-governance` D3/D7, phase-1 completion is *model-coherent software validation only* — the human
field test (Stage B) and formal verification (Stage C) remain the real gates, and no result here may be reported
as "governance-validated".
