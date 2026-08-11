# Foundations Canon Map — the literature an AI Government must be built against

> **PARTIAL PROMOTION 2026-08-11.** Claims **V1, V2, V4, V5, V12** have been promoted to **CITED** tier
> (named primary sources with volume/page) in `research_outputs/aigov-v{1,2,4,5,12}-*.md` — still
> *cited-not-quote-verified*, no `/research-verify` WebFetch pass. **Four corrections landed and are folded
> in below, each marked `[CORRECTED 2026-08-11]`.** One produced a genuine falsification (the Henry George
> self-financing claim). The rest of this map remains discovery-tier.
>
> **TIER DISCIPLINE — READ FIRST.** Everything not marked as promoted is **DISCOVERY-TIER: model recall, unverified.**
> No claim, number, date or attribution here may bear design weight until promoted through `/research` +
> `/research-verify` into an audit-tier memo in `research_outputs/`. This document exists so the F0 literature
> family starts from a *structured hypothesis about what matters*, not a blank page — it is the **search plan**,
> not the evidence. Inherited caveat from `mars-governance` D7: model-coherent ≠ validated.
> Date: 2026-08-11. Owner: family `aigov-foundations` (F0).

---

## 0. How to use this map

Three kinds of content, deliberately separated because they carry different weight:

| Kind | Meaning | Design consequence |
|---|---|---|
| **WALL** | A formal impossibility / theorem. If real, it *bounds what may be promised*. | The design must route around it or fail closed at it. Never "solve" it. |
| **LENS** | An empirical/theoretical tradition with a load-bearing claim. | Shapes structure; contestable. |
| **FORK** | A live, unsettled dispute where the framework must **choose** and own the choice. | Becomes a ratified Decision in the umbrella ledger. |

---

## 1. WALLS — the formal results that bound any AI Government

These are the reason the honest posture is *fail-closed escalation*, not optimization. The existing
`Mars_Governance/governance/fail_safe_gate.py` is already a correct response to W5–W6; the rest need equivalents.

| # | Result | Statement (as recalled — VERIFY) | What it forbids us from promising |
|---|---|---|---|
| W1 | **Arrow (1951)** | No rank-order social welfare function over ≥3 alternatives satisfies unrestricted domain + Pareto + independence of irrelevant alternatives + non-dictatorship. | There is no "correct" aggregation of citizen preferences. Any objective function the AI optimizes is a *chosen* value judgment, not a discovered one. |
| W2 | **Gibbard–Satterthwaite (1973/75)** | Any onto, non-dictatorial, single-valued voting rule over ≥3 alternatives is manipulable. | No strategy-proof democratic mechanism. "Gaming-resistant voting" is unachievable; only *gaming-detectable* and *gaming-costly* are. |
| W3 | **Sen's liberal paradox (1970)** | No rule satisfies unrestricted domain + Pareto + minimal liberalism (≥2 individuals each decisive over one pair). **`[CORRECTED 2026-08-11]` requires n ≥ 2 individuals AND ≥ 4 alternatives** (not ≥3). *J. Political Economy* 78(1):152–157. | Individual rights and collective efficiency genuinely conflict. Rights must be *lexically prior constraints*, not terms in a welfare sum. |
| W4 | **Myerson–Satterthwaite (1983)** | No mechanism for bilateral trade with private values is simultaneously efficient, individually rational and budget-balanced. | No perfectly efficient allocation mechanism for the colony's internal market. Some deadweight loss or subsidy is structural. |
| W5 | **McKelvey chaos (1976)** | In ≥2 policy dimensions, **whenever no point is unbeaten (empty core)** an agenda-setter can reach *any* outcome — including points **outside the Pareto set** — via a sequence of pairwise majority votes. *JET* 12(3):472–482; extended to concave preferences by Schofield, *RES* 45(3):575–594 (1978). **`[CORRECTED 2026-08-11]` the result is CONDITIONAL on the empty core AND assumes a frictionless, INSTITUTION-FREE environment** — which is what motivated the *structure-induced equilibrium* literature. | **Agenda control is the capture channel.** An AI that curates option menus is, structurally, an agenda-setter. **But institutions can bound the chaos** — so supplying agenda structure is a *solution lever*, not just a risk. Strengthens the randomized-agenda-order design. |
| W6 | **Median voter (Black 1948 / Downs 1957)** | With single-peaked preferences on ONE dimension, majority rule selects the median ideal. | The only regime where aggregation is well-behaved. Detect single-peakedness; **certify only inside it** (already implemented, 0 silent failures on 500-panel ensembles). |
| W7 | **Ashby's law of requisite variety (1956)** | Only variety can absorb variety: a regulator needs variety ≥ the disturbance it regulates. | An AI cannot "match" a society's variety. It must **attenuate** variety (rules, categories, budgets) — and attenuation *is* Scott's legibility loss. The trade-off is unavoidable, so make it explicit and local. |
| W8 | **Hayek's knowledge problem (1945) / Mises calculation (1920)** | The knowledge relevant to allocation is dispersed, tacit and revealed only in local action; prices aggregate it. | Central optimization of a general economy is not merely hard, it is *ill-posed*. **Exception to work:** hard closed physical loops (O₂, water, power, pressure) — see §4. |
| W9 | **Goodhart / Campbell** | A measure that becomes a target ceases to be a good measure. | Every metric the governor optimizes will be gamed. Metrics need adversarial review + rotation + a declared corruption model. |
| W10 | **Condorcet jury (1785)** | Majority accuracy → 1 as n grows **only if** voter errors are independent and better-than-chance. | Correlated error (shared media, AI-generated advice, preference cascades) destroys epistemic democracy. **An AI advising everyone is itself the correlation mechanism.** Pluralism (≥2 model variants) is a mitigation already used. |
| W11 | **Perrow normal accidents (1984)** | Tight coupling + interactive complexity ⇒ accidents are a system property, not operator error. | A closed colony is maximally tight-coupled. Governance must assume its own failures, not exclude them. |
| W12 | **Tainter (1988)** | Complex societies face declining marginal returns to added complexity. | Adding institutional machinery has a cost curve. The governor must be able to **remove** rules, not only add them (sunset clauses as a first-class instrument). |

**Consequence for the AI Governor's charter.** W1+W3 ⇒ the AI never selects the objective. W2+W5 ⇒ the AI's
agenda-setting power must be structurally checked (randomized agenda order, published preference peaks,
independent verifier). W7+W8 ⇒ subsidiarity is not a political preference but an engineering requirement.
W9+W10 ⇒ metric pluralism and model pluralism are safety features. W11+W12 ⇒ fail-closed and sunset.

---

## 2. LENSES — the six literatures, and what each contributes

### L1. Political economy of institutions
- **North (1990)** — institutions = rules of the game; transaction costs; path dependence.
- **Acemoglu & Robinson (2012, 2019)** — *inclusive vs extractive* institutions; **the Narrow Corridor**: liberty
  exists only where state capacity and societal capacity grow *together*. ⇒ **An AI Governor is a massive
  unilateral increase in state capacity.** Without a matched increase in society's capacity to constrain it,
  the predicted outcome is a *despotic Leviathan*. This is the single most load-bearing warning in the map:
  every capability added to the governor must ship with a matching citizen-side check.
- **Olson (1965, 1982)** — concentrated benefits / diffuse costs; distributional coalitions ossify over time.
- **Buchanan & Tullock (1962)** — the *constitutional* vs *in-period* distinction, and the optimal-majority
  calculus: threshold chosen to minimize (external costs + decision costs). ⇒ **voting thresholds are derivable,
  not arbitrary** — a genuinely implementable result for the ruleset department.
- **Stigler (1971) / Tullock (1967) / Krueger (1974)** — regulatory capture, rent-seeking as real resource waste.

### L2. Social choice, mechanism design, and voting technology
- Walls W1–W6, W10 above.
- **Mechanism design** (Hurwicz–Maskin–Myerson): revelation principle; **VCG/Clarke** — efficient but not
  budget-balanced and collusion-fragile; **Lindahl** pricing for public goods; **Samuelson condition** ΣMRS = MRT.
- **Radical Markets (Posner & Weyl 2018)** — **quadratic voting** (cost ∝ votes², so intensity is expressible),
  **quadratic funding** (Buterin–Hitzig–Weyl) for public goods, **COST/Harberger self-assessed tax**. Directly
  addresses "direct democracy + optimize taxes + financial freedom" as a *single* mechanism family.
- **Liquid democracy** — delegation with revocation. Known pathology: **delegation concentration** (super-voters)
  empirically observed in LiquidFeedback deployments. Mitigation: delegation caps, decay, transparency.
- **Sortition / citizens' assemblies** — Athenian precedent; modern: Ireland's Citizens' Assembly, Ostbelgien's
  permanent citizens' council, France's Convention Citoyenne. ⇒ a **statistically representative deliberating
  body** is the most plausible producer of the "general guidelines" the governor consumes (fixes A2).
- **Deliberation** — Habermas (legitimacy from discourse); **Fishkin** deliberative polling (preferences
  *change* under deliberation — so measuring raw preference is measuring an artifact); **Landemore** epistemic
  democracy / open democracy.
- **Deployed civic tech** — **vTaiwan / Pol.is** (Taiwan): consensus-mapping that surfaces *bridging* statements
  rather than majority statements; Estonia X-Road. ⇒ the closest real-world existence proof of machine-assisted
  collective choice, and a concrete design to study rather than reinvent.
- **Negative result carried in:** blockchain voting is judged counterproductive for public elections
  (secrecy-vs-traceability, consensus-level fraud, endpoint compromise) — already an **audit-tier** finding in the
  `mars-governance` ledger; the resolved design uses tamper-evident logging + **risk-limiting audits (paper_rla)**.

### L3. Economics of allocation, taxation, and freedom
- **Optimal taxation** — Ramsey (inverse-elasticity); **Mirrlees (1971)**: with unobservable ability, the optimal
  income tax is nonlinear and shaped by the elasticity + density of the ability distribution; **Diamond–Saez**
  formulas; **Atkinson–Stiglitz** (no differential commodity taxation under weak separability).
- **Land value tax / Georgism `[CORRECTED 2026-08-11 — a genuine falsification]`** — TWO separate claims that
  this map originally ran together:
  1. **Taxing an inelastically-supplied factor is non-distortionary** (George, *Progress and Poverty*, 1879).
     **SURVIVES.** This is the whole justification for the colony fiscal base, and it needs no further conditions.
  2. **The Henry George theorem** — aggregate differential land rents *exactly equal* public-goods expenditure
     at optimal city size (**Arnott & Stiglitz, *QJE* 93(4):471–500, 1979** — *not* "Stiglitz 1977").
     **FALSIFIED AS AN APPLICATION HERE.** Its conditions require free inter-jurisdictional mobility (Tiebout),
     a city at rent/transport-optimal size, no congestion, identical agents, and public goods as the sole cause
     of agglomeration. **Five fail in a colony — and one of them (no exit) is a load-bearing feature of this
     polity** (the same premise as charter C21). The self-financing equality may NOT be invoked.
  ⇒ The fixed scarce factor is still *pressurized habitable volume* (+ radiator area), and an LVT-analogue on
  it is still the leading instrument — **on inelasticity grounds, not on a self-financing theorem.** Whether
  rents cover the bill is now an EMPIRICAL question for the twin (umbrella H4), which
  `aigov/specs/d2_economy.py::_falsification_test` already computes as a number.
  See `research_outputs/aigov-v2-land-value-tax-henry-george.md`.
- **Externalities** — Pigou (tax the externality) vs **Coase (1960)** (with low transaction costs, initial
  assignment is efficiency-neutral; with high TC it is decisive).
- **Money in a closed economy** — seigniorage, unit of account under a non-tradeable resource basket, and the
  question of whether a colony currency is backed by energy/O₂ (energy-standard proposals) or fiat with an
  ECLSS-linked anchor. **Genuinely open; not settled in the literature; treat as a research target.**
- **Freedom-side counterweights** — **Nozick (1974)** entitlement theory / minimal state; **Friedman** on the
  price system; vs **Rawls (1971)** (veil of ignorance, difference principle, *lexical priority of liberty*) and
  **Sen** (capability approach; famines are entitlement failures, and a free press + democracy prevent them).
  ⇒ the "optimize taxes AND maximize financial freedom" tension is **exactly** the Rawls–Nozick axis. The governor
  must expose the frontier and let the polity pick a point; claiming an optimum is a category error (W1).
- **Contested — do not rely on:** Chamley–Judd zero-capital-tax (rebutted by Straub–Werning 2020).

### L4. Trade, geostrategy, and external relations
- **Ricardo** comparative advantage; **Heckscher–Ohlin**; **Krugman** new trade theory (increasing returns ⇒
  trade between similar economies; home-market effect).
- **Gravity model of trade** — flows ∝ economic mass, ∝ 1/distance. ⇒ **Derivable colony result:** at 5.5×10⁷–4×10⁸ km
  and months of transit, the gravity model predicts near-zero routine trade. **A Mars colony is structurally
  near-autarkic**, so its economics is closer to a closed-loop life-support economy than to a trading city-state.
  This is a strong, checkable prediction the Trade department should be built to test, not assume away.
- **Hirschman (1945)** *National Power and the Structure of Foreign Trade* — asymmetric dependence *is* coercive
  power. ⇒ already implemented as the **"resupplier-as-coercer" survival veto** in
  `Mars_Governance/governance/connection.py`. Excellent alignment; extend it.
- **Farrell & Newman (2019)** *weaponized interdependence* — network chokepoints ("panopticon" + "chokepoint"
  effects). ⇒ the comms relay and the resupply cadence are the colony's chokepoints. Model them.
- **Space law (real, verifiable constraints)** — Outer Space Treaty 1967 (Art. II: no national appropriation;
  Art. VI: state responsibility for non-governmental actors); Moon Agreement 1979 (few ratifications); Artemis
  Accords (2020, safety zones); US Commercial Space Launch Competitiveness Act 2015 and Luxembourg's 2017 law
  (resource-extraction rights). ⇒ **the legal envelope for colony property law**; these are the actual constraints
  on the Justice/Property department and are cheaply verifiable.
- **Geostrategy proper** — Mackinder/Spykman/Mahan are *analogy-grade* for space and should be treated with
  suspicion; prefer **Dolman, *Astropolitik* (2002)** and **Bowen, *War in Space* (2022)** for orbital-mechanics-
  grounded strategic reasoning (delta-v, not distance, is the metric of "closeness").

### L5. Philosophy of governance, legitimacy, and the emergency
- **Legitimacy** — consent (Locke), discourse (Habermas), performance/output legitimacy (Scharpf's input vs
  output legitimacy — an AI governor is a maximal *output*-legitimacy bet, which is exactly the fragile kind).
- **The emergency** — Schmitt's "sovereign is he who decides on the exception" is the *diagnosis* even if one
  rejects the *prescription*; Rossiter's constitutional dictatorship; the Roman dictator's fixed term. ⇒ the
  unresolved question already flagged verbatim in the colonization roadmap: *who overrides when a binding vote
  conflicts with a life-support hard limit?* Design requirement: **declared trigger, enumerated powers,
  enumerated untouchables, automatic expiry, mandatory post-hoc audit, and a different body for each of
  declare / exercise / terminate / audit.**
- **Rule of law** — Fuller's eight desiderata of legality (generality, promulgation, non-retroactivity, clarity,
  non-contradiction, possibility of compliance, constancy, congruence between rule and administration).
  ⇒ **a directly implementable checklist**: every rule the governor emits can be mechanically linted against
  Fuller's eight. This is one of the cheapest, highest-value implementable results in the whole map.
- **Constitutional design** — separation of powers (Montesquieu); entrenchment and amendment rules; Elster on
  *Ulysses and the Sirens* (pre-commitment) — the governor's own constraints are precisely a Ulysses contract.

### L6. Social engineering, behaviour, and cybernetics
- **Kuran (1995)** *Private Truths, Public Lies* — **preference falsification**: under social pressure people
  misreport preferences, producing stable-looking regimes that collapse suddenly (preference cascades).
  ⇒ In a small, high-stress, no-exit colony this effect is *maximal*. Direct democracy measures **expressed**
  preferences; the governor must model the gap and treat sudden unanimity as a warning sign, not a success metric.
- **Nudge (Thaler & Sunstein)** and its critics — an AI that sets defaults is engaged in choice architecture
  whether or not it intends to be. Requires an explicit, published manipulation policy.
- **Merton** — unintended consequences; **Cialdini** — influence; **Dunbar ~150** (contested — do not build on it;
  Lindenfors et al. 2021 give mean 69.2, 95% CI 3.8–292.0, and Dunbar rebuts — the dispute is live).
- **Milgram `[CORRECTED 2026-08-11 — the blanket flag was wrong]`** — the **BEHAVIOUR replicates robustly**
  (Burger 2009; Blass 1963–85; recent online replication). Only the **mechanism** (agentic state → *engaged
  followership*) and the **reporting integrity** (Perry 2013: omitted conditions) are contested. So the
  *phenomenon* is usable and the *mechanism* is not — and the sharper reading is **worse** for an AI Governor:
  if harm-compliance runs through **identification with the enterprise** rather than surrender of agency, a
  governor that supplies a compelling mission frame is a **more** effective compliance engine than one issuing
  orders. Direct support for charter C03 (emergency authority) + C15 (fail-closed) + the anti-steering
  primitives. **Zimbardo remains replication-contested — do not build on it.**
  See `research_outputs/aigov-v12-contested-set.md`.
- **Cybernetics** — **Wiener**; **Ashby** (W7); **Beer's Viable System Model** and **Project Cybersyn** (Chile,
  1971–73) — *the* historical precedent for computer-assisted government, ended by the 1973 coup, and the source
  of the S1–S5 functional decomposition used in `department-ontology.md`; **Deutsch, *The Nerves of Government*
  (1963)**; **Forrester** system dynamics (and the contested *Limits to Growth*).
- **Resilience** — Holling's adaptive cycle / panarchy; Taleb's antifragility; **Weick & Sutcliffe** on
  high-reliability organizations (preoccupation with failure, reluctance to simplify, deference to expertise) —
  a colony is an HRO, and HRO doctrine partially *contradicts* algorithmic centralization (deference to expertise
  means the person at the valve outranks the model).
- **Modern AI-governance practice** — Hidalgo's *augmented democracy* (personal digital twins voting as proxies);
  DAO governance failures (token-weighted voting ⇒ plutocracy; The DAO 2016); Buterin on plural/quadratic funding.

---

## 3. FORKS — where the framework must choose (each becomes a ratified Decision)

| # | Fork | Options | Soraya's drafted lean |
|---|---|---|---|
| K1 | Source of the "general guidelines" | referendum · **sortition assembly** · quadratic-voted priorities · liquid delegation | **Sortition assembly + quadratic priority budget.** Sortition resists capture and produces *reasoned* guidelines; QV expresses intensity. Referendum alone maximizes preference-falsification error (L6). |
| K2 | Objective structure | single welfare function · **lexicographic constraint stack** · Pareto-frontier exposure | **Constraint stack + frontier exposure.** W1/W3 forbid a defensible scalar objective; rights become hard constraints, not weights. |
| K3 | Fiscal base | income tax · consumption tax · **volume/area LVT-analogue** · resource royalties | **LVT-analogue on pressurized volume + thermal/radiator area**, plus Pigouvian pricing on O₂/water draw. Non-distortionary on a physically-enumerable fixed factor. **`[CORRECTED 2026-08-11]` the "Henry-George-financed public goods" justification is REMOVED** — its conditions fail in a no-exit colony (see L3). The instrument stands on factor inelasticity; coverage is measured, not derived. |
| K4 | Economic coordination | central plan · **market with hard physical caps** · full laissez-faire | **Cap-and-market**: physically-binding closed loops centrally *capped* (W8 exception), everything else priced and decentralized. Directly implements the Hayek/Scott counter-design. |
| K5 | Emergency authority | AI holds override · human caretaker · **split: AI *detects*, human *declares*, third body *audits*** | **Split.** The AI may never hold the exception (Fork 1). `fail_safe_gate` already implements "detect and escalate". |
| K6 | Scale strategy | one design for all scales · **phase-change gates** | **Phase-change gates** (see idea-anchor Fork 2). Continuity is almost certainly false. |
| K7 | Property regime under OST Art. II | ownership · **usufruct/possession with self-assessed value** | **Possession + Harberger self-assessment.** Sidesteps the non-appropriation problem legally, and is efficient (COST). |
| K8 | Minority protection absent exit | majority rule + rights · **structural (supermajority + veto rights + rotation)** | **Structural.** Tiebout ("vote with your feet") **does not exist on Mars** — the standard Earth discipline device is absent, so protection must be built in, not assumed. |

---

## 4. The one derived result worth stating plainly

**Hayek's objection is at its weakest exactly where this project starts, and at its strongest exactly where the
project aspires to end.**

A closed life-support loop (O₂ partial pressure, water, power, thermal rejection, pressure integrity) is
centrally *plannable*: the state variables are few, physically measurable, causally tight, and the failure mode
is death rather than inefficiency. That is a genuine, defensible exception to W8 — and it is the entire
justification for a colony-scale AI Governor.

The same argument gives **no support whatever** to centrally planning a terrestrial nation's economy, where the
relevant knowledge is dispersed and tacit and the failure mode of a wrong plan is stagnation rather than
asphyxiation.

**Therefore the honest architecture is not "an AI that runs everything at increasing scale". It is a
*subsidiarity engine*: the governor centrally runs the small set of hard physical commons, and everywhere else
maintains the conditions under which decentralized discovery works — prices, possession rules, courts, and a
protected right to experiment.** Scaling colony → city → nation means the *centrally-run set shrinks* as a share
of the whole, not grows. State that in the charter, and the project is defensible; omit it, and it is
*Seeing Like a State* with better tooling.

---

## 5. Verification queue for F0 (what `/research` + `/research-verify` must confirm)

Ordered by *how much design weight the claim would bear*, highest first. Only these need audit-tier promotion;
the rest of the map may remain discovery-tier orientation.

| # | Claim to verify | Bears weight on | Status |
|---|---|---|---|
| V1 | Exact statements + preconditions of W1, W2, W5, W6, W7 | The entire fail-closed charter (F1) | ✅ **CITED** — `aigov-v1-social-choice-walls.md`; 3 corrections, 0 falsified |
| V2 | Henry George theorem conditions; LVT efficiency results | K3 fiscal base — the whole Economy department | ✅ **CITED** — `aigov-v2-land-value-tax-henry-george.md`; **H2 FALSIFIED**, K3 justification revised |
| V3 | Buchanan–Tullock optimal-majority derivation | Ruleset thresholds — makes them derived, not asserted | open |
| V4 | Fuller's eight desiderata (exact list) | The rule-linter (cheapest high-value implementable) | ✅ **CITED** — `aigov-v4-fuller-legality-desiderata.md`; implementation matches **8/8** |
| V5 | OST Art. II / VI text; Artemis Accords safety zones; 2015 US + 2017 LU resource laws | K7 property regime — real legal envelope | ✅ **CITED** — `aigov-v5-space-law-property-envelope.md`; K7 survives; **new: Art. VI ⇒ derivative authority** (charter C25) |
| V6 | vTaiwan/Pol.is mechanism + measured outcomes | K1 guideline-production mechanism |
| V7 | Liquid-democracy delegation-concentration empirics | K1 pathology bounds |
| V8 | Gravity-model coefficients / distance elasticity of trade | Trade department's autarky prediction |
| V9 | Kuran preference-falsification mechanism + cascade evidence | Legitimacy metrics; the "sudden unanimity" alarm |
| V10 | Cybersyn's actual architecture and its documented failure modes | The one real precedent — learn, don't repeat |
| V11 | Acemoglu–Robinson Narrow Corridor formulation | The capability↔check pairing rule |
| V12 | Contested set (Chamley–Judd, Dunbar, Milgram, Limits to Growth) — confirm contested status | Prevents building on sand |
