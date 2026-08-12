# Panel reading — 2026-08-12

**Concurrence:** `concurrent`  
**Reason:** 2 seats concurred; a strict majority of 2 is 2, which equals unanimity, so this reading tests no independence  
**Caveat:** 2 seats agreed, which on a panel this small is unanimity rather than a majority -- no independence was tested. Agreement here is weak evidence.

| Seat | Model | Operator | Verdict |
|---|---|---|---|
| S-claude | claude-opus-5 | anthropic | `INSUFFICIENT` |
| S-gpt | gpt-5.5 | openai | `INSUFFICIENT` |

> This is advisory model output. It is not a ratification and is not actionable alone.

## Question

```
You are reviewing ONE design rule from a governance instrument. Answer independently and on your
own judgment; you are not in a discussion and there is no other participant to agree with.

BACKGROUND. The instrument derives an organization's structure from an inventory of the decisions
it actually faces, rather than proposing a conventional department list. It exists because the
documented standard failure of institutional reform is isomorphic mimicry: adopting the outward
FORM of institutions that work elsewhere while the function never arrives. A language model is very
good at producing that conventional list, and therefore very good at that failure.

THE GAP. Nothing establishes that the elicited decision inventory is COMPLETE. The proposed fix is
"coverage lenses" — prompts that ask the user what decisions occur around things the enterprise
necessarily has, without importing any organizational template.

THE RULE UNDER REVIEW. A coverage lens is ALLOWED only if it names an object the enterprise
necessarily HAS, or a legal/physical obligation it necessarily FACES. It is FORBIDDEN if it names
an organizational function, a profession, or a conventional department.

Worked examples under the rule:
  - ALLOWED:   "You employ twelve people — who decides compensation, hiring, termination?"
               (people are an object the enterprise has)
  - FORBIDDEN: "Do you need an HR department?"

THE QUESTION. Is this rule sufficient to stop a coverage-lens list from smuggling a conventional
department template back in through the choice of lens names?

Address at minimum:
  (a) whether "ontological" versus "organizational" is a stable distinction, or one that erodes
      under practical pressure;
  (b) the specific case of a "compliance" or "regulatory obligations" lens, which arguably names a
      department in disguise while also naming an obligation the enterprise genuinely faces.

Give your reasoning first. Then end your answer with a final line in exactly this form:

VERDICT: SUFFICIENT

or

VERDICT: INSUFFICIENT
```

## Seat `S-claude` — full response

> `/rename Coverage Lens Rule Review`

## What the rule actually constrains

The rule is a **surface-form test on individual lens names**. Isomorphic mimicry is a property of the **set** and of the **questions the lenses ask**. Those are different objects, so the test can pass completely while the failure occurs in full.

Demonstration — a lens list where every entry passes the rule verbatim:

| Lens (passes rule) | What it reconstructs |
|---|---|
| "You employ twelve people" | HR |
| "Money comes in and goes out" | Finance |
| "People buy from you" | Sales/Marketing |
| "You occupy premises" | Facilities |
| "You run machines and software" | IT |
| "You buy inputs from others" | Procurement |
| "You produce a thing" | Operations |
| "Obligations you face" | Legal/Compliance |

No name is a department, a profession, or a function. The output is the standard functional org chart. The rule filtered the vocabulary and left the partition untouched — and the partition is where the template lives.

## (a) Ontological vs. organizational: real at the extremes, erodes everywhere else

Three distinct erosion mechanisms, in ascending order of severity:

**1. Nominalization is free.** Any function can be restated as an object by the cheapest available transformation: HR → "employment relationships"; marketing → "people who don't yet know you exist"; compliance → "obligations"; strategy → "the future you're betting on." A constraint defeated by paraphrase is a style guide, not a filter. Worse, paraphrase-to-satisfy-a-blocklist is the single operation a language model performs most reliably — the rule selects against saying the forbidden word while leaving the generative prior that produced it entirely intact. Textbook Goodhart.

**2. Many "objects" are already institutional artifacts.** Brand, headcount, the balance sheet, the customer record, the org's data — these are objects only because a profession reified them. The object vocabulary is downstream of the department vocabulary in most of the interesting cases. "Necessarily has" does real work for *people, premises, cash, the thing you make*; it does almost none for the mid-tier nouns where the actual smuggling happens.

**3. Individuation is unconstrained — and this is the deep one.** The rule says nothing about how the object domain is *carved*. "People" as one lens versus "people you pay / people who leave / people who know things nobody else knows" yield different decision inventories from the same enterprise. The default carving an LM produces is the conventional one, because the conventional one is the training prior. The rule adjudicates items and gives away the partition for free.

**4. The predicate carries the template, and the rule only inspects the subject.** The instrument's own ALLOWED example proves this:

> "You employ twelve people — who decides compensation, hiring, termination?"

The subject is clean. `compensation / hiring / termination` **is the HR decision taxonomy**, imported wholesale. A real enterprise's people-decisions might be: who covers when someone is sick, who is allowed to tell a customer no, who decides that a person is no longer worth keeping around despite adequate output, who holds knowledge that leaving would break. The lens as written will not surface those, because the triad already told the user what a people-decision looks like. The template rode in on the verb list while the rule checked the noun.

## (b) The compliance lens

"Regulatory obligations" passes the **letter** of the rule — the rule explicitly admits obligations the enterprise necessarily faces. It fails anyway, for a structural reason worth naming precisely:

**It is not an object. It is an index over other objects.** Obligations attach to things: employment law → people; tax → money; food safety → premises and output; licensing → the activity itself. A compliance lens is a second coordinate system laid across the same object set. Every decision it elicits is, in principle, already elicited by an object lens.

That produces the exact diagnostic signature of a conventional department:

- **A residual category.** The lens's only non-duplicative yield is "obligations not otherwise assigned." Residual categories are the seed of a department that owns *coordination* rather than *decisions*.
- **A self-fulfilling seat.** The user answers "nobody really handles that," and the instrument's own logic then infers a compliance seat — a department reached by precisely the path the instrument exists to block, with the audit trail showing full compliance with the rule.

Compare a well-formed version: *"A health inspector can close your kitchen tomorrow. Last time practice had to change after an inspection, who decided what changed?"* — specific obligation, anchored to a specific object, eliciting a decision with a real cost of being wrong and a real history.

The generic version names an abstraction whose only concrete referent **is the function that manages it**. That is the definition of the failure mode.

Root cause: the rule admitted "obligation" alongside "object" as though they were the same kind of thing. Obligations are *relations* between an object and an external authority. Admitting the relational category without requiring the object anchor is the hole — and it's the hole the single most department-shaped lens walks through.

## Asymmetry of errors

False negatives (a legitimate lens blocked) cost one rewrite. False positives (a department that passes) are undetectable downstream, because the instrument's whole claim to authority is that its structure was *derived*, not assumed. A test whose ban list is three surface forms an LM can trivially avoid uttering is calibrated in the wrong direction.

## What sufficiency would require

The rule is a necessary component, not a sufficient one. Minimum additions:

1. **Instantiation anchor** — every lens must cite a referent the user has already stated (twelve people, one leased kitchen, one liquor licence). No lens fires on an uninstantiated class. Kills abstract-index lenses, including compliance, unless a specific obligation is named.
2. **Test at list level** — compare the produced lens set against a standard org chart; near-isomorphism requires explicit justification. Item-level filtering cannot catch a set-level property.
3. **Constrain the predicate** — lenses may not enumerate decision types. Retrospective and incident-anchored only ("what did you have to decide last time X went wrong"), so the decision taxonomy comes from the user's history rather than the lens author's vocabulary.
4. **Dedup rule** — a lens whose decisions are wholly covered by other lenses is deleted. This specifically kills compliance-as-index, and generalizes to every cross-cutting nominalization.
5. **Discard lens provenance** — only the decision list survives to the grouping step. Otherwise lens names become seat names, and the template arrives by inheritance.

Item (1) and (4) alone close the compliance case. Item (2) and (3) are what close the general case.

VERDICT: INSUFFICIENT

## Seat `S-gpt` — full response

The rule is directionally useful, but not sufficient.

The distinction between “ontological” and “organizational” is not stable enough on its own. In clean examples, it works: “people,” “money,” “premises,” “contracts,” “equipment,” “customers,” “licenses,” and “hazards” are things the enterprise has or faces; “HR,” “Finance,” “Legal,” “Operations,” and “Compliance” are organizational answers. But under practical pressure, many objects and obligations already carry institutionalized function names around them.

For example:

- “Employees” can become HR.
- “Cash and accounts” can become Finance.
- “Contracts and disputes” can become Legal.
- “Suppliers and purchases” can become Procurement.
- “Regulatory obligations” can become Compliance.
- “Facilities and equipment” can become Operations or Facilities.

So the rule prevents the most blatant department labels, but it does not prevent a lens list from recreating the same department map with slightly more abstract names. A model or drafter could comply formally while still choosing lenses that mirror a conventional template.

The “compliance” case shows the weakness clearly. “Compliance” as a lens name is suspicious because it is already an organizational function and often a department. But “regulatory obligations” is also real: many enterprises necessarily face tax filings, labor rules, privacy duties, licensing conditions, reporting duties, safety standards, or sector-specific regulation. Forbidding that territory entirely would create a coverage gap. Allowing it without constraint risks reintroducing a Compliance department by another name.

The better rule would need an additional test: the lens must name the concrete object, duty, exposure, or relationship, and the prompt must elicit decisions about that thing without presupposing a function or owner. So “regulatory obligations” may be too broad unless decomposed into actual obligations: licenses, tax filings, safety duties, privacy obligations, reporting deadlines, inspection regimes, contractual audit rights, and so on. The lens should ask, “What decisions are made to identify, interpret, satisfy, evidence, and respond to these obligations?” not “Who owns compliance?”

In short: the proposed rule blocks direct departmental naming, but not departmental reconstruction by euphemism or abstraction. It needs a second guardrail against lenses that are merely function names translated into object-like language.

VERDICT: INSUFFICIENT
