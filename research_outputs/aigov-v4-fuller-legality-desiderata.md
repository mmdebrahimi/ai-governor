# V4 — Fuller's eight desiderata of legality: does the implemented linter match the canon?

> **Family:** `aigov-foundations` · **Claim ID:** V4 · **Captured:** 2026-08-11
> **Method (honest label):** WebSearch-grounded, **cited-not-quote-verified**.
> **Why it matters:** invariant **I10** and charter clause **C11** are already implemented as
> `aigov/contract.py::fuller_lint`. This memo checks the implementation against the source list — the
> cheapest high-value verification in the whole queue, because the code shipped before the check.

---

## Source

**Lon L. Fuller, *The Morality of Law*** — Part II, "The Morality That Makes Law Possible"; the chapter is
literally titled **"Eight Ways to Fail to Make Law"**, argued through the allegory of **King Rex**, a
monarch whose successive failures instantiate each way. First edition 1964; **revised second edition 1969**
contains additional material and is the edition to cite. Drawn from Fuller's 1963 Storrs Lectures at Yale.

Fuller's position is deliberately **procedural, not substantive** — he calls it the *"inner morality of
law"*, sitting between natural law and legal positivism.

---

## The eight, as failures and as desiderata

| # | Fuller's way to FAIL | Positive desideratum | `fuller_lint` check | Implemented? |
|---|---|---|---|---|
| 1 | Failure to achieve rules at all — every issue decided **ad hoc** | **generality** | `applies_to_class` non-empty and not `person:<name>` | ✅ `FULLER-1` |
| 2 | Failure to **publicize** the rules the party must observe | **promulgation** | `published is True` | ✅ `FULLER-2` |
| 3 | Abuse of **retroactive** legislation | **prospectivity** | `effective_cycle >= current_cycle` | ✅ `FULLER-3` |
| 4 | Failure to make the rules **understandable** | **clarity** | `predicate` non-empty | ✅ `FULLER-4` (shallow) |
| 5 | Enactment of **contradictory** rules | **non-contradiction** | registry-level pairwise `predicate` vs `NOT predicate` on the same class | ✅ `FULLER-5` (registry) |
| 6 | Rules requiring conduct **beyond the powers** of the affected party | **possibility of compliance** | predicate not in the unsatisfiable set | ✅ `FULLER-6` (shallow) |
| 7 | **Frequent changes** such that the subject cannot orient action | **constancy through time** | `sunset_cycles > 0` | ✅ `FULLER-7` |
| 8 | Failure of **congruence** between rules as announced and their **actual administration** | **congruence** | `enforcement_ref` non-empty | ✅ `FULLER-8` |

**Match: 8 / 8.** The implemented linter's list is the canonical list, in the canonical order, with no
invented or omitted desideratum. Charter clause **C11**'s wording ("general, promulgated, prospective,
clear, non-contradictory, possible to obey, stable, and administered as written") is a faithful rendering.

---

## Two corrections to how the project may describe this

1. **Fuller's claim is stronger than "these are good properties."** He argues that a **total failure in any
   one** of the eight directions does not produce a *bad* legal system — it produces **something that is
   not a legal system at all**. That is a stronger warrant for making I10 a hard validation error rather
   than a warning, and the charter should say so.

2. **The standing objection must be carried, not hidden.** Formal compliance with all eight does **not**
   guarantee just law — the canonical counterexample is that apartheid-era South Africa arguably satisfied
   all eight while being repeatedly condemned internationally. (Fuller replied that apartheid legislation
   departed from the inner morality because it defined race arbitrarily; the objection is live, not
   settled.) **Design consequence: the Fuller linter is a PROCEDURAL floor, never a justice check.** A rule
   that passes `fuller_lint` is well-formed, not good. Any claim that the AI Governor's rules are
   *legitimate* because they pass the linter would be exactly this fallacy.

3. **`FULLER-1`, `-4` and `-6` are structurally SHALLOW** — the implementation already records this in
   `contract.FULLER_DEPTH` ("we can only check it names a class, not that the class is general"; "non-empty
   predicate, not a semantic clarity judgment"; "rejects only literally-unsatisfiable predicates"). That
   self-labelling is confirmed as accurate and should not be softened: three of eight checks test the
   *shape* of a declaration, not its content.

---

## Verdict

**V4 CONFIRMED, implementation matches 8/8.** No design change required. Two documentation changes are
warranted: (a) state Fuller's total-failure claim as the warrant for I10 being an error not a warning;
(b) carry the apartheid objection explicitly so the linter is never read as a legitimacy certificate.

## Sources

- [Eight Ways to Fail to Make Law — Fuller (Brandeis University PDF)](https://people.brandeis.edu/~teuber/Fuller_Eight_Ways_To_Fail_To_Make_Law.pdf)
- [Lecture Notes — Lon Fuller, *The Morality of Law* ("Eight Ways to Fail to Make Law")](https://tomwilk.net/wp-content/uploads/2019/10/Lecture-Notes-Fuller.pdf)
- [Fuller's eight principles — Maximum New York](https://www.maximumnewyork.com/p/fullers-eight-principles)
- [Lon L. Fuller — Grokipedia (edition note: rev. 2nd edn 1969)](https://grokipedia.com/page/Lon_L._Fuller)
