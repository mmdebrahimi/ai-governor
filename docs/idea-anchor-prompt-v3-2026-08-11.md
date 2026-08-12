# Idea-anchor prompt v3 — the re-anchor after V14

> **Status: DRAFT PROMPT, not an anchor.** This is the *input* to `/idea-anchor`, written for you to paste
> and run. `/idea-anchor` is user-confirmed under the Soraya contract — Soraya drafts, you anchor.
> Date: 2026-08-11.
>
> **Why a v3.** `docs/idea-anchor-v2-2026-08-11.md` is ANCHORED and its three fundamental questions are
> answered (D21–D25: coupled / neutral-core + land pack / family-only + open-source framework). Two things
> have happened since that make it stale as an *input*:
>
> 1. Those three answers are now **settled context**, not open forks. Feeding them back as questions wastes
>    `/idea-anchor`'s three-question budget.
> 2. **V14 changed the largest constraint in the project.** The governance-reform literature's central
>    finding — isomorphic mimicry — says a system that recommends institutional forms from a catalogue of
>    what worked elsewhere is a machine for producing the standard failure. That sits in direct tension with
>    "induce the right ontology and progressively run things autonomously," which is the stated goal. This
>    is a genuine, unresolved, north-star-level fork and it deserves the anchor's attention.
>
> **Deliberately left open.** The prompt states what is known and leaves the real forks unresolved.
> Handing `/idea-anchor` a finished specification makes its questions ceremonial.

---

## The prompt — paste everything inside the fence, after running `/idea-anchor`

```
I want to build a governance instrument. I point it at whatever information an organisation
actually has, it works out how that information should be structured, and it advises on how to
run the thing well. Over time I want it to take on more of the routine analysis and execution
itself, so it runs almost autonomously — while the actual decisions stay with people.

The first real instance is our family's enterprise: a set of farms in several countries, run by
us — forestry for timber, automated and regenerative farming, a chain of high-value farm
products, and eco-tourism and retreats on the same land. We're doing this because we love the
work — robotics, AI, farming, hospitality — and because holding assets across very different
time horizons (a 40-year forest and a 2-year retreat business) is our thesis rather than a
compromise: we have permanent capital and don't have to sell anything on someone else's
schedule. The by-products look valuable in their own right too — comparable farming data across
several countries, and a diversified carbon and ecosystem position backed by real land.

I've already built a fair amount of the machinery, and it works. There's a contract that forces
every "department" to declare what it can measure, which levers it may pull, and what goals it
was given rather than chose. There's a charter of things the system may never do, where each
clause names who enforces it and the unenforceable ones are labelled as aspirations rather than
hidden — about seventy percent of the clauses are machine-checked, and that fraction is a
measured number, not a claim. There's a way for people to supply the numbers a vague instruction
leaves out, so the system never invents a threshold. There's a simulator, and a runtime that
refuses to act on anything unratified. Roughly four hundred tests.

What I don't have is the dynamic part. Every department is hand-authored today. I want to
connect a new source of information and have the system work out the ontology — the entities,
the relationships, the measures that matter — instead of me writing it each time.

But I don't think "connect a data source" is even the normal case, and this is the part I most
want thought through. Most organisations don't know what data they have. Half of what matters
isn't in any system — it's in someone's head, or a spreadsheet nobody owns. Half of what is in a
system is mislabelled, or the person who named the field left years ago. So the tool can't just
read databases and infer. It has to be able to interrogate the organisation itself: work out what
it would need to know in order to advise well, compare that against what actually exists, and
come back with three honest lists — here's what I found and understood, here's what I found but
can't interpret without you telling me what it means, and here's what's simply missing, with what
it would cost to start collecting and which decision it would improve. I would much rather it ask
ten awkward questions than quietly assume one answer.

Then I did a deep read of how governance has actually worked and failed over the last few
hundred years, and it produced one finding that I think may cut against the whole idea, so I want
to put it in front of you rather than around it.

The best-documented failure mode in governance reform is that organisations adopt the outward
FORM of an institution that works somewhere else — the law, the board, the procedure — and the
function never arrives. It looks like reform for a while and then measurably isn't. If that's
right, then a system that generates plausible institutional arrangements from a catalogue of what
worked elsewhere is very good at producing exactly that failure, and better at it than a human
consultant would be. The prescription in that literature is the reverse of what I was building
toward: start from a problem the people there nominated themselves, and a measurable gap, and let
them propose the form. I don't know how to reconcile that with "induce the right ontology and
progressively take over the running of it." Both can't be fully true and I'd rather find out now.

Four more things I learned that I think constrain this, and haven't designed for:

Once a measure becomes a target it stops being a good measure, and the gaming is predictable in
shape — people hold performance back so next year's target stays reachable, and uniform targets
pull the good performers down to the line. My whole derivation runs from decisions to the
statistics that inform them, so I'm manufacturing exactly the objects that degrade this way.

The closest existing thing to "advises but doesn't decide" is an independent fiscal watchdog, and
the honest evidence is that those work mainly where the discipline was already there — and least
well where they're needed most. That might be the real ceiling on this whole idea.

When a decision about a person gets automated, accountability erodes because people defer to the
machine, and the wrongly-classified have nowhere to go. That's not hypothetical — it's the
mechanism behind the benefits scandal that brought down a national government.

And the thing that actually holds authority is the menu, not the decision. A menu of one is a
decision wearing a costume; a menu of ten gets handed straight back to me. Nothing in what I've
built specifies how wide that menu should be, or who frames it.

There's also a problem underneath all of it that I can't see past. The derivation runs backwards
from decisions — you tell me what you decide, I tell you what you'd need to know. But
organisations can't state their decisions either. Ask someone what decisions they make and you
get a list of tasks. If that input is wrong then everything downstream is confidently wrong, and
I have no idea how to get past it.

On that last point I've made a call, so treat it as settled input rather than an open question:
I do want the system to arrive at a recommendation and tell me what to do. But it has to get
there by interrogating me hard first — asking a lot of questions, and helping me work out what
the right first-principles questions even are. So the constraint isn't "never give an answer",
it's "the answer must be traceable to what you got out of me about my situation, not to a
template of what worked somewhere else."

What I'm still genuinely unsure about: how wide the menu of options should be, and whether that's
a technical parameter or the whole authority question in disguise; what happens when someone
doesn't answer an interrogation question — refusing to proceed makes it inert, guessing makes it
the thing I built it to prevent, and I don't have a third answer; whether the first target inside
our own enterprise should be operations or the family's own decisions; and how far "almost fully
autonomous" can actually go before it stops being advisory in any meaningful sense.
```

---

## What survives, and must not be re-litigated

These are ratified. If `/idea-anchor` reopens them, point it here.

| Decision | Status | Where |
|---|---|---|
| **D1** — the system is an administrative + analytic organ, never a sovereign decider | **RATIFIED, unchanged** | rests on Arrow / Gibbard–Satterthwaite, target-independent |
| **D2** — scale 100–1000 people | **RATIFIED, coincidentally still right** | an enterprise with staff, contractors and guests sits in the same band |
| **D21** — v2 north star: governance instrument, Earth, family land enterprise as first instance; Mars demoted to sandbox | **RATIFIED** | `docs/idea-anchor-v2-2026-08-11.md` |
| **D22** — Q1: gap report and governance advice ship **coupled**, on one contract | **RATIFIED** | not a fork any more |
| **D23** — Q2: **neutral core + land pack** on top, not a fork of the core | **RATIFIED** | |
| **D24** — Q3: **family-only use, open-source framework** | **RATIFIED** | |
| **Privacy boundary** | **STANDING** | family composition, ages, capital position and property holdings never enter any repository; the repo is public |

---

## The forks `/idea-anchor` will probably surface — Soraya's drafted positions, for ratification

Recorded so you ratify a draft rather than author analysis from scratch. **These are predictions of the
questions, not answers to be assumed.**

### 1. Does the instrument ever propose a FORM? *(the big one — V14 §1)*

**Drafted position: NO — and this is a hard rail, not a default.** The instrument emits a *problem* plus a
*measurable performance gap*; humans propose the form. Reasons in order of strength:

- It is what the evidence says works. PDIA's first principle is locally-nominated performance problems
  *instead of* transplanting best practice; the failure it names is precisely what a form-generator does.
- The same conclusion arrives independently from Khan's political settlements (a rule is under-specified
  unless you name who holds the power it redistributes) and from the resource-curse prescription critique
  (standard advice fails because it presupposes the capacity it is meant to create). Three routes, one place.
- It fails safe. A wrong gap report is an argument; the human corrects it, and the correction *is* the
  ontology work. A wrong institutional recommendation is harm.
- The contract already has the right primitive: **I6 (falsification test)** is the machine-checkable form of
  "looks reformed vs. performs better."

**What this costs, stated honestly:** it demotes "induce the right ontology and run it" from the goal to a
*bounded* capability — ontology induction becomes a proposal about *what to measure*, never about *how to be
organised*. If you want the system to design institutions, this position is the thing standing in the way,
and you should overrule it deliberately rather than let it erode.

### 2. Menu cardinality — technical parameter or the authority question? *(D20)*

**Drafted position: it is the authority question, and it should be answered in the charter, not in code.**
Recommended rule: the menu always contains **the status quo plus at most three alternatives**, each with its
falsification test and its named losers. Below that, the framing is doing the deciding; above it, the human
delegates back by fatigue. McKelvey's chaos theorem already tells us agenda control *is* control, so the
cardinality rule belongs where the non-negotiables live.

**This is flagged as carrying hidden authority** — it looks like a parameter and is actually the boundary of
who governs.

### 3. The unanswered question — what happens when nobody answers? *(anchor §4.2, still unsolved)*

**Drafted position: a third answer exists and is worth building — degrade, don't block.** An unanswered field
does not halt the analysis and does not get guessed. It **propagates as reduced confidence** into every
downstream conclusion that depends on it, and the conclusion carries the unanswered question as its
provenance. So the output is *"I can tell you this much, and here is the one question that would sharpen
it."* That makes the question itself a deliverable rather than a blocker, which is the behaviour you said you
wanted (ten awkward questions over one silent assumption).

Ranking rule: ask only the *k* questions with the highest decision-sensitivity — the ones where a different
answer changes a recommendation. Everything else stays unasked.

### 4. Operations first, or family decisions first?

**Drafted position: OPERATIONS first, unambiguously — and this reverses the intuition.** Family and
succession governance looks like the safest target because it is small and trusted. It is the highest-risk
one: you cannot fire a relative, so the exit discipline that constrains every other organisation is absent; a
legible record of who wanted what persists into every future dispute, and *"the system said"* is a weapon in
a way *"I thought"* is not; and the cost of being wrong is relational, which no capital repairs. Point it at
parcels, plantings, yields, water, occupancy and cost. Treat family governance as a deliberately-decided
later extension with tighter retention limits. (D19; V14 §5.1 is the empirical backing.)

### 5. How far can "almost fully autonomous" go?

**Drafted position: autonomy in ANALYSIS and in EXECUTION of already-ratified rules; never in DECIDING —
and never in MEANING.** This is what the kernel already enforces and it is compatible with a very high degree
of hands-off operation. The addition V14 forces: **meaning is the fifth invented-something channel and it is
the most dangerous**, because a wrong threshold is a wrong number but a wrong mapping silently corrupts
everything derived from it and nothing downstream can detect it. So an ambiguity is classified and asked,
never inferred.

---

## What has changed in the machinery since v2 (context for the anchor, not forks)

From `research_outputs/aigov-v14-governance-history-and-mechanisms.md`:

- **Three new drafted invariants** — I12 redress (any output classifying a person carries a named accountable
  human, a redress route that doesn't require the subject to disprove the model, and a bar on citing the
  system as justification); I13 no-profile-by-resemblance; I14 equilibrium check (must be able to emit *"no
  incremental recommendation is safe here"*).
- **I4′** — the gaming model extends from instruments to *derived measures*; ratchet and threshold effects
  are checkable from a measure's own definition.
- **I8 qualification** — a subsidiarity recommendation must name the tier where discretion actually sits plus
  a capture check at that tier; and flag any change that improves a proxy while the welfare quantity is
  unobserved.
- **Externally validated, no change needed:** I1 ≈ meritocratic recruitment; I6 ≈ the mimicry/performance
  distinction; DT1's `Estimate` (value + method + error bar) ≈ V-Dem's measurement model; C29 /
  `check_reverse_coverage` ≈ X-Road's minimal centralization.
- **An unresolved internal contradiction** — V13's four-layer architecture (registers → accounts → indicators
  → real-time) violates its own purpose→data rule at the register layer, because registers are built before
  the decisions that would justify them. Drafted resolution: registers are exempt from the *derivation* axis
  but bounded on the *retention* axis. Needs to be a recorded decision rather than an accident of
  implementation order.

---

## Privacy boundary (standing, non-negotiable)

The family's composition, ages, capital position and property holdings are **private and must not enter any
repository**. Nothing of that kind appears in the prompt above or in any committed file — the prompt
describes the venture at the level of business concept only: no names, no amounts, no jurisdictions. The repo
`github.com/mmdebrahimi/ai-governor` is **public**.
