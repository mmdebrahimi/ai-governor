# Idea-anchor prompt — autonomous farming swarm (2026-10-26)

> **Status: DRAFT PROMPT, not an anchor.** This is the *input* to `/idea-anchor`, written to paste
> and run. Date: 2026-10-26.
>
> **Relationship to the portfolio.** This is a candidate sibling (or child) of family F13
> `aigov-land-enterprise`. It is NOT yet a ledger family — whether it becomes one is downstream of
> the anchor. Two recorded facts it must be read against:
>
> 1. **F13 action log, 2026-09-01:** "AI/sensor build downgraded to hobby" — a ratified scoping
>    decision that made weak rural connectivity less disqualifying in the jurisdiction ranking.
>    This idea, taken seriously, SUPERSEDES that decision. The prompt says so explicitly rather
>    than letting the contradiction sit silent.
> 2. **F13 elicited programme:** long-rotation high-value trees (nuts), possible silvopastoral
>    livestock, residence + retreat. The crops this idea names (potatoes, berries, corn/wheat) are
>    NOT that programme. The mismatch is a real fork, not sloppiness — it is stated and left open.
>
> **Deliberately left open.** Per the v3 pattern: handing `/idea-anchor` a finished specification
> makes its questions ceremonial. Settled context is stated as settled; the forks are stated as
> forks.

---

## The prompt — paste everything inside the fence, after running `/idea-anchor`

```
I want to design an automated farming system: a coordinated set of farm machines — a swarm — that
can autonomously manage the production of common produce end to end. Assume ordinary crops:
potatoes, berries, corn or wheat. The system should handle the full production loop: planting,
continuous monitoring of whatever parameters matter (soil, moisture, plant health, weather
exposure), pest and disease management including spraying decisions, harvesting, and getting the
harvest into storage. Humans set the goals and ratify the rules; the machines run the season.

Context you should treat as settled, not re-litigate: our family is building a land enterprise —
farms in more than one country, held long-term with permanent capital. That venture is still
prospective (no farm is owned yet; jurisdictions are ranked and researched). We already have a
governance instrument with real teeth: a decision inventory that derives what the enterprise must
know from what it must decide, a contract that forces every component to declare what it measures
and which levers it may pull, a charter of things the system may never do, and a runtime kernel
that refuses to execute anything unratified — about 430 passing tests. "Autonomy in analysis and
in execution of already-ratified rules, never in deciding" is our standing rule, and a machine
swarm is, on paper, the purest possible instance of it: the ratified rules become the spray
thresholds, the harvest triggers, the irrigation schedule.

Now the two tensions I want put in front of you rather than hidden.

First, I am contradicting my own recorded decision. Two months ago, while ranking jurisdictions,
we explicitly downgraded the farm-automation build from a core capability to a hobby — it even
changed how we scored countries, because a hobby doesn't need rural broadband. This idea promotes
it back to a first-class system. I should either supersede that decision deliberately or admit
this is a hobby wearing a project's clothing. I genuinely don't know which it is yet, and I'd
rather you force the question than let me drift into a lab I never decided to fund.

Second, the crops don't match the farm. The enterprise programme we actually elicited is
long-rotation nut trees, possibly livestock grazing between them, and a residence with a retreat
business. Nothing in that programme is potatoes, berries, or wheat. So either this swarm is for a
farm we haven't decided to run — a second, annual-crop operation nobody has ratified — or it's
not really for our enterprise at all and is a venture in its own right (a product, a research
platform, or the thing we pilot on a leased field before any land is bought). Those lead to very
different designs and I've left it unresolved on purpose.

Third, and I know our own discipline well enough to flag it: "a swarm of robots" is a FORM. Our
entire method exists because adopting a form before deriving the function is the best-documented
way to fail. The honest function statement is something like "produce a crop to spec with near-zero
recurring human field labour, under rules the family ratified." Whether the answer to that is a
swarm of small robots, one big conventional machine with better autonomy, a service contract with
an ag-robotics vendor, or mostly-boring drip irrigation plus two good cameras — I should not be
allowed to assume. The field is also crowded: large equipment makers are shipping autonomous
tractors, and there are venture-backed companies (and a well-known graveyard of dead ones) in
weeding, berry picking, and crop scouting. I don't want to rebuild what can be bought; I want to
know which link of the chain is genuinely unserved, and whether the unserved part is the machines
at all or the ORCHESTRATION — the layer that takes ratified rules and runs a mixed fleet against
them, which is exactly what our kernel already knows how to govern.

What I'm still genuinely unsure about: whether this starts in simulation (a season simulator the
kernel drives, the way Mars was our sandbox) or on real dirt at garden scale; what scale counts as
the real test — a plot, a hectare, a commercial field; whether to pick ONE crop and one
operation (say, scouting-plus-targeted-spraying on potatoes) or insist on the full loop from the
start; whether the family's "we love robotics" energy is a reason to build hardware or precisely
the bias to guard against; and what the success metric even is — cost per kilo against a
conventional benchmark, labour hours avoided, or something honest about learning value, since the
first season of any such system is certain to lose money against a human with a tractor.
```

---

## What survives, and must not be re-litigated

| Decision | Status | Where |
|---|---|---|
| **D1** — the system is an administrative + analytic organ; never a sovereign decider. Machines execute ratified rules only | **RATIFIED, unchanged** | kernel; `apply()` refuses unratified instruments |
| **V2 north star** — governance instrument; family land enterprise is the first real instance; Mars frozen as sandbox | **RATIFIED** | F13 ledger, 2026-08-12 |
| **Anti-mimicry rail** — never propose a FORM first; derive from decisions/functions | **RATIFIED** | V14; `aigov/decisions.py` |
| **F13 elicited programme** — long-rotation trees, possible livestock, residence + retreat; partner-operated model for operations | **ELICITED (E19a/E19b/E20)** | F13 action log rows 20, 41–46 |
| **"Automation = hobby" (2026-09-01)** | **RECORDED — this prompt proposes superseding it** | F13 action log row 46; supersession must be a deliberate decision, not drift |
| **Privacy boundary** | **STANDING** | no family composition, amounts, holdings, or specific locations in any public file; this prompt names none |

---

## Forks `/idea-anchor` will probably surface — drafted positions, for ratification

Predictions of the questions, not answers to be assumed.

### 1. Is this for the enterprise, or a venture in itself? *(the big one)*

**Drafted position: a venture in itself, piloted BEFORE land purchase — and that's a feature.**
The enterprise programme (nut trees on a 20–40 year rotation) needs almost none of this for a
decade; annual crops need all of it immediately. A leased annual-crop pilot field lets the swarm
be real without waiting on (or distorting) the jurisdiction decision. Cost, stated honestly: it
is a second operation with its own capital line, and it must not silently become the reason a
jurisdiction with good broadband outranks one with good land.

### 2. Supersede "automation = hobby," or build it as a hobby?

**Drafted position: supersede, but with a bounded first season** — one crop, one or two
operations, a written kill condition, and a capital cap ratified up front. A hobby has no kill
condition, which is exactly why it was safe to downgrade; promoting it without one re-imports the
unbounded-operating-state problem the F13 init explicitly carved out.

### 3. Build machines, or build the orchestration layer over bought machines?

**Drafted position: orchestration over bought/rented machines, hard rail for season one.** The
unserved link is far more likely to be "a governed loop that runs a mixed fleet against ratified
rules and refuses everything else" than a better berry-picking gripper — and the orchestration
layer is the only part where the existing 430-test machinery is a genuine head start. Building
hardware first is the form-first failure wearing a soldering iron.

### 4. Simulation first, or dirt first?

**Drafted position: both, asymmetrically.** A season simulator as the twin (the Mars pattern —
the sandbox proved the machinery before anything real) + one trivially small real plot the same
season, because the sim will be wrong in ways only dirt reveals, and the ledger's own history
says running the real thing finds defects the green suite cannot.

### 5. Which crop first?

**Drafted position: potatoes.** Mechanization is mature end-to-end (planting, hilling, scouting,
harvest), the per-plant economics tolerate a robot's mistakes, storage is a solved spec, and
scouting-plus-targeted-intervention on potatoes is a real, bounded, measurable season-one goal.
Berries are the opposite: soft-fruit harvest is the hardest open problem in ag robotics and the
place ventures go to die — it should be a later gate, chosen deliberately if ever.

---

## Privacy boundary (standing, non-negotiable)

No family composition, ages, capital amounts, property holdings, or specific locations appear in
the prompt above or in this file. The venture is described at business-concept level only. The
repo `github.com/mmdebrahimi/ai-governor` is **public**.
