# AI Government F0 — Foundations (canon → audit-tier evidence)
<!-- project-schema: 0.1 -->

> Initialized 2026-08-11. Project ID: aigov-foundations. Originating goal (verbatim): "Read and research the economics, geostrategy, philosophy-of-governance and social-engineering literature and promote the twelve load-bearing claims V1-V12 in docs/foundations-canon-map.md from discovery-tier model recall to audit-tier verified memos, and confirm that the contested set is genuinely contested, so the framework's design bounds rest on evidence rather than recall."
> Seeded by Soraya `decompose` (2026-08-11), `/project-init` protocol executed by hand. Parent umbrella: `aigov`.

## Project Context
- **Project ID:** aigov-foundations
- **Project root:** C:\Users\Farshad\PythonProjects\Skill_Development\AI_Governor
- **Captured:** 2026-08-11
- **Originating goal:** (see verbatim above)
- **Refined goal (if 3c produced one):** For each of the twelve claims V1–V12 in `docs/foundations-canon-map.md` §5, produce a `/research` + `/research-verify` supported memo in `research_outputs/` whose cited sources resolve and whose load-bearing quotes verify verbatim; and produce one memo confirming the contested set (Chamley–Judd, Dunbar, Milgram, Limits to Growth) is genuinely contested. Claims that fail verification are recorded as FALSIFIED and the design bound they supported is revised — a failed verification is a successful outcome of this family, not a defect.
- **Role:** FAMILY ledger under umbrella `aigov`. Critical-path position: **Gate A** (parallel with `aigov-constitution`).
- **Horizon (months):** 3
- **Schema:** project-schema 0.1

## Empirical Concerns
- **Verdict:** PASS
- **Check status:** attempted
- **Provisional:** NO
- **Findings:** The goal makes no factual assertion of its own — it asserts that a *named set of claims is currently unverified*, which is true by construction (`docs/foundations-canon-map.md` carries an explicit discovery-tier banner and was produced from model recall). One claim in that map has already been promoted: **V1-partial** — Gibbard–Satterthwaite's statement and preconditions were WebSearch-confirmed 2026-08-11 (Gibbard 1973 Econometrica 41:587-600; Satterthwaite 1975 JET 10:187-217), including the common conflation of G–S with Arrow's IIA/unanimity conditions, which is recorded so it does not propagate.

## Project vs Research-Program
- **Verdict:** PASS
- **Provisional:** NO
- **Classification:** project
- **Rationale:** The *field* (economics + governance philosophy + geostrategy) is unbounded, but this family's goal is bounded to a fixed, enumerated list of twelve claims with a mechanical completion test (a verified memo exists per claim), inside a 3-month horizon. The unbounded reading — "read all the literature" — is explicitly NOT this family's goal and would be unfalsifiable; the enumerated-claims framing is what makes it a project.

## Refinement Candidates
- **Verdict:** PASS
- **Provisional:** NO
- **Refined-from:** originating-goal
- **Candidates:** C1 (= refined goal): all twelve V-claims verified + contested-set memo. C2 (design-critical four): verify only V1 (walls), V2 (Henry George), V4 (Fuller), V5 (space law) — the four whose failure would change an already-committed design decision — and defer the rest. C3 (breadth-first): a `/research-leads` discovery sweep across the six literatures first, to find load-bearing claims the canon map MISSED, before verifying the ones it named.

## MVP Criteria
<!-- attempt-budget: 3 -->
- file-exists research_outputs/aigov-v1-social-choice-walls.md
- file-exists research_outputs/aigov-v2-land-value-tax-henry-george.md
- file-exists research_outputs/aigov-v4-fuller-legality-desiderata.md
- file-exists research_outputs/aigov-v5-space-law-property-envelope.md
- project-state-row project_state/aigov.md:F0-contested-set-confirmed-landed
<!-- project-state:end:mvp-criteria -->

> **Predicate repointed 2026-08-11** — see the defect note in `aigov-dept-contract.md`: a
> `project-state-row` predicate must never target the ledger that holds it, or it matches its own
> criterion line and is self-satisfying. Now correctly **unmet**.

> **Bar status: PROPOSED (draft-then-ratify)** under the v1.12 execute-mode exception. Deliberately set at
> **C2's four design-critical claims**, not all twelve — those four are the ones whose failure would force a
> design change already made. V3, V6–V12 continue after the bar as ordinary candidate actions.

## Goal Hierarchy
### Long-term (12+ months tier)
A foundation where every design bound the AI Government claims is traceable to a verified source, and every claim that failed verification is visibly recorded as such.

### Mid-term (3-12 months)
| # | Milestone | Success Criterion | Horizon |
|---|---|---|---|
| 1 | The four design-critical claims verified (V1, V2, V4, V5) | Supported memos exist; `/research-verify` sidecars show quotes verbatim | ≤1.5 mo |
| 2 | Mechanism + legitimacy claims verified (V3, V6, V7, V9) | Supported memos exist | ≤2.5 mo |
| 3 | Precedent + framing claims verified (V8, V10, V11) | Supported memos exist | ≤3 mo |
| 4 | Contested set confirmed contested (V12) | One memo showing each is disputed in the literature, with both sides cited | ≤3 mo |

### Short-term (≤1 month)
| # | Action | Class | Owner | Horizon |
|---|---|---|---|---|
| 1 | `/research` V1 — Arrow, G–S, Sen, McKelvey, median-voter, Ashby: exact statements + preconditions | research | claude | ≤1 wk |
| 2 | `/research` V2 — Henry George theorem conditions + LVT efficiency evidence | research | claude | ≤2 wk |
| 3 | `/research` V4 — Fuller's eight desiderata, exact list | research | claude | ≤2 wk |
| 4 | `/research` V5 — OST Art. II/VI, Artemis Accords, 2015 US + 2017 LU resource laws | research | claude | ≤3 wk |
| 5 | `/research-verify` each memo; record any FALSIFIED claim + the design bound it revises | research | claude | ≤4 wk |

## State Snapshot
### Assumptions
- The canon map named the claims that actually matter (rather than missing a decisive literature) — confidence: medium (C3 exists to test this)
- Verification via `/research` + `/research-verify` is strong enough for theorem statements — confidence: medium-high for formal results, lower for empirical/contested ones
- A failed verification will actually be allowed to revise the design rather than be quietly dropped — confidence: high (it is written into this family's goal)
### Evidence
| # | Claim | Source | Confidence | Captured |
|---|---|---|---|---|
| 1 | G–S: onto + non-dictatorial + deterministic + ≥3 alternatives + unrestricted domain ⇒ manipulable | Gibbard 1973 Econometrica 41:587-600; Satterthwaite 1975 JET 10:187-217 (WebSearch 2026-08-11) | high | 2026-08-11 |
| 2 | A common secondary-source error conflates G–S conditions with Arrow's unanimity + IIA | WebSearch result review 2026-08-11 | medium | 2026-08-11 |
<!-- project-state:end:evidence -->
### Unknowns
- Whether the Henry George theorem's conditions survive a colony's non-land fixed factors (pressurized volume, radiator area)
- Whether OST Art. II forecloses the usufruct/self-assessment property regime (K7) or merely constrains it
- Whether any decisive literature was missed by the canon map (C3)
- Whether Cybersyn's documented failure modes are recoverable from sources or mostly retrospective narrative
### Hypotheses (Active)
| ID | Statement | Status (open/under-investigation/falsified/confirmed) | Last-tested |
|---|---|---|---|
| H1 | All five walls in V1 verify as stated in the canon map | confirmed | 2026-08-11 |
| H2 | The Henry George theorem's conditions are satisfiable by a colony's fixed factors | falsified | 2026-08-11 |
| H3 | The contested set is genuinely contested (not settled in either direction) | confirmed | 2026-08-11 |
| H4 | No decisive literature was missed by the canon map | open | - |
<!-- project-state:end:hypotheses -->
### Decisions Made
| Decision | Date | Notes |
|---|---|---|
| DF1 — MVP bar set at C2's four design-critical claims, not all twelve | 2026-08-11 | those four can force a design change already committed; the rest inform but do not overturn |
| DF2 — A FALSIFIED claim is a successful outcome and MUST revise the design bound it supported | 2026-08-11 | prevents verification theatre |
| Hypothesis H1 updated | 2026-08-11 | Status -> confirmed WITH CORRECTIONS. All five walls verify; none falsified. Three statements were imprecise: W3 needs >=4 alternatives (not >=3); W5 is CONDITIONAL on an empty core and assumes an institution-free environment (so institutions can bound the chaos -- a solution lever, not just a risk); W1's escape route via dropping Pareto is closed by Wilson (1972). No committed design bound invalidated. |
| Hypothesis H2 updated | 2026-08-11 | Status -> FALSIFIED. The Henry George theorem's self-financing equality cannot be invoked for a colony: 5 conditions fail (free inter-jurisdictional mobility, optimal-size city, no congestion, identical agents, public-goods-as-sole-agglomeration-cause), and the first is a load-bearing ABSENCE of this polity. Canonical source is Arnott & Stiglitz QJE 93(4):471-500 (1979), not 'Stiglitz 1977'. Design revised per DF2: fiscal base retained on FACTOR INELASTICITY grounds; coverage is now measured (umbrella H4), not derived. |
| Hypothesis H3 updated | 2026-08-11 | Status -> confirmed for Chamley-Judd (OVERTURNED within its own models, stronger than 'contested') and Dunbar (live dispute); REFINED for Milgram (behaviour replicates, mechanism + reporting integrity contested -- the blanket flag was too coarse and had discarded a usable finding); Limits to Growth NOT CHECKED, stays flagged-unverified. |
| DF3 -- memo tier is CITED, not quote-verified | 2026-08-11 | All five memos carry named primary sources with volume/page but NO per-URL WebFetch verbatim-quote pass. Say 'cited', never 'verbatim verified'. The /research-verify pass is a named follow-on. |
<!-- project-state:end:decisions-made -->
### Pending Decisions
| Decision | Proposer | Blocker | Notes |
|---|---|---|---|
| Whether to run C3 (breadth-first discovery sweep) before verification | claude | none | costs ~1 wk; tests H4, which the enumerated-claims framing cannot |
<!-- project-state:end:pending-decisions -->

## Bellman-Inspired Decision Frame
### Current state (one-line summary)
`docs/foundations-canon-map.md` written (12 walls, 6 literatures, 8 framework forks, 12-item verification queue) at DISCOVERY tier; one claim (G–S) promoted to audit-tier via WebSearch; zero `/research` memos written.

### Target state / terminal condition
See ## MVP Criteria — supported memos for V1, V2, V4, V5 plus a confirmed-contested record for V12.

### Progress proxy
- **MVP bar:** 5 / 5 criteria met (see `## MVP Criteria`) — bar REACHED 2026-08-11
- **v0.1 metric:** `unknowns-retired` count + `gates-passed` count
- **v0.2+:** weighted combination (TBD)

### Candidate next actions
| # | Action | Class | Expected progress | Expected info gain | Uncertainty | Cost |
|---|---|---|---|---|---|---|
| 1 | /research V1 (the five walls) | research | medium | high (largest correctness risk) | low | medium |
| 2 | /research V2 (Henry George / LVT) | research | medium | high (whole fiscal department) | medium | medium |
| 3 | /research V4 (Fuller) | research | medium | medium (cheapest implementable) | low | low |
| 4 | /research V5 (space law) | research | medium | high (property regime legality) | medium | medium |
| 5 | C3 breadth sweep to test H4 | research | low | high (unknown unknowns) | high | medium |
<!-- project-state:end:candidate-actions -->

### Re-evaluation trigger
- **Default:** re-run `/project-state` after any action class fires
- **Manual override:** `/project-state aigov-foundations`

## Allowed Action Classes (v0.2 placeholder — not enforced in v0.1)
- `propose` · `research` · `write-plan` · `edit-local-code` (requires approval) · `run-tests` · `ask-user` · `stop`

## Action Log
| # | Date | Action class | Description | Outcome |
|---|---|---|---|---|
| 1 | 2026-08-11 | propose | /project-init protocol executed by hand (family seed) | ledger created |
| 2 | 2026-08-11 | research | WebSearch: Gibbard-Satterthwaite exact statement + preconditions | V1-partial promoted to audit-tier; Arrow-conflation error recorded |
| 3 | 2026-08-11 | edit-local-code | Added an N/M MVP-bar fraction to ### Progress proxy; prior version in git history | 0 / 5 — terminal_met now machine-readable by advance_ranker (was unknown-by-absence) |
| 4 | 2026-08-11 | research | WebSearch V1: Arrow, Gibbard-Satterthwaite, Sen, McKelvey-Schofield, Black, Ashby -- exact statements + preconditions | 5 walls CITED; 3 corrections; wrote research_outputs/aigov-v1-social-choice-walls.md |
| 5 | 2026-08-11 | research | WebSearch V2: Henry George theorem conditions + LVT efficiency | H2 FALSIFIED for a colony; source corrected to Arnott & Stiglitz QJE 1979; wrote aigov-v2-land-value-tax-henry-george.md |
| 6 | 2026-08-11 | research | WebSearch V4: Fuller's eight desiderata exact list | implementation matches 8/8; two doc caveats added; wrote aigov-v4-fuller-legality-desiderata.md |
| 7 | 2026-08-11 | research | WebSearch V5: OST Art. II/VI, US 2015 Act, Luxembourg 2017 law | K7 survives on the in-place/extracted distinction; NEW finding: Art. VI => derivative authority; wrote aigov-v5-space-law-property-envelope.md |
| 8 | 2026-08-11 | research | WebSearch V12: Chamley-Judd, Dunbar, Milgram contested-status check | 3 of 4 confirmed contested in 3 different ways; Milgram flag corrected; Limits to Growth NOT checked; wrote aigov-v12-contested-set.md |
| 9 | 2026-08-11 | edit-local-code | Applied findings to code+docs: charter clause C25 (OST Art. VI disclosure duty), canon-map corrections, Fuller apartheid caveat in the generated charter | 88 tests pass; checkable fraction 0.7083 -> 0.68 (25 clauses, 17 enforced) -- honest fall, recorded |
<!-- project-state:end:action-log -->

## Open Questions for User
- MVP bar is PROPOSED under the execute-mode exception and is deliberately narrower than "verify all twelve" — redirect if the full twelve should gate.
- Whether to spend ~1 week on the C3 breadth sweep first. It is the only action that can test H4 ("nothing decisive was missed"), which the enumerated-claims framing structurally cannot.

## Last Evaluation (v0.2 placeholder — not enforced in v0.1)
- **Date:** 2026-08-11
- **Progress signal:** (init only; V1 partially advanced)
