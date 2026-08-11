# V2 — Land value taxation and the Henry George theorem: does the colony fiscal base survive?

> **Family:** `aigov-foundations` · **Claim ID:** V2 · **Captured:** 2026-08-11
> **Method (honest label):** WebSearch-grounded, **cited-not-quote-verified** (no `/research-verify`
> WebFetch pass yet).
> **Why it matters:** framework fork **K3** selected a *volume/area LVT-analogue* as the colony's fiscal
> base, and department **D2** (`aigov/specs/d2_economy.py`) is built on it. This memo tests whether the
> justification the canon map gave for that choice actually holds.

---

## Result in one line

**The efficiency argument SURVIVES. The self-financing argument is FALSIFIED for a colony.** They are two
different claims and the canon map ran them together.

---

## Supported claims

| # | Claim | Primary source | Locator | Tier | Verdict |
|---|---|---|---|---|---|
| V2.1 | The **Henry George theorem**: in a city of optimal population size, **aggregate differential land rents exactly equal expenditure on the pure local public good**. | Arnott & Stiglitz, "Aggregate Land Rents, Expenditure on Public Goods, and Optimal City Size", *Quarterly J. Economics* **93**(4): 471–500 (Nov 1979) | §"the generality of the Henry George Theorem" p. 477; §"land rents as a measure of the benefits from public goods" p. 490 | cited | statement CONFIRMED |
| V2.2 | Its conditions: **no congestion**; public goods the **only** cause of urbanization; spatially homogeneous economy; **identical agents**; **optimal jurisdiction size achieved via Tiebout-like mobility**; constant returns to scale in non-land factors; **free mobility of labour and capital across cities**; public goods satisfying the Samuelson condition and financed by **non-distortionary land taxes**. | ibid.; Stiglitz's generality result | Wikipedia's simplified-model assumption list: linear transport costs, circular city, even population distribution, homogeneous land, no congestion, CRS | cited | conditions CONFIRMED — and they are **stringent** |
| V2.3 | Optimal city size sits where increasing-returns forces (public goods, scale economies) exactly offset decreasing-returns forces (transport cost, land rent, congestion) — **locally constant returns to scale**. That balance point is precisely where the rent–expenditure equality bites. | ibid. | | cited | CONFIRMED |
| V2.4 | Land value taxation is **non-distortionary** because land is supplied inelastically — the classical single-tax argument. | George, *Progress and Poverty* (1879) | the "single tax" movement | cited | CONFIRMED, and **independent of V2.1's conditions** |
| V2.5 | The theorem extends to **second-best** regimes (Arnott 2004) and to **dynamic** settings in present-value terms, holding under congestion or production externalities **provided those externalities are priced correctly**. | Arnott (2004), *J. Urban Economics*; Fu (2025), *International Studies of Economics* | | cited | CONFIRMED — relaxes some but not all conditions |

---

## FALSIFICATION — hypothesis H2 of `aigov-foundations`

> **H2 as stated:** *"The Henry George theorem's conditions are satisfiable by a colony's fixed factors."*
> **Verdict: FALSIFIED.**

The theorem's machinery is **inter-jurisdictional**. Optimal city size is reached because mobile agents
arbitrage utility differences *across competing cities* — Tiebout sorting. A Mars colony has:

| HGT condition | Colony reality | Holds? |
|---|---|---|
| Free mobility of labour/capital across cities | **There is one settlement and no exit.** The canon map already recorded that Tiebout sorting does not exist on Mars — that is the same premise as charter clause **C21** (minority protection must be structural *because* there is no exit). | **NO** |
| City at *optimal* population size | Population is capped by **life-support carrying capacity**, not by a rent/transport-cost optimum | **NO** |
| No congestion | A pressurized habitat is congestion-dominated by construction | **NO** |
| Identical agents, homogeneous land | Habitat volume is radically heterogeneous (core vs periphery, radiation shielding, thermal access) | **NO** |
| Public goods are the only cause of agglomeration | The cause of agglomeration is **survival** (shared ECLSS), not public-goods provision | **NO** |

**Five of the theorem's conditions fail, and one of them (no exit) is a load-bearing feature of the polity
this project is designing.** The self-financing equality therefore **cannot be invoked** to claim that a
colony's volume rents will fund its public-goods bill.

### The design bound this revises (per family decision DF2)

- **REMOVED:** the canon-map claim that the fiscal base is *"Henry-George-financed public goods"* — i.e.
  that rents would **automatically** cover the bill. That inference is unsupported here.
- **RETAINED, on a different and stronger footing:** the LVT-analogue is chosen because the taxed factor
  (pressurized volume, radiator area) is **inelastically supplied and physically enumerable**, so the tax
  is non-distortionary and near-impossible to evade (V2.4 — which needs none of the failed conditions).
- **CONSEQUENCE for department D2:** whether volume+area rents fund the public-goods bill is now an
  **empirical question the twin must answer**, not a theorem the design may lean on.
  `aigov/specs/d2_economy.py::_falsification_test` already computes it as a *number* (revenue 9 250 vs
  bill 8 600 credits/cycle, on a declared envelope) rather than asserting it — which is, in retrospect,
  exactly the right shape. **Hypothesis H4 of the umbrella ledger is now the live question, and it is
  correctly framed as measurable rather than derivable.**

---

## Verdict

**V2 CONFIRMED as a statement; H2 FALSIFIED as an application.** This is the family working as designed —
decision **DF2** ("a FALSIFIED claim is a successful outcome and MUST revise the design bound it
supported"). The fiscal instrument survives; its *justification* changed, and the change makes the project
more honest: the fiscal base rests on factor inelasticity (robust) instead of on a self-financing theorem
whose preconditions a no-exit closed colony structurally cannot meet.

## Sources

- [Aggregate Land Rents, Expenditure on Public Goods, and Optimal City Size — QJE 93(4):471–500 (Oxford Academic)](https://academic.oup.com/qje/article-abstract/93/4/471/1932537)
- [Same paper — RePEc/IDEAS record](https://ideas.repec.org/a/oup/qjecon/v93y1979i4p471-500..html)
- [Henry George theorem — Wikipedia (simplified-model assumption list)](https://en.wikipedia.org/wiki/Henry_George_theorem)
- [The Henry George Theorem in a second-best world — ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0094119014000771)
- [Dynamic Henry George Theorem and Optimal City Sizes — Fu (2025), Wiley](https://onlinelibrary.wiley.com/doi/10.1002/ise3.70013)
