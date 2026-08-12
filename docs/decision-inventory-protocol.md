# The decision inventory — how to run the session

> The instrument that answers *"what do we need to keep in-house?"* without handing you a list of
> what other organisations have. Code: `aigov/decisions.py`. Tests: `tests/test_decisions.py`.
> Written 2026-08-11 after the user ratified Pending Decision 5; **revised 2026-08-12** after three
> defects were found by running it (see *What changed and why*).

## Why this exists

Asked what departments an enterprise needs, the tempting answer is finance, operations, legal, HR.
That answer is the documented standard failure of institutional reform — adopting the outward FORM
of something that works elsewhere while the function never arrives. An AI is extremely good at
producing that list, which makes it extremely good at that failure.

The ratified resolution: the instrument **does** give a final recommendation, but must reach it by
interrogating first. The binding constraint is **traceability** — the recommendation has to be
derivable from what was elicited about *this* situation.

So structure is not proposed. It is **computed**:

```
decisions you actually face
  -> per-decision internalize-vs-market verdict          (Coase 1937 / Williamson)
  -> pairs worth asking about, from EXPENSIVE shared facts only   (Galbraith)
  -> your yes/no on each pair
  -> retained capabilities, ONLY where every pair inside was affirmed
```

Point at anything the tool produces and ask "where did that come from?" — you get your own
decisions back, in your own words.

**It says "capability", not "department", on purpose.** A group of decisions that must be made
together might need one part-time person, a standing meeting, a committee, or eventually a
department. Picking the form is a separate, later, human step; doing it here would import the
template one level down.

## What you supply, per decision

Four numbers decide the sourcing. All four are yours; none has a default.

| Question | Why it matters |
|---|---|
| How many times a year does this come up? | Frequency is what turns a one-off into a capability. |
| What would an outsider charge to make this call ONCE — all-in, including finding, briefing and checking them? | Williamson's transaction cost. The "all-in" part is the bit people forget. |
| What would it cost per year to hold this in-house? | Salary, tools, and the attention it takes off other things. |
| Is there anyone to buy this from at all? | If nobody sells it, that settles it on its own. |

Then the questions that **change** the answer rather than complete it:

- **What do you know about this that an outside expert could not find out?** This is the one that
  matters most, and it is explained below.
- **What has to be KNOWN before you can make this call?** Facts, not sources.
- **For each of those facts — which is it?**
  - **(a) written down**, so anyone handed the file would have it;
  - **(b) specific to how you operate**, so you would have to explain it;
  - **(c) something you know from experience** and have never written down.

  Only **(b)** and **(c)** are reasons two decisions might have to be made by the same person. This
  question is new, and it is the fix for the second defect below.
- **Who ANSWERS for this decision — the role, not the person?** Roles, never names. A role survives
  the person leaving, and a name in a saved file is a privacy problem waiting to happen. "Nobody
  yet" is a real answer and is reported, not filled in for you.
- **What happens if you get it wrong once?** Recoverable, expensive, or permanent. This sets the
  *checking* requirement — a separate axis, described below.
- **Is this ONE decision, or several?** Could two reasonable people answer different *parts* of the
  question differently? If you say it is compound, the tool **refuses to give it a verdict** and
  asks you to split it. "Manage financing" and "should we offer $1.2M for 123 Main St" are both
  legitimate English and produce completely different structures from the same enterprise — a
  verdict on the first is not approximate, it is meaningless. Leaving this unanswered does not
  block anything; it just gets asked.

## The four verdicts

| Verdict | Meaning |
|---|---|
| **INTERNALIZE** | Hold it. Either going to the market costs more over a year, or there is no market. |
| **HYBRID** | Buy the execution, keep the judgment. The market is cheaper on price, but the decision turns on things only you know. |
| **MARKET** | Buy it. Cheaper, and nothing private blocks an outsider from doing it well. |
| **UNDECIDABLE** | You have not answered enough yet. No default is applied — the gap is named instead. |

**HYBRID is the one that earns its keep**, and it was not in the first version. On the first run the
tool recorded private information, printed it as a "degraded" note, and then ignored it — every such
decision came out MARKET. That was wrong on the theory: asset specificity *drives* internalization
rather than annotating it. Where a decision depends on knowledge the market cannot acquire at any
price, a cheaper market price is not the same option.

In practice HYBRID is what a family office actually does: hire the land agent, make the call
yourself.

**Every decision gets an accountable role — including the MARKET ones.** Outsourcing the work does
not outsource the accountability: somebody internal still picks the supplier, briefs them and
inspects the result. An unowned bought-in judgment is how a supplier quietly ends up deciding for
you.

## Assurance — how hard to check, which is NOT who holds it

Consequence and sourcing are **different questions**, and running them together is a real modelling
error. Brain surgery is about as high-consequence as a decision gets, and it is still bought from
outside. What consequence drives is how hard you check, not who holds the capability.

| You said getting it wrong once is… | Checking requirement |
|---|---|
| recoverable | **self-check** — the person deciding checks their own work |
| expensive to unwind | **second opinion** — someone not making the call reviews it before it commits |
| permanent | **independent review** — by someone independent of the person making it |
| (unanswered) | **undecidable** — named as a gap, never defaulted |

**One consequence matters more than it looks.** If a decision is bought in *and* irreversible, the
reviewer must also be independent of **the supplier**. A supplier paid to do the work is not a check
on whether the work should happen. On a real inventory this fires on exactly the decisions you would
worry about — "do we sell the north parcel?" comes out MARKET on price and still demands a reviewer
who is not the broker earning the commission.

`stake_per_decision` is deliberately **not** consulted. Turning money-at-stake into a level would
need a cutoff nobody ratified; it stays context for the humans.

This axis is new for the same reason HYBRID was. `reversibility` was elicited, asked about in the
interview, described here as a question that "changes the answer" — and then fed no verdict at all.
A field that changes nothing should either drive something or stop being asked.

## How capabilities form

The tool never groups two decisions on its own. It does three things in order:

1. **Proposes pairs worth asking about.** Two retained decisions become a candidate only if they
   share a fact of kind **(b)** or **(c)**. Sharing a written-down number is not a reason to group —
   that is shared *data*, not shared *context*.
2. **Asks you, per pair:** *"Would these two decisions come out materially worse if different people
   made them and could only exchange written notes?"* A yes/no. There is no score and no weighting,
   because a weight would be a number the instrument invented.
3. **Forms a capability only from a COMPLETE group** — one where every pair inside it was
   independently affirmed. A group that is merely connected is not a smaller capability; it is not a
   capability at all, and it comes back to you under **HUMAN GROUPING REQUIRED**.

MARKET and UNDECIDABLE decisions are never grouped. You do not staff a capability you buy outright,
and you must not staff one you have not finished thinking about.

**Capabilities are never auto-named.** Calling a group "Finance" would import a template through the
back door. The tool produces the grouping; the label — and the organisational form — are yours.

## What changed and why (2026-08-12)

Three defects, all found by *running* the module rather than by reading it or by the test suite.

| # | Defect | Fix |
|---|---|---|
| 1 | **Chaining.** Grouping was a connected component over shared facts, so A–B and B–C put A and C together even when they share nothing. Four decisions — refinance, renovate, pick contractor, contractor bonus — collapsed into one unit. | Group only on affirmed pairs, and only when the group is **complete**. |
| 2 | **Cheap facts grouped as hard as tacit ones.** "Should we acquire this building" and "can we run payroll Friday" merged because both need the cash balance — a number in a spreadsheet. | Classify each fact (a)/(b)/(c); only (b) and (c) propose a pair. |
| 3 | **A test pinned the chaining as correct**, with a docstring arguing for it. | Deleted; a chaining-*refusal* test stands in its place. |

A result previously reported as a non-obvious insight — acquisition, cash-phasing and planting
forming one unit — was partly defect 1. Cash-phasing and planting share zero facts and were joined
only through acquisition as a bridge. It is withdrawn.

Two further gaps were closed in the same pass: **assurance** (consequence was elicited and fed
nothing) and **atomicity** (nothing checked that a "decision" was one decision). Both are described
above.

**One proposed change was deliberately NOT made.** A review suggested replacing "what do you know
that an outsider could not?" with a broader *decision specificity* question, kept advisory. It was
dropped: an elicited field that feeds no verdict is precisely the defect shape found twice in this
module already (`private_information` before HYBRID existed, `reversibility` before assurance did).
Adding a third one — deliberately, and calling it advisory — would be repeating a known mistake. If
specificity is worth asking, it has to drive something.

## Running it

1. List the decisions first, in your own words, without worrying about the numbers. Ten to twenty is
   plenty. Use questions you actually face, not categories.
2. Answer what you can. Leave the rest blank — blank is a legitimate state and produces a question,
   not a guess.
3. Run it. You get verdicts, the pairs it wants you to rule on, and a short list of exactly what is
   still missing.
4. Answer the coupling questions. There will be far fewer than you expect: the fact-kind filter cuts
   them hard, and only retained decisions are ever paired.
5. Run it again. Now you get capabilities.

```python
from aigov.decisions import DecisionRecord, CouplingRecord, build_inventory, render_report
print(render_report(build_inventory(decisions, couplings)))
```

## What it will not do

It does not rank decisions, choose a strategy, name a capability, pick an organisational form, or
say which matters most. It converts an elicited inventory into a structure. Judgment stays with the
people who answered the questions.

**Two honest limits.**

It cannot tell you whether your inventory is *complete*. A decision you never mention produces no
capability, and nothing here will notice the absence. That is why the first pass should be generous
rather than tidy. A "coverage lens" fix was drafted for this and is **not implemented** — a review
on 2026-08-12 found the proposed rule insufficient, so the gap stands open rather than being closed
badly.

The pair filter cannot see a coupling between two decisions that share no *recorded* fact but turn
on the same unwritten context. Add such a pair by hand if you spot one. The filter is a cost
control, not a claim about reality.
