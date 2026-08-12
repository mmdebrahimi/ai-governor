# V14 — Methods and history of governance: what transfers, what doesn't, and what it changes here

> Eight iterative research rounds, 2026-08-11. Weighting as directed: recent cases weighted heavily,
> historical cases retained only where they carry a mechanism still legible today.
>
> **Scope discipline.** This is not a history essay. Every section ends in an *extraction*: something that
> either constrains the AI Governor's design, validates an invariant already built, or contradicts one.
> Sections that produced nothing extractable were cut.
>
> **Evidence-quality warning, stated once and applying throughout.** The "successful example" literature is
> overwhelmingly case-based and selection-prone: countries that adopted a reform and then did well are
> over-represented, and the counterfactual is usually absent. Exactly **one** finding in this entire corpus
> is a clean causal estimate with a plausible identification strategy (Gonçalves 2014, §4.2). Everything
> else is correlational, qualitative, or contested. Treat the *mechanisms* as hypotheses worth testing, not
> as established transferable knowledge.

---

## 1. The finding that dominates all others: the transfer problem

If this memo produced only one result, it would be this one, and it is a direct challenge to the project.

Andrews, Pritchett & Woolcock (*World Development* 51, 2013; and *Looking Like a State*, JDS 2013) name two
mechanisms by which governance reform reliably fails:

| Mechanism | What it is |
|---|---|
| **Isomorphic mimicry** | Adopting the *outward form* of a functioning institution elsewhere to camouflage a persistent lack of function. Governments look better for a period — when laws are newly passed — but never demonstrate higher performance. |
| **Premature load bearing** | Placing unrealistic expectations on a fledgling system, which destroys indigenous learning, the legitimacy of change, and the support of key constituencies. |

Their diagnosis is **capability traps**: state capability stagnates or decays for decades while resources
and legitimacy keep flowing, precisely *because* the mimicry is rewarded.

Their prescription (PDIA) has four principles, and every one of them cuts against a "governance AI" as
naively conceived:

1. Solve **locally nominated and prioritised performance problems** — *instead of* transplanting best practice.
2. Encourage **positive deviance and experimentation** — *instead of* requiring agents implement policy as designed.
3. Create **feedback loops for rapid learning** — *instead of* lagged ex-post evaluation.
4. **Engage many agents** to create viable interventions — *instead of* depending on external experts.

### 1.1 Extraction — the anti-mimicry rail (the sharpest constraint in this memo)

**A system that recommends institutional forms from a catalogue of what worked elsewhere is an
isomorphic-mimicry engine operating at machine speed.** That is not a rhetorical flourish; it is the literal
description of the failure mode, and an AI is better at producing plausible institutional forms than any
consultant, which makes it *better at the failure* too.

The design consequence is concrete and restrictive:

> **The instrument may not propose an institutional form. It proposes a *problem* and a *measurable
> performance gap*, and the humans propose the form.**

This is not a limitation bolted on for safety — it is what the evidence says actually works. It also
re-frames the gap report (anchor §2 Q1) from "a stage on the way to governance advice" to **the
epistemically correct primary output**: a locally-nominated problem plus the measurement gap around it is
*exactly* the PDIA entry point.

Note the pleasant surprise: **the Department Contract already contains the right primitive.** Invariant I6
(falsification test) is the machine-checkable form of "looks reformed vs. performs better." The contract was
built for a different reason and lands on the literature's central distinction.

### 1.2 The evidence caveat on PDIA itself

Honesty rail: PDIA's own evidence base is thin. Andrews describes the original work as "observe, describe and
identify" research; *Building State Capability* (2018) is case-based, not experimental. There is a live
critique that PDIA has itself become a donor buzzword — i.e. susceptible to isomorphic mimicry. **Do not
treat PDIA as a validated method.** Treat the *diagnosis* (mimicry, premature load bearing) as well-evidenced
and the *prescription* as a reasonable prior.

---

## 2. What the state-capacity literature actually establishes

**Evans & Rauch (1999, *ASR* 64(5)), "Weberianness":** an original dataset of core economic agencies across
35 developing countries, 1970–1990. Three traits — (i) meritocratic recruitment, (ii) job stability,
(iii) long-term career rewards — significantly enhance growth, controlling for initial GDP per capita and
human capital.

**The disaggregation matters more than the headline.** Recent micro-level work separates which trait does
what: recruitment *by examination* curbs corruption and clientelistic service provision and raises work
motivation; *job stability* mainly reduces political services (protected bureaucrats are less likely to
support electoral mobilisation). Merit exams improve both bureaucratic and democratic quality; job stability
improves mainly the latter.

**Evans' own qualification — embedded autonomy (1995).** Capacity derives from state–society *relations*,
not from insulation. The association between autonomy and capacity is not always positive; connections
between private sector and public bureaucracy are needed for structural transformation. Cingolani, Thomsson &
de Crombrugghe (*World Development*, 2015) test capacity and autonomy separately and find autonomy in policy
*formulation* acts as a **moderator** — a precondition for Weberian effects to materialise at all.

### 2.1 Extraction

The AI-organ analogue of meritocratic recruitment is **provenance of the objective** — the organ did not
select its own goal, and the goal's origin is auditable. That is invariant **I1**, already implemented and
already the load-bearing one.

The analogue of *embedded* autonomy is the finding that **an insulated organ is not the target state.**
A governance instrument that is maximally independent of the people it advises is, on this evidence, less
effective, not more. This bears directly on anchor §4.8 (all three ratified answers push the first real human
user further out).

---

## 3. Measurement: the state of the art already outputs intervals, not numbers

**V-Dem** (Democracy Report 2026, dataset v16, Coppedge et al. 2026) is the benchmark. Structure worth
copying:

- Five high-level principles measured separately — electoral, liberal, participatory, deliberative,
  egalitarian — rather than one collapsed "democracy" score.
- ~3,500 country experts; 202 countries from 1789; 600+ measured attributes.
- The measurement model (Pemstein et al. 2026) combines expert ratings of *actual and hypothetical*
  countries with experts' **stated uncertainty** and demographics, and produces **best, upper- and
  lower-bound estimates** — explicitly modelling coder error rather than hiding it.

The standing methodological critique of the whole index field: composite indices are rarely constructed with
regard to measurement theory, and a valid index must weight components to approximate the true latent
variable — most don't.

### 3.1 Extraction — a validated architectural choice

The twin's `Estimate` type (value + method + relative error + interval, with `read()` refusing LATENT and
bare-reads of ESTIMATED variables) is **the same discipline the leading governance-measurement project in the
world arrived at independently.** That is a genuine validation of DT1, and it is worth stating plainly because
so little else in this project has external corroboration.

The extension this suggests: **do not collapse to a single score.** V-Dem's five-principle separation exists
because collapsing loses the thing decision-makers need. Any composite the instrument emits must be
decomposable back to its components.

---

## 4. Recent implemented cases, weighted heavily

### 4.1 Estonia — X-Road (1998–present)

Architecturally the most relevant precedent in the entire memo.

- **Not a central database.** A secure data *exchange layer* connecting public and private databases in real
  time. Data flows directly sender→receiver; nothing is stored in a central hub.
- Researchers characterise it as **"minimal centralization"** — interoperability without centralised
  repositories that would threaten privacy or invite misuse. The explicit reading: *technological design
  choices encode governance values.*
- Security servers sign messages over mutually authorised TLS; message logs are timestamped to preserve
  long-term evidential value.
- Scale: 900+ institutions and enterprises, ~233 public-sector bodies, ~1,900 interfaced information
  systems, 3,000+ services; adopted in 25+ countries.
- **The once-only principle is a *legal obligation*, not a technical feature** — citizens supply data once,
  and agencies are legally required to share and reuse it. X-Road merely enables it.

**Caveats.** Estonia had no legacy systems after 1991 — the single biggest confounder for anyone copying it.
And within Estonia, smaller municipalities lack the resources and expertise to participate meaningfully:
**capacity, not connectivity, gates adoption.**

**Extraction.** (a) "Minimal centralization" is the correct architectural posture, and it is the same
principle as retention-as-control (C29 / `check_reverse_coverage`): the strongest control over misuse is
non-existence of the aggregate. (b) The once-only finding is a warning: **the technical layer does not
produce the outcome.** A gap report that identifies what should be shared achieves nothing without the
obligation to share it — which is an authority question, not a code question. (c) The capacity finding maps
onto the unanswered-question problem: the organisations least able to answer the interrogation loop are the
ones the tool would most help.

### 4.2 Brazil — participatory budgeting (the one clean causal result)

Gonçalves (*World Development* 53, 2014, 94–110): panel of all Brazilian municipalities, 1990–2004.
PB-adopting municipalities shifted expenditure toward sanitation and health, matching popular preferences,
with **infant mortality falling by roughly 1–2 per 1,000 births — holding per-capita budgets constant.**
The effect came from *reallocation*, not from more money. Corroborated independently by Touchton & Wampler
(2014); Touchton et al. (2019) find effects on tax collection. As of 2000, 169 of 5,561 municipalities
practised PB, covering ~27% of the population.

**Counter-evidence, which matters as much.** There is now a literature on PB *discontinuation* — factors
associated with abandonment in Brazilian municipalities >50,000 people, 2000–2016. And the broader social
accountability literature finds mixed tangible impacts.

**Extraction.** This is the existence proof the project needs: **changing *who decides the allocation*
produces a measurable welfare outcome with no additional resources.** It is the strongest available argument
that governance machinery is worth building at all. But the discontinuation literature says the gains do not
self-sustain — which makes **institutional persistence a first-class design variable**, not an afterthought.

### 4.3 Taiwan — vTaiwan / Pol.is (2014–present)

The mechanism, precisely:

- **Conversations do not allow replies.** A participant may only agree, disagree, or contribute their own
  statement for others to vote on. This structurally removes the surface for trolling and flaming.
- Echo chambers are replaced by an **attitude map** — you see where you stand relative to others.
- **Consensual statements get more visibility than divisive ones.** Tang: "People compete to bring up the
  most nuanced statements that can win most people across."

Outcomes: core of roughly a dozen laws and regulations (revenge porn, fintech, the Uber consultation — 925
Pol.is voters, 1,875 in the live-streamed consultation, 4,000+ crowdsourcing the agenda). Over 50% of the
population has used the Join platform.

**Limitations, stated by the sources.** vTaiwan is now fully volunteer-based, which limits scope. **Government
is not mandated to consider any consensus reached.** Agencies remain reluctant beyond contested issues.

**Extraction.** The reply-suppression + divisiveness-demotion design is a *mechanism*, not a platform — it is
implementable in the existing intake in an afternoon, and it attacks exactly the failure the polarization
metric currently only *detects*. The intake measures bimodality and fails closed; Pol.is **changes the
incentive so bimodality is less likely to form.** Detection and prevention are complements.

The limitation is the more important half: **a consensus mechanism with no obligation attached is
advisory theatre.** Note this is the same finding as Estonia's once-only principle, arriving from the
opposite direction.

### 4.4 Ireland — citizens' assemblies, and the OECD evidence base

Ireland is the benchmark: four consecutive randomly-selected assemblies, three successful referendums, a
record no other country matches. The 2012 convention was 66 randomly selected citizens plus 33 MPs; later
bodies were entirely citizens selected by lot from the Presidential electoral register.

**The finding that directly tests this project.** A study of the 2016–18 Assembly analysed **over 380,000
spoken words** across expert testimony, Q&A and other agenda items, and found that **expert inputs *structure*
subsequent discussion but do not *dominate* it.** (An incidental finding worth flagging: participants reacted
less strongly to testimony by female experts.)

**OECD (2020) *Catching the Deliberative Wave*:** 289 case studies, 1986–Oct 2019; 12 models of deliberative
process; three routes to institutionalisation; average 90 participants; three core phases — learning,
deliberation, decision. The 11 good-practice principles include, notably:

- a clear, **neutrally-phrased** purpose tied to a well-defined public problem;
- **accountability** — the outcome should influence public decisions, with government at minimum publicly
  responding and preferably acting;
- transparency of design, process, reports **and funding**;
- representativeness — a lottery-selected microcosm, equal chance of selection for everyone.

OECD (2021) *Evaluation Guidelines* add checkable criteria: was the mandate clear and was it clear how
recommendations would be used; was the process connected to the policy cycle; was the question framed
non-leadingly; was it free from external interference.

**Caution from the comparative work** (Pilet et al., *EJPR* 2023, 15 countries): assemblies have potential to
re-engage the disenfranchised, but their supporters are not yet motivated by the institution itself.

**Extraction.** Three things. (a) The OECD principles and evaluation criteria are a **ready-made,
internationally-vetted, largely checkable specification** for the guideline-intake process this project
already built — adopt them rather than inventing a bar. (b) The 380,000-word expert study is the **empirical
falsification test for the entire advisory posture**: "does the AI's analysis dominate the panel?" is
measurable, has been measured for human experts, and found not to dominate. That is a real, runnable
experiment for this project and should be the acceptance test for the advisory claim. (c) "Neutrally-phrased
purpose" and "non-leading question framing" are precisely what an AI generating the interrogation questions
would be worst at — and there is now a published evaluation standard to test against.

### 4.5 The Netherlands — water boards (13th century → present)

Included despite age because the mechanism is intact and directly transferable to the first instance.

- Local self-organisation by farmers and landowners against flooding; institutionalised as *waterschappen*;
  Rijnland's commission dates to 1248.
- Three design pillars per the Dutch Water Authorities' own framing: **democratic legitimacy**, **financial
  independence** (guaranteed by the right to levy local taxes), and **adequate capacity**.
- **Functional, single-purpose jurisdiction** — boundaries drawn *hydrologically*, not politically. 21 boards
  operate as independent layers of government with statutory powers equivalent to municipalities.
- **Beneficiary-pays**: those protected fund the protection, which sustains willingness to be governed.

**Two honest caveats.** The "oldest democratic institution" claim is contested in the scholarly literature.
And on IJsselmonde — a small island — water management ran through **31 local jurisdictions and ~65 polders**;
the study's own subtitle pairs "adaptation" with **"petrification."** Polycentric systems ossify as readily
as they adapt.

**Extraction — the most usable institutional template in the memo for a multi-country land enterprise:**
a governance body scoped to *one* physical problem domain, with boundaries drawn by the physical system
rather than by ownership or politics, funded by those it benefits, with representation weighted by stake.
Plus the failure mode to instrument against from day one: **fragmentation that outlives its usefulness.**

### 4.6 Agricultural cooperatives — Netherlands and Denmark

Cooperatives exceed 50% agricultural market share in Austria, Denmark, Finland, France, Ireland, the
Netherlands and Sweden.

**Netherlands (Bijman).** The key external factor is enabling legislation that **"poses few but clear rules"**
on structure and operation — leaving room for governance innovation as cooperatives grew into
multi-billion-revenue international companies while preserving effective member control. Socio-cultural
precondition: the polder tradition of self-organisation and decentralised government.

**Denmark.** Emphasis falls on social infrastructure rather than legal design — social capital, cohesion,
education, trust, infrastructure access. Also the honest note that **cooperative ownership can itself become
a limitation** in some circumstances.

**The most transferable finding, and the one that needs careful handling: membership homogeneity.** Across
both literatures, the less heterogeneous the membership, the lower the **influence-cost** problem.
Heterogeneity arises from farm size and cost structure, product type, and members' personal characteristics —
age, risk aversion, preferences — and it directly generates governance problems through information asymmetry.

> **Framing correction, made explicitly.** This finding does **not** say heterogeneity is bad or that
> differing horizons are a defect. It says heterogeneity **raises influence costs**, and that governance
> machinery must be sized to the influence costs actually present. Under permanent capital, holding assets
> across a 40-year and a 2-year horizon is a thesis, not a compromise — and the cooperative literature's
> own answer is *more capable governance*, not less heterogeneity. Influence cost is a measurable design
> parameter, not a verdict.

**The emerging frontier, and a precise structural precedent.** In 2016 the Netherlands delegated coordination
and distribution of state agri-environmental subsidies to **"agricultural collectives"** — farmers and
landowners organised as publicly certified conservation organisations. **Forty region-based collectives now
cover the entire Dutch countryside, each with its own governing board elected by participating farmers.**
Theoretically this is a multi-layered arrangement of *nested sets of institutions*.

**Extraction.** (a) "Few but clear rules, room for internal innovation" is the correct shape for the
department contract itself — and is what it already does. (b) Influence cost is a **derivable measure** from
member characteristics the enterprise already knows, and is a strong candidate for the first thing the
instrument actually computes. (c) The 40-collective model is a working, certified, elected-board precedent
for exactly the multi-site land-governance problem in scope.

---

## 5. The failure cases, which carry the hard design constraints

### 5.1 The Dutch childcare benefits scandal (*toeslagenaffaire*) — the single most important negative case

**What happened.** Between 2005 and 2019, ~26,000 parents were wrongly accused of fraudulent childcare
benefit claims and ordered to repay in full — typically **€20,000–€60,000**, with late fees, no payment
arrangements. Families were driven into debt; children were placed into foster care. In January 2021 the
Rutte cabinet **resigned** over infringement of the fundamental rights of an estimated 35,000 recipients.

**The mechanism, in detail, because every element recurs in any governance AI:**

1. By 2011 the tax administration had built an **AI-based risk-classification model** to check claims at
   scale, trained on examples of correct and incorrect applications.
2. **Citizenship was one of the fraud indicators.** Applicants of foreign origin were selected for detailed
   screening; dual nationality flagged people as likely fraudsters.
3. The system was **modelled on a past fraud case**, so anyone bearing even slight resemblance to that
   profile was treated as a potential criminal.
4. There were **no meaningful avenues for dispute resolution.**

**The accountability finding, which is the transferable one.** Automation **erodes internal accountability**:
deference to an algorithm weakens internal challenge by attributing the decision to a less-explainable
machine. The tax authority survived partly because it had "the luxury of political accountability" — an
agency without that would suffer more lasting legitimacy damage.

**Extraction — a new invariant, drafted.** This case is the empirical backing for anchor decision D19
(family/succession governance is the *highest*-risk application, not the safest). It yields a concrete
requirement the contract does not currently encode:

> **Candidate invariant I12 — redress.** Any instrument output that *classifies a person* must carry
> (a) a named accountable human, (b) a redress route that does not require the subject to disprove the
> model, and (c) a prohibition on the system's output being cited as the *justification* for the decision.

And a second, from mechanism (3):

> **Candidate invariant I13 — no profile-by-resemblance.** A classification may not be derived from
> similarity to a prior adverse case. This is a distinct failure from a wrong threshold: it is the
> *meaning* channel (anchor §"fifth invented-something channel") producing a category nobody authorised.

### 5.2 Targets and gaming — Bevan & Hood, and the direct threat to the derivation chain

Bevan & Hood (*Public Administration* 84, 2006, 517–538) on the English NHS star ratings: a single 0–3 score
per trust, derived from ~50 targets, enforced by "naming and shaming" with zero-rated chief executives at
risk of their jobs. The authors describe governance by targets as combining targets with **"an element of
terror,"** drawing an explicit parallel to the Soviet regime, and identify the underlying error as
**synecdoche** — taking a part to stand for the whole.

**Effects ran in both directions, and honesty requires both.** On the four-hour A&E target, patients waiting
over four hours fell from 23% (2002, pre-target) to 5.3% (2004); waiting times fell in England while rising
in Wales. *And* hospitals and ambulance services gamed the ratings; in 2005, to meet a target that 100% of
patients be offered a GP appointment within two working days, many GPs **stopped booking appointments more
than two or three days ahead.**

**Hood's taxonomy gives two named, checkable gaming shapes:**

| Shape | Definition |
|---|---|
| **Ratchet effect** | Managers curtail performance *below potential* to be sure of meeting incrementally rising future targets. |
| **Threshold effect** | Uniform targets don't elicit excellence from top performers and may incentivise reducing performance to *just* meet the standard. |

Hood extends this to **"creative categorization"** — meso-level gaming on the *input* side, by reclassifying
units of spending.

Goodhart's law proper: once an indicator is made a target it loses the information content that qualified it
for the role. The familiar aphorism form is Strathern's (1997), on audit in British universities.

**Extraction — a concrete change to code that already exists.** V13's purpose→data rule derives statistics
from decisions. Goodhart says that the moment a derived statistic becomes a target, it degrades. The
Department Contract already has **I4 (gaming model)** — but I4 attaches to *instruments*. It must extend to
**derived measures**, and the ratchet/threshold pair makes it partly checkable rather than free text:

> **I4′ — every derived measure declares its gaming model, and specifically whether it is exposed to the
> ratchet effect (is the target incrementally rising?) and the threshold effect (is the target uniform
> across heterogeneous units?).**

Both questions are answerable from the measure's own definition, which makes this implementable now.

### 5.3 Decentralization — the qualification of I8 (subsidiarity)

Bardhan & Mookherjee (*Economic Journal* 116(508), 2006; and the relative-capture framework, 1999) model
devolution where the centre is uninformed and cannot monitor allocation. Central bureaucrats act as monopoly
providers charging bribes, causing underprovision especially for the poor; local governments are directly
responsive but may be captured by elites.

**The finding that matters most here — a measurement trap.** Decentralization may change the **form** of rent
extraction rather than eliminate it: bribes charged by central bureaucrats are replaced by **elite capture of
local government**, appearing as regressive cross-subsidies hidden in government finances. So **corruption
measures based on bribes fall while efficiency and equity decline.** The metric improves as the outcome worsens.

**West Bengal evidence (89 village governments, 1978–98)** is more nuanced than the standard capture story:
poverty, land inequality and low-caste composition had negligible adverse effects on targeting of private
goods *within* villages, but were associated with lower employment generation and significantly lower
resource allocation *to the village as a whole*. **Capture operated at the inter-village allocation tier,
not the intra-village one.**

The authors' own conclusion: neither empirical studies nor their theory yields general conclusions about
which level of government is more vulnerable to capture.

**Extraction.** I8 currently encodes: `Legitimacy.LOW` ⇒ no `QUANTITY_ALLOCATION`. That shape — a
*prohibition* — survives this evidence. What does **not** survive is any reverse implication that devolution
is good where legitimacy is adequate. Two additions:

> **I8 qualification.** A subsidiarity recommendation must name **the tier at which discretion actually
> sits** (the West Bengal finding is that this matters more than devolution per se) and must carry a
> **capture check at that tier**.
>
> **And a general rail from the measurement trap:** a proposed change that improves the *measured* value of
> a corruption/efficiency proxy while the underlying welfare quantity is unobserved must be flagged, not
> recommended. This is the twin's LATENT refusal applied to policy evaluation.

### 5.4 Fiscal rules and councils — the endogeneity trap, which applies to this whole project

Fiscal rules correlate with stronger fiscal performance across three decades and a broad cross-section
(IMF). Fiscal councils are technical, nonpartisan watchdogs in varied forms — parliamentary budget offices
(Canada, Italy, US), supreme audit offices (France, Finland), independent entities attached to the executive
(Belgium, Croatia). The IMF frames them as **complements, not substitutes**: rules give councils a clear
metric to leverage; councils magnify the reputational cost of breaching rules. More independent councils
correlate with smaller deficits and better compliance.

**The IEO's caveats are the important part, and they are pointed:**

- Councils are effective **only if policymakers have already internalised the merits of fiscal discipline** —
  raising the possibility that the council's presence merely *captures* that internalisation.
- They work only with a critical mass of expertise and resources — so the approach **is least effective
  where it is most needed** (low-income countries).
- Compliance remains a problem: deviations from deficit and debt limits are widespread and persistent.

**Extraction — an honest prior about what this project can achieve.** The closest institutional analogue to
"an advisory body that analyses and recommends but does not decide" is the independent fiscal council, and
the best available evidence on it says: *it works where the will already exists, and its measured effect may
be largely selection.* This should be stated in the anchor's assumptions rather than discovered later. It
also sharpens the strongest argument for the gap report: a gap report creates a **reputational cost for not
knowing**, which is the mechanism the IMF credits councils with — magnifying the cost of breach — rather
than depending on advice being taken.

### 5.5 Anti-corruption — and the incremental/big-bang fork

**What worked, where it worked.** Hong Kong's ICAC (1974) came from scandal, not planning: senior officer
Peter Godber fled with unexplained millions in 1973; public fury forced creation of a body reporting directly
to the Governor and insulated from the police. Three-pronged design — operations, corruption *prevention*,
and community relations. Singapore's CPIB (1952, the world's first such agency) reports directly to the PM,
can arrest without warrant and access financial records regardless of seniority, and can investigate the
Prime Minister.

**What the comparative evidence says.** Singapore and Hong Kong succeeded through strong political will and
single well-resourced "Type A" agencies; China, India and the Philippines failed with weak will and multiple
under-resourced "Type B" agencies (per-capita expenditure and staff-population ratios serve as measurable
proxies for "political will"). A competing emphasis: establishing an agency alone is unlikely to succeed
without a base of social trust and participation. The imitation record is poor — Thailand's 1975 commission
was ineffective and had to be replaced in 1999.

**The fork.** Rothstein (*RIPE* 18(2), 2011) argues the good-governance regime's incrementalism is
*dysfunctional*: corruption is a **collective action** problem, not a principal-agent problem, because under
systemic corruption **there are no "principled principals."** Small institutional devices cannot start a
virtuous circle and may create a social trap. His advice: **if you have few resources, save them until you
can muster a big-bang change — otherwise the anti-corruption bodies you install are seen as supporting
corruption.** Georgia post-2003 is the standard illustration (124th of 133 on the 2003 CPI; on the Global
Corruption Barometer, 69% expected corruption to rise in 2004, 11% a year later).

**Counter-evidence:** the EBA's *Anti-Corruption Reform — Evolution or Big Bang?* (2016) weighs this against
Teorell & Rothstein's own "Getting to Sweden" work, where change looks gradual. And the Basel Institute's
Georgia report notes the radical reforms occurred 2004–08 when the state–business nexus was weak; during
2008–12 ruling elites rebuilt links to private interests.

**Extraction — a required capability the design does not have.** Any advisory instrument defaults to
incremental recommendations, because incremental recommendations are what advice looks like. Rothstein's
claim is that in a self-reinforcing bad equilibrium, **incremental advice is actively harmful.** So:

> **Candidate invariant I14 — equilibrium check.** Before emitting an incremental recommendation, the
> instrument must assess whether the system is in a self-reinforcing equilibrium in which incremental change
> is counterproductive; if it is, the instrument must be able to output **"no incremental recommendation is
> safe here"** rather than a smaller version of the same advice.

This is a fail-closed shape the project already knows how to build — the same shape as the intake refusing to
average a polarized panel.

---

## 6. Geostrategy: what actually has predictive power

The institutionalist frame (Acemoglu & Robinson) holds that countries rise and fall on institutions rather
than culture, geography or chance; *The Narrow Corridor* (2019) adds that liberty sits in a narrow corridor
held open only by incessant struggle between state and society.

**The critiques are substantive and worth carrying:**

- **Predictive failure.** A&R predicted China would follow the Soviet path, exhausting its economic success
  before becoming politically inclusive. Reviewers call this simplistic, and argue growth is also shaped by
  geopolitics, technological discovery and natural resources — systematically downweighted in the quest to
  prove institutions primary.
- **Category breadth (Dixit).** The theory's categories are too broadly defined and essential interactions
  within and across them are relegated to the margins.
- **Political settlements (Mushtaq Khan).** The deepest challenge: A&R's argument implicitly rests on why
  some organisations are more powerful than others, which is not generally true. Khan puts **the distribution
  of power prior to formal rules** — a more inclusive political *settlement* is more likely to be stable and
  thus permit development, regardless of the formal institutional form.

**Botswana** is the standing test case, and it does not resolve cleanly. Independent 1966, ~83% in poverty in
1985, then among the fastest-growing economies on diamond revenue. The institutionalist reading credits
pre-existing institutional quality; critics argue institutional quality at the critical juncture was *not*
sufficient, and that **political coalitions lay the foundation for institutional development** rather than
the reverse — Botswana kept Dutch Disease in check *despite* fragile state institutions. Botswana and
Mauritius are nearly alone in achieving NIC-rivalling growth while remaining democratic.

The standard resource-curse prescriptions — macro policy, diversification, natural resource funds,
transparency, direct distribution — have had limited success because they **presuppose the strong state
institutions that are absent.**

### 6.1 Extraction

Khan's ordering is the one to adopt: **the distribution of power is prior to the formal rules.** For the
instrument this is not abstract. It means that a recommendation expressed as a *rule* ("adopt this
allocation procedure") is under-specified unless it also names **who currently holds the power the rule would
redistribute, and whether they can block it.** A governance AI that models rules but not power is modelling
the part of the system that is downstream of the part that decides.

This is also the second independent route to the anti-mimicry conclusion in §1: prescriptions that
presuppose the capacity they are meant to create are exactly isomorphic mimicry.

---

## 7. AI in government: the evaluation gap

The OECD's *Digital Government Outlook 2026* states plainly that despite proliferating governance tooling, a
**mismatch persists between decision-making and evidence** — agencies deploy faster than they measure.

Ex-ante machinery is mature; ex-post evaluation is nearly absent:

| Instrument | Status |
|---|---|
| Canada — **Algorithmic Impact Assessment** | Mandatory, completed **before** deployment, **results published openly** (Directive on Automated Decision Making) |
| UK — **Algorithmic Transparency Recording Standard** | Departments publish records of algorithmic tools in decision-making |
| Australia — **AI Assurance Framework** | Piloted with 21 volunteer agencies, Sept–Nov 2024 |
| UK — **Guidance on the Impact Evaluation of AI Interventions** (2024, updated Jul 2025) | The **only** counterfactual-evaluation methodology found; adapts the Treasury Magenta Book |

The OECD Trust Survey found **public resistance is a potential challenge in almost half of use cases
reviewed** — shaped in part by prior high-profile algorithmic failures (i.e. §5.1).

**Extraction.** (a) There is **no outcome benchmark to beat**, which is both the opportunity and the reason
to keep claims modest — nobody has demonstrated measured outcome value from government AI at scale. (b)
Canada's published AIA is a **directly reusable artifact shape for the gap report**: a structured, public,
pre-deployment assessment is very close to what the gap report already wants to be. (c) The near-total
absence of ex-post evaluation means the falsification tests this project builds (I6) would be, on this
evidence, unusually rigorous for the field — worth noting, and worth not overclaiming.

---

## 8. What this changes — the actionable list

Ordered by how much they change the build.

| # | Change | Source | Status |
|---|---|---|---|
| **1** | **Anti-mimicry rail** — the instrument proposes a *problem + measurable performance gap*, never an institutional *form*. This kills "induce an ontology from a catalogue of governance patterns." | §1 PDIA, §6 Khan | **New, and the biggest** |
| **2** | **I4′** — extend the gaming model from instruments to **derived measures**, with ratchet and threshold as checkable sub-questions | §5.2 Bevan & Hood, Hood | **Implementable now** |
| **3** | **I12 redress** — any output classifying a person carries a named accountable human, a redress route not requiring the subject to disprove the model, and a bar on citing the system as justification | §5.1 toeslagenaffaire | **New invariant, drafted** |
| **4** | **I13 no-profile-by-resemblance** — no classification derived from similarity to a prior adverse case | §5.1 | **New invariant, drafted** |
| **5** | **I14 equilibrium check** — must be able to emit "no incremental recommendation is safe here" | §5.5 Rothstein | **New invariant, drafted** |
| **6** | **I8 qualification** — a subsidiarity recommendation names the tier where discretion sits + a capture check at that tier; and flag any change that improves a proxy while the welfare quantity is unobserved | §5.3 Bardhan & Mookherjee | **Amendment to shipped code** |
| **7** | Adopt **OECD deliberative good-practice + evaluation criteria** as the intake bar rather than inventing one | §4.4 | **Substitution, cheap** |
| **8** | Adopt the **380,000-word expert-dominance study** as the acceptance test for the advisory claim | §4.4 | **Falsification test, runnable** |
| **9** | Add **Pol.is-style reply-suppression + divisiveness-demotion** to the intake — prevention alongside the existing detection | §4.3 | **Implementable now** |
| **10** | **Influence cost** as the first derived measure for the land enterprise — computable from member characteristics already known | §4.6 | **Candidate first product** |
| **11** | Record the **fiscal-council endogeneity prior** in the anchor's assumptions: advisory bodies work where the will already exists | §5.4 | **Honesty, anchor edit** |
| **12** | Do **not** collapse composites to a single score — V-Dem separates five principles for a reason | §3 | **Design rule** |

### 8.1 What this *validates* (no change needed)

- **I1 objective provenance** ≈ meritocratic recruitment, the trait with the strongest evidence (§2).
- **I6 falsification test** is the machine-checkable form of the mimicry/performance distinction (§1.1).
- **DT1 `Estimate` with method + error bar** matches V-Dem's measurement model independently (§3.1).
- **C29 / `check_reverse_coverage`** ≈ X-Road's "minimal centralization" (§4.1).
- **Fail-closed intake on a polarized panel** is the same shape I14 needs (§5.5).

---

## 9. The internal contradiction this research surfaces

Stated plainly because it argues against something already written.

**V13's four-layer architecture (registers → accounts → indicators → real-time) is a legibility
architecture.** Three independent literatures converge on the danger: PDIA (§1) says transplanted form
without function is the standard failure; Bardhan & Mookherjee (§5.3) say greater legibility enables capture
at whichever tier holds discretion; Goodhart/Bevan-Hood (§5.2) say measures degrade once they are targets.

The purpose→data rule was V13's control for exactly this. But **layers 1–2 (registers, accounts) are
foundational by construction — they are built *before* the decisions that would justify them.** That is
precisely the derivation the purpose→data rule forbids. The rule and the architecture are in tension, and
V13 did not notice.

Two candidate resolutions, neither yet chosen:

- **(a) Registers are decision-derived too** — build only the register fields some declared decision needs,
  accepting that the register will be incomplete and will grow. Consistent with the rule; expensive and
  slower; risks a register too partial to be useful.
- **(b) Registers are exempt but retention-bounded** — accept that a register is infrastructure, and control
  the risk on the *retention* axis instead (C29, reverse coverage) rather than the derivation axis.

**(b) looks right and is what the shipped code already implies**, but it should be a recorded decision rather
than an accident of implementation order — and it means the purpose→data rule needs an explicit stated
exception rather than remaining an absolute that the architecture quietly violates.

---

## 10. Judgement: why eight rounds was enough

Rounds 7–8 (anti-corruption, decentralization, family governance, big-bang) **reinforced** constraints
already surfaced in rounds 1–6 rather than producing new ones — the convergence signal. Specifically, the
anti-mimicry finding (§1) arrived independently a second time via Khan's political settlements (§6) and a
third time via the resource-curse prescription critique (§6), which is the point at which further rounds buy
restatement rather than information.

**Named residual gaps, not covered and deliberately so:**

- **Constitutional design proper** (presidential vs parliamentary, electoral system choice) — out of scope
  for an administrative organ that is barred from proposing forms (§1.1).
- **China's governance system**, which is the largest recent case by population and the one most often
  claimed as a counter-model. Excluded because the evidence quality on internal mechanism is poor and the
  transferability question is dominated by regime-type factors the instrument cannot condition on.
- **Rigorous impact evaluation of PDIA** — searched, not found, and flagged as a real weakness in §1.2.
- **Sunset clauses and ex-post regulatory review** — searched via the fiscal-rules corpus and absent there;
  the literature sits in regulatory-governance/administrative law and would need its own round if the
  charter's sunset invariant (I7) is to be evidence-grounded rather than reasoned.

---

## Sources

**Measurement + state capacity**
- [V-Dem Democracy Report 2026](https://www.v-dem.net/documents/75/V-Dem_Institute_Democracy_Report_2026_lowres.pdf) · [V-Dem Institute](https://www.v-dem.net/) · [Structure of V-Dem indices](https://v-dem.net/documents/57/structureofaggregation.pdf)
- [Evans & Rauch, "Bureaucracy and Growth," *ASR* 64(5), 1999](https://journals.sagepub.com/doi/10.1177/000312249906400508) · [Cingolani et al., "Minding Weber More Than Ever?", *World Development* 2015](https://www.sciencedirect.com/science/article/abs/pii/S0305750X15000492)

**Transfer problem**
- [Andrews, Pritchett & Woolcock, "Escaping Capability Traps through PDIA," *World Development* 51, 2013](https://www.sciencedirect.com/science/article/abs/pii/S0305750X13001320) · [HKS working-paper PDF](https://www.hks.harvard.edu/sites/default/files/centers/cid/files/publications/faculty-working-papers/240_Andrews,+Pritchett,+Woolcock_BeyondCapabilityTraps_PDIA_FINAL.pdf) · [Pritchett, Woolcock & Andrews, "Looking Like a State," *JDS* 49(1), 2013](https://ideas.repec.org/a/taf/jdevst/v49y2013i1p1-18.html)

**Implemented cases**
- [Estonia X-Road (e-Estonia)](https://e-estonia.com/solutions/interoperability-services/x-road/) · [Estonia's experience for European data spaces, *ScienceDirect* 2025](https://www.sciencedirect.com/science/article/pii/S2352340925010753)
- [Gonçalves, "Participatory Budgeting … Infant Mortality in Brazil," *World Development* 53, 2014](https://www.sciencedirect.com/science/article/abs/pii/S0305750X13000156) · [IPD Columbia copy](https://ipdcolumbia.org/publication/the-effects-of-participatory-budgeting-on-municipal-expenditures-and-infant-mortality-in-brazil/)
- [vTaiwan (CrowdLaw for Congress)](https://congress.crowd.law/case-vtaiwan.html) · [RadicalxChange, *Taiwan: Grassroots Digital Democracy That Works*](https://www.radicalxchange.org/updates/papers/Taiwan_Grassroots_Digital_Democracy_That_Works_V1_DIGITAL_.pdf) · [Computational Democracy Project case studies](https://compdemocracy.org/case-studies/)
- [OECD, *Innovative Citizen Participation and New Democratic Institutions* (Catching the Deliberative Wave)](https://www.oecd.org/en/publications/innovative-citizen-participation-and-new-democratic-institutions_339306da-en.html) · [OECD Good Practice Principles](https://www.oecd.org/content/dam/oecd/en/topics/policy-issue-focus/innovative-citizen-participation/good-practice-principles-for-deliberative-processes-for-public-decision-making.pdf) · [OECD Evaluation Guidelines (2021)](https://www.oecd.org/en/publications/evaluation-guidelines-for-representative-deliberative-processes_10ccbfcb-en.html) · [Reactions to experts in the 2016–18 Irish Citizens' Assembly](https://www.tandfonline.com/doi/full/10.1080/07907184.2023.2211014) · [Pilet et al., *EJPR* 2023, 15 countries](https://ejpr.onlinelibrary.wiley.com/doi/10.1111/1475-6765.12541)
- [Dutch Water Authority model (Dutch Water Authorities)](https://dutchwaterauthorities.com/wp-content/uploads/2021/05/The-Dutch-water-authority-model.pdf) · [Huygens Institute, *The polder model: political culture in water boards c.1200–c.1800*](https://www.huygens.knaw.nl/en/projecten/het-poldermodel-politieke-cultuur-in-de-waterschappen-ca-1200-ca-1800/)
- [Bijman, *Agricultural Cooperatives in the Netherlands: Key Success Factors*](https://www.researchgate.net/publication/308993047_Agricultural_Cooperatives_in_the_Netherlands_Key_Success_Factors) · [Candemir et al., *Journal of Economic Surveys* 2021](https://onlinelibrary.wiley.com/doi/10.1111/joes.12417) · [Collaborative agri-environmental governance in the Netherlands, *Ecology & Society* 28(1)](https://ecologyandsociety.org/vol28/iss1/art28/)

**Failure cases**
- [Dutch childcare benefits scandal (overview)](https://en.wikipedia.org/wiki/Dutch_childcare_benefits_scandal) · [Hadwick & Lan, *Lessons to Be Learned from the Dutch Childcare Allowance Scandal*, SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4282704) · [The Dutch benefits scandal: a cautionary tale for algorithmic enforcement](https://eulawenforcement.com/?p=7941)
- [Bevan & Hood, "What's Measured Is What Matters," *Public Administration* 84, 2006](https://www.semanticscholar.org/paper/What's-measured-is-what-matters:-targets-and-gaming-Bevan-Hood/e98f90e166542a9b0ec5171f641a30b48cd09884) · [Bevan, "Setting Targets for Health Care Performance," *NIER* 2006](https://journals.sagepub.com/doi/10.1177/002795010619700102) · [Hood, "Goodhart's Law and the Gaming of UK Public Spending Numbers," *PPMR* 44(2)](https://www.tandfonline.com/doi/abs/10.1080/15309576.2020.1749092)
- [Bardhan & Mookherjee, "Decentralisation and Accountability in Infrastructure Delivery," *Economic Journal* 116(508), 2006](https://academic.oup.com/ej/article-abstract/116/508/101/5089395) · [author PDF](https://people.bu.edu/dilipm/ec722/papers/BardhanMook2006EcJ.pdf) · [Pro-poor targeting in West Bengal, *JDE*](https://www.sciencedirect.com/science/article/abs/pii/S0304387806000058)
- [IMF, *Second-Generation Fiscal Rules* (SDN/18/04)](https://www.imf.org/external/datamapper/fiscalrules/sdn1804-on-second-generation-fiscal-rules.pdf) · [IMF WP 2025/198, *Fiscal Rules and Fiscal Councils*](https://www.imf.org/-/media/files/publications/wp/2025/english/wpiea2025198-source-pdf.pdf) · [IEO, *The IMF's Advice on Fiscal Rules and Institutions* (2025)](https://ieo.imf.org/en/-/media/ieo/files/evaluations/completed/12-16-2025-imf-advice-on-fiscal-policy/fp-bp4-chapter-2-the-imfs-advice-on-fiscal-rules-and-institutions.pdf)
- [Rothstein, "Anti-corruption: the indirect 'big bang' approach," *RIPE* 18(2), 2011](https://www.tandfonline.com/doi/abs/10.1080/09692291003607834) · [2007 working paper](https://www.gu.se/sites/default/files/2020-05/2007_3_Rothstein.pdf) · [EBA, *Anti-Corruption Reform — Evolution or Big Bang?* (2016)](https://eba.se/app/uploads/2016/12/2016_08_webb_Tillganp.pdf) · [Basel Institute, Georgia country report](https://baselgovernance.org/sites/default/files/2019-04/georgia.informalgovernance.country_report.pdf) · [*Combating Corruption in Asian Countries*, Daedalus 147(3)](https://direct.mit.edu/daed/article/147/3/202/27206/Combating-Corruption-in-Asian-Countries-Learning) · [It takes a whole society: Hong Kong's ICAC](https://www.emerald.com/pap/article/25/2/109/317430/It-takes-a-whole-society-why-Hong-Kong-s-ICAC)

**Geostrategy**
- [Khan, "Political Settlements and the Analysis of Institutions," *African Affairs*](https://academic.oup.com/DocumentLibrary/afraf/Political%20Settlements%20virtual%20issue%20Intro%20article,%20Mushtaq%20Khan.pdf) · [Dixit, review of *The Narrow Corridor*](https://www.princeton.edu/~dixitak/home/CorridorReviewFinal.pdf) · [*Foreign Affairs*, "Government, Geography, and Growth"](https://www.foreignaffairs.com/reviews/why-nations-fail-daron-acemoglu-james-robinson) · [Poteete, "Is Development Path Dependent or Political?", *JDS* 45(4)](https://www.tandfonline.com/doi/abs/10.1080/00220380802265488)

**Industrial policy + AI in government**
- [Juhász, Lane & Rodrik, "The New Economics of Industrial Policy," *Annual Review of Economics* 16, 2024](https://www.annualreviews.org/content/journals/10.1146/annurev-economics-081023-024638) · [ungated PDF](https://drodrik.scholars.harvard.edu/sites/g/files/omnuum7106/files/annurev-economics-081023-0246380-final.pdf)
- [OECD, *Digital Government Outlook 2026* — Adopting and governing AI in government](https://www.oecd.org/en/publications/digital-government-outlook_0496b2bc-en/full-report/adopting-and-governing-ai-in-government_7ef312a9.html) · [OECD Trust Survey 2026 — Trustworthy AI in the public sector](https://www.oecd.org/en/publications/oecd-survey-on-drivers-of-trust-in-public-institutions-2026-results_9eb63fec-en/full-report/trustworthy-artificial-intelligence-in-the-public-sector_6f98c91a.html)
