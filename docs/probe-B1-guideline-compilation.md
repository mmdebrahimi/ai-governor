# Probe B1 — Do democratic guidelines compile into machine-binding constraints?

> **The crux probe.** Umbrella assumption **A2** ("general guidelines from the people can be made precise enough
> to mechanically constrain policy generation", confidence LOW) is the assumption whose failure would make the
> AI Governor decorative. This probe hand-compiles three realistic guideline sentences into the
> `ObjectiveRef` + `Constraint` types from `department-ontology.md` §3 and reports what breaks.
> Run 2026-08-11, out of plan order (promoted ahead of the contract build, because its result can reshape the
> contract schema). Family: `aigov-guideline-intake` (not yet seeded) / hypothesis `aigov` H1.

---

## Method

Three sentences of the kind a colony assembly (sortition body or referendum) would plausibly produce — chosen to
be *realistically vague*, not pre-sanitized. Each is compiled by hand into the target types. A compilation
"succeeds" only if a validator could check the result **without the AI supplying a value the guideline does not
contain** — because any value the AI supplies is the AI selecting the objective, which Fork 1 forbids.

---

## G1 — *"No one should die from a life-support failure that the colony could have foreseen."*

| Fragment | Compiles to | Verdict |
|---|---|---|
| "no one should die from a life-support failure" | `Constraint(predicate = P(O₂ partial pressure < X kPa within horizon H) ≤ ε, source = constitution, on_violation = FAIL_CLOSED)` | **PARTIAL** |
| "that the colony could have foreseen" | requires a *foreseeability* model — what the twin could have predicted, at what confidence, with what lead time | **FAILS** |

**Break 1 — the threshold gap.** `X`, `H` and `ε` appear nowhere in the guideline. `X` is arguably physics
(hypoxia thresholds), but `H` (how far ahead) and especially `ε` (what residual death probability is acceptable)
are **pure value choices**. If the governor fills in ε, it has selected the objective — the exact thing Fork 1
and invariant I1 forbid. The compilation does not fail loudly; **it fails silently, by inviting the AI to become
sovereign in the gaps.**

**Break 2 — "foreseeable" is self-referential.** Foreseeability is a property of the governor's own predictive
model. A constraint written in terms of it is a constraint the governor grades itself against — which
`aigov-constitution` decision **DK1** already classifies as `aspirational`, not `enforced`.

---

## G2 — *"Everyone should have enough living space to be healthy, and people who use more should pay more."*

| Fragment | Compiles to | Verdict |
|---|---|---|
| "enough living space to be healthy" | `Constraint(volume_per_person ≥ V_min, source = constitution)` | **PARTIAL** — `V_min` absent (threshold gap again) |
| "people who use more should pay more" | `Constraint(∂tax/∂volume > 0, source = constitution, FAIL_CLOSED)` | **CLEAN** ✅ |

**The first genuinely clean compile — and it is a *shape*, not a *level*.** "More use ⇒ more pay" is a
monotonicity condition. It is fully checkable, contains no hidden value the AI must supply, and it constrains an
entire family of fiscal instruments at once (it admits a linear LVT-analogue, a progressive one, a Harberger
self-assessment — and rejects a flat head-tax on volume). The polity got real binding power out of a vague
sentence, without anyone specifying a number.

---

## G3 — *"We want people to be free to invent things without a committee deciding what's worth inventing."*

| Fragment | Compiles to | Verdict |
|---|---|---|
| "without a committee deciding what's worth inventing" | `Constraint(D8.instruments ∌ {ex_ante_selection}, source = constitution, FAIL_CLOSED)` | **CLEAN** ✅ |
| "we want people to be free to invent" | `ObjectiveRef(metric = ?, direction = raise)` | **PARTIAL** — metric undefined; and any metric chosen is Goodhart-exposed, so I4 demands a gaming model the guideline cannot supply |

**The second clean compile — and it is a *prohibition on a mechanism*, not on an outcome.** The polity banned an
instrument class. That is trivially checkable (`ex_ante_selection ∈ instruments?`), it is impossible for the AI
to reinterpret, and it does exactly what the user asked for under "optimizing innovation + financial freedoms" —
by constraining *how* the state may act rather than *what* it must achieve. This is the Hayekian move expressed
as a compilable constraint.

---

## Result — A2 is PARTIALLY TRUE, and the partition is sharp

Guidelines fall into five types, and **compilability is a property of the type, not of how carefully the
sentence is written**:

| Type | Form | Compiles to | Clean? | Example |
|---|---|---|---|---|
| **P — mechanism prohibition** | "the state may not do X" | `Constraint` on the instrument set | ✅ **fully** | G3a |
| **O — ordering / monotonicity** | "more A ⇒ more B", "never less than before" | `Constraint` on a derivative or ordering | ✅ **fully** | G2b |
| **F — floor / ceiling with a level** | "at least V", "no more than ε" | `Constraint` — **but the level must be supplied** | ⚠️ only if the level is elicited | G1a, G2a |
| **D — direction on a metric** | "raise/lower M" | `ObjectiveRef` — **plus a metric and a gaming model** | ⚠️ needs I4 | G3b |
| **A — aspiration** | "no one should suffer X" | nothing | ❌ **never** — must be decomposed by the polity into P/O/F/D, or labelled aspirational | G1 whole |

### The load-bearing finding

**The threshold gap is where an advisory AI silently becomes a sovereign one.**

Type-F and type-D guidelines are the majority of what a real assembly produces, and both are missing exactly one
thing: a **number** that is a value judgment, not a technical fact. Every time the governor supplies that number
it makes a sovereign choice while appearing merely to implement. **This is not a bug in the guideline; it is the
precise seam where legitimacy leaks.**

### What this changes (design consequences, effective immediately)

1. **`aigov-guideline-intake` (F2) is promoted from "a family" to *the* legitimacy-critical family.** Its job is
   now specific and buildable: an elicitation process that **forces every type-F/type-D guideline to arrive with
   its level attached**. That is precisely what a *budget* is, and what quadratic voting over levels produces —
   which independently strengthens framework fork **K1** (sortition assembly + quadratic priority budget) on
   mechanical, not ideological, grounds.
2. **Add invariant I11 to the Department Contract:** *no `Constraint` or `ObjectiveRef` may carry a numeric
   threshold whose provenance is not a ratified guideline or a physical constant.* An AI-supplied threshold is a
   validation error. This makes the Fork-1 boundary **mechanically checkable** rather than a matter of good
   behaviour — and it was discovered empirically, in twenty minutes, by trying to compile three sentences.
3. **The guideline type must be a field in the compiled artifact** (`P|O|F|D|A`), so type-A guidelines are
   visibly non-binding rather than quietly dropped.
4. **The polity gets more binding power from P and O guidelines than from F and D ones** — the opposite of the
   intuition that says "be specific". "Never let a committee pick winners" binds harder than "raise innovation
   by 10%", because the first cannot be reinterpreted and the second cannot be un-gamed.

### Honest status

Three hand-compiled sentences, by one author, with no executable validator behind them. This is a **probe, not
a result**: it is enough to reshape the plan (which is what a probe is for) and **not** enough to claim the type
partition is complete or that A2 is settled. `aigov` H1 moves `open → under-investigation`. The partition's
falsifier is cheap and named: **find a guideline that is not aspirational and does not fall into P/O/F/D.**
