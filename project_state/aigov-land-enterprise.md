# AI Governor — Land Enterprise Instance (F13)

<!-- project-schema: 0.1 -->

> Initialized 2026-08-12. Project ID: aigov-land-enterprise. Originating goal (verbatim user input): "Apply the governance instrument to the family land enterprise: elicit the decisions the enterprise actually faces, derive its retained capabilities, accountable roles and data needs, and run capital and management choices through a governed loop instead of ad hoc judgement".

> **PRIVACY — STANDING, NON-NEGOTIABLE, READ BEFORE WRITING ANYTHING HERE.**
> This ledger lives in a **PUBLIC** repository (github.com/mmdebrahimi/ai-governor). Family
> composition, ages, names, capital position, amounts, property holdings and specific locations
> **NEVER** enter this file or any other file in this repo. Accountability is recorded as a **ROLE
> or an unfilled SLOT**, never a person. Decisions are recorded by **SHAPE** ("whether to acquire a
> parcel in a given jurisdiction"), never by instance ("whether to buy X for $Y"). The elicited
> inventory carrying real specifics lives OUTSIDE this repo — see Open Questions.

## Project Context
- **Project ID:** aigov-land-enterprise
- **Project root:** C:\Users\Farshad\PythonProjects\Skill_Development\AI_Governor
- **Captured:** 2026-08-12
- **Originating goal:** Apply the governance instrument to the family land enterprise: elicit the decisions the enterprise actually faces, derive its retained capabilities, accountable roles and data needs, and run capital and management choices through a governed loop instead of ad hoc judgement
- **Refined goal (from 3c top-ranked candidate):** Complete a decision inventory of the land enterprise covering at least 15 real recurring decisions with all four sourcing inputs answered, producing at least one ConfirmedCapability, an accountable role slot per decision, and a NAMED list of every remaining gap
- **Horizon (months):** 12
- **Schema:** project-schema 0.1
- **Relationship to the rest of the portfolio:** this is the **first real instance** of the V2 north star. The Mars families (F0-F12) are the SANDBOX that proved the machinery; they are FROZEN as of 2026-08-12 by user decision. Machinery that transfers: `aigov/decisions.py`, `aigov/panel.py`, `aigov/seats.py`, the contract invariants, the no-invented-numbers rail. Machinery that does NOT transfer: anything denominated in kPa, m^3 or kW.

## Empirical Concerns
- **Verdict:** FLAG
- **Check status:** skipped-by-flag
- **Provisional:** YES
- **Findings:** The goal embeds a MECHANISM claim, not merely an intention: that an organisation's retained capabilities can be DERIVED from an inventory of the decisions it faces. That claim rests on Coase 1937, Williamson's asset specificity, and Galbraith's information-processing view of organisation design, all of which are sound economics — but the specific derivation implemented here is an engineering bet, not an established result, and it has already produced three confirmed defects when run (transitive clustering, cheap-fact grouping, a test that pinned the defect as correct). FLAG rather than PASS because `--no-web-check` opted out of confirming the method against fresher sources; LLM training knowledge detected no factual error but cannot certify the method.

## Project vs Research-Program
- **Verdict:** FAIL
- **Provisional:** NO
- **Classification:** hybrid
- **Rationale:** BOUNDED components — elicit the decisions, derive retained capabilities, produce accountable role slots, derive the data needs. Each has a checkable completion state. UNBOUNDED component — "run capital and management choices through a governed loop" describes a permanent OPERATING STATE, not a deliverable; it has no terminal condition and would never be finishable. The bounded part is the project; the unbounded part is what the project makes possible.

## Refinement Candidates
- **Verdict:** FAIL
- **Provisional:** YES
- **Refined-from:** originating-goal
- **Candidates:** (1) TOP-RANKED — Complete a decision inventory covering at least 15 real recurring decisions with all four sourcing inputs answered, producing at least one ConfirmedCapability and a NAMED list of every remaining gap. (2) Produce an accountable ROLE slot for every decision in the inventory, including the MARKET-sourced ones, with zero unfilled at close. (3) Derive the data and instrumentation list: every fact the inventory says must be KNOWN, classified transferable-record / organization-specific / tacit, with an acquisition route named for each. (4) Run ONE real capital-allocation decision end to end through elicit, sourcing verdict, assurance level and recorded decision. CAVEAT (3a FLAG): all four candidates presume the derivation method is sound; candidate 4 is the one that would actually falsify it.

## Goal Hierarchy

> PROVISIONAL — see Open Questions for User

### Long-term (12+ months tier)
The land enterprise runs its recurring capital and management decisions through a governed loop: what must be known is derived from what must be decided, structure is derived rather than imported, and decision authority stays with the family.

### Mid-term (3-12 months)
| # | Milestone | Success Criterion | Horizon |
|---|---|---|---|
| 1 | Decision inventory elicited | at least 15 recurring decisions recorded, all four sourcing inputs answered on each, zero UNDECIDABLE remaining unnamed | 1-2 months |
| 2 | Structure derived, not chosen | at least one ConfirmedCapability from affirmed pairs; every ungrouped link reported for human grouping rather than auto-merged | 2-3 months |
| 3 | Accountability complete | an accountable ROLE for every decision including MARKET ones; zero unfilled slots at close | 3-4 months |
| 4 | Data needs derived | every must-know fact classified by kind with a named acquisition route; the instrumentation list falls out of this, not out of a template | 4-6 months |
| 5 | First governed decision | one real capital-allocation choice run end to end and recorded with its derivation | 6-9 months |

### Short-term (≤1 month)
| # | Action | Class | Owner | Horizon |
|---|---|---|---|---|
| 1 | Correct the 18 drafted entry decisions, then answer them into a private answers file | ask-user | user | 1-2 hrs |
| 2 | Choose where the private answers file lives outside this public repo | ask-user | user | same day |
| 3 | Run `--answers <path>` on the filled file and read the derived verdicts | run-tests | claude | minutes |
| 4 | Split any decision the instrument refuses as compound, and re-run | ask-user | user + claude | same day |
| 5 | Answer the coupling questions the retained set surfaces | ask-user | user | 1 wk |
| 6 | Report derived capabilities, ungrouped links, unowned decisions and named gaps | propose | claude | 1 wk |

## State Snapshot

### Assumptions
- The decision-inventory method derives structure that is actually usable — confidence: **medium** (sound theory, three defects already found and fixed by running it, never yet run on a real inventory)
- The user can name at least 15 recurring decisions without prompting from a template — confidence: **high**
- Enough decisions will share ORGANIZATION-SPECIFIC or TACIT facts to produce at least one affirmed coupling — confidence: **medium**, and candidate 4 is what tests it
- A multi-country operation raises jurisdiction-specific decisions that do NOT generalise across parcels — confidence: **high**
- Structure derived for this enterprise will not transfer to another enterprise — confidence: **high**, and that is the design intent, not a limitation

### Evidence
| # | Claim | Source | Confidence | Captured |
|---|---|---|---|---|
| 1 | Isomorphic mimicry is the documented standard failure of institutional reform; adopting the FORM without the function | Andrews/Pritchett/Woolcock via research_outputs/aigov-v14-governance-history-and-mechanisms.md | high | 2026-08-12 |
| 2 | An LLM is exceptionally good at producing a conventional department list, therefore exceptionally good at that failure | V14 memo, section on the anti-mimicry rail | high | 2026-08-12 |
| 3 | Running the derivation on a realistic inventory found 3 defects the green test suite did not | this repo, 2026-08-12 run | high | 2026-08-12 |
| 4 | Persona prompts change style but not judgment; model heterogeneity is the real decorrelation lever | research_outputs/aigov-v15-persona-panels-and-model-diversity.md | high | 2026-08-12 |
<!-- project-state:end:evidence -->

### Unknowns
- Which decisions the enterprise actually faces — the entire point of milestone 1, and unanswerable from here
- Whether any two decisions are genuinely coupled, which only the user can affirm
- What the enterprise already knows versus what it would have to start measuring
- Which decisions are already effectively bought in (advisors, agents, managers) without anyone having decided to buy them
- Whether jurisdiction differences fragment the inventory into per-country sub-inventories

### Hypotheses (Active)
| ID | Statement | Status (open/under-investigation/falsified/confirmed) | Last-tested |
|---|---|---|---|
| H1 | At least 15 recurring decisions can be elicited without offering a template | open | never |
| H2 | At least one pair of decisions will be affirmed as genuinely coupled, producing a ConfirmedCapability | open | never |
| H3 | The derived structure will NOT resemble a conventional department list (finance, operations, legal, HR) | open | never |
| H4 | A majority of must-know facts will be TACIT or ORGANIZATION-SPECIFIC rather than transferable records | open | never |
| H5 | At least one decision currently treated as internal will come out MARKET on the Coase test | open | never |
<!-- project-state:end:hypotheses -->

### Decisions Made
| Decision | Date | Notes |
|---|---|---|
| Seeded as family F13, the first REAL instance of the V2 north star, after the user corrected a drift into Mars-sandbox work | 2026-08-12 | The umbrella family table contained 13 Mars phase-1 families and zero Earth families, so the code-owned advance_ranker structurally could not surface farm work. This ledger fixes that. |
<!-- project-state:end:decisions-made -->

### Pending Decisions
| Decision | Proposer | Blocker | Notes |
|---|---|---|---|
| Where the PRIVATE elicited inventory lives, given this repo is public | claude | user ratification | drafted position: the private Skill_Development repo, with only a pointer from here |
| Whether jurisdiction gets its own axis in the inventory or is just another elicited fact | claude | milestone 1 evidence | drafted position: elicited fact first; promote to an axis only if the inventory forces it |
<!-- project-state:end:pending-decisions -->

## Bellman-Inspired Decision Frame

### Current state (one-line summary)
Seeded 2026-08-12. Nothing elicited yet. The instrument itself is built and hardened — `aigov/decisions.py` derives retained capabilities from elicited affirmed pairs, refuses transitive chaining, refuses to group on transferable records, splits assurance from sourcing, and refuses a verdict on a compound decision; `docs/decision-inventory-protocol.md` is the session runbook. What is missing is the one thing no code can supply: the user's actual decisions.

### Target state / terminal condition
A decision inventory of at least 15 real recurring decisions with all four sourcing inputs answered; at least one ConfirmedCapability derived from affirmed pairs; an accountable ROLE for every decision including bought-in ones; every must-know fact classified by kind with an acquisition route; and every remaining gap NAMED rather than defaulted. The unbounded operating state (running every decision through the loop) is explicitly NOT the terminal condition.

### Progress proxy
- **v0.1 metric:** `unknowns-retired` count + `gates-passed` count (raw counts, unweighted)
- **v0.2+:** weighted combination of unknowns-retired, gates-passed, evidence-confidence-improved, hypotheses-falsified (TBD via v0.2 design)

### Candidate next actions
| # | Action | Class | Expected progress | Expected info gain | Uncertainty | Cost |
|---|---|---|---|---|---|---|
| 1 | Correct the 18 drafted entry decisions, then answer them into a private answers file | ask-user | high | highest | low | 1-2 hrs user time |
| 2 | Choose where the private answers file lives outside this public repo | ask-user | medium | low | low | same day |
| 3 | Run `--answers <path>` on the filled file and read the derived verdicts | run-tests | high | high | low | minutes |
| 4 | Split any decision the instrument refuses as compound, and re-run | ask-user | medium | medium | low | same day |
| 5 | Answer the coupling questions the retained set surfaces | ask-user | high | high | medium | 1 wk |
| 6 | Report capabilities, ungrouped links, unowned decisions and named gaps | propose | medium | high | low | 1 wk |
<!-- project-state:end:candidate-actions -->

### Re-evaluation trigger
- **Default:** re-run `/project-state` after any action class fires
- **Manual override:** user invokes `/project-state aigov-land-enterprise` at any time
- **Specific to this family:** re-evaluate immediately if the elicited inventory produces a structure that DOES resemble a conventional department list, because that is the signal the anti-mimicry rail failed

## Allowed Action Classes (v0.2 placeholder — not enforced in v0.1)
- `propose` — auto
- `research` — auto
- `write-plan` — auto
- `edit-local-code` — REQUIRES per-action human approval
- `run-tests` — auto if local + sandboxed
- `ask-user` — auto
- `stop` — auto

## Action Log
| # | Date | Action class | Description | Outcome |
|---|---|---|---|---|
| 1 | 2026-08-12 | propose | /project-init invoked | ledger created |
| 2 | 2026-08-12 | edit-local-code | Drafted 31 candidate decision SHAPES as aigov/instances/land_enterprise.py - questions only, every elicited field left unanswered | 31 candidates; 16-decision first-pass subset flagged; L22/L26/L31 flagged suspected-compound; no jurisdiction, amount, holding or person named |
| 3 | 2026-08-12 | edit-local-code | Added scripts/land_enterprise_inventory.py (report / --candidate-list / --interview-sheet / --first-pass) and generated both docs from it so they cannot drift from the code | docs/land-enterprise-decision-candidates.md + docs/land-enterprise-interview-sheet.md written; worksheet is 16 decisions x 9 questions |
| 4 | 2026-08-12 | run-tests | Ran build_inventory over the draft list and the full suite | 31/31 UNDECIDABLE with every missing field named - correct pre-elicitation state, 0 capabilities, is_complete False; 402 tests pass, 0 regressions |
| 5 | 2026-08-12 | ask-user | User ratified inventory scope: agri-venture ENTRY and PARTNER SELECTION only, not operating-farm decisions | First draft was mis-specified - no operating farm exists (venture is prospective) and the stated model is partnering with established in-country agribusinesses, so most operating decisions belong to the partner. Decisions Made row + goal supersession PARKED on the /project-state cwd gate |
| 6 | 2026-08-12 | edit-local-code | Rewrote aigov/instances/land_enterprise.py for the entry phase - 18 decisions, SCREENING vs COMMITMENT phase marker, operating draft preserved as OPERATING_CANDIDATES_DEFERRED | 18 candidates (6 SCREENING / 12 COMMITMENT); E02 and E15 flagged suspected-compound; no jurisdiction named - country list stays out of the public repo |
| 7 | 2026-08-12 | run-tests | Regenerated both docs from the entry set and ran the suite | 18/18 UNDECIDABLE with gaps named; privacy scan for candidate-country leakage clean; 402 tests pass, 0 regressions |
| 8 | 2026-08-12 | edit-local-code | Emit ba-beautify .docx as the read-facing deliverable for all three documents | ba-beautify parser drops every block before the first ## heading - candidates doc converted to an EMPTY docx (0 tables) and the policy library lost both rail headers; confirmed by executed kill-test, fixed in the generator by wrapping content in ## sections; all three rebuilt and re-verified |
| 9 | 2026-08-12 | run-tests | Exercised the decision instrument end-to-end on a synthetic fully-answered 18-decision entry inventory - a size no prior test reached (largest was 4) | 8 new tests, 402->410, 0 regressions; 10 MARKET / 4 INTERNALIZE / 4 HYBRID; 2 capabilities derived |
| 10 | 2026-08-12 | research | Measured the coupling-question count at full size against the predicted pairwise blowup | FORECAST MISS: predicted >20 questions and a usability wall; actual 7 vs a naive bound of 40, because coupling_candidates pairs only over RETAINED decisions - MARKET and UNDECIDABLE are excluded at source |
| 11 | 2026-08-17 | edit-local-code | Built the answers-intake path: aigov/answers.py + --answers / --answers-template on the inventory script | TOML (stdlib, read-only) keyed on worksheet wording not field names; omitted key = unanswered, never defaulted; load_answers REFUSES a path inside the public repo (exit 2 verified on the real CLI) |
| 12 | 2026-08-17 | edit-local-code | Refreshed the stale candidate-actions table - action 1 still said Claude should draft the list, which was already done | Direct-Edit + this mirror per AC9 (no /project-state op covers candidate-actions). 6 actions now reflect the real next moves; the ranker no longer points at completed work |
| 13 | 2026-08-17 | run-tests | Round-tripped the synthetic 18-decision inventory through the answers file and ran the real CLI on a partial file | 19 new tests, 410->429, 0 regressions; round trip reproduces every verdict and every elicited field; compound-refusal and no-market-INTERNALIZE both fire on the real surface |
| 14 | 2026-08-17 | edit-local-code | Refreshed the Goal Hierarchy short-term table, stale in the same way as candidate-actions | Direct-Edit + this mirror per AC9 (no /project-state op covers Goal Hierarchy; v0.5 --refresh-goal-hierarchy is the named gap). Both tables now agree on the same 6 next moves |
| 15 | 2026-08-17 | ask-user | E01 answered: family makes the call, market supplies the research; frequency is one batch pass per year across all candidates | Instrument DERIVED hybrid independently from the numbers - matching what the user described in their own words. 1 of 18 fully answered |
| 16 | 2026-08-17 | research | Built the jurisdiction screen bundle the user asked for - published ratings, land law, treaty coverage and repatriation across the candidate set | DISCOVERY tier, written to the private D: folder not the public repo. Headline: NO candidate permits foreign-controlled freehold of agricultural land - every route is a term of use, so treaty protection matters more than title. One candidate eliminated outright on a statutory ban |
| 17 | 2026-08-17 | research | Verified the bundle treaty and advisory claims against Global Affairs Canada and travel.gc.ca | Thailand FIPA confirmed in force since 1998-09-24 (drafted as unverified); Indonesia CEPA signed 2025-09-24 with ISDS pending ratification; Laos and Ethiopia CONFIRMED to have no treaty recourse; Indonesia advisory correction - high caution not normal precautions, Papua avoid-non-essential |
| 18 | 2026-08-17 | edit-local-code | Split E02 into E02a (what the regime permits - factual) and E02b (whether we will build on a term of use - authority) | 19 decisions; SUSPECTED_COMPOUND_IDS drops E02 and keeps E15; derivation is cleaner after the split - two capabilities, zero ungrouped |
| 19 | 2026-08-17 | run-tests | Patched both fixtures for the split and inspected the derivation | 3 failures - two mine, one was derive_capabilities correctly refusing a transitive bridge my fixture created. 429 pass, 0 regressions |
| 20 | 2026-08-17 | ask-user | E02b answered: FREEHOLD OWNERSHIP is a hard requirement, not a preference; security against appropriation is the primary criterion | DISQUALIFIES the entire 9-country candidate set - every one bars foreign-controlled freehold of agricultural land. Also elicited the use programme: long-rotation high-value trees, possible livestock, farm-automation experiments, and a central family residence doubling as a retreat/B and B. The tree rotation independently rules out 25-30 year leasehold on economics, so ownership is not a tradeable preference |
| 21 | 2026-08-17 | research | Re-aimed the jurisdiction screen from ownership-first after E02b disqualified the original candidate set | New candidate set where foreign private freehold of agricultural land IS available: Chile, Uruguay, Portugal, Paraguay, Costa Rica. Argentina/Brazil/Bolivia/Venezuela/Georgia excluded with reasons recorded so they are not re-proposed. Earlier bundle marked SUPERSEDED rather than deleted - a closed door is worth recording |
| 22 | 2026-08-17 | propose | Named three decisions the users programme needs that the drafted 19 do not cover | Which species programme to commit to (drives return more than the country does); whether to operate the hospitality business or let someone else run it; whether family members will be resident (changes visa, tax, safety weighting and who can hold an on-site accountable role) |
| 23 | 2026-08-17 | research | Answered the Israel question and researched the holding-structure / treaty-nationality interaction | Israel: ~93 percent of land is state/JNF held and LEASED 49-98 yrs, not sold; foreign nationals cannot lease it absent Law of Return eligibility; freehold is confined to the ~7 percent private Tabu land and agricultural land is the most restricted category; residential build on ag land needs 7-15+ yr rezoning. Fails the ownership requirement AND the residence-on-site requirement |
| 24 | 2026-08-17 | research | Established that investment-treaty protection follows the nationality of the investing ENTITY, not the passport | Directly reshapes E12: the liability plan (a separate local company per country) can DESTROY treaty protection because a local company owning local land is a domestic investor. Fix is a foreign holding above each local entity, which then needs substance to survive a denial-of-benefits clause, and must be in place BEFORE any dispute - treaty shopping accepted prospectively, refused retroactively |
| 25 | 2026-08-17 | edit-local-code | Added five decisions the elicited programme exposed that the drafted set did not cover | E19 species programme, E20 hospitality operate-or-contract, E21 family residence plus tax residence, E22 ORDER of residence change vs acquisition (Canadian departure tax crystallises gains), E23 how much substance each holding entity carries. 24 decisions total |
| 26 | 2026-08-17 | run-tests | Extended the synthetic fixture and added a guard test against future silent breakage | 430 pass, 0 regressions. Guard fails once with a named list when a decision is added upstream without a fixture entry - the fixture had been hand-patched three times, each surfacing as scattered KeyErrors. Derivation still clean: 2 capabilities, 0 ungrouped, pruning 61 naive to 16 asked |
<!-- project-state:end:action-log -->

## Open Questions for User
- **FLAG resolution needed for `Empirical Concerns`:**
  - Why it's flagged: the goal embeds a mechanism claim — that retained capabilities are DERIVABLE from a decision inventory. The economics behind it is sound; the specific implementation is an engineering bet that has already produced three defects when run, and `--no-web-check` opted out of confirming the method against fresher sources.
  - Recommended resolution: this does NOT need resolving before milestone 1. Refinement candidate 4 (run one real capital decision end to end) is the falsification test; treat the FLAG as retired only when that produces a decision the user would actually have made.
  - If it does not converge: the fallback is that the instrument is an interrogation aid rather than a derivation engine, which is still useful and much weaker than the current claim.
- **PRIVACY (needs a ratified answer before milestone 1):** where does the elicited inventory with real specifics live? This repo is public. Drafted position: the private `Skill_Development` repo, with only a non-identifying pointer recorded here. Alternative: a gitignored path inside this repo, which keeps it local but loses off-machine backup.
- **Scope of "the enterprise":** does the inventory cover the operating farm decisions only, or also the acquisition decisions that precede owning anything? Drafted position: BOTH, because acquisition decisions are the ones with the largest irreversibility and the atomicity gate will force them to be split properly.
- **Who else answers?** The inventory is only as good as who is in the room. Drafted position: start with the user alone; add others once the decision list is stable, since a second voice on a half-formed list produces argument rather than signal.

## Last Evaluation (v0.2 placeholder — not enforced in v0.1)
- **Date:** 2026-08-12
- **Progress signal:** (none yet — v0.1 init only)
