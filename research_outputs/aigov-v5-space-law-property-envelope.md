# V5 — The space-law envelope: what property regime may a colony actually have?

> **Family:** `aigov-foundations` · **Claim ID:** V5 · **Captured:** 2026-08-11
> **Method (honest label):** WebSearch-grounded, **cited-not-quote-verified**.
> **Why it matters:** framework fork **K7** chose *usufruct/possession with Harberger self-assessment* to
> sidestep the Outer Space Treaty's non-appropriation rule, and department **D2** already implements a
> `self_assessed_valuation_rule`. This memo tests whether the legal envelope permits it — and surfaces a
> constraint on the project's *legitimacy* story that no other memo would have found.

---

## Supported claims

| # | Claim | Source | Locator | Tier |
|---|---|---|---|---|
| V5.1 | **OST Art. II:** "Outer space, including the Moon and other celestial bodies is not subject to national appropriation by claim of sovereignty by means of use or occupation, or by any other means." No state may claim the Moon, Mars, or an asteroid as territory; treated as **absolute**. | Outer Space Treaty (1967), Art. II | | cited |
| V5.2 | Art. II names only **"national"** appropriation and is textually silent on private entities. The gap is argued closed **indirectly via Art. VI**; the **International Institute of Space Law stated in 2004** that territorial claims by a national **or private** entity are prohibited. | OST Art. II/VI; IISL position statement (2004) | | cited |
| V5.3 | **OST Art. VI:** States "bear international responsibility for national activities in outer space… whether such activities are carried on by governmental agencies or by **non-governmental entities**," which require **"authorization and continuing supervision"** by the appropriate State. | OST (1967), Art. VI | the lynchpin between international space law and domestic licensing (FAA launch, FCC spectrum, NOAA remote sensing) | cited |
| V5.4 | The **"in place" vs "extracted"** distinction: the US executive position (Sec. Vance, Senate testimony) is that non-appropriation applies to celestial natural resources **only while "in place"**, and does not bar ownership of resources **removed** from their place — removal being "use" permitted by Art. I. | US executive-branch interpretation; codified 2015; reinforced by the Artemis Accords | **not universally accepted** | cited |
| V5.5 | **US Commercial Space Launch Competitiveness Act (2015)** — first state to legislate; entitles a US citizen engaged in recovery "to any asteroid resource or space resource obtained, including to **possess, own, transport, use and sell**", "free from harmful interference", subject to international obligations. | 51 U.S.C. ch. 513 (2015) | contains **no** detailed licensing procedure | cited |
| V5.6 | **Luxembourg Law of 20 July 2017** (adopted 13 July 2017, in force 1 Aug 2017) — **Art. 1: "Space resources are capable of being owned."** Art. 2(1) requires prior **written ministerial mission authorisation**. First European state to legislate. Excludes satcoms, orbital slots, frequency bands. | Loi du 20 juillet 2017 | detailed licensing regime, moderate fees, low tax rates | cited |
| V5.7 | **Shared design feature of both statutes:** ownership is granted **only after extraction**, deliberately avoiding conflict with Art. II. | | | cited |

---

## What this means for K7 (the property regime)

**K7 SURVIVES — and the reason is sharper than the canon map gave.**

The colony's scarce fixed factor is **pressurized habitable volume**, and a habitat module is a
**manufactured artifact**, not celestial territory. Ownership of, and taxation on, a *built structure and
the right to occupy it* is not a claim of sovereignty over Mars. The distinction that makes the US and
Luxembourg statutes work (**own the extracted, never the in-place**) maps directly:

| Object | Legal character | Regime |
|---|---|---|
| The regolith/terrain a habitat sits on | **in place** — celestial body | **Not appropriable** (Art. II). No freehold. |
| The habitat module, its pressure shell, its volume | manufactured from extracted resources | **Ownable** (V5.5–V5.7) |
| The *right to occupy* a given volume | a possession/use right granted by the polity | **Harberger self-assessment applies cleanly** — it prices a use right, not territory |

So D2's `self_assessed_valuation_rule` + `volume_tax_rate` are legally coherent as drafted. **No design
change required.** What *is* required is a wording discipline: the regime must be described as
**possession/usufruct in built volume**, never as "land ownership" — the latter phrasing would assert
exactly the thing Art. II forbids.

---

## The finding no other memo would have surfaced — a constraint on LEGITIMACY, not on mechanism

**Art. VI (V5.3) makes a Mars colony a *supervised non-governmental activity of some State*, not a sovereign
polity.** Under the treaty as it stands, the colony's governance is legally **derivative**: some state
party bears international responsibility for it and owes "continuing supervision."

This bears directly on the project's central claim. Ratified decision **D1** says binding authority rests
with the *polity*. Under current space law, binding authority over that polity's activities also rests with
a **supervising state**, whether or not the colonists consent. Consequences:

1. **The AI Governor is not, and under current law cannot be, the top of its own authority chain.** There
   is a legal principal above the assembly. The charter should say so rather than implying autarkic
   sovereignty.
2. This is a *second* external coercion channel alongside the one already modelled — the
   resupplier-as-coercer survival veto in `Mars_Governance/governance/connection.py` (Hirschman's
   asymmetric-dependence mechanism). **Supervisory jurisdiction is the legal twin of resupply dependence**,
   and department **D5 (External Relations)** should model both, not just the physical one.
3. It sharpens the **scale-gate** question (deferred family `aigov-scale-gates`): a colony transitioning
   toward genuine self-government is not merely growing — it is **changing legal status**, which no amount
   of internal mechanism design accomplishes.

**Proposed new charter clause (drafted, for ratification — not self-adopted):**
> *C25 — The Governor shall record, and shall not obscure, the external legal authorities to which the
> polity's activities remain subject.* Enforcement site: `human_only`; `enforced_by: ASPIRATIONAL` (no
> executable invariant — it is a disclosure duty, not a checkable predicate).

---

## Verdict

**V5 CONFIRMED. K7 unchanged and better justified.** One new, material constraint discovered
(Art. VI supervisory jurisdiction ⇒ derivative authority), producing one drafted charter clause and one
scope note for department D5. Recorded as an unknown retired and a pending decision raised, per DF2.

**Live legal caveat, carried not hidden:** whether Art. II prohibits extraction and ownership of space
resources at all "remains one of the most actively debated questions in space law" — the US/Luxembourg
"extraction is use, not appropriation" reading is a **position**, not settled law, and not all nations
agree. The colony property regime therefore rests on a contested interpretation.

## Sources

- [The Next Fifty Years of the Outer Space Treaty — US Dept. of State](https://2009-2017.state.gov/s/l/releases/remarks/264963.htm)
- [Interpretation as Creation: Article VI of the Outer Space Treaty — Chicago Journal of International Law](https://cjil.uchicago.edu/print-archive/interpretation-creation-article-vi-outer-space-treaty)
- [Circumventing the Non-Appropriation Principle of International Space Law — Berkeley J. Int'l Law](https://www.berkeleyjournalofinternationallaw.com/post/circumventing-the-non-appropriation-principle-of-international-space-law)
- [Law of 20 July 2017 on the exploration and use of space resources (Luxembourg, full text PDF)](https://space-law.keio.ac.jp/pdf/datebase/each_countries/luxembourg/space_resources.pdf)
- [Luxembourg adopts space resources law — SpaceNews](https://spacenews.com/luxembourg-adopts-space-resources-law/)
- [The Luxembourg Space Law — Ogier](https://www.ogier.com/news-and-insights/news/the-luxembourg-space-law/)
- [Luxembourg Law on Space Resources Rests — KU Leuven Working Paper No. 189 (2017)](https://ghum.kuleuven.be/ggs/publications/working_papers/2017/189deman)
- [Bold steps forward: investment impact of enacting space resources legislation — ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0265964624000663)
