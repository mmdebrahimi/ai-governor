# AI Government — Constitutionally-Bounded AI Governor for a Mars Colony
<!-- project-schema: 0.1 -->

> Initialized 2026-08-11. Project ID: aigov. Originating goal (verbatim user input): "Build an AI Government: a constitutionally-bounded AI Governor runtime plus a set of pluggable departments that converts democratically-ratified general guidelines into a running, auditable institutional framework for a Mars colony (electorate 100-1000), designed and TESTED in simulation before any colony exists. Phase-1 terminal: the kernel runs >=12 decision cycles across >=3 departments spanning all three central-legitimacy ratings on a colony digital twin, where every binding action is (ratified AND certified-non-steering AND constraint-satisfying) or fail-closed escalated, under an adversarial suite, reproducibly via pytest. Reuses the existing Mars_Governance collective-choice organ (193 passing tests). Scale-out to city/nation/world is an explicit non-goal of phase 1."

## Project Context
- **Project ID:** aigov
- **Project root:** C:\Users\Farshad\PythonProjects\Skill_Development\AI_Governor
- **Captured:** 2026-08-11
- **Originating goal:** (see verbatim above)
- **Refined goal (if 3c produced one):** Build and validate in simulation a constitutionally-bounded AI Governor kernel plus a Department Contract, such that on a colony digital twin at electorate 100–1000 the kernel executes ≥12 decision cycles across ≥3 departments spanning all three central-legitimacy ratings (HIGH/MEDIUM/LOW), where every binding action is either (ratified ∧ certified-non-steering ∧ constraint-satisfying) or fail-closed escalated, under a named adversarial suite, reproducibly via pytest. The user's broader ambition (colony → city → nation → world) is retained in Project Context as an open-ended research program, NOT as this ledger's terminal.
- **Role:** UMBRELLA ledger (Soraya decompose, 2026-08-11) — see ## Project Families / ## Requirements Flow-down / ## Mission Terminal Condition.
- **Horizon (months):** 12
- **Schema:** project-schema 0.1
- **User-facing framing docs:** `docs/idea-anchor-DRAFT-2026-08-11.md` (3 forks AWAITING RATIFICATION), `docs/foundations-canon-map.md`, `docs/department-ontology.md`, `docs/decomposition-flowdown.md`

## Empirical Concerns
- **Verdict:** PASS
- **Check status:** attempted
- **Provisional:** NO
- **Findings:** (1) The goal's one directly checkable factual claim — "Mars_Governance ... 193 passing tests" — was VERIFIED by direct execution on 2026-08-11 (`python -m pytest tests/ -q` → `193 passed in 27.14s`), not by recall. (2) WebSearch confirmed the Gibbard–Satterthwaite statement as used in the framing: an onto, non-dictatorial, deterministic social choice function over ≥3 alternatives under unrestricted domain is manipulable (Gibbard 1973 Econometrica 41:587–600; Satterthwaite 1975 JET 10:187–217). The goal's framing does NOT contradict it: because the AI is scoped as advisory + every binding action must be ratified, the goal never asserts a strategy-proof or welfare-optimal mechanism. Search also surfaced a common conflation of G–S with Arrow's IIA/unanimity conditions — recorded so it does not propagate. (3) NO factual error detected in the goal. The load-bearing UNPROVEN item is not empirical but assumptional: that democratic guidelines can be compiled into machine-binding constraints (tracked as H1, not as an empirical defect). (4) Remaining canon claims in `docs/foundations-canon-map.md` are DISCOVERY-TIER model recall and are queued for audit-tier promotion as V1–V12 in family `aigov-foundations`.

## Project vs Research-Program
- **Verdict:** FAIL
- **Provisional:** NO
- **Classification:** hybrid
- **Rationale:** BOUNDED components (testable inside 12 months, all with measurable criteria): the Department Contract + validator invariants, the constitutional charter's machine-checkable clauses, the colony digital twin, the governor kernel's one-cycle contract, three department instances, the adversarial suite, and the ≥12-cycle integrated run. UNBOUNDED components (retained in Project Context for audit, excluded from this ledger's terminal): "an AI government able to run a country / eventually the world", the colony→city→nation→world scale ladder, and any claim of real-world governance validity. The user's own goal text already declares scale-out an explicit non-goal of phase 1, which is why the bounded core is clean rather than entangled. Consistent with the sibling `mars-governance` ledger's D3 (open-ended program, bounded phase).

## Refinement Candidates
- **Verdict:** FAIL
- **Provisional:** NO
- **Refined-from:** originating-goal
- **Candidates:** C1 (top-ranked, integrated — the refined goal above): a governed simulation — kernel + contract + ≥3 departments + adversarial suite, ≥12 cycles on a twin, every binding action ratified-certified-constrained or fail-closed escalated. C2 (contract-only): a `DepartmentSpec` + validator enforcing I1–I10 such that two structurally different departments (HIGH and LOW central-legitimacy) are both expressible and their coupling is declared bilaterally — falsifies assumption A1 cheaply. C3 (guideline-compilation): a guideline-intake mechanism (sortition assembly + quadratic priority budget) whose output compiles to `ObjectiveRef` + `Constraint` with no human rewriting — falsifies crux assumption A2, the single highest-information test in the project. C4 (charter-only): a constitutional charter for the machine in which every clause is either machine-checkable or explicitly labelled aspirational, with the checkable fraction reported as a measured number.

## Project Families
| # | Family slug | Status | Success-criteria pointer | Critical-path role | blocked_by |
|---|---|---|---|---|---|
| F0 | `aigov-foundations` | ACCEPTED (seeded 2026-08-11) | its `## MVP Criteria` — V1/V2/V4/V5 audit-tier memos + contested-set record | Gate A — evidence base for every design bound | none |
| F1 | `aigov-constitution` | ACCEPTED (seeded 2026-08-11) | its `## MVP Criteria` — charter + invariant module + measured checkable fraction | Gate A — the machine limits (D0) | aigov-foundations |
| F3 | `aigov-dept-contract` | ACCEPTED (seeded 2026-08-11) | its `## MVP Criteria` — contract + validator I1–I11 + mutation-proof | Gate B — the scaling primitive | aigov-constitution |
| F2 | `aigov-guideline-intake` | ACCEPTED (seeded 2026-08-11) | elicited-level guidelines compile with no human rewrite (crux A2) | Gate B — legitimacy-critical | aigov-foundations, aigov-constitution |
| F6 | `aigov-collective-choice` | ACCEPTED (seeded 2026-08-11) | zero test loss (193/193) porting the Mars_Governance organ | Gate B — the sovereign channel (D3) | aigov-constitution |
| F4 | `aigov-twin` | ACCEPTED (seeded 2026-08-11) | twin reproduces reused ECLSS/analog baselines within a stated tolerance | Gate C — the world departments act on | aigov-dept-contract |
| F5 | `aigov-kernel` | ACCEPTED (seeded 2026-08-11) | no action applies without ratified ∧ certified ∧ constraint-satisfying | Gate D — the runtime | aigov-guideline-intake, aigov-dept-contract, aigov-twin, aigov-collective-choice |
| F7 | `aigov-dept-lifesupport` | PROPOSED — seed at Gate D | closed loop respects physical bounds (HIGH legitimacy) | Gate D — department instance | aigov-dept-contract, aigov-twin |
| F8 | `aigov-dept-economy` | PROPOSED — seed at Gate D | fiscal instrument funds the public-goods bill AND passes I8 (LOW legitimacy) | Gate D — department instance | aigov-dept-contract, aigov-twin |
| F9 | `aigov-audit-arbitration` | PROPOSED — seed at Gate E | never certifies a capture it cannot faithfully audit | Gate E — the checks (D15 + D13) | aigov-kernel |
| F10 | `aigov-adversarial` | PROPOSED — run at every gate | every named attack ends in detection or escalation, never silent success | cross-cutting red team | aigov-kernel |
| F11 | `aigov-integration` | PROPOSED — seed at Gate F | ≥12 cycles · ≥3 departments · adversarial load · reproducible via pytest | Gate F — mission terminal | aigov-audit-arbitration, aigov-adversarial, aigov-dept-lifesupport, aigov-dept-economy |
| F12 | `aigov-scale-gates` | PROPOSED — DEFERRED to phase 2 | colony→city→nation phase-change gates | post-phase-1 | aigov-integration |
<!-- project-state:end:project-families -->

> **Schema note (2026-08-11).** Rewritten from the ad-hoc `Family (ledger id) / Bounded goal / Status`
> shape to the **canonical five columns** parsed by `scripts/advance_ranker.py` (`Family slug`, `Status`,
> `Success-criteria pointer`, `Critical-path role`, `blocked_by`) per
> `~/.claude/skills/soraya/references/umbrella-ledger-schema.md`. The old shape made the code-owned
> `--advance` eligibility gate return `blocked:no-accepted-families` for the whole portfolio — it could not
> see a single family. `blocked_by` edges are the authored flow-down from `docs/decomposition-flowdown.md`;
> predecessor done-ness is computed at read time from each family's own `### Progress proxy`, never stored
> here (fail-closed: unknown blocks).

## Requirements Flow-down
| From | To | Requirement that flows |
|---|---|---|
| Fork 1 (AWAITING RATIFICATION) | all families | The AI never selects the objective, never amends its own constraints, never holds the exception |
| Fork 2 (AWAITING RATIFICATION) | all families | Scale = colony 100–1000; nation-scale is out of phase-1 scope |
| Fork 3 (AWAITING RATIFICATION) | all families | Primary deliverable is a runnable governed simulation, not a document and not a deployable stack |
| aigov-foundations V1 (walls) | aigov-constitution, aigov-kernel, aigov-audit-arbitration | Certify only inside the domain where the property is faithful; otherwise escalate |
| aigov-foundations V4 (Fuller) | aigov-dept-contract (I10), aigov-kernel | Every machine-emitted rule passes the legality linter |
| aigov-foundations V2 (Henry George) | aigov-dept-economy | Fiscal base + its efficiency claim |
| aigov-foundations V5 (space law) | aigov-dept-economy, aigov-kernel | Property regime must survive OST Art. II — usufruct + self-assessment |
| aigov-constitution | aigov-dept-contract | Constraint.source=constitution entries originate in the charter, never in a department |
| aigov-dept-contract I8 | all department families | LOW central-legitimacy ⇒ rule/price instruments only — the subsidiarity engine |
| aigov-dept-contract I3 | aigov-dept-lifesupport, aigov-dept-economy | Bilateral coupling declaration (both contend on pressurized volume + power) |
| aigov-dept-contract I9 | aigov-kernel, aigov-audit-arbitration | Separation of powers: generate ≠ decide ≠ verify; ≤1 role per actor per decision |
| aigov-collective-choice | aigov-kernel | ratify() GATES apply — a menu applies only if certified ∧ non-steering ∧ ratified |
| aigov-collective-choice | aigov-audit-arbitration | paper-RLA tamper audit reused as the verification primitive |
| aigov-guideline-intake | aigov-kernel | The compiled guideline set is the kernel's ONLY source of objectives |
| aigov-twin | aigov-dept-lifesupport, aigov-dept-economy, aigov-adversarial | Shared world-state; no department holds a private copy of a shared var |
| mars-governance D7 | all families | Every "confirmed" result is MODEL-COHERENT, not governance-validated |
| colonization roadmap Gates 2/5 | aigov-twin, aigov-dept-lifesupport | Power and life-support-closure envelopes bound what the twin may assume |
<!-- project-state:end:requirements-flowdown -->

## Mission Terminal Condition
Phase-1 terminal (mechanically assertable): the AI Governor kernel, on the colony digital twin at electorate 100–1000, consumes a ratified guideline set and runs ≥12 decision cycles across ≥3 departments spanning all three central-legitimacy ratings (HIGH/MEDIUM/LOW), where every binding action is (ratified ∧ certified-non-steering ∧ constraint-satisfying) or fail-closed escalated, under the aigov-adversarial suite, reproducibly via pytest. The PROGRAM terminal is NOT mechanical: "an AI government able to run a colony/city/nation/world" is open-world and has no mechanical closure. Soraya asserts phase-1 completion mechanically and then REQUESTS explicit user sign-off; the judgment that no further families are needed is always the user's. Per inherited mars-governance D3/D7, phase-1 completion is model-coherent software validation only — human field test (Stage B) and formal verification (Stage C) remain the real gates, and no result here may be reported as "governance-validated".
<!-- project-state:end:mission-terminal -->

## Goal Hierarchy
> PROVISIONAL — three authority forks in `docs/idea-anchor-DRAFT-2026-08-11.md` are awaiting user ratification; see Open Questions for User.

### Long-term (12+ months tier)
A constitutionally-bounded AI Governor — proven in adversarial simulation before it is ever given power — that converts democratically-produced guidelines into a running, auditable institutional framework, centrally administering only the hard physical commons and otherwise maintaining the conditions for decentralized discovery.

### Mid-term (3-12 months)
| # | Milestone | Success Criterion | Horizon |
|---|---|---|---|
| 1 | Foundations promoted to audit-tier | V1–V12 have supported memos in research_outputs/; contested set confirmed contested | 1-2 mo |
| 2 | Constitutional charter (D0) | Every clause machine-checkable or explicitly labelled aspirational; checkable fraction reported as a measured number | 1-2 mo |
| 3 | Department Contract + validator | I1–I10 enforced as validator errors; I6 demonstrated by a mutated spec that FAILS | 2-3 mo |
| 4 | Colony digital twin | Reproduces reused ECLSS/analog baselines within a stated tolerance | 3-5 mo |
| 5 | Governor kernel one-cycle contract | No action applies without ratified ∧ certified-non-steering ∧ constraint-satisfying | 4-6 mo |
| 6 | Three departments spanning HIGH/MEDIUM/LOW legitimacy | All three validate; D1↔D2 coupling declared bilaterally; I8 holds | 6-9 mo |
| 7 | Adversarial suite + integrated ≥12-cycle run | Every named attack ends in detection or escalation, never silent success | 9-12 mo |

### Short-term (≤1 month)
| # | Action | Class | Owner | Horizon |
|---|---|---|---|---|
| 1 | Ratify the 3 authority forks (AI role / scale / deliverable) | ask-user | user | ≤1 wk |
| 2 | Build DepartmentSpec + validator (I1–I10) with a mutation test for I6 | edit-local-code | claude | ≤2 wk |
| 3 | Hand-compile 3 real guideline sentences into ObjectiveRef+Constraint (crux A2 probe) | propose | claude | ≤1 wk |
| 4 | Draft the D0 charter clause list and MEASURE the machine-checkable fraction | write-plan | claude | ≤2 wk |
| 5 | Promote V1 (the five walls) to an audit-tier memo | research | claude | ≤2 wk |
| 6 | Port the Mars_Governance organ; confirm 193/193 from the new root | run-tests | claude | ≤1 wk |

## State Snapshot
### Assumptions
- A1 — a polity's functions decompose into separable departments with a uniform interface — confidence: medium
- A2 — "general guidelines from the people" can be made precise enough to mechanically constrain policy generation — confidence: low (THE CRUX)
- A3 — simulation can validate governance mechanisms before real citizens exist — confidence: medium (inherited from mars-governance)
- A4 — the Hayek/central-planning objection is genuinely weaker inside a closed life-support loop — confidence: medium-high
- A5 — "optimize taxes AND maximize financial freedom AND optimize innovation" is jointly coherent — confidence: low (these trade off; expose the frontier, never claim an optimum)
- A6 — adversarial pressure (capture, gaming, preference falsification) can be simulated meaningfully — confidence: medium (synthetic adversaries are weaker than real ones)
- A7 — an AI can be constitutionally constrained by rules it also executes — confidence: low (needs structure — separation generate≠tally≠verify — not prose)
- A8 — scale-out colony→city→nation is continuous — confidence: low (likely false; treat as phase changes)
### Evidence
| # | Claim | Source | Confidence | Captured |
|---|---|---|---|---|
| 1 | Mars_Governance governance suite passes 193/193 | direct execution `python -m pytest tests/ -q`, 2026-08-11 | high | 2026-08-11 |
| 2 | G–S: any onto, non-dictatorial, deterministic SCF over ≥3 alternatives under unrestricted domain is manipulable | Gibbard 1973 Econometrica 41:587-600; Satterthwaite 1975 JET 10:187-217 (WebSearch 2026-08-11) | high | 2026-08-11 |
| 3 | Blockchain voting judged counterproductive for public elections; resolved design uses tamper-evident log + risk-limiting audit | inherited audit-tier finding, mars-governance ledger | high | 2026-06-05 |
| 4 | Multi-peaked-electorate escalation gate yields 0 silent mis-certifications across 500-panel ensembles | Mars_Governance results/innovation_governance_failsafe_2026-06-08.md | medium | 2026-06-08 |
<!-- project-state:end:evidence -->
### Unknowns
- How a population produces a guideline precise enough to bind a machine without a technocrat writing it (A2)
- Whether two structurally different departments are expressible without shared mutable state (A1)
- Which fiscal instrument actually funds the colony public-goods bill (LVT-analogue yield is uncomputed)
- Who declares, exercises, terminates and audits the emergency when a binding vote conflicts with a life-support hard limit
- Whether the twin can reproduce ECLSS baselines at the fidelity department decisions require
- What fraction of a constitutional charter is machine-checkable at all
- Whether synthetic adversaries are strong enough for the adversarial suite to mean anything
### Hypotheses (Active)
| ID | Statement | Status (open/under-investigation/falsified/confirmed) | Last-tested |
|---|---|---|---|
| H1 | Democratically-produced guidelines can be compiled into ObjectiveRef+Constraint with no human rewriting | under-investigation | 2026-08-11 |
| H2 | Two departments at opposite central-legitimacy ratings are both expressible under one DepartmentSpec with bilateral coupling | open | - |
| H3 | A machine-checkable majority of constitutional clauses exists (checkable fraction > 0.5) | open | - |
| H4 | A volume/area LVT-analogue plus Pigouvian O2/water pricing funds the colony public-goods bill without quantity allocation | open | - |
| H5 | Every attack in the adversarial suite terminates in detection or escalation, never silent success | open | - |
<!-- project-state:end:hypotheses -->
### Decisions Made
| Decision | Date | Notes |
|---|---|---|
| D0 — Umbrella seeded; only unblocked families get ledgers (anti-sprawl); downstream families seeded at gate clearance | 2026-08-11 | matches advance_ranker eligibility semantics; preserves self-init population budget |
| F0-contested-set-confirmed-landed | 2026-08-11 | `research_outputs/aigov-v12-contested-set.md`. 3 of 4 checked, all genuinely contested but in THREE DIFFERENT WAYS. Chamley–Judd is stronger than "contested" — OVERTURNED within its own models (Straub & Werning, AER 110(1):86-119, 2020: positive long-run capital tax whenever IES<1; zero is knife-edge). Dunbar contested as flagged (Lindenfors et al. 2021 Biology Letters: mean 69.2, 95% CI 3.8–292.0; Dunbar rebuts; live dispute). MILGRAM: canon-map flag was TOO COARSE — the BEHAVIOUR replicates robustly (Burger 2009; Blass 1963–85; recent online replication), only the MECHANISM (agentic state → engaged followership) and reporting integrity (Perry 2013) are contested. *Limits to Growth* NOT CHECKED — stays flagged-unverified. |
| D6 — Milgram flag corrected: phenomenon usable, mechanism not | 2026-08-11 | Recovered a design-relevant finding the blanket flag had discarded, and it cuts AGAINST the governor: if harm-compliance runs through IDENTIFICATION WITH THE ENTERPRISE rather than surrender of agency, a governor supplying a compelling mission frame is a MORE effective harm-compliance engine than one issuing orders. Strengthens charter C03 (emergency authority) + C15 (fail-closed escalation) + the anti-steering primitives. |
| D7 — H2 of aigov-foundations FALSIFIED; fiscal justification revised (DF2 in action) | 2026-08-11 | The Henry George theorem's self-financing equality CANNOT be invoked for a colony: 5 of its conditions fail, and one — free inter-jurisdictional mobility (Tiebout) — is a load-bearing ABSENCE of this polity (same premise as charter C21). REMOVED the "Henry-George-financed public goods" claim. RETAINED the volume/area LVT-analogue on the independent and robust ground of FACTOR INELASTICITY (George 1879), which needs none of the failed conditions. Whether rents fund the bill is now an EMPIRICAL question for the twin (umbrella H4), which `d2_economy._falsification_test` already computes as a number rather than asserting. |
| D8 — Art. VI makes the colony a SUPERVISED non-governmental activity, not a sovereign polity | 2026-08-11 | `research_outputs/aigov-v5-space-law-property-envelope.md`. Under OST Art. VI a State party bears international responsibility and owes "authorization and continuing supervision" over the colony's activities. The AI Governor is therefore NOT the top of its own authority chain — a second external coercion channel alongside the resupplier-as-coercer veto already modelled in Mars_Governance/governance/connection.py. Drafted charter clause C25 (disclosure duty, ASPIRATIONAL, human_only) awaits ratification; department D5 scope widened to model legal as well as physical dependence. |
| F1-charter-checkable-fraction-landed | 2026-08-11 | Family aigov-constitution MET its MVP bar 4/4. 24-clause charter in aigov/charter_invariants.py + the four non-negotiable invariants (N1 objective-provenance, N2 no-self-amendment via constraint fingerprint, N3 exception-is-split across 4 distinct actors with auto-expiry, N4 separation-of-powers), each tripped by a violating fixture. MEASURED machine-checkable fraction = 17/24 = 0.7083 (H1 predicted >0.5 — CONFIRMED). docs/charter.md is GENERATED from the enforcing code (python -m aigov.render_charter) so prose cannot drift; idempotence checked. Honest split: 17 enforced / 1 pending / 6 aspirational. |
| D5 — A failing pin caught a real charter overclaim | 2026-08-11 | The fraction pin first read 18/24 and FAILED against a measured 0.75. The MEASUREMENT was right and the EXPECTATION was wrong: clause C15 named `fail_safe_gate`, an invariant that exists in Mars_Governance but is NOT wired into this repo. Resolution was to add PENDING status + overclaim detection (enforced_by must resolve to an IMPLEMENTED invariant), not to edit the pin to match. Naming an unimplemented invariant is now a charter integrity error. |
| F3-contract-mutation-proof-landed | 2026-08-11 | Family aigov-dept-contract MET its MVP bar 6/6. aigov/contract.py + guidelines.py + two opposite-legitimacy reference specs (D1 HIGH, D2 LOW) + 56 tests. Mutation-proof at two levels: spec falsification tests can come out FALSE, and with the validator patched to a no-op 24 of 28 mutation tests go RED (4 survivors are the negative controls). Hypotheses H1/H2/H3 of that family CONFIRMED — H2 with a named residual (InstrumentClass is author-declared, so subsidiarity is mechanically ENFORCED over declared classes and AUDITED at classification). |
| D4 — MVP-bar predicate defect found and fixed before any --until-mvp loop ran | 2026-08-11 | All three family bars used `project-state-row <own-ledger>:<pattern>`, which matched the criterion's OWN line and was self-satisfying (MET before any work existed). Repointed at the umbrella. GENERAL RULE: a project-state-row predicate must never target the ledger that holds it. |
| D1 — RATIFIED Fork 1: the AI is an ADMINISTRATIVE + ANALYTIC ORGAN under human sovereignty. It generates options, simulates, drafts instruments, executes ratified rules and audits itself; it NEVER selects the objective, amends its own constraints, or holds the exception. | 2026-08-11 | Resolved Pending Decision row 1. Enforced by invariants I1 (objective provenance), I9 (generate≠decide≠verify), I11 (threshold provenance). Flows down to ALL families. |
| D2 — RATIFIED Fork 2: V1 scale is COLONY, electorate 100–1000. City / nation / world are explicit NON-GOALS of phase 1; scale transitions are named phase-change gates (attention budget, enforcement distance, exit-option collapse) in deferred family aigov-scale-gates. | 2026-08-11 | Resolved Pending Decision row 2. Matches sibling mars-governance D2 scale params. |
| D3 — RATIFIED Fork 3: primary deliverable is a RUNNABLE GOVERNED SIMULATION (kernel + contract + ≥3 departments + adversarial suite on a twin), not a document and not a deployable stack. | 2026-08-11 | Resolved Pending Decision row 3. The constitution is produced anyway, as an executed input file rather than prose. |
| Hypothesis H1 updated | 2026-08-11 | Status → under-investigation; Last-tested → 2026-08-11. Note: Probe B1 (docs/probe-B1-guideline-compilation.md, 2026-08-11): hand-compiled 3 realistic guideline sentences. A2 is PARTIALLY TRUE — compilability is a property of guideline TYPE: P (mechanism prohibition) and O (ordering/monotonicity) compile FULLY and cleanly; F (floor/ceiling) and D (metric direction) compile only if the level/metric is elicited; A (aspiration) never compiles. Load-bearing finding: the threshold gap is where an advisory AI silently becomes sovereign. New invariant I11 added to the department contract. Falsifier: find a non-aspirational guideline outside P/O/F/D. |
| F6-organ-vendored-zero-test-loss | 2026-08-11 | Family aigov-collective-choice MET its MVP bar 4/4. Mars_Governance organ vendored to aigov/choice/ (governance, models, sandbox, prototypes, tests, docs, results + its conftest); **193/193 from the new root**, zero test loss. Source tree byte-unchanged (24 git-status entries before and after). Charter C15 flipped PENDING -> ENFORCED; measured checkable fraction 0.68 -> 0.72. Root suite 89 + organ 193 = 282 green. |
| D9 — CORRECTION: the Mars_Governance '132 tests' figure was NOT stale | 2026-08-11 | This project claimed on 2026-08-11 (session board + report) that the 132 figure in results/innovation_governance_failsafe_2026-06-08.md was stale. Measured in an isolated detached worktree: **HEAD carries exactly 132 tests / 11 files**. The 193 comes from ~6 weeks of UNCOMMITTED work (24 entries, mtimes 2026-06-27/28, incl. civic_education.py + connection.py + 2 test files). 132 was correct for the commit; the claim is retracted and the session board corrected. |
| D10 — Vendor rather than path-depend on a sibling working tree | 2026-08-11 | Depending on Space_Reflectors_Project by path would couple this project to ANOTHER SESSION'S uncommitted working tree. Vendoring pins a known-good state, leaves the source untouched (R4), and incidentally preserves that 6-week backlog. Provenance label is 'vendored from the WORKING TREE at 2026-08-11', never 'from HEAD'. |
| F2-threshold-gap-closed-at-source | 2026-08-11 | Family aigov-guideline-intake MET its MVP bar 3/3. `aigov/intake.py`: reproducible sortition, quadratic priority budget (over-budget ballots REJECTED not clipped), MEDIAN level elicitation with fail-closed escalation on genuine polarization, and a compile path with NO route to a binding type-F guideline lacking a panel-supplied level (verified by negative tests). 39 tests; root suite 128 green. The threshold gap probe B1 found is now closed at the SOURCE as well as at the validator (I11). |
| D11 — TWO real metric defects found by SWEEPING, not by unit tests | 2026-08-11 | The intake's polarization detector passed 29 green unit tests twice on hand-picked fixtures while being wrong. Sweep 1 exposed range-normalisation measuring NOISE (a tight cluster scored 0.500; a wide unimodal panel false-escalated). Sweep 2, after the fix, exposed that an unconstrained 2-means split scored ONE outlier at 1.000 — handing any single panelist a UNILATERAL VETO on aggregation, the exact strategic vector the median was chosen to resist. Both fixed; both would have shipped on a green suite. Verify-in-batch means INSPECT, not exit-code. |
| D12 — Procedural parameters carry provenance too (recursive honesty) | 2026-08-11 | The polarization tolerance is itself a number. `compile_guidelines` REFUSES an AI_SUPPLIED ProceduralParameter (G2), and the default 0.900 is DERIVED by `calibrate_polarization()` (400 unimodal + 400 two-camp panels; 26 errors/800 = 3.25%; unimodal p95 0.867 < 0.900 < bimodal p50 0.996) with a test pinning the default to within 0.02 of the derivation. The residual class overlap is real and reported, not hidden. |
| D13 — The binding path now contains NO hand-typed number | 2026-08-11 | Closing the loop between F2 and F3: `aigov/guidelines.py` produces `RATIFIED` by running a real intake round, and D1/D2 READ their thresholds via `level_of(...)` rather than restating literals (source-scan test enforces it). Previously the registry declared `level=25.0` under a comment claiming it was elicited — a prose claim the structure did not back, the same overclaim class as charter clause C15's. The AI-is-advisory property is now structural in the DATA path as well as the validator (I11). Residual, labelled: the citizens are a deterministic FIXTURE; only the mechanism is real. |
| F4-twin-baselines-reproduced | 2026-08-11 | Family aigov-twin MET its MVP bar 3/3. `aigov/twin.py` serves all 10 declared StateVars at matching observability, reproduces the vendored per-capita references (O2 1.01%, CO2 4.92%, food 0.11%) within a 5% tolerance, scale-invariance to 1.3e-16, holds pressure flat at break-even crop fraction over 12 cycles, and reproduces EVERY failure mode D1 declares. 34 tests; root suite 162 green. Gate C CLEARED — F5 (kernel) now has all four predecessors met. |
| D14 — Observability is now ENFORCED, closing a third invented-number channel | 2026-08-11 | `StateVar.observability` was a declared field nothing checked. The twin now REFUSES to serve a LATENT variable as a measurement and returns ESTIMATED ones wrapped with method + error bar. Three channels are now structurally closed: I11 (no AI-supplied THRESHOLD), intake G1/G2 (no AI-supplied LEVEL), DT1 (no AI-read LATENT STATE). |
| D15 — An unphysical-state defect found by RUN INSPECTION, with all tests green | 2026-08-11 | The twin reported an O2 partial pressure of 304 kPa at cycle 12 under full photosynthetic closure — three atmospheres of pure O2 in a hull rated for about one. Every test passed. Closed by declaring the fire-hazard (30.0 kPa) and structural (101.325 kPa) bounds as PHYSICAL constants and refusing to serve state past a hull breach. THIRD consecutive run in which inspection, not the suite, found the real defect. |
| F5-kernel-cannot-act-ungated | 2026-08-11 | Family aigov-kernel MET its MVP bar 3/3. `aigov/kernel.py`: `apply()` raises `UngatedActionError` on 7 of the 8 gate-condition combinations (only ratified AND CERTIFY AND constraint-satisfying applies), takes only `(self, cert)` so there is no bypass parameter, binds the REAL vendored anti-steering gate for `crop_area_allocation` (strawman agendas certify 0/80 panels) and REFUSES every other instrument as NOT_CERTIFIABLE rather than inventing a check, probes constraints on a twin COPY, and leaves the status quo standing through a fully-refused run. 20 tests; root suite 182; vendored organ 193/193 preserved. **Gate D partially cleared** — the runtime exists; D15 audit (F9) and the adversarial suite (F10) remain. |
| D16 — A VACUOUS PASS: green suite, nonsense run | 2026-08-11 | `test_twelve_cycles_never_apply_an_ungated_action` was GREEN while the governed run LOST THE ATMOSPHERE at cycle 1. The kernel started from InstrumentSettings() zeros, so refusing every action meant running life support at zero — and 'nothing applied' was precisely what the test asserted, so it was structurally blind to the failure. Found by INSPECTING a run. Fixed via `status_quo_settings()` whose crop fraction is DERIVED from PLANT_O2_OVERPRODUCTION_FACTOR, plus a dedicated test asserting a fully-refused run leaves the colony ALIVE. FOURTH consecutive run in which inspection, not the suite, found the real defect. |
| D17 — The non-steering certifier's DOMAIN is now an enforced boundary | 2026-08-11 | aigov-collective-choice H2 asked whether the organ generalizes beyond the resource domain. Rather than leaving it open or inventing a generic check, the kernel certifies ONLY `crop_area_allocation` and refuses everything else. The governor can therefore currently act on exactly one instrument — a real, stated limit on its authority rather than a gap papered over. |
<!-- project-state:end:decisions-made -->
### Pending Decisions
| Decision | Proposer | Blocker | Notes |
|---|---|---|---|
| RESOLVED 2026-08-11: Fork 1 — AI as administrative organ vs sovereign decider | claude | user ratification | drafted position: administrative organ, encoded constitutionally; see idea-anchor §2 |
| RESOLVED 2026-08-11: Fork 2 — V1 scale target: colony 100–1000 vs city vs nation-general | claude | user ratification | drafted position: colony, with scale transitions named as gates |
| RESOLVED 2026-08-11: Fork 3 — Primary deliverable: runnable governed sim vs framework document vs deployable stack | claude | user ratification | drafted position: runnable governed simulation |
| K1–K8 framework forks (guideline source, objective structure, fiscal base, coordination, emergency, scale, property, minority protection) | claude | Fork 1-3 ratification + F0 evidence | drafted leans in docs/foundations-canon-map.md §3 |
<!-- project-state:end:pending-decisions -->

## Bellman-Inspired Decision Frame

Per D5: surfaces the Bellman cognitive frame at the architecture level. v0.1 populates this at init; v0.2's `/project-step` reads from it to decide next actions. v0.1 does NOT iterate over the frame — it sets it up.

3 authority forks RATIFIED (D1 organ / D2 colony 100–1000 / D3 runnable sim). Gate A+B partially cleared: 2 of 3 seeded families MET their MVP bars — aigov-dept-contract 6/6 (contract + validator I1–I11 + two opposite-legitimacy reference specs + mutation-proof) and aigov-constitution 4/4 (24-clause charter, four non-negotiable invariants, MEASURED checkable fraction 0.7083). 88 tests green. aigov-foundations 0/5 — the four /research memos are the open Gate-A work. No kernel, no twin, no departments beyond the two reference specs.

### Target state / terminal condition
See ## Mission Terminal Condition — the refined goal C1: kernel + contract + ≥3 departments spanning all central-legitimacy ratings, ≥12 cycles on the twin under adversarial load, every binding action ratified-certified-constrained or fail-closed escalated, reproducible via pytest.

### Progress proxy
- **v0.1 metric:** `unknowns-retired` count + `gates-passed` count (raw counts, unweighted)
- **v0.2+:** weighted combination of unknowns-retired, gates-passed, evidence-confidence-improved, hypotheses-falsified (TBD via v0.2 design)

### Candidate next actions
| # | Action | Class | Expected progress | Expected info gain | Uncertainty | Cost |
|---|---|---|---|---|---|---|
| 1 | Ratify the 3 authority forks | ask-user | high (unblocks everything) | high | low | ~0 |
| 2 | Build DepartmentSpec + validator I1–I10 + I6 mutation test | edit-local-code | high (scaling primitive) | high | medium | low |
| 3 | Hand-compile 3 guideline sentences (crux A2 probe) | propose | medium | highest (could reshape the project) | high | low |
| 4 | Draft D0 charter clause list; measure checkable fraction | write-plan | high | high | medium | low |
| 5 | Promote V1 (five walls) to audit-tier memo | research | medium | high | low | medium |
| 6 | Port Mars_Governance organ; confirm 193/193 from new root | run-tests | high | low | low | low |
<!-- project-state:end:candidate-actions -->

### Re-evaluation trigger
- **Default:** re-run `/project-state` after any action class fires (auto-append to Action Log triggers stale-state check)
- **Manual override:** user invokes `/project-state aigov` at any time
- **v0.2+:** automated trigger when N actions fire OR T days elapse OR a hypothesis falsifies (TBD)

## Allowed Action Classes (v0.2 placeholder — not enforced in v0.1)
- `propose` — auto
- `research` — auto (delegate to /research / /athena-research / /research-verify)
- `write-plan` — auto (delegate to /technical-plan / /save-plan)
- `edit-local-code` — REQUIRES per-action human approval
- `run-tests` — auto if local + sandboxed
- `ask-user` — auto
- `stop` — auto

## Action Log
| # | Date | Action class | Description | Outcome |
|---|---|---|---|---|
| 1 | 2026-08-11 | propose | /project-init invoked (umbrella) | ledger created |
| 2 | 2026-08-11 | research | Verified reuse asset: ran Mars_Governance pytest suite | 193 passed in 27.14s |
| 3 | 2026-08-11 | research | WebSearch confirmed Gibbard-Satterthwaite statement + preconditions | Evidence row 2 added; common Arrow conflation recorded |
| 4 | 2026-08-11 | write-plan | Wrote idea-anchor draft, canon map, department ontology, decomposition | 4 docs in docs/; 3 forks parked for ratification |
| 5 | 2026-08-11 | write-plan | Wrote plans/AI_Governor_Phase1_Technical_Plan.md (~78 steps, all gate-class auto) | plan written; blocked at step 0 on fork ratification |
| 6 | 2026-08-11 | run-tests | Validated 4 ledgers (6/6 end markers each) + 15/15 MVP predicates parse via mvp_criteria.py | 0 missing, 0 duplicate markers; all predicates classify |
| 7 | 2026-08-11 | propose | Probe B1 (crux A2): hand-compiled 3 guideline sentences to ObjectiveRef+Constraint | A2 PARTIALLY TRUE; P/O/F/D/A type partition found; threshold gap identified; new invariant I11 |
| 8 | 2026-08-11 | propose | /project-state --update-hypothesis | Hypothesis H1: status → under-investigation; note: probe B1 P/O/F/D/A type partition + threshold gap + I11 |
| 9 | 2026-08-11 | ask-user | /project-state --resolve-pending-decision 1 | Fork 1 RATIFIED as drafted: AI = administrative organ under human sovereignty |
| 10 | 2026-08-11 | ask-user | /project-state --resolve-pending-decision 2 | Fork 2 RATIFIED as drafted: V1 scale = colony, electorate 100–1000 |
| 11 | 2026-08-11 | ask-user | /project-state --resolve-pending-decision 3 | Fork 3 RATIFIED as drafted: deliverable = runnable governed simulation |
| 12 | 2026-08-11 | edit-local-code | Rewrote ## Project Families to the canonical advance_ranker 5-column schema (Family slug / Status / Success-criteria pointer / Critical-path role / blocked_by); prior version in git history | eligibility gate went from blocked:no-accepted-families (portfolio invisible) to portfolio_status=ok; ordering=[aigov-foundations, aigov-dept-contract] |
| 13 | 2026-08-11 | edit-local-code | Direct-Edit umbrella ## Project Families: F6 aigov-collective-choice PROPOSED -> ACCEPTED; prior version in git history | family seeded + advanced to its bar in the same run (spillover) |
| 14 | 2026-08-11 | run-tests | Verified the whole portfolio after the F6 port | root 89 + vendored organ 193 = 282 tests green; all 4 seeded family bars MET |
| 15 | 2026-08-11 | edit-local-code | Direct-Edit umbrella ## Project Families: F2 PROPOSED -> ACCEPTED; prior version in git history | family seeded + advanced to its bar in the same run |
| 16 | 2026-08-11 | run-tests | Portfolio verification after the F2 registry wiring | root 134 + vendored organ 193 = 327 tests green; all 5 ACCEPTED family bars MET |
| 17 | 2026-08-11 | edit-local-code | Direct-Edit umbrella ## Project Families: F4 PROPOSED -> ACCEPTED; prior version in git history | Gate C cleared; F5 kernel unblocked |
| 18 | 2026-08-11 | edit-local-code | Direct-Edit umbrella ## Project Families: F5 PROPOSED -> ACCEPTED; prior version in git history | runtime landed; 7 of 13 families now ACCEPTED and all at their bars |
<!-- project-state:end:action-log -->

## Open Questions for User
- **Fork 1 (AUTHORITY):** Is the AI a *sovereign decider* or an *administrative + analytic organ* under human sovereignty? Drafted position: administrative organ, encoded constitutionally. Rationale + risk of the alternative in `docs/idea-anchor-DRAFT-2026-08-11.md` §2.
- **Fork 2 (AUTHORITY):** What scale is V1 targeting — colony (100–1000), city, or nation-general? Drafted position: colony, with the scale transitions named as explicit gates.
- **Fork 3 (AUTHORITY):** What is the primary ~1-month deliverable — a runnable governed simulation, a framework/constitution document, or a deployable stack for a real community? Drafted position: runnable governed simulation.
- **Non-blocking, drafted:** the eight framework forks K1–K8 (guideline source, objective structure, fiscal base, economic coordination, emergency authority, scale strategy, property regime, minority protection) have drafted leans in `docs/foundations-canon-map.md` §3 and become ratified Decisions once F0 evidence lands.

## Last Evaluation (v0.2 placeholder — not enforced in v0.1)
- **Date:** 2026-08-11
- **Progress signal:** 3 authority forks ratified (D1/D2/D3). 2 of 3 seeded family MVP bars MET (aigov-dept-contract 6/6, aigov-constitution 4/4); 88 tests green. 6 hypotheses retired across families (contract H1/H2/H3, constitution H1/H2/H3 — H2-contract and H3-constitution confirmed WITH named residuals). Umbrella H1 open → under-investigation (probe B1: A2 partially true, P/O/F/D/A partition). 3 unknowns retired: guideline compilability partition, I8 mechanical checkability, charter checkable fraction (0.7083 measured). 2 real defects found and fixed by verification rather than assumed away: self-satisfying project-state-row predicates, and a charter overclaim (C15 naming an unwired invariant) caught by a failing pin. Gates passed: Gate B partial (contract landed); Gate A partial (charter landed, foundations research open).
