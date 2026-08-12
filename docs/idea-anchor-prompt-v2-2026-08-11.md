# Idea-anchor prompt v2 — the re-anchor after the north star moved

> **Status: DRAFT PROMPT, not an anchor.** This is the *input* to `/idea-anchor`, written for the user to
> paste and run. `/idea-anchor` is user-confirmed under the Soraya contract — Soraya drafts, the user
> anchors. Date: 2026-08-11.
>
> **Why a v2.** The north star moved twice this session: from *"AI government for a Mars colony"* (v1,
> `idea-anchor-DRAFT-2026-08-11.md`, forks ratified) to *"a dynamic governance AI, first instance an
> Earth-based family land enterprise, with the colony demoted to a simulator."* The v1 anchor and its
> three ratified forks are **superseded in target but not in content** — see §"What survives" below.
>
> **Deliberately left open.** The prompt below states what is known and leaves the genuine forks
> unresolved. `/idea-anchor`'s job is to ask at most three *fundamental* questions; handing it a finished
> specification would make that step ceremonial.

---

## The prompt (paste this after `/idea-anchor`)

```
I want to build a governance AI — a system I can point at whatever data an organisation or
community actually has, that works out the right way to structure that information, and then
advises on how to run the thing well. Over time I want it to take over more of the routine
execution itself so it runs almost autonomously, while the actual decisions stay with people.

The first real instance is our family's enterprise: a set of farms in several countries, run by
us — forestry for timber, automated and regenerative farming, a chain of high-value farm
products, and eco-tourism and retreats on the same land. We're doing this because we love the
work — robotics, AI, farming, hospitality — and because we think holding assets across very
different time horizons (a 40-year forest and a 2-year retreat business) is a strength rather
than a compromise: we have permanent capital and don't have to sell anything on someone else's
schedule. We also think the by-products are valuable in their own right — comparable farming
data across several countries, and a diversified carbon and ecosystem position backed by real
land.

I've already built a fair amount of the machinery. There's a contract that forces every
"department" to declare what it can measure, which levers it may pull, and what goals it was
given rather than chose. There's a charter of things the AI may never do, where each clause
says who enforces it and the unenforceable ones are labelled as aspirations. There's a way for
people to supply the numbers a vague instruction leaves out, so the AI never invents them. There's
a simulator, and a runtime that refuses to act on anything unratified.

What I don't have is the dynamic part. Right now every department is hand-authored. I want to be
able to connect a new data source and have the system work out the ontology — the entities, the
relationships, the measures that matter — instead of me writing it each time. That's the piece
that would make this a general governance AI rather than one bespoke model of one enterprise.

But I don't think "connect a data source" is the normal case, and this is the part I most want
thought through. Most organisations don't actually know what data they have. Half of what matters
isn't in any system — it's in someone's head, or a spreadsheet nobody owns. Half of what is in a
system is mislabelled, or the person who named the field left years ago. So the tool can't just
read databases and infer; it has to be able to interrogate the organisation itself. It should
work out what it would need to know in order to advise well, compare that against what actually
exists, and then come back with three honest lists: here's what I found and understood, here's
what I found but can't interpret without you telling me what it means, and here's what's simply
missing — with what it would cost to start collecting it and what decision it would improve.
I would much rather it ask ten awkward questions than quietly assume one answer. In fact I
suspect that gap report — "here is what you'd need to know to run this well, and here is how much
of it you don't have" — might be worth more on its own than the governance advice sitting on top
of it, at least at first.

What I'm genuinely unsure about: how much of the ontology the AI should derive on its own versus
propose for us to approve; whether the primary product is the governance advice or the gap report
that has to come first; whether the first target should be our own enterprise or something
deliberately more generic; how far "almost fully autonomous" can go before it stops being
advisory in any meaningful sense; and whether this stays a tool for our family or becomes
something other people use.
```

---

## What survives from v1 (do not re-litigate)

The v1 forks were ratified and the reasoning is target-independent. Carry them forward:

| v1 decision | Still holds? | Why |
|---|---|---|
| **D1 — the AI is an administrative organ, never a sovereign decider** | **YES, unchanged** | Rests on Arrow / Gibbard–Satterthwaite, not on Mars. There is no correct preference aggregation to discover, so an optimizing AI sovereign only hides a value choice. Applies identically to a family enterprise. |
| **D2 — V1 scale is 100–1000 people** | **YES, coincidentally** | A family enterprise with staff, contractors and guests sits in the same band. The small-*n* disclosure findings (V13 §6.1) apply with full force. |
| **D3 — deliverable is a runnable governed simulation** | **PARTIALLY** | Still the right *epistemology* (test before deploying). But the new north star adds a live advisory instance, which v1 explicitly excluded. **This is the fork most likely to move.** |

**What is demoted:** Mars, the colony, ISRU, the Outer Space Treaty envelope. The colony becomes the
**sandbox** — a safe place to test governance mechanisms with no real consequences — not the destination.

**What is newly load-bearing and was not in v1:**
- **Ontology induction** — the "dynamic" capability. Not in the v1 decomposition at all.
- **The purpose→data rule** (V13): *the logic runs from purpose to data, not the other way round.* This
  directly constrains the ontology-induction goal. Deriving an ontology **from data sources alone** is the
  legibility trap; deriving it from **decisions alone** yields an unimplementable wish-list. The ontology
  is the **join** of the two.
- **Retention as the control** (V13 §6.2) — an access rule cannot bind a successor regime; only
  non-existence can. Already implemented as `check_reverse_coverage`.
- **Multi-horizon is the thesis, not a tension.** Permanent capital makes long-dated illiquidity a
  discount you are *paid* to accept. Any framing that treats the four business lines as competing
  claimants is a fund frame misapplied to a family office.
- **The interrogation loop (added 2026-08-11 at the user's prompting).** The v2 draft assumed a data
  source *exists and is connectable*. That is the exceptional case, not the normal one. The system must
  be able to question the ORGANISATION, not merely read its databases — and the gap it reports may be
  worth more than anything it computes.

### The fifth invented-something channel: MEANING

Four channels through which the AI could supply something nobody gave it are closed by construction:

| # | Invented thing | Closed by |
|---|---|---|
| 1 | a **threshold** | I11 + departments reading levels from the ratified registry |
| 2 | a **level** | intake G1/G2 — a binding floor is unconstructible without a panel-supplied number |
| 3 | a **state reading** | twin DT1 — `read()` refuses LATENT; ESTIMATED carries method + error bar |
| 4 | a **future use** | C29 + `check_reverse_coverage` — data with no ratified consumer |
| **5** | **a MEANING** | **NOT YET CLOSED — this is the new work** |

An AI that guesses what an ambiguous field means is doing exactly what the other four forbid, and it is
the **most dangerous** of the five because it is invisible: a wrong threshold is a wrong number, but a
wrong mapping silently corrupts everything derived from it, and nothing downstream can detect it.

**Two-thirds of the detector already exists**, which the user's observation surfaced:

| Case | Detector | Status |
|---|---|---|
| needed but **not available** | `twin.check_state_coverage` — declared but unserved | ✅ built |
| available but **not needed** | `twin.check_reverse_coverage` — served but unclaimed | ✅ built 2026-08-11 |
| available + needed but **meaning unclear** | — | ❌ **the gap** |
| available + needed + clear but **untrusted** | — | ❌ (provenance/quality; a fourth class worth naming) |

The first case is already implemented as a *validation error*. The user's insight reframes it: at
discovery time it is not an error, it is **a question to ask a human**. Same detector, different mode.

**Design consequence, drafted:** the interrogation loop must **never resolve an ambiguity by inference**.
It classifies, then asks — and an unanswered question leaves the field UNUSABLE rather than guessed,
exactly as the intake leaves a polarized panel's level unset rather than averaging it. Fail-closed on
semantics, by the same discipline as fail-closed on everything else.

---

## The forks `/idea-anchor` will probably surface (Soraya's drafted positions, for ratification)

Recorded here so the user ratifies a draft rather than authoring analysis from scratch. **These are
predictions of the questions, not answers to be assumed.**

1. **Derive vs propose the ontology.** *Drafted position: PROPOSE, always.* The system infers a candidate
   ontology and the humans ratify it. A self-derived, self-adopted ontology is the AI choosing what
   counts — the same class of act as choosing the objective, which C01 forbids. Cheap to relax later,
   expensive to retrofit.
2. **Own enterprise vs generic product first.** *Drafted position: own enterprise first, with the
   department contract kept domain-agnostic.* The enterprise gives real humans, real money and real
   consequences — the thing the whole project has never had. Genericity is preserved by the contract's
   shape, not by building for a hypothetical second user.
3. **Where "almost fully autonomous" stops.** *Drafted position: autonomy in ANALYSIS and in EXECUTION
   of already-ratified rules; never in DECIDING.* This is not a compromise — it is what the kernel already
   enforces, and it is compatible with a very high degree of hands-off operation.
4. **Tool vs product.** *Genuinely open — this is an authority/strategy call, not a technical one.* Flagging
   it rather than drafting a position, because the answer changes what gets built and by whom.
5. **Is the GAP REPORT the first product, ahead of the governance advice?** *Drafted position: YES, and
   this may be the most consequential change in the whole re-anchor.* Reasons, in order of strength:
   - **It is shippable far sooner.** It needs the derivation (which V13 gives us) and the coverage checks
     (two of three already built) — not the kernel, not the twin, not a ratified guideline set.
   - **It validates the one axis we have never touched.** The standing gap in this project is that *no
     real human has used any of it*. A gap report is delivered to humans, who immediately know whether it
     is useful or nonsense. That is the fastest available route to the feedback we lack.
   - **It is valuable while being wrong.** A governance recommendation that is wrong is harmful. A gap
     report that is wrong is merely an argument — the human corrects it, and the correction is itself the
     ontology work. It fails safe in a way the governance layer does not.
   - **For a greenfield operation it is worth more, not less.** Telling an enterprise what to instrument
     *before* it builds is far cheaper than retrofitting measurement onto a running operation.
   *Risk of this position:* it is a scope reduction dressed as a strategy, and could become a permanent
   detour from the governance goal. Mitigation: keep the derivation shared — the gap report and the
   governor must run off the SAME department contract, so the first is genuinely a stage of the second
   rather than a different product.

---

## Privacy boundary (standing)

The family's composition, ages, capital position and property holdings are **private and must not enter
any repository**. Nothing of that kind appears in this prompt or in any committed file. The prompt above
describes the venture at the level of business concept only — no names, no amounts, no jurisdictions.
