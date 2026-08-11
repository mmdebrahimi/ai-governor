# AI Government — Idea Anchor (DRAFT, awaiting user ratification)

> **Status: DRAFT.** `/idea-anchor` is a park-and-ratify skill under the Soraya contract — Soraya may draft
> it, never anchor it. Its protocol was executed by hand (rephrase → ≤3 fundamental questions → assumptions
> → blunt critique → next step). The three forks in §2 are **authority decisions**, not technical ones;
> Soraya's recommended answer is drafted for each so the user ratifies rather than authors.
> Date: 2026-08-11. Author: Soraya (executed `/idea-anchor` protocol by hand — the Skill tool cannot invoke it).

---

## 1. Rephrase (formal statement of the idea)

Build an **AI Government**: a composable system of *departments*, each covering one function a polity must
perform (fiscal policy, collective choice, trade, justice, life-support/resources, innovation, education,
security, …), coordinated by an **AI Governor** — a runtime that

1. **ingests** a set of general guidelines produced by a democratic process (the polity's ratified values,
   priorities and constraints — not a policy list),
2. **instantiates** the concrete institutional framework those guidelines imply: rules, budgets, instrument
   settings, procedures, and the metrics they will be judged by,
3. **operates and adapts** that framework over repeated decision cycles under real resource constraints, and
4. **remains auditable and reversible** at every step — every binding action traceable to a ratified guideline
   and to a certified, non-steering procedure.

Target instance ladder: **Mars colony → city → nation → (aspirationally) planetary.**
Epistemic standard, inherited from the existing `mars-governance` ledger (decision D1): the system is
**designed and TESTED before the polity it governs exists** — staged software simulation → human field test →
formal verification.

**The one-sentence version.** *A constitutionally-bounded machine that converts democratic intent into a
running, auditable institutional framework — proven in simulation before it is ever given power.*

---

## 2. The three fundamental questions (authority forks — user ratifies)

These are the only questions whose answers **change the framing** rather than the implementation. Each carries
Soraya's drafted position + the risk of the alternative.

### Fork 1 — Is the AI a *sovereign* or an *administrative organ*?

| Option | Meaning |
|---|---|
| **(a) AI as administrative + analytic organ** *(recommended)* | The AI generates options, simulates consequences, drafts instruments, executes ratified rules, and audits itself. **Humans hold all binding authority.** The AI may never select the objective function, amend its own constraints, or override a ratified decision. |
| (b) AI as sovereign decider | The AI optimizes a social welfare function and issues binding decisions; humans supply only high-level guidelines. |

**Drafted position: (a), and encode it constitutionally rather than stylistically.**

*Why.* Three independent reasons, one ethical and two formal:

1. **There is no correct social welfare function to optimize.** Arrow's impossibility theorem (no rank-order
   aggregation rule satisfies unanimity + independence + non-dictatorship) and Gibbard–Satterthwaite (any
   non-dictatorial, onto rule over ≥3 alternatives is manipulable) mean an AI sovereign does not *discover*
   the polity's preference — it *imposes* a choice of aggregation rule, which is itself a contested value
   judgment it has no legitimacy to make. Option (b) doesn't remove politics; it hides it inside a weight vector.
2. **Legitimacy, not capability, is the binding constraint.** A perfect optimizer with no mandate is
   ungovernable-by-consent; the first genuine conflict destroys it. Option (a) makes consent the load-bearing input.
3. **The existing asset already commits to (a).** `Mars_Governance/governance/ai_advisor.py` curates *option
   menus* (never chooses); `binding_elections.ratify()` **gates** `run_advised_cycle`; `fail_safe_gate.py`
   escalates rather than certifying what it cannot audit; `exogenous_preferences.py` is an anti-steering check.
   Flipping to (b) discards ~193 green tests of exactly the right shape and re-opens every risk they closed.

*Risk of (b):* the project becomes an argument for technocratic autocracy — unadoptable, and formally
indefensible on its own terms. *Residual risk of (a):* "advisory" AI can steer through agenda control; this is
a real capture channel and is precisely what the anti-steering + fail-closed primitives exist to bound.

### Fork 2 — What scale is V1 actually targeting?

| Option | Electorate | Notes |
|---|---|---|
| **(a) Colony scale, 100–1000** *(recommended)* | 10²–10³ | Matches the existing `mars-governance` scale parameters (D2: electorate 100–500, resources 10–1000). Direct democracy is genuinely tractable here. |
| (b) City scale | 10⁵–10⁶ | Direct democracy degrades; needs delegation/liquid democracy + a professional administration layer. |
| (c) Nation-general from the start | 10⁷–10⁸ | Direct democracy on all matters is arithmetically impossible (attention budget). |

**Drafted position: (a) for V1, with the scale transitions named as explicit gates rather than a "later" hand-wave.**

*Why.* **Scale is a phase change, not a parameter.** At 10³ a citizen can plausibly attend to the proposals
that affect them; at 10⁸ they cannot, so *every* nation-scale design is necessarily representative/delegated
and the mechanism problem is different in kind. Building for (a) first is not a retreat: it is the only rung
where the "TESTED before it exists" bar is reachable, and it is where the reusable asset already lives. The
"eventually the world" clause should be an explicit **non-goal of V1** with named gates, or the project is
unfalsifiable.

*Named scale gates (proposed, to be worked in a later family):* G1 attention-budget breach (proposals/yr ×
citizen minutes > available civic time) → delegation required. G2 enforcement-distance breach (rules cannot be
observed locally) → federation/subsidiarity required. G3 exit-option collapse (citizens cannot leave) →
minority-protection hardening required.

### Fork 3 — What is the primary deliverable in ~1 month?

| Option | Deliverable |
|---|---|
| **(a) A runnable governed simulation** *(recommended)* | An executable AI-Governor kernel + ≥3 departments operating a simulated colony on a digital twin over ≥12 decision cycles, with a passing test suite and an adversarial-stress report. |
| (b) A framework/constitution document | A rigorous written institutional design; no runtime. |
| (c) A deployable stack for a real community | Software a real group (DAO, co-op, town) could actually adopt. |

**Drafted position: (a).** It is the only one of the three that is *falsifiable* on the month horizon, it
directly extends the 193-test asset, and it is the literal meaning of "TESTED before the colony exists."
(b) is a by-product of (a) — the constitution is an *input file* to the kernel, so you get the document anyway,
but a version that has been executed against adversaries rather than merely written. (c) is a plausible V2 but
imports legal, identity and adoption problems that would consume the whole month before any mechanism is tested.

---

## 3. Assumptions currently embedded in the idea (named, mostly unproven)

| # | Assumption | Confidence | Where it gets tested |
|---|---|---|---|
| A1 | A polity's functions decompose into separable **departments** with a uniform interface | medium | F3 (department contract) — falsified if ≥2 departments cannot be specified without shared mutable state |
| A2 | "General guidelines from the people" can be expressed precisely enough to **mechanically constrain** policy generation | **low — the crux** | F2 (kernel): guidelines must compile to constraints/objectives; if they can't, the governor is decorative |
| A3 | A simulation can validate governance mechanisms before real citizens exist | medium | inherited from `mars-governance`; Stage-B human field test is the real gate |
| A4 | The central-planning objection (Hayek) is weaker in a **closed life-support colony** than on Earth | medium-high | F0/F4 — the closed physical loop genuinely makes O₂/water/power centrally plannable; almost nothing else is |
| A5 | Optimizing "taxes / trade / innovation / financial freedom" simultaneously is coherent | **low** | F0 — these trade off; the governor must expose the frontier, not claim an optimum |
| A6 | Adversarial pressure (capture, gaming, preference falsification) can be simulated meaningfully | medium | F6 (adversarial stress) — synthetic adversaries are weaker than real ones; name it, don't hide it |
| A7 | An AI can be *constitutionally* constrained by rules it also executes | **low — needs structure, not prose** | F1: separation `generator ≠ tally ≠ verifier`, already a flow-down requirement in `mars-governance` |
| A8 | Scale-out (colony → city → nation) is continuous | **low — likely false** | Fork 2 gates; treat as phase changes |

---

## 4. Blunt early critique (carry into design; do not soften)

1. **"AI government" is the maximal high-modernist artifact — and Scott's *Seeing Like a State* is a direct
   attack on it.** State legibility projects fail not because planners are stupid but because making society
   legible *destroys the local practical knowledge* (mētis) that made it function. Any design that begins
   "the AI knows the state of society" has already lost the argument. **The counter-design is polycentricity
   + subsidiarity** (Ostrom): the governor centrally runs only what is *physically* forced to be central, and
   otherwise maintains the conditions for decentralized discovery (prices, possession rules, courts, freedom
   to experiment). This is not a compromise — it is what makes "optimize taxes" and "maximize financial
   freedom / innovation" non-contradictory instead of incoherent.

2. **The Hayekian knowledge problem is the strongest objection and the colony is the one honest exception.**
   Dispersed, tacit, locally-revealed knowledge cannot be aggregated by a central computer — *except* where
   the resource is a hard closed physical loop with catastrophic failure (O₂ partial pressure, water, power,
   pressure integrity, radiation dose). A Mars colony is precisely that case. **This is the strongest possible
   justification for the project and it must be stated with its limit attached**: the justification does *not*
   generalize to a terrestrial nation's economy. Claiming otherwise is the single fastest way to make the work
   indefensible.

3. **Theater risk is the #1 failure mode.** Sixteen elegant department specs that no one can falsify is the
   default outcome of a project shaped like this. The structural defence is the **department contract**: a
   department is only real if it declares *state variables · instruments it may move · objectives it is GIVEN
   (never chooses) · hard constraints · metrics · known failure modes · one executable falsification test*.
   A "department" that cannot fill that contract is an essay, and should be labelled one.

4. **A1 (separability) is doing more work than it looks like.** Fiscal policy is not separable from labor,
   housing, health or innovation — that's *the* lesson of general-equilibrium economics. The contract must
   therefore make **coupling explicit** (declared shared state + a coordination organ that arbitrates), or the
   departments will silently fight and the twin will produce plausible nonsense.

5. **"Guidelines input by democracy" hides a full research problem (A2).** *How* does a population express a
   guideline that is precise enough to bind a machine, without a technocrat writing it for them? Options exist
   (constitutional principles + budgets + weighted priorities + veto rights + quadratic-voted priority
   allocation), all with known pathologies. If this isn't solved, the AI Governor is a technocrat with a
   plebiscite fig-leaf — which is exactly the thing to avoid.

6. **Emergency power is the unresolved hole the prior roadmap already flagged verbatim:** *"who holds emergency
   override authority when a binding vote conflicts with a life-support hard limit?"* Every governance system
   dies at this seam (Schmitt's point, whether or not one likes his answer). It must be designed explicitly —
   who declares it, what it may touch, what it may never touch, how it auto-expires, and who audits it — or
   the emergency channel becomes the capture channel.

7. **The month horizon is a plan-scoping constraint, not a capability estimate.** In one month, "runnable
   kernel + 3 departments + adversarial stress on a twin" is achievable. "All departments a society needs"
   is not, and committing to it guarantees a shallow result across the board. Depth on three beats a gloss
   on twelve — and the department contract is what makes the other nine *additive later* instead of a rewrite.

8. **Honest inheritance.** The prior `mars-governance` work carries decision **D7: all Stage-A "confirmed"
   results are MODEL-COHERENT, not governance-validated.** That caveat transfers wholesale to everything built
   here. Nothing in this project may be reported as "validated governance" on the strength of a green test suite.

---

## 5. Recommended next step

**Ratify the three forks in §2** (that is the only blocking input), then run the decomposition in
`docs/decomposition-flowdown.md` starting at **F0 (foundations canon scan)** and **F1 (constitutional core)**
in parallel — both research-only, both cheap, both gate everything downstream.

Do **not** start any department implementation before **F3 (department contract)** exists; that is the
sequencing decision that determines whether this project scales to twelve departments or collapses into twelve
bespoke essays.

---

## 6. Relationship to existing work (verified 2026-08-11)

| Asset | Path | Status | Role here |
|---|---|---|---|
| `mars-governance` umbrella (9 families) | `Space_Reflectors_Project/Mars_Governance/project_state/` | Stage-A MVP across families | **Collective-choice organ** — becomes a department, not a rival project |
| Governance code + tests | `Space_Reflectors_Project/Mars_Governance/` | **193 tests pass** (re-run 2026-08-11) | Kernel primitives: advisor, ratify-gate, fail-closed escalation, anti-steering |
| Colonization roadmap (6 modules, gates 0–6) | `Space_Reflectors_Project/drafts/modular_space_colonization_roadmap_v2_DEEP_2026-06-06.md` | worked/open ledger | Physical-constraint envelope the twin must respect |
| Mars ISRU research memos | `Skill_Development/research_outputs/mars-isru-propellant-*` | audit-tier | Resource department grounding |
| `research-department`, `sme-panel`, `/research`, `/innovate` | `~/.claude/skills/` | shipped | The government's *research organ* — already built |
| Soraya minister/portfolio machinery | `~/.claude/skills/soraya/` | shipped | The *execution* substrate (Φ-bounded mission driver) |
