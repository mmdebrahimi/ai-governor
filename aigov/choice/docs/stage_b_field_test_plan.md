# Stage B — Human Field-Test Plan (family `mars-gov-stage-bc-plan`)

The Stage-A bar was **software simulation under documented assumptions** — *model-coherent, not
governance-validated* (umbrella D1/D7). Stage B is the first test against the one thing simulation cannot
produce: **real humans**. It is a **plan**, not a build (class-e research-only); execution needs real
participants, ethics approval, and funding the agent cannot supply (an **external wall**, named honestly).

## Goal
Measure the **un-simulable** properties of the AI-advised direct-democracy design with real Earth-based
proxy participants, before any colony exists. Priority order (from the 2026-06-06 review): **comprehension
→ framing-sensitivity → agenda-trust/contestation → coercion/social-pressure → abstention**.

## Participants & setting
- **N ≈ 100–300** Earth proxy participants (analog-habitat crews — HI-SEAS / MDRS / Mars500 alumni pools —
  plus general-public cohorts for contrast). Mirrors the 100–500 electorate scale (D2).
- Repeated **decision cycles** over weeks on real (resource-allocation) questions with real stakes-proxies
  (small budgets / perks), run through the built sandbox UI over the `run_advised_cycle` pipeline.
- **Ethics/consent gate is mandatory and is a hard external dependency** — no field test runs without IRB-
  equivalent approval. Surface, do not bypass.

## Hypotheses → measurements (each falsifiable)
| # | Property | Measure | Pass signal |
|---|---|---|---|
| B1 | **Comprehension** | post-ballot quiz: can a voter restate each option + its resource consequence? | ≥80% correct on a held-out option |
| B2 | **Framing-sensitivity** | same underlying choice, two option-orderings/wordings (A/B) → outcome divergence | divergence ≤ a pre-registered ε |
| B3 | **Agenda-trust / contestation** | rate at which participants use write-in / citizen-injection; perceived-fairness survey | injection usable in <X min; fairness ≥ threshold |
| B4 | **Coercion / social-pressure** | seeded confederate pressure in a close-quarters subgroup → secrecy-leak / vote-shift | shift ≤ pre-registered bound |
| B5 | **Abstention** | turnout under public-aggregate vs (counterfactual) public-individual turnout | abstention-coercion channel absent |

## Design controls (anti-confound)
- **A/B framing arms** + a **no-recommendation control** (to isolate automation-bias).
- **Pre-registration** of every threshold (B1–B5) BEFORE data collection — thresholds are political, not
  technical (echoes the steering-threshold caveat); the user/IRB sets them, not the agent.
- The **AI advisor is the system under test** — its menus are logged for the standing bias audit; an
  **independent panel** rates option diversity (the real-human analogue of the C2-b exogenous check).

## What Stage B can FALSIFY that Stage A cannot
- That voters actually understand AI-curated menus (B1) — the legitimacy metric deferred since the voting
  family was a *constant*, not a measurement.
- That the positive agenda right is *usable* by real people under time/social pressure (B3) — not just
  expressible in code.
- That automation bias doesn't quietly convert "veto" into "rubber-stamp" (B2 + no-rec control).

## Wall classification (honest)
**External wall** — needs humans + ethics approval + funding. Code cannot close it; the agent's
contribution ends at this protocol + the instrumented sandbox. Converting to a code wall is impossible
here (the whole point is real-human signal). Next actor: **the user** (recruit + IRB + fund).

## Exit → Stage C
Stage B does NOT validate the formal state machine — it validates the *human interface*. Formal
correctness of the cycle (cert · disposal · ratification · fallback · invariants · caretaker) is **Stage C**.
