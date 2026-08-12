# Idea Anchor v2 — the governance instrument (ANCHORED 2026-08-11)

> **Status: ANCHORED.** `/idea-anchor`'s protocol was executed by hand (rephrase → ≤3 fundamental
> questions → assumptions → blunt critique → next step) and the **three fundamental questions were
> answered by the user on 2026-08-11** — see §2. This is now the north star of record. The critique in §4
> is NOT superseded by ratification: the named risks stand and must be carried forward.
> Date: 2026-08-11. Supersedes `idea-anchor-DRAFT-2026-08-11.md` (v1, Mars-colony target) in TARGET, not
> in content — see §6.

---

## 1. Rephrase

**The idea, stated formally:**

> A **governance instrument** that converts an organisation's messy, partial and partly-undocumented
> information environment into a **governed decision loop** — by deriving what must be *known* from what
> must be *decided*, interrogating people for whatever is missing or ambiguous rather than inferring it,
> and progressively assuming the analytic and executive load while **decision authority stays with humans**.

Four claims are doing the work, and each is falsifiable:

| # | Claim | Falsifier |
|---|---|---|
| R1 | Data requirements are **derivable** from declared decisions, not enumerable in the abstract | an organisation whose decisions are known but whose data needs still can't be derived |
| R2 | The **gap** between needed and available is itself a valuable output | a gap report a real organisation shrugs at |
| R3 | Missing or ambiguous information must be **elicited, never inferred** | a case where asking is so costly that inference is the only viable path |
| R4 | Autonomy in **analysis and execution** is separable from authority to **decide** | a deployment where the separation collapses in practice (see critique §4.3) |

**First instance:** a family-run, multi-country land enterprise — forestry, regenerative and automated
farming, a high-value products chain, and eco-tourism on the same land — operated as **permanent capital**
across horizons from ~1 to ~40 years.

**What this is not:** not an AI that governs; not a data warehouse; not a dashboard. The distinguishing
feature is that it is **honest about its own ignorance** and structurally unable to paper over it.

---

## 2. The three fundamental questions — ANSWERED 2026-08-11

> **All three were answered with the "keep both doors open" option, and the pattern is deliberate.**
> The user has permanent capital and no external clock, so optionality is rational here in a way it would
> not be for a funded venture. Soraya's drafted positions (each the narrower, faster option) were NOT
> taken; they are preserved below unedited so the reasoning that was set aside stays visible.
>
> | Q | Answer | Soraya had drafted |
> |---|---|---|
> | Q1 primary artifact | **Both, deliberately coupled** | gap report first |
> | Q2 domain | **Neutral core, land pack on top** | opinionated for land |
> | Q3 users | **Family-only, but open-source the framework** | family-only |
>
> **Architectural consequence (the three answers compose cleanly):**
> - the **department contract is the neutral core** — it already is, and stays domain-agnostic;
> - a **land pack** sits on top: parcel register, asset/cohort register, SEEA ecosystem accounts,
>   remote-sensed area frames — shipped as specs against the same contract, not as a fork;
> - the **gap report and the governance layer consume the SAME contract** and ship together, so neither
>   is validated in isolation and the detour risk in Q1 is structurally removed;
> - **public/private split matches the existing repo boundary**: neutral core + land pack are open, the
>   family's instance and data are not.
>
> **The one cost, carried honestly (see §4.8):** all three answers move the moment of contact with a real
> human further out, and that is the single axis this project has never tested.



These are the only three whose answers change the *framing* rather than the implementation. Everything
else is downstream and Soraya will resolve it.

### Q1 — Is the primary artifact the GAP REPORT or the GOVERNANCE ADVICE?

| Option | What the project becomes |
|---|---|
| **A — Gap report first** *(drafted)* | A diagnostic instrument: "here is what you would need to know to run this well; here is what you have; here is what's ambiguous; here is what's missing and what it would cost." Governance advice is a later layer built on the same contract. |
| B — Governance first | A decision-support system; the gap analysis is an internal subroutine, never shipped as a product in its own right. |

**Drafted position: A.** Four reasons, strongest first:
1. **It is the only part that can be validated by a human this month.** The standing hole in this entire
   project is that *no real person has ever used any of it*. A gap report is delivered to people who
   immediately know whether it is insightful or obvious.
2. **It fails safe.** A wrong governance recommendation is harmful; a wrong gap report is merely an
   argument, and the human's correction *is* the ontology work. That inverts the usual risk of being wrong.
3. **It is shippable without the kernel, the twin, or a ratified guideline set** — three of the four
   pieces it needs already exist.
4. **For a greenfield operation it is worth more, not less** — telling you what to instrument *before*
   you plant is far cheaper than retrofitting measurement onto a running farm.

**Risk of A, stated plainly:** it is a scope reduction that can dress itself as strategy and quietly
become a permanent detour from governance. Mitigation: both must run off the **same department contract**,
so the gap report is a *stage of* the governor, not a different product.

### Q2 — Is the instrument OPINIONATED about land/physical-asset enterprises, or DOMAIN-NEUTRAL?

| Option | Consequence |
|---|---|
| **A — Opinionated: land and physical-asset operations** *(drafted)* | Ships with a real starting ontology — parcel register, asset/cohort register, SEEA ecosystem accounts, remote-sensed area frames. Immediately useful, narrower market. |
| B — Domain-neutral | Ships an empty framework the user must populate. Broader in principle, far weaker in practice. |

**Drafted position: A, strongly.** This is the question I most want answered and the one I think is
least obvious. The V13 research produced a *large* amount of domain-specific leverage for land:
- **SEEA Ecosystem Accounting** became a full international statistical standard in March 2021 — extent,
  condition and services, spatially explicit, 89 countries on the central framework. It is the existing,
  credible vocabulary for exactly the carbon and ecosystem value you want to sell.
- **Area Sampling Frames + remote sensing** are a mature toolkit (FAO handbooks; USDA-NASS Cropland Data
  Layer; India's FASAL; EC MARS; GEOGLAM). **Statistics Canada replaced an agricultural survey outright
  with satellite imagery.**
- **Point sampling needs only an accurate map** — no pre-existing register. That is precisely the
  greenfield-in-a-country-with-no-agricultural-statistics case.

A domain-neutral tool can offer none of this. It can only offer the empty derivation. **An opinionated
land instrument is perhaps ten times more useful on day one, and the generality is preserved anyway
because the department contract underneath is domain-agnostic.**

### Q3 — Is the user your family only, or is this built for others?

| Option | Consequence |
|---|---|
| **A — Family-only for the foreseeable future** *(drafted)* | No UI burden, no support, no liability surface, no genericity tax. Optimise wholly for depth on one real case. |
| B — Built for others from the start | Forces multi-tenancy, onboarding, support, and — the real cost — an answer to *who is liable when the advice is wrong and someone acted on it*. |

**Drafted position: A, with one deliberate exception.** Build for yourselves; keep the **department
contract and the derivation** clean enough to lift out later. Do not build multi-tenancy, auth, or a UI
for hypothetical users. The single exception: **write the gap report as if a stranger would read it**,
because that discipline is what makes it a product later, and it costs nothing now.

**The unasked question behind Q3, surfaced rather than buried:** if this ever advises people outside the
family on decisions involving real money, "who is accountable when it is wrong" stops being philosophical.
That is a genuine authority call and it belongs to you, not to me.

---

## 3. Assumptions currently embedded (named, with confidence)

| # | Assumption | Confidence | Where it gets tested |
|---|---|---|---|
| A1 | An organisation's **decisions** can be enumerated well enough to derive its data needs | **LOW–MEDIUM — the new crux** | see critique §4.1 |
| A2 | People will actually **answer** the system's questions | **LOW — the operational crux** | first real gap report |
| A3 | The gap report is valuable on its own (R2) | MEDIUM, untested | first real delivery |
| A4 | An ontology can be *proposed* reliably enough to be worth ratifying rather than authoring | MEDIUM | ontology-induction family |
| A5 | The Mars-derived machinery transfers to an Earth enterprise | MEDIUM–HIGH for contract/charter/intake; **LOW for the twin** | the twin is life-support-specific and largely does not transfer |
| A6 | Users will accept *options + a frontier* rather than demanding a single answer | **LOW** | critique §4.3 |
| A7 | Family decision-making is a domain this tool should touch at all | **UNTESTED and contested** | critique §4.4 |
| A8 | Permanent capital makes multi-horizon holding an edge rather than a compromise | MEDIUM–HIGH | agreed; the fund-frame objection does not apply to a family office |
| A9 | Small-*n* disclosure limits are survivable at enterprise scale | MEDIUM | measured: at n≈200 three-way cross-tabs are 84% disclosive |

---

## 4. Blunt critique

### 4.1 The hardest problem is upstream of the one we are solving
The derivation runs **decision → statistic → observation → instrument**. It assumes the decisions are
*given*. They are not. Ask a farm manager "what decisions do you make?" and you get a list of *tasks*, not
decisions. Ask a family what it decides and you get either everything or nothing.

**Decision elicitation is a harder problem than data elicitation, and we have not touched it.** Every
piece of machinery built so far — the contract, the coverage checks, the whole V13 derivation — takes the
declared decision set as input. If that input is wrong, everything downstream is confidently wrong. This
is now the single largest unexamined assumption in the project (A1).

### 4.2 The unanswered-question problem will kill it before the ontology problem does
The design says: classify, then ask; never resolve an ambiguity by inference. Correct in principle.
In practice a system that asks forty questions receives six answers.

- **Fail-closed** (unanswered ⇒ field unusable) ⇒ the system is inert in any real organisation.
- **Fail-open** (unanswered ⇒ assume) ⇒ it is doing exactly the thing the whole architecture forbids.

Neither is acceptable and **I do not currently have a third answer.** Candidates worth testing: ask only
the *k* highest-value questions ranked by how much a decision changes on them; let an unanswered field
degrade the *confidence* of downstream advice rather than block it; or make the question itself the
deliverable. This is a real unsolved design problem and should not be smoothed over in a plan.

### 4.3 "Almost fully autonomous" and "never decides" are in more tension than I said last time
Our charter says the AI proposes a *menu* and humans choose. But:
- a menu of **one** is a decision wearing a costume — the human is rubber-stamping;
- a menu of **ten** is useless and gets delegated straight back.

**Authority lives in the cardinality and framing of the menu, and nobody has specified either.** The
McKelvey result already told us this — agenda control *is* control. We built anti-steering machinery for
exactly one instrument in the resource domain, and refuse to certify anything else. That refusal is
honest, but it means the governor can currently act on one lever. Scaling that honestly is unsolved.

### 4.4 Family governance is the highest-risk application, not the safest — and I want this on the record
It looks like the safe first target because it is small, trusted and available. I think it is the opposite,
for three reasons that the research this session produced directly:

1. **No exit.** You cannot fire your brother. The Tiebout mechanism that disciplines every other
   organisation — leave if you dislike it — is absent, which is exactly why our charter needed structural
   minority protection for the colony case.
2. **A legible record persists into every future dispute.** The Dutch-registry lesson generalises
   uncomfortably: harm came not from bad intent at collection but from **data persisting into changed
   circumstances**. A system that durably records who wanted what, and what the model recommended, creates
   an artefact that will be present in family disagreements a decade from now. "The system said" is a
   weapon in a way that "I thought" is not.
3. **The cost of being wrong is not financial.** A wrong operational recommendation costs money, which you
   can afford. A wrong family-governance recommendation costs relationships, which no capital repairs.

**Recommendation: point it at OPERATIONS first — parcels, plantings, yields, water, occupancy, cost —
and treat family/succession governance as a later, deliberately-decided extension, not a natural
continuation.** Retention limits (C29/C30) should be *tighter* for anything touching people than for
anything touching land.

### 4.5 The north star has moved twice in one session
v1 was a Mars colony. Then the family enterprise with Mars as simulator. Now a general governance
instrument with the enterprise as first instance. Each move was well-motivated, and I argued for two of
them — but three moves would mean the anchoring process is not working. **This document should hold for
weeks, or the problem is the framing method rather than the framing.**

### 4.6 The gap report may be a consulting deliverable rather than a product
What makes it valuable — deep engagement with one organisation's specific mess — is exactly what does not
scale. This is the wall every data-catalogue and data-governance startup has hit. It does not invalidate
Q1-A, but it does mean "the gap report is the product" needs testing on a *second* organisation before
anyone believes it generalises.

### 4.8 The ratified answers share one failure mode — and it is the one this project already has
Each of the three answers is individually defensible, and the "no external clock" reasoning is sound.
But they compose in one direction: **both-coupled** means neither artifact ships first; **neutral-core-
first** means the useful land pack arrives later; **open-source-the-framework** exposes the design to
scrutiny rather than the product to use. Every one pushes the first real user further out.

That matters because the standing hole is not architectural — it is that **no human has ever used any of
this**. Four sessions of green tests hid four real defects; the only reliable detector so far has been
running the thing and looking. A human using it is the same detector, one level up.

**Mitigation that costs nothing and preserves all three choices:** the decision-elicitation probe in §5 is
*unaffected* by every one of these answers. It needs no code, no core, no pack, and one hour. Under these
choices the build is longer, which makes the probe **more** important, not less.

### 4.7 Honest inheritance
Everything built so far is **model-coherent, not validated**. The research memos are **cited, not
quote-verified**. In four consecutive work sessions this month the test suite was **green while the
artefact was wrong** — the defect was found by inspection every single time, never by the suite. Treat
green as necessary, never sufficient.

---

## 5. Recommended next step

**Answer the three questions in §2.** They gate everything else, and two of the three (Q1, Q2) change what
gets built first.

Then, before any building: **run the decision-elicitation probe by hand.** Take ONE real operational
decision you actually face — say, *"which parcels do we plant next season, with what?"* — and run the
derivation manually: decision → the statistic it turns on → the minimum observation → the cheapest
instrument. Then check the two things that matter:
- Did it surface a data need you had not thought of? (tests R1/A1)
- Was the resulting question-list something you would actually answer? (tests A2)

That probe costs an hour and can invalidate the two weakest assumptions in the project. It is the direct
analogue of probe B1, which cost twenty minutes and produced the P/O/F/D/A partition plus invariant I11 —
by far the highest-yield thing done this session.

**Do not seed families or write code until Q1–Q3 are answered.** The current decomposition points at a
Mars colony and would scaffold the wrong twelve workstreams.

---

## 6. What survives from v1, and what does not

| v1 element | Status | Why |
|---|---|---|
| **D1 — AI is an administrative organ, never a sovereign decider** | **SURVIVES UNCHANGED** | Rests on Arrow / Gibbard–Satterthwaite, not on Mars. No correct preference aggregation exists to discover, so an optimizing sovereign merely hides a value choice. |
| **D2 — scale 100–1000** | **SURVIVES, coincidentally** | Staff + contractors + guests land in the same band. The small-*n* disclosure findings apply at full force. |
| **D3 — deliverable is a runnable governed simulation** | **SUPERSEDED** | v2 adds a live advisory instance, which v1 explicitly excluded. This is the one that moves. |
| Department Contract (I1–I11) | **SURVIVES** | Domain-agnostic by construction. |
| Charter + the four non-negotiables | **SURVIVES** | Machine limits are target-independent. |
| Guideline intake (sortition, QV, median, fail-closed) | **SURVIVES** | Directly reusable for family/stakeholder input. |
| Collective-choice organ (193 tests) | **SURVIVES as the ratification channel** | |
| **Colony twin** | **LARGELY DOES NOT TRANSFER** | It models O₂, thermal and pressure. A land twin models soil, water, carbon, biomass and cash. The *interfaces* transfer; the physics does not. |
| Mars, ISRU, Outer Space Treaty envelope | **DEMOTED to sandbox** | Useful as a consequence-free test environment, not as a destination. |

**Newly load-bearing, absent from v1 entirely:**
- **Ontology induction** — the "dynamic" capability.
- **The interrogation loop** — and the finding that the *gap* may be worth more than the computation.
- **The purpose→data rule** — the ontology is the **join** of what decisions require and what data exists.
  Data-only is the legibility trap; decisions-only is an unimplementable wish-list.
- **Retention as the control** (C29) — an access rule cannot bind a successor regime; only non-existence
  can. Implemented as `check_reverse_coverage`.
- **The fifth invented-something channel: MEANING.** Guessing what an ambiguous field means is the same
  class of act as inventing a threshold, and the most dangerous of the five because a wrong mapping is
  invisible and silently corrupts everything derived from it.

---

## 7. Privacy boundary (standing, non-negotiable)

Family composition, ages, capital position and property holdings are **private and must never enter any
repository**. This document and every committed artefact describe the venture at business-concept level
only — no names, no amounts, no jurisdictions. The repository is public.
