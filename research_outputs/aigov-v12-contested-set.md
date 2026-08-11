# V12 — Is the contested set genuinely contested?

> **Family:** `aigov-foundations` · **Claim ID:** V12 · **Captured:** 2026-08-11
> **Method (honest label):** WebSearch-grounded, **cited-not-quote-verified**.
> **Purpose:** `docs/foundations-canon-map.md` flagged four famous results as *"contested — do not rely
> on"*. This memo checks that the flag is warranted, because a *wrongly*-flagged claim is as damaging as a
> wrongly-trusted one: it silently removes an argument the project could legitimately have used.

---

## Result

**3 of 4 checked. All three checked are genuinely contested — but in three DIFFERENT ways, and the canon
map's blanket "do not build on them" was too coarse for one of them.** The fourth (*Limits to Growth*) was
**NOT checked** in this pass and remains flagged-unverified.

| Claim | Contested? | *How* it is contested | Canon-map flag |
|---|---|---|---|
| **Chamley–Judd zero capital tax** | **YES — theoretically overturned** | Straub & Werning, *AER* **110**(1): 86–119 (Jan 2020): the conclusion *"does not follow from the very models used to derive it."* In Judd (1985) the long-run capital tax is **positive and significant whenever the IES < 1**; above that it converges to zero *"possibly only after centuries of high tax rates."* In Chamley (1986) the model's upper bound on capital taxes can **bind forever**. Zero is a **knife-edge** special case. | flag CORRECT |
| **Dunbar's number (~150)** | **YES — statistically undermined, still disputed** | Lindenfors, Wartel & Lind, *Biology Letters* (2021) "'Dunbar's number' deconstructed": best-specified model gives mean group size **69.2, 95% CI 3.8–292.0** — self-described as *"not very informative"*; across methods CIs span 2–520. Bernard–Killworth empirical work suggests ~291 (median network 231). **Dunbar has publicly rebutted** and the Stockholm group replied — the dispute is live, not resolved. | flag CORRECT |
| **Milgram obedience** | **PARTIALLY — and the canon map got this one wrong** | The **behaviour replicates**: Burger (2009) "150-volt solution" found obedience only slightly below Milgram's 45 years earlier; Blass found no significant decline 1963–1985; a recent online-recruitment study closely mirrored the 1960s rates. What has collapsed is the **interpretation** (Burger's prompt analysis: the most forceful prompt — *"you have no choice, you must continue"* — produced **universal disobedience**; a VR replication refutes the "agentic state" in favour of "engaged followership") and the **reporting integrity** (Perry 2013: Milgram omitted non-supporting conditions, incl. an unpublished 1962 "Relationship" condition). | **flag TOO COARSE — see below** |
| ***Limits to Growth*** | **NOT CHECKED** | no search run in this pass | flag **unverified** |

---

## The correction: Milgram

The canon map listed Milgram alongside Dunbar as *"replication-contested — do not build on them."* That is
**inaccurate**. The distinction matters for a project about institutional design:

- **The behavioural finding is robust.** Ordinary people, under an authority's instruction, will inflict
  what they believe to be serious harm at high rates, and this has not decayed over sixty years.
- **The mechanism story is not.** "Agentic state" is contested; "engaged followership" — people comply
  because they *identify with the enterprise*, not because they surrender agency — is the live competitor.
- **The archival record is compromised.** Selective reporting is documented.

**Design consequence.** The AI Government may rely on the *phenomenon* (institutional design must assume
that instruction-following under a legitimising frame produces harm compliance — this is a direct argument
for charter clauses **C03** on emergency authority and **C15** fail-closed escalation) but may **not** rely
on any *mechanism* account, and must cite the phenomenon carefully given the reporting critique.

Note the sharper reading is *worse* for an AI Governor, not better: if compliance runs through
**identification with the enterprise** rather than surrender of agency, then a governor that supplies a
compelling mission frame is a **more** effective harm-compliance engine than one that issues orders. That
strengthens the case for the anti-steering primitives, and it is a genuinely new argument the canon map's
blanket flag would have hidden.

---

## Verdict on hypothesis H3 of `aigov-foundations`

> **H3:** *"The contested set is genuinely contested (not settled in either direction)."*
> **Verdict: CONFIRMED for Chamley–Judd and Dunbar; REFINED for Milgram; NOT CHECKED for Limits to Growth.**

Chamley–Judd is not merely "contested" — it is **overturned within its own models**, which is a stronger
result than the flag claimed. Dunbar is contested exactly as flagged. Milgram required splitting
phenomenon from mechanism. *Limits to Growth* stays flagged-unverified and is a named follow-on.

**No design bound in the AI Government currently rests on any of the four**, so no revision is forced — the
value of this memo is that it (a) prevents a future argument from leaning on Chamley–Judd, (b) *recovers* a
usable and design-relevant finding from Milgram that the blanket flag had discarded, and (c) records
honestly that one of the four was not checked.

## Sources

- [Positive Long-Run Capital Taxation: Chamley-Judd Revisited — Straub & Werning, AER 110(1) (AEA)](https://www.aeaweb.org/articles?id=10.1257%2Faer.20150210)
- [Same paper — NBER Working Paper 20441](https://www.nber.org/papers/w20441)
- ['Dunbar's number' deconstructed — Lindenfors, Wartel & Lind, Biology Letters (2021)](https://royalsocietypublishing.org/doi/10.1098/rsbl.2021.0158)
- [Robin Dunbar's rebuttal — The Conversation](https://theconversation.com/dunbars-number-why-my-theory-that-humans-can-only-maintain-150-friendships-has-withstood-30-years-of-scrutiny-160676)
- [Why we dispute 'Dunbar's number' — The Conversation (Lindenfors et al.)](https://theconversation.com/why-we-dispute-dunbars-number-the-claim-humans-can-only-maintain-150-friendships-161944)
- [Replicating Milgram: Would people still obey today? — Burger (2009), PubMed](https://pubmed.ncbi.nlm.nih.gov/19209958/)
- [Rethinking Milgram's obedience studies — British Psychological Society](https://www.bps.org.uk/research-digest/rethinking-milgrams-obedience-studies)
- [Participant concerns for the Learner in a VR replication of the Milgram obedience study — PLOS One](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0209704)
