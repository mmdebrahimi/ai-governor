# V13 — What data does a government actually need? A state information architecture

> **Family:** `aigov-foundations` · **Claim ID:** V13 · **Captured:** 2026-08-11
> **Method (honest label):** 5 iterative WebSearch rounds, each query shaped by the previous round's
> findings. **CITED tier — named primary sources with dates and figures, NOT quote-verified** (no
> per-URL WebFetch pass). Say "cited", never "verified".
> **Why it exists:** the AI Governor has a Department Contract, a charter, an intake and a twin — but no
> account of *what the state should know*. This is that account. It is also, per Scott, the single most
> dangerous artefact in the whole design, so it is written as a **budget** rather than a wish-list.

---

## 0. The question was slightly wrong, and the correction is the main finding

"What data would a government need to collect to do its job optimally?" invites a **list**. Every serious
framework in this literature says the answer is not a list but a **derivation**, and one sentence from EU
data-protection doctrine states it best:

> **The logic runs from purpose to data, not the other way round.**
> (GDPR Art. 5(1)(b) purpose limitation → Art. 5(1)(c) data minimisation: data must be *"adequate, relevant
> and limited to what is necessary in relation to the purposes."*)

So the correct output is a **procedure**:

```
decision the department must make
  → the statistic that decision actually turns on
    → the minimum observation that produces that statistic
      → the collection instrument, chosen last and cheapest-first
```

**We have already built the machine that runs this procedure.** `DepartmentSpec` forces every department to
declare its `objectives_received`, `instruments` and `metrics`; the state variables it may read follow from
those. `twin.check_state_coverage` already refuses a department that declares a variable the world does not
serve. What was missing was the *content* — this memo — not the mechanism.

**Consequence: any data item that cannot be traced back to a specific decision by a specific department is
not a gap in our collection. It is a proposal to make society more legible for its own sake, which is
exactly the failure mode the project exists to avoid.**

---

## 1. The four-layer architecture (the real shape of a statistical system)

Every mature system is these four layers, built bottom-up. Layer 1 is not optional and everything else is
derived from it.

| Layer | What it is | Evidence |
|---|---|---|
| **L1 — Registers (the spine)** | Continuously-updated lists of the *entities* that exist: people, businesses, dwellings/parcels, and the relationships between them | Nordic model: population registers Sweden **1957**, Norway **1964**, Denmark & Finland **1969**; Denmark's business register **1975**, dwellings **1977** |
| **L2 — Accounts (the closed books)** | Double-entry frameworks that force consistency: national accounts (SNA), and now environmental accounts (SEEA) | SNA 2008; **SEEA Ecosystem Accounting adopted as an international statistical standard, UNSC 52nd session, March 2021** (ch. 1–7) |
| **L3 — Indicators (the dashboard)** | Derived measures of condition and wellbeing that the accounts do not capture | Stiglitz–Sen–Fitoussi 2009 (12 recommendations, 3 domains); OECD *Beyond GDP* / *For Good Measure* 2018 |
| **L4 — Real-time signals (the nowcast)** | High-frequency, passively-collected proxies: satellite, scanner, mobile, admin transactions | Statistics Canada **replaced an agricultural survey with satellite imagery**; Chessa (2016) scanner data in the CPI |

### The build order is the finding, not the list

The Nordic sequence is instructive because it is *empirical*, not theoretical: build the register spine,
add domain registers one at a time, and the expensive top-level product falls out for free at the end.
**Denmark ran the world's first fully register-based census in 1981; Finland in 1990** — no questionnaire
at all. By the 2010 round, **nine countries** were primarily register-based (Austria, Belgium, Denmark,
Finland, Iceland, Netherlands, Norway, Slovenia, Sweden).

The lesson for a greenfield polity — colony or farm group — is blunt: **do not start by designing surveys.
Start by deciding what entities exist and giving each a persistent identifier.** Everything downstream is
cheaper forever.

---

## 2. There is an agreed MINIMUM, and it is small

The UN does not treat "what to collect" as open-ended. It defines three explicit tiers:

| Tier | Meaning |
|---|---|
| **Minimum Requirement Data Set (MRDS)** | what *every* country is expected to produce |
| **Recommended** | annual + some quarterly accounts, important for assessing an economy |
| **Desired** | useful if resources permit |

The MRDS is a named, finite set of tables (Country Notes plus tables 1.1, 1.2, 2.1/2.4, 2.2/2.5, 2.3/2.6,
4.1/1.3, 4.2 of the UN National Accounts Questionnaire). The underlying source data required is
correspondingly small: **output by activity, labour market statistics, household statistics, and company
business accounts.**

Sobering context on feasibility: conceptual SNA compliance rose from 97 countries (2007) to 176 (2017),
but the Statistical Commission recorded **concern at the low level of compliance with the minimum set** —
i.e. many states cannot produce even the minimum. Any design that assumes a rich data environment is
assuming something most real governments do not have.

**Adopt the tiering itself.** It is the correct answer to scope creep: a proposed data item must be
argued into a tier, and the minimum tier must stay defensible on its own.

---

## 3. Five constraints that bound collection — the reason "collect everything" is wrong

This is the part a naive design omits, and each constraint is quantified.

### C1 — The privacy budget is finite and every published statistic spends it
The 2020 US Census replaced data-swapping with a **differential-privacy Disclosure Avoidance System**.
The structural consequence: *releasing more tables requires injecting more noise*, so the Bureau **withheld
some tables** rather than degrade the rest. Accuracy was deliberately concentrated at larger geographies;
at block level users were warned to expect artefacts (children apparently living alone, "vacant" units with
population > 0). A live concern in the literature is that the distortion may be **systematic bias** (rural
vs urban redistribution), not merely noise.
→ **Design rule: publication is rationed. Decide the accuracy targets first, then see how many tables the
budget affords.**

### C2 — Surveys are decaying, and the bias is now directional
CPS ASEC weighted response: **69.0% (2019) → 62.0% (2025)**. Consumer Expenditure Survey: **73.8% (2008) →
66.7% (2013)**. Telephone response fell ~75% over two decades.
More importantly the bias became real *and signed*: linking CPS to tax data found **no bias before COVID**,
but since 2020 nonresponse biases income estimates **upward by 2–3%** and official poverty **downward**.
Formal triggers exist — OMB requires a nonresponse-bias study below **80%** response; the Census Bureau
flags below **60%** unit response, **70%** item response, or **>5%** longitudinal attrition.
→ **Design rule: a survey-first system has a decaying denominator. Prefer registers and passive
instruments; treat every survey as a liability with a maintenance cost.**

### C3 — Goodhart, already load-bearing in our design
Any metric that becomes a target stops measuring. Our contract already forces every `Metric` to declare a
`gaming_model` (invariant I4). This memo does not soften that; it extends it — **a statistic collected by
the state is a higher-value target than an internal KPI, because more is allocated on it.**

### C4 — Legibility (Scott), the deepest one
Making society measurable destroys the local practical knowledge that made it work. This is not a
side-effect of bad measurement; it is what measurement *does*. Our subsidiarity invariant (I8) is the
mechanical response: a LOW-central-legitimacy department may set rules and prices but not allocate — and
therefore **does not need the data that allocation would require**.
→ **Design rule: legitimacy rating bounds the data appetite. If a department may not allocate, do not
build it the dataset an allocator would need. The dataset is what makes the temptation actionable.**

### C5 — Purpose limitation is a legal, not merely ethical, boundary
GDPR Art. 5(1)(b)–(c) and the Art. 89 derogation: processing for statistical purposes is a **compatibility
presumption, not a blanket exemption**. Anonymisation removes data from scope entirely (Recital 26).
Enforcement is real — H&M was fined **€35.3M** on minimisation grounds.
→ **Design rule: every dataset carries a declared purpose; a new use needs a new basis, not a shrug.**

---

## 4. The institutional precondition nobody budgets for

Round 1 turned up a detail worth elevating: the Nordic register systems work because **every Nordic country
has a national statistics act giving the statistical institute the legal right to access administrative
data**. The technology was never the constraint; the legal instrument was.

The **UN Fundamental Principles of Official Statistics** (10 principles; UNECE 1992 → UN Statistical
Commission 1994 → ECOSOC 2013 → **UN General Assembly resolution 68/261, January 2014**) make this explicit:
the GA stated that these values *"should be guaranteed by legal and institutional frameworks."* Principle 1
covers relevance, impartiality and equal access; the confidentiality principle requires individual data —
for natural **or legal** persons — to be used **exclusively for statistical purposes**.

A **Maturity Model** (endorsed March 2020) scores compliance across **11 dimensions** on three levels
(Developing / Practising / Leading), which is a ready-made self-assessment instrument.

**Bearing on our charter.** Three of the ten principles are constitutional in character and belong in D0,
not in a statistics manual:
1. **Professional independence** — the statistical function must not be directable by the executive it
   measures. In our terms: *the body that produces the numbers cannot be the body that acts on them.* This
   is the `generate ≠ decide ≠ verify` separation (I9), extended to a fourth role: **measure**.
2. **Exclusive statistical use** — data collected to compute a statistic may never be used to act against
   the individual who supplied it. Without this, honest reporting collapses.
3. **Equal access** — statistics are published to everyone simultaneously, or the holder gains an
   information advantage over the polity that funded it.

**Drafted charter clauses (for ratification, not self-adopted):**
> **C26** — The measurement function shall be independent of the executive function; no body may both
> produce a statistic and be judged by it. *(candidate invariant: extend I9's role set with `MEASURE`)*
> **C27** — Data collected for statistical purposes shall never be used in an action against the person
> or entity that supplied it. *(aspirational at software level; enforceable only by siting + audit)*
> **C28** — Every dataset shall declare its purpose, its tier, and the decision it serves; an item that
> serves no declared decision shall not be collected. *(candidate invariant, mechanically checkable)*

C28 is the mechanical form of §0 and is the one I would most want in the code.

---

## 5. The derivation, applied to our sixteen departments

Minimum tier only. Each row is *the decision → the statistic → the cheapest instrument*.

| Dept | The decision it must make | Minimum statistic | Cheapest instrument |
|---|---|---|---|
| **D1 Life-support / Resources** | how much to produce, when to buffer | stock + flow per closed loop (O₂, water, power, thermal) | **direct sensor telemetry** — no survey, no register |
| **D2 Economy / Fiscal** | rate-setting on the fixed factor | inventory of the taxed factor (volume/area) + its distribution | **register** (physically enumerable) |
| **D3 Collective choice** | who may vote, on what | eligibility register + the ratification record | **register** |
| **D4 Justice** | case throughput, backlog | case register with timestamps | **admin by-product** |
| **D5 External relations / Trade** | dependence exposure | inbound/outbound flows by counterparty + concentration | **admin by-product (customs/shipping)** |
| **D6 Health / Population** | carrying capacity vs demand | population register + vital events + capacity | **register + admin** |
| **D7 Education / Civic** | skills supply vs need | education register (Nordic pattern) | **register** |
| **D8 Innovation** | is the experiment space open | count of *permitted* experiments, not outcomes | **admin by-product** |
| **D9 Labour / Housing** | floor compliance | employment + dwelling registers | **register** |
| **D10 Infrastructure** | maintenance vs failure | asset register + condition | **register + inspection sample** |
| **D11 Security / Continuity** | risk exposure | incident log + near-miss log | **admin by-product** |
| **D12 Information integrity** | is the record intact | append-only log + audit trail | **the ledger itself** |
| **D13 Coordination** | resolve contention | the declared shared variables only | **derived — collects nothing new** |
| **D14 Foresight / twin** | what happens if | *the union of the above, and nothing else* | **derived — collects nothing new** |
| **D15 Audit** | is a certification faithful | the certification record + a verification sample | **derived + sample** |
| **D0 Constitution** | are limits holding | invariant results | **derived** |

**Four of sixteen departments collect nothing new.** They consume. That ratio is the health check: if a
"data need" appears that no department's decision requires, it is legibility for its own sake.

Note the instrument column ordering — **sensor > register > admin by-product > sample survey > census**.
Cost, burden and decay all rise left-to-right. A census is the instrument of last resort, and the Nordic
evidence is that a mature register system removes the need for one entirely.

---

## 6. Instantiation for the farm enterprise (the actual north star)

The same derivation, for a multi-country family farming group. This is where the research is immediately
usable, and the fit is much better than I expected before Round 4.

### The register spine you should build first
1. **Parcel register** — every land parcel, with boundary geometry, tenure, and a persistent ID. This is
   the population register of a land business; everything hangs off it.
2. **Asset register** — plantings (species, cohort year), structures, equipment, water rights.
3. **Entity register** — legal entities per jurisdiction, and who owns what. With multi-country structure
   this *is* your tax and investor reporting substrate.
4. **People register** — staff, contractors, guests. Minimal fields; GDPR purpose-limited from day one,
   since you will operate inside the EU regime in at least one jurisdiction.

### The accounts layer — and this is the strong finding
**SEEA Ecosystem Accounting is the right framework and it became an actual international standard in
March 2021.** Its five core accounts measure ecosystem **extent**, **condition**, and **services**, are
spatially explicit, and **89 countries** already implement the SEEA Central Framework. For a business whose
thesis includes lumber, regenerative farming, carbon and eco-tourism, this is not a nice-to-have: it is the
existing, credible, internationally-recognised vocabulary for saying what your land is worth beyond the
crop. **A fund will understand SEEA. It will not understand a bespoke sustainability spreadsheet.**

### The real-time layer — cheaper than you'd think
Round 4's operational finding is directly transferable:
- **Point sampling requires only an accurate map, no pre-existing sampling frame.** That is the answer to
  "how do we measure a holding in a country with no agricultural register."
- **Area Sampling Frames + pixel counting + regression/calibration estimators** are the standard toolkit
  (FAO *Handbook on Remote Sensing for Agricultural Statistics*).
- Operating precedents at national scale: **USDA-NASS Cropland Data Layer**, **India FASAL** (5 km grid,
  segments with >5% agricultural area, four crop strata by Dalenius–Hodges, ~15% sample per stratum,
  covering **90% of national production**), **EC MARS**, **China CropWatch**, **GEOGLAM**.
- **Pakistan SUPARCO**: ten land-use strata, 20–30 segments of ~30 ha each, probability-proportional-to-area.
- Sensor availability (Sentinel-1/2/3 + MODIS + high-res SAR) now supports **country-wide cultivated-area
  estimation including small plots**.
- **Statistics Canada replaced an agricultural survey outright with satellite imagery** — the existence
  proof that this substitutes for, rather than supplements, ground collection.

### The four business lines, and the one number each actually turns on
| Line | The decision | The statistic |
|---|---|---|
| Lumber / trees | thin, harvest, or hold | standing volume by cohort + growth increment (remote-sensed, ground-truthed on a sample) |
| Automated farming | plant / input / irrigate | yield per hectare + water and input per unit output |
| High-value products chain | make vs buy, price | landed cost per unit + realised price by channel |
| Eco-tourism / retreat | capacity and pricing | occupancy, RevPAR, and **repeat rate** (the honest quality signal) |

**And the cross-cutting one the governance machinery exists for:** land, water, capital and family attention
allocated across four claimants with 1-to-40-year horizons. That allocation is the decision. The statistic
it turns on is **committed vs available capacity per resource per period** — which is precisely a
`StateVar` set under our existing contract.

---

## 7. Honest status and what the next rounds should attack

**Tier:** cited, not quote-verified. Every figure above carries a named source and a date; none has had a
verbatim-quote check. Do not put any of these numbers in an investor document without that pass.

**What these five rounds did NOT cover, ranked by how much it would change the design:**
1. **Small-polity / subnational minimums.** Everything found is national-scale. A 200-person colony or a
   6-farm group has *n* too small for most survey inference, and the disclosure problem is far worse (in a
   village, "the household with three children" is an identifier). **This is the biggest open gap.**
2. **Cost.** Not a single figure found on what a statistical system costs per capita. Without it, "minimum
   tier" is unpriced and therefore not really a constraint.
3. **Failure cases.** I searched for what states *should* collect, not for statistical systems that
   collapsed, were captured, or were weaponised. The Scott critique is theoretical here; the empirical
   record of measurement-enabled harm is unexamined and would sharpen C4 considerably.
4. **Firm-level analogue.** Whether the SNA/SEEA structure genuinely transfers to a private group, or
   whether management-accounting frameworks fit better.
5. **Data quality dimensions** — the formal frameworks (relevance, accuracy, timeliness, coherence,
   accessibility) were referenced but not retrieved.

**Recommended next round:** #1 and #3 together — small-n statistics and the harm record — because both
attack the design rather than extend it, and both could change what we build.

## Sources

- [SNA 2008 full text — UNSD](https://unstats.un.org/unsd/nationalaccount/docs/sna2008.pdf) · [UN National Accounts Questionnaire (MRDS tables)](https://unstats.un.org/unsd/nationalaccount/docs/NAQsb-e.pdf)
- [Register-based statistics in the Nordic countries — UNECE 2007 (FAO mirror)](https://openknowledge.fao.org/server/api/core/bitstreams/f15768e1-3a19-4828-bdf0-ddee2a62e9ea/content) · [Stats NZ, international census models](https://www.stats.govt.nz/assets/Consultations/Modernising-our-approach-to-the-2028-Census/Supplementary-materials/International-examples-on-census-models.pdf)
- [SEEA Ecosystem Accounting adopted — seea.un.org](https://seea.un.org/news/seea-ecosystem-accounting-adopted) · [Establishing SEEA EA as a global standard — ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S2212041622000092)
- [Beyond GDP — OECD](https://www.oecd.org/en/publications/2018/11/beyond-gdp_g1g98ae6.html) · [Recommendations of the Stiglitz-Sen-Fitoussi Report — INSEE](https://www.insee.fr/en/statistiques/fichier/1372482/ecofra10d.PDF)
- [Why did people stop responding to federal economic surveys? — Brookings](https://www.brookings.edu/articles/why-did-people-stop-responding-to-federal-economic-surveys-what-can-be-done/) · [Administrative data + CPS ASEC nonresponse bias — US Census Bureau (2025)](https://www.census.gov/newsroom/blogs/research-matters/2025/09/administrative-data-nonresponse-bias-cps-asec.html)
- [Why the Census Bureau Chose Differential Privacy (C2020BR-03)](https://www2.census.gov/library/publications/decennial/2020/census-briefs/c2020br-03.pdf) · [Differential privacy and redistricting — Science Advances](https://www.science.org/doi/10.1126/sciadv.abk3283)
- [ONS Working Paper 8 — statistical uses for mobile phone data](https://cy.ons.gov.uk/methodology/methodologicalpublications/generalmethodology/onsworkingpaperseries/onsmethodologyworkingpaperseriesno8statisticalusesformobilephonedataliteraturereview) · [Data Science and Official Statistics — Harvard Data Science Review](https://hdsr.mitpress.mit.edu/pub/1g514ljw/release/4)
- [FAO Handbook on Remote Sensing for Agricultural Statistics](https://openknowledge.fao.org/server/api/core/bitstreams/dcadd248-cccb-43ad-9e3c-7aa0cf2bb577/content) · [FAO Handbook on Crop Statistics](https://openknowledge.fao.org/server/api/core/bitstreams/257243dc-35c7-4f37-b5bc-d05b8088094c/content) · [Integration of remote sensing into NSO sampling designs — SJIAOS 2023](https://doi.org/10.3233/SJI-220116)
- [UN Fundamental Principles of Official Statistics — UNSD](https://unstats.un.org/fpos/) · [FPOS — UNECE](https://unece.org/statistics/FPOS) · [FPOS Maturity Model — SJIAOS](https://content.iospress.com/articles/statistical-journal-of-the-iaos/sji210805)
- [GDPR Art. 5 — principles relating to processing](https://gdpr-info.eu/art-5-gdpr/) · [Reviving Purpose Limitation and Data Minimisation in Data-Driven Systems (arXiv)](https://arxiv.org/pdf/2101.06203)

---

# ROUND 6 (appended) — the two gaps that attack the design

Round 5 ended by naming small-*n* statistics and the empirical harm record as the highest-value next
targets, *because both could change what we build rather than merely extend it*. Both did.

## 6.1 At colony scale, the state mostly cannot publish

**The thresholds.** Official practice guards identity disclosure with a **minimum-count rule of 5 or 10**
per cell. **HIPAA defines a "small geographic area" — elevated re-identification risk — as population
under 20,000.** Our ratified V1 scale is **100–1000**: between **1/20 and 1/100** of that threshold.

Three disclosure types matter, and the second is the one small polities get wrong:

- **identity disclosure** — a cell of 1–2 with a unique characteristic names someone;
- **attribute disclosure** — a **zero cell or a full cell** lets an intruder infer that *nobody* or
  *everybody* in a subgroup has a trait, **without identifying anyone**;
- **inferential disclosure**.

At n=200 the zero-cell problem dominates, which is why the naive fix (suppress small cells) fails: the
suppression pattern is itself informative.

**Computed, not asserted** (illustrative synthetic non-uniform split, threshold 5, counting zero cells as
disclosive):

| Cross-tab | n=200 | n=1000 | n=20 000 |
|---|---|---|---|
| age(5) x role(6) | 17% | 1% | 0% |
| age(5) x role(6) x sex(2) | **84%** | 2% | 0% |
| any x household(40) | **100%** | **100%** | 2% |
| health-status(4) x age(5) | 6% | 1% | 0% |

**Reading:** at colony scale, **one-way tables are fine, two-way tables are marginal, three-way tables are
impossible, and anything keyed to household is impossible even at the top of our scale range.**

**This inverts a common intuition and should be stated plainly.** People assume a small colony is *easier*
to govern with data because it is small enough to know everything about. The opposite is true: **small *n*
means every statistic is an identifier.** A 200-person polity has *less* usable statistical capacity than a
nation, not more — the governor may hold detail it can never publish, and publishing is what makes a
statistic a public good rather than a private advantage (FPOS Principle 1: equal access).

**The available levers, in order of preference:**

1. **Model-based small-area estimation over direct counts.** Statistics Canada's 2025 methodology work
   finds small-area estimates are **inherently less disclosure-risky than direct Horvitz-Thompson
   estimates**, especially at very low sampling rates, because SAE borrows strength from model structure
   rather than reporting raw local counts. This is the single best lever we have.
2. **k-anonymity via generalisation** rather than perturbation for **georeferenced** data — noise-based
   methods cause severe utility damage on spatial data, which matters for both a colony and a farm group.
3. **Coarsen categories before suppressing records.** Suppression loses data, reduces power, and
   **introduces bias if suppressed records differ systematically** from the rest.

**Counterweight, carried honestly:** Domingo-Ferrer and colleagues push back on alarmism — they report
**no successful attacks against properly anonymised national statistical institute releases**, and note
that the famous re-identification attacks targeted data that had only been *pseudonymised*. So the risk is
real but is a function of doing SDC properly, not an argument that publication is hopeless.

## 6.2 The harm record: retention is the control, not access

The empirical literature Round 5 flagged as missing is a single well-developed body of work:
**Seltzer & Anderson, "The Dark Side of Numbers: The Role of Population Data Systems in Human Rights
Abuses," *Social Research* 68(2): 481-513 (Summer 2001)**, with Seltzer's earlier "Population Statistics,
the Holocaust, and the Nuremberg Trials," *Population and Development Review* 24(3): 511ff (1998).

Their thesis: population data systems serve legitimate administrative purposes **and** carry an inherent
dual-use risk, because they permit identification of vulnerable subpopulations — or the definition of
whole populations as outcasts.

**The Netherlands is the paradigm case, and the details are the point.** The Dutch civil registry was
comprehensive and built with **benign intent** — it recorded religion partly to ensure proper burials, and
was designed to support accurate social research. After the 1940 invasion it was captured rapidly and used
to identify Jews and Roma. The comparative outcome: **Dutch Jewish mortality ~73%, against ~40% in Belgium
and ~25% in France.** Punch-card technology supplied the speed. The French *Fichier Juif* was the subject
of a formal government commission (Remond, 1996).

**The generalisable lesson, and it is not the obvious one:**

> **The harm arose not from malicious intent at the moment of collection, but from data persistence under
> changed political circumstances.** The unexpected becomes catastrophic simply because the data is there.

### Why this breaks our drafted clause C27

C27 as drafted reads: *"Data collected for statistical purposes shall never be used in an action against
the person or entity that supplied it."* That is an **access control**. Access controls are enforced by the
regime that holds the data — and the Dutch case is precisely the scenario where **the regime changes and
the control evaporates while the data survives**.

**An access control cannot bind a successor. Only non-existence can.**

### Drafted clauses (for ratification, not self-adopted)

> **C29 — Retention is the control.** Every field in every register shall carry a **mandatory expiry**, and
> shall be **destroyed** on expiry unless a live, ratified decision requires it. A dataset with no expiry
> is a standing offer to a future government the polity has not met.
> *Candidate invariant — mechanically checkable: every register field declares `retention_cycles > 0`;
> a field with no consumer among any department's declared decisions fails validation.*

> **C30 — Sensitive-attribute non-collection.** Fields that identify group membership of a kind
> historically used for persecution (religion, ethnicity, health status, political affiliation) shall not
> be collected **unless** a specific ratified decision requires them, and then only in the coarsest form
> that serves it, with the shortest expiry that serves it.
> *Rationale is empirical, not squeamish: the Dutch registry recorded religion for burial administration.
> The benign purpose is exactly the historical pattern.*

> **C31 — Publication floor.** No statistic shall be published whose cells fall below the ratified
> minimum-count rule, and the polity shall prefer model-based estimates to direct counts wherever both
> are available. *Candidate invariant, mechanically checkable against a published table.*

**C29 is the one I would most want in code**, and it is checkable today with the machinery we have: the
Department Contract already forces every department to declare the state variables it consumes, so a field
consumed by *no* declared decision is detectable — the same shape as `twin.check_state_coverage`, run in
the opposite direction. Call it **coverage-in-reverse**: not "is every declared variable served?" but
**"is every served variable declared by someone?"** A variable the world offers that no department needs
is exactly the unbounded-retention risk C29 targets.

## 6.3 Consequence for the fourth invented-number channel

Our three closed channels were: invented **threshold** (I11), invented **level** (intake G1/G2), invented
**state reading** (twin DT1). Round 6 identifies a fourth, of a different kind — not a fabricated number
but a **retained one**:

> **The invented FUTURE USE.** Data collected for a stated purpose, retained past that purpose, and
> available to a decision nobody ratified. C29 is the structural close; the reverse-coverage check is the
> mechanism.

## Round 6 sources

- [Statistical Disclosure Control Analysis for Small Area Estimation — Statistics Canada (2025)](https://www150.statcan.gc.ca/n1/pub/11-522-x/2025001/article/00015-eng.pdf)
- [A method for managing re-identification risk from small geographic areas in Canada — PMC2858714](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2858714/)
- [FAO Statistical Disclosure Control Protocol](https://openknowledge.fao.org/server/api/core/bitstreams/833ee200-0484-4f87-8f5c-b3fed4a3722b/content)
- [Statistical Disclosure Control: Moving Forward — Domingo-Ferrer, Sanchez & Muralidhar (2025)](https://journals.sagepub.com/doi/10.1177/0282423X241312023)
- [Seltzer & Anderson, The Dark Side of Numbers — PhilPapers record](https://philpapers.org/rec/SELTDS)
- [Statistical Confidentiality and Human Rights — Margo Anderson (UWM)](https://sites.uwm.edu/margo/statistical-confidentiality-and-human-rights/)
- [The Dark Side of Numbers: Updated — Springer](https://link.springer.com/chapter/10.1007/978-3-531-90427-6_7)
- [Dangerous Data: the role of data collection in genocides — The Engine Room](https://www.theengineroom.org/dangerous-data-the-role-of-data-collection-in-genocides/)
