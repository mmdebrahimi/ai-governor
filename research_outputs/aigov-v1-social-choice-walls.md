# V1 — The social-choice walls that bound any AI Government

> **Family:** `aigov-foundations` · **Claim ID:** V1 · **Captured:** 2026-08-11
> **Method (honest label):** WebSearch-grounded promotion of `docs/foundations-canon-map.md` §1 from
> DISCOVERY-tier model recall to **CITED** tier — every claim below now carries a named primary source
> with volume/page. This is **NOT** a full `/research-verify` pass: per-URL WebFetch verbatim-quote
> checking has not been run, so the tier is **cited-not-quote-verified**. Do not report these as
> "verbatim verified". Upgrading to quote-verified is a named follow-on action in the family ledger.
> **Purpose:** these five results are the reason the AI Governor's posture is *fail-closed escalation*
> rather than *optimization*. If any is mis-stated, a committed design bound is wrong.

---

## Supported claims

| # | Claim (as now stated) | Primary source | Locator | Tier | Design bearing |
|---|---|---|---|---|---|
| W1 | With ≥3 alternatives and ≥2 individuals, **no social welfare function** satisfies unrestricted domain + weak Pareto (unanimity) + IIA + non-dictatorship while producing a complete and transitive social ranking. Equivalently: any constitution over ≥3 alternatives satisfying transitivity, IIA and unanimity **is a dictatorship**. | Arrow, *Social Choice and Individual Values* (1951; 2nd edn 1963) | conditions U / P / IIA / ND; completeness + transitivity are **axioms**, not conditions | cited | The AI may never select the objective (charter C01, invariant N1). There is no "correct" aggregation to discover. |
| W2 | Any **onto**, non-dictatorial, deterministic single-valued social choice function over ≥3 alternatives under unrestricted domain is **manipulable**. | Gibbard, *Econometrica* **41**(4): 587–601 (1973); Satterthwaite, *J. Econ. Theory* **10**(2): 187–217 (1975) | 3 conditions: ≥3 alternatives · onto/non-imposed · non-dictatorial | cited (WebSearch 2026-08-11) | No strategy-proof mechanism exists. Only *gaming-detectable* and *gaming-costly* are achievable — hence metric gaming models (I4) and the adversarial suite. |
| W3 | **No social decision function** satisfies unrestricted domain + Pareto + **minimal liberalism** (≥2 individuals each decisive over ≥1 assigned pair). Requires n ≥ 2 individuals and **≥ 4 alternatives**. | Sen, "The Impossibility of a Paretian Liberal", *J. Political Economy* **78**(1): 152–157 (1970) | minimal-liberalism condition; follow-ups: *Collective Choice and Social Welfare* (1970); "Liberty, Unanimity and Rights", *Economica* **43**(171): 217–245 (1976) | cited | Rights are **lexically prior constraints**, never terms in a welfare sum (charter C20, invariant I5 fail-closed). |
| W5 | In a **multidimensional** policy space majority rule is globally unstable: for almost all committees, when no point is unbeaten (**empty core**), *any* policy can be reached by some sequence of pairwise majority votes — including points **outside the Pareto set**. A monopoly agenda setter who knows preferences and faces sincere voters has near-total control of the outcome. | McKelvey, "Intransitivities in Multidimensional Voting Models and Some Implications for Agenda Control", *J. Econ. Theory* **12**(3): 472–482 (1976) | extended from Euclidean to concave preferences by Schofield, *Rev. Econ. Studies* **45**(3): 575–594 (1978) — hence *McKelvey–Schofield* | cited | **Agenda control is the capture channel.** An AI that curates option menus IS an agenda setter. Drives the anti-steering + randomized-agenda-order design. |
| W6 | If preferences are **single-peaked on one dimension**, a Condorcet winner always exists and majority rule selects the **median** voter's ideal (or any point between the two bimedians when n is even). | Black, "On the Rationale of Group Decision-making", *J. Political Economy* **56**(1): 23–34 (1948) | stated for an **odd** number of committee members; in **two** dimensions a coordinate-wise median is **not** necessarily a Condorcet winner | cited | The only regime where aggregation is well-behaved ⇒ **certify only inside single-peakedness, escalate outside it** (the existing `fail_safe_gate` design). |
| W7 | For a system to be regulated, the regulator's **variety** must be ≥ the variety of the system regulated ("only variety can absorb variety"; Ashby's own slogan: *"variety destroys variety"*). It is an **information law**, not a physical law. | Ashby, *An Introduction to Cybernetics* (1956), ch. 11 | related to Shannon & Weaver (1949) theorem 10 on noise removable via a correction channel | cited | A regulator cannot match a society's variety ⇒ it must **attenuate** — and attenuation is exactly Scott's legibility loss. Forces subsidiarity as an engineering constraint, not a preference. |

---

## Material refinements to the canon map (three corrections, all now folded in)

1. **W3 needs ≥ 4 alternatives, not ≥ 3.** `docs/foundations-canon-map.md` stated Sen's paradox without the
   alternative-count precondition. The explicit formulation requires two individuals *i ≠ j* and **four
   distinct** alternatives (x_i, y_i, x_j, y_j). Corrected here; the design bearing is unchanged.

2. **W5 is CONDITIONAL on an empty core, and its "chaos" is institution-free.** The canon map read as
   though multidimensionality alone implies unbounded agenda power. The accurate statement: *whenever no
   point is unbeaten*, the global cycle almost always encompasses the entire space. The theorems assume a
   **frictionless, institution-free** decision environment — which is precisely what motivated the later
   **structure-induced equilibrium** literature (Shepsle). **Design consequence: institutional rules can
   bound the chaos.** That is a *stronger* justification for the project's agenda-order constraints than
   the canon map gave — the AI Governor's job at this seam is to *supply the structure*, not to lament the
   theorem.

3. **Dropping Pareto does not rescue W1.** Wilson (1972) showed that without Pareto only rules that are
   constant (completely unresponsive) or fully determined by a single agent remain. This closes an escape
   route the canon map left implicit, and it strengthens charter clause C01.

---

## The one quotable line for the charter

Ashby himself noted that the law of requisite variety **disposes of the notion that extraordinarily complex
situations demand concentrating extraordinary powers in a central entity.** That is the cybernetic argument
for subsidiarity stated by the founder of the field the AI Governor's control architecture borrows from —
and it directly supports charter clause **C08** (*"a body that cannot centrally know shall not centrally
allocate"*) and invariant **I8**.

*Tier note: this sentence is a paraphrase surfaced by WebSearch, not a WebFetch-verified verbatim quote.
It must be quote-verified before it is used as an epigraph in any published artifact.*

---

## Verdict

**H1 of `aigov-foundations` ("all five walls verify as stated in the canon map") — CONFIRMED WITH
CORRECTIONS.** No wall was falsified. Three statements were imprecise (W3's alternative count, W5's
conditionality and institution-free assumption, W1's Wilson closure) and are corrected above. **No committed
design bound is invalidated**; W5's refinement *strengthens* the case for the agenda-order constraints.

**Residual (named):** cited-not-quote-verified. The follow-on is a `/research-verify` pass demanding a
verbatim sentence + locator per load-bearing claim, per the standing lesson that summarizers paraphrase.

## Sources

- [Arrow's Theorem — Stanford Encyclopedia of Philosophy](https://plato.stanford.edu/entries/arrows-theorem/)
- [Arrow impossibility theorem — Encyclopedia of Mathematics](https://encyclopediaofmath.org/wiki/Arrow_impossibility_theorem)
- [The Gibbard–Satterthwaite theorem: a simple proof (Univ. of Pittsburgh PDF)](https://people.cs.pitt.edu/~kirk/CS1699Fall2014/gibbard-sat.pdf)
- [The Impossibility of a Paretian Liberal — Harvard DASH](https://dash.harvard.edu/handle/1/3612779)
- [Sen's Theorem: Geometric Proof and New Interpretations — D. Saari (UC Irvine PDF)](https://www.math.uci.edu/~dsaari/Sen's%20theorem.pdf)
- [McKelvey–Schofield chaos theorem — Wikipedia](https://en.wikipedia.org/wiki/McKelvey%E2%80%93Schofield_chaos_theorem)
- [Limits on Agenda Control in Spatial Voting Games — Feld, Grofman & Miller (UC Irvine PDF)](https://sites.socsci.uci.edu/~bgrofman/48%20Feld-Grofman-Miller-Limits%20on%20Agenda%20Control.pdf)
- [Black's Singlepeakedness theorem — RangeVoting.org](https://www.rangevoting.org/BlackSingle.html)
- [Single-Peaked Preferences and the Median Voter Theorem — York University (PDF)](http://www.yorku.ca/bucovets/4080/choice/3.pdf)
- [W. Ross Ashby, Cybernetics and Requisite Variety (1956) — panarchy.org](http://panarchy.org/ashby/variety.1956.html)
- [Requisite Variety and Its Implications for the Control of Complex Systems — Springer](https://link.springer.com/chapter/10.1007/978-1-4899-0718-9_28)
