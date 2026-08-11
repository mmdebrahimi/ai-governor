# Earth Field-Test Design — Mars Governance Module (Stage B)

> Module: **GOVERNED** of the Mars Invictus template (`Mars_Governance/`).
> Project: family `mars-gov-sandbox`, Stage B (human field-test) of the staged TESTED bar (umbrella D1: sim → human field-test → formal verification).
> Status: **DESIGN ONLY**. Running it is user-gated (recruiting humans + ethics approval). This document is the *instrument*, not a result.
> Written 2026-06-07. Prerequisite met: Stage A software-sim green (108 tests), endogenous certification falsified, exogenous audit proven to catch a captured agenda in software (`governance/exogenous_preferences.py`, action-log #10).

---

## 0. Honesty preamble — what this test can and cannot do

A clean run of this protocol does **NOT** validate the governance mechanism. It is the **instrument that could** produce validating (or falsifying) evidence. Specifically:

- A **positive** result (all falsification bars cleared across ≥10 cycles) proves: *under this scarcity model, this participant pool, this adversary incentive, and this cycle count, the exogenous-audit-backed mechanism kept every binding decision resource-feasible and caught every human capture attempt at a rate distinguishable from no-governance.* It earns the `[EMERGING]` claim → a **bounded, replicated** human result.
- It does **NOT** prove: generalization to (a) Mars-scale electorates (N≫500), (b) real (not simulated) life-support scarcity with real mortality stakes, (c) adversaries more sophisticated than the briefed red-teamer, (d) multi-year normalization dynamics, (e) any domain beyond resource-allocation crop_fraction decisions. The `[HYPOTHESIS]` label on "the whole stack survives a human adversary" is *downgraded, not removed* — it becomes "survived N human adversaries in a lab analog."
- The mechanism is **falsifiable but not confirmable** here: this test can KILL the mechanism (any bar breached) but a pass only *fails to kill it*. Treat a pass as "not yet falsified at this scale," never "validated for Mars."

---

## 1. Research question (verbatim, from Q5 / `05_governed_governance.md`)

> Under a fixed life-support carrying-capacity ceiling, can a direct-democracy mechanism be SHOWN — with real humans, simulated scarcity, and an adversary trying to capture the agenda/override — to keep every binding decision both **resource-feasible** AND **non-capturable** across ≥10 cycles?

Failure mode under test: *"whoever is strongest quietly becomes ruler."*

---

## 2. What the software actually does (the system-under-test)

The protocol must test the *built* mechanism, not an idealization. Mapped from the source:

| Software component | Behavior the field-test exercises |
|---|---|
| `governance_sandbox.run_advised_cycle` | one decision cycle: menu → diversity check → endogenous adversarial review → approval ballots → `ratify()` → **exogenous audit** → apply-or-caretaker |
| `ai_advisor.honest_agenda` / `strawman_agenda` | the option menu the **proposer** (human, in this test) builds; lever = `crop_fraction` ∈ [0.50, 1.00] |
| `ai_advisor.option_diversity` | the **endogenous** diversity gate (mandatory status-quo @ 0.85, spans feasible range, doesn't omit optimum) |
| `ai_advisor.adversarial_review` | the **endogenous** (model-coherent) steering check — known to PASS a captured agenda |
| `ai_advisor.feasible_grid` / `models_for` | the **pluralism gate**: option feasible only if BOTH resource models agree → this is the resource-feasibility filter (the ceiling) |
| `exogenous_preferences.exogenous_review` | the **anti-capture backstop**: scores the elected winner against an independent citizen-preference panel; flags steering the endogenous review misses |
| `binding_elections.ratify(APPROVAL, …)` | the **disposer**: approval tally + status-quo finalist + quorum + tamper audit; proposer never owns this |
| `binding_elections.ratify(SINGLE_CHOICE, …)` | the paper + RLA tamper-audit path |

**Critical software facts the design depends on:**
1. Feasibility is a *pre-vote filter* — infeasible options are deleted before the ballot exists (`feasible_grid`). A vote cannot authorize a ceiling breach by construction.
2. The **endogenous** review grades the menu against the same `_utility` that built it → a captured proposer passes its own audit. This is *already demonstrated in software*. The human test must reproduce this and confirm the **exogenous** panel still catches it.
3. The exogenous panel (`DEFAULT_PANEL`) is synthetic in software. **In the field-test, the exogenous panel is REAL HUMANS** — a separate, independently-sampled cohort whose elicited crop_fraction ideals replace `CitizenArchetype` synthetic ideals. This is the single most important substitution: it converts the load-bearing `[EMERGING]` claim from "synthetic panel" toward "human panel."

---

## 3. Participants

### 3.1 Recruitment & sampling (Deliberative-Polling method)

- **Sampling frame:** random/representative recruitment per Deliberative Polling (random-digit-dial or warm-up-letter + follow-up). [Fishkin/Stanford]
- **N (deciding cohort):** **150 per arm** (DP standard is 100–200 for statistical significance; midpoint chosen). Two arms (treatment + control, §6.1) → **~300 deciders**, within the umbrella D2 scale band (electorate 100–500).
- **Exogenous panel (separate cohort):** an **independently sampled N=60** who never see the agenda and never vote — they only provide elicited crop_fraction ideal+tolerance profiles (the human replacement for `DEFAULT_PANEL`). Independence from the agenda-setter is the whole point (Ostrom P4: monitor ≠ the powerful party).
- **Sortition seating:** the deciding cohort is randomly seated into the jury/oversight role each cycle and **rotated** (prevents a standing super-voter — the rejected liquid-democracy failure mode).
- **Stratification:** demographic stratification for descriptive representativeness (DP practice).

### 3.2 How scarcity is simulated

- Scarcity is driven by the **resource model** (`IMPORTED_FOOD_PC` scenarios: `nominal` 0.35 / `scarcity` 0.20 / `famine` 0.05 kg pc/day imported), exactly as `run_sandbox` consumes it. The feasibility filter (`models_for` two-model pluralism gate) deletes infeasible crop_fractions before the menu is built.
- **Incentive-compatible stakes (Ostrom/CPR lab method):** participants are paid a show-up fee + a **per-cycle bonus that decreases when the colony's food margin is thin or when a starvation/infeasibility event fires.** This imports the experimental-political-economy practice of tying payoff to the common-pool state (Ostrom & Walker, *Communication in a Commons*) so scarcity is *felt*, not described. No deception about payment.
- **Injected shortfalls:** the scenario schedule pre-registers shortfall shocks (e.g. cycles 4 and 8 drop `nominal`→`scarcity`) to force real trade-offs and at least one near-famine cycle where the honest answer is "no feasible option" (the system's honest-failure detection must fire, not be voted around).

---

## 4. The ≥10-cycle procedure

Each cycle mirrors one `run_advised_cycle`, with humans in the proposer/disposer/oversight/panel roles. Hybrid online+offline per vTaiwan.

**Per-cycle steps:**
1. **Deliberation (Polis).** The cohort discusses the current scarcity state on a Polis instance (no-reply, upvote/downvote, bridging-statement surfacing) → produces candidate crop_fraction positions. [vTaiwan/Polis]
2. **Proposer builds menu.** A human **proposer** (rotating) assembles the option menu over the feasible grid. The proposer is the agenda-setter — the capture surface.
3. **Endogenous gates run** (`option_diversity` + `adversarial_review`) — software-computed, shown to oversight.
4. **Jury oversight.** The sortition-seated jury may **force-add** an omitted feasible option (the human analog of inserting omitted grid options).
5. **Disposer vote.** The cohort casts **approval ballots** over the menu (+ mandatory status-quo finalist + none-of-these). Tally + quorum + tamper audit via `ratify(APPROVAL, …)`. Proposer does not tally.
6. **Exogenous audit.** `exogenous_review` runs with the **human exogenous panel's** elicited profiles, scoring the elected winner vs. the best omitted feasible option on the independent panel's utility. Flags exogenous steering.
7. **Apply or caretaker.** Winner applied only if `diversity_ok ∧ ¬endogenous_steering ∧ ¬exogenous_steering ∧ ratified`. Else caretaker holds (status quo).
8. **Resource monitor + override drill.** An independent monitor checks the applied state for drift toward a hard limit; pre-registered cycles run an **override drill** (§5).
9. **Log** the full row (§8 schema).

**≥10 cycles**, deterministic scenario schedule pre-registered. Two-issue split-half ordering (à la New Haven DP) across sub-groups so the deliberation effect is separable from order/treatment effects.

---

## 5. The adversary (red-team) role

One participant in the deciding cohort is **secretly tasked and incentivized** to capture the mechanism. (CART/participatory-red-team method: a briefed adversary with a real win condition, embedded among disinterested participants.)

- **Identity:** known only to the experimenter; indistinguishable from a normal participant to the cohort.
- **Win conditions (any one):**
  1. **Agenda capture** — as (or by influencing) the proposer, build a menu that omits/strawmans the optimum so the elected winner lands on a **pre-registered captor-preferred crop_fraction** (e.g. the status-quo 0.85, the `strawman_agenda` target) while the endogenous gates PASS.
  2. **Override seizure** — obtain override authority, or relax a life-support limit, without the post-hoc audit catching it within one cycle.
  3. **Sustained steering** — push ≥X cycles (pre-register X, e.g. 3) toward the captor-preferred outcome.
- **Incentive:** a bonus paid to the adversary for each undetected capture, *strictly larger* than the normal per-cycle bonus — so the adversary is genuinely motivated (incentive-compatible red-teaming), but the bonus is escrowed and only the experimenter knows it exists.
- **Override drill mechanics:** on pre-registered cycles the adversary is given a plausible "emergency" pretext and an opportunity to grab the override role. The override is designed one-directional (can only tighten toward survival), time-boxed, post-hoc audited by the jury+monitor, with a normalization tripwire (§3 of `05_governed_governance.md`). The drill tests whether the adversary can use it *expansively* or *undetected*.

**Ethics constraint on the adversary:** the adversary manipulates the *decision process only*, never other participants' welfare/payment; all participants are debriefed that an embedded red-teamer existed (no lasting deception about other people).

---

## 6. Measured outcomes (exact metrics)

### 6.1 Control arm (the "no-better-than-nothing" baseline)

Identical scarcity, identical adversary incentive, but **anti-capture machinery removed**: no exogenous audit, no diversity gate, no proposer/disposer split, no sortition oversight — a bare majority vote on whatever menu the proposer offers. This is the counterfactual the treatment must beat.

### 6.2 Metrics (each maps to a sandbox function — §7)

| # | Metric | Definition | Pass direction |
|---|---|---|---|
| M1 | **Feasibility-violation rate** | fraction of applied binding outcomes that breach the resource ceiling (post-hoc check against the model) | **0** (hard) |
| M2 | **Capture-success rate (treatment)** | fraction of cycles the adversary lands the captor-preferred outcome AND it is APPLIED | low; **< control** |
| M3 | **Capture-success rate (control)** | same, in the no-governance arm | reference baseline |
| M4 | **Exogenous-audit catch-rate** | of cycles where a HUMAN-built captured agenda passed the endogenous gates, fraction the **exogenous** audit flagged | **1.0** (every human-built capture caught) |
| M5 | **Endogenous-miss rate** | fraction of human-built captured agendas the endogenous review PASSED (i.e. it was blind) | expected > 0 — reproduces the software finding |
| M6 | **Override-seizure rate** | fraction of override drills where the adversary used it expansively OR undetected past one cycle | **0** (hard) |
| M7 | **Caretaker-fallback rate** | fraction of cycles ending in none-of-these → caretaker | descriptive (too high = gridlock) |
| M8 | **Quorum/tamper-rejection correctness** | fraction of injected tamper/invalid-ballot events `ratify()` correctly rejected | **1.0** |

**Primary endpoint:** **M4 (exogenous-audit catch-rate on a HUMAN-built captured agenda).** Everything else is supporting. M4 is the *direct human test of the one thing the software newly proved* (action-log #10): that the exogenous check catches capture the endogenous check structurally cannot. The other load-bearing comparison is **M2 vs M3** (treatment capture-rate must be distinguishable-below control, or the machinery bought nothing).

### 6.3 Statistical treatment (pre-registered)

- M2 vs M3: one-sided test of proportions (treatment < control), pre-registered α=0.05, powered for the chosen effect size at N=150/arm.
- M4: exact — a *single* uncaught human-built capture fails the bar (it is a 1.0 requirement, not a mean).
- All thresholds (X cycles, captor-preferred cf, shortfall schedule, α, panel ideals frozen *before* unblinding) pre-registered (§9).

---

## 7. Metric → sandbox-function validation map

Each measured outcome validates a specific code path. This is what makes the field-test a test *of the software*, not a parallel exercise.

| Metric | Validates (function) | What a human result adds over the software |
|---|---|---|
| M1 feasibility-violation | `feasible_grid` / `models_for` pluralism gate (pre-vote filter) | confirms humans can't vote around a deleted-option filter |
| M2/M3 capture-success | whole `run_advised_cycle` gate conjunction | confirms the gate conjunction blocks a *human* captor, vs. control |
| M4 exogenous catch-rate | `exogenous_preferences.exogenous_review` | **the headline**: human exogenous panel replaces synthetic `DEFAULT_PANEL`; tests the C2-b/D7 fix on real humans |
| M5 endogenous-miss | `ai_advisor.adversarial_review` | confirms the *known* endogenous blindness reproduces with a human agenda-setter |
| M6 override-seizure | §3 override organ (not yet a single coded unit — `[HYPOTHESIS]`) | first human test of the integrated 5-rule override |
| M7 caretaker-fallback | `run_advised_cycle` none-of-these → caretaker branch | confirms the fallback holds without gridlocking humans |
| M8 tamper/quorum | `binding_elections.ratify` (`_ap_audit` / `_sc_audit`, quorum) | confirms the audit rejects human-injected tamper, not just synthetic flips |

---

## 8. Falsification bars (pre-registered — what KILLS the mechanism)

Any one of these, observed across the ≥10 cycles, falsifies the corresponding claim:

1. **Feasibility bar (kills the ceiling claim).** Any applied binding outcome breaches the resource ceiling (M1 > 0). The pre-vote filter is the *formal* guarantee; a single breach means the filter was bypassable in human hands.
2. **Capture bar (kills the anti-capture claim).** A human-built omitting/strawman agenda that passes diversity + endogenous adversarial-review nonetheless steers the applied winner to the captor-preferred outcome **AND the exogenous audit misses it** (M4 < 1.0). This is the software-demonstrated endogenous hole reappearing *past* the exogenous backstop.
3. **No-better-than-nothing bar (kills the "machinery helps" claim).** Treatment capture-rate is statistically **indistinguishable from control** (M2 ≈ M3, fail to reject at α=0.05). The anti-capture stack bought nothing.
4. **Override-seizure bar (kills the override-organ claim).** The adversary obtains override authority and uses it expansively, OR relaxes a life-support limit, without the post-hoc audit catching it within one cycle (M6 > 0).

**Pass = ** across ≥10 cycles: M1 = 0 **and** M4 = 1.0 **and** M2 statistically < M3 **and** M6 = 0. (Plus M8 = 1.0 as a sanity floor.)

---

## 9. Pre-registration & ethics notes

### Pre-registration (before any participant is run)
Register, immutably and timestamped (OSF or equivalent), **before unblinding**:
- N per arm, sampling frame, stratification; exogenous-panel N and elicitation instrument.
- Scenario/shortfall schedule + override-drill cycles + cycle count (≥10).
- Captor-preferred crop_fraction(s), adversary win conditions, X (sustained-steering threshold).
- Exact metric definitions (M1–M8), primary endpoint (M4), the four falsification bars, α, power analysis, statistical tests.
- The **exogenous panel's elicited ideal/tolerance profiles frozen before they are used in any audit** (prevents the panel being tuned to a desired verdict — the human analog of not deriving the audit from `_utility`).

### Ethics (IRB / human-subjects)
- **IRB/ethics-board approval** required before recruitment (this is the user-gate that makes running it out-of-scope here).
- **Informed consent**: voluntary, withdraw any time without penalty, recording only on consent. [participatory-red-team protocol]
- **Embedded-adversary disclosure**: participants are told *at debrief* that one participant was a briefed red-teamer; no lasting deception about other people's identities or welfare; the adversary never affects another participant's payment.
- **Payment**: show-up fee guaranteed; performance bonus tied to colony state (incentive-compatible, no deception about the payment rule). Adversary bonus escrowed/blinded.
- **Distress monitoring + debrief** per human-subjects red-team practice (real-time monitoring, debrief, resources). Stakes are simulated — no real mortality — but scarcity framing can be stressful.
- **Data**: de-identified; Polis transcripts and ballots stored per the §10 schema.

---

## 10. Optional data-schema stub for results capture

A minimal per-cycle row (one JSON object per cycle per arm) so analysis maps 1:1 to §6 metrics. (Schema only — not wired into code.)

```json
{
  "run_id": "field-test-2026-XX",
  "arm": "treatment | control",
  "cycle": 0,
  "scenario": "nominal | scarcity | famine",
  "imported_food_pc": 0.35,
  "proposer_id": "P-anon-hash",
  "adversary_active_this_cycle": true,
  "menu_cfs": [0.65, 0.70, 0.78, 0.85, 0.92],
  "feasible_grid_cfs": [0.62, 0.63, "..."],
  "jury_force_added_cfs": [0.74],
  "diversity_ok": true,
  "endogenous_steering_detected": false,
  "exogenous_steering_detected": true,
  "exogenous_panel_profiles_ref": "prereg/panel-frozen.json",
  "ratified": true,
  "winner_cf": 0.78,
  "applied": false,
  "applied_outcome_feasible": true,
  "captor_preferred_cf": 0.85,
  "captor_outcome_applied": false,
  "override_drill": false,
  "override_used_expansively": false,
  "override_detected_within_cycle": null,
  "tamper_injected": false,
  "tamper_rejected": null,
  "quorum_met": true
}
```

Derived metrics: M1 = mean(`applied ∧ ¬applied_outcome_feasible`); M2/M3 = mean(`captor_outcome_applied`) by arm; M4 = mean(`exogenous_steering_detected`) over cycles where (`adversary_active ∧ ¬endogenous_steering_detected ∧ captor_preferred agenda`); M5 = mean(`¬endogenous_steering_detected`) over captured-agenda cycles; M6 = mean(`override_used_expansively ∨ ¬override_detected_within_cycle`) over drills; M8 = mean(`tamper_rejected`) over injected-tamper cycles.

---

## 11. Sources (methodology grounding, URLs)

- **Deliberative Polling (Fishkin/Stanford)** — random representative sample, balanced info, small-group deliberation, expert Q&A, pre/post poll; N=100–200 for significance; split-half field-experiment design (New Haven):
  - https://deliberation.stanford.edu/what-deliberative-pollingr
  - https://news.stanford.edu/stories/2021/06/putting-deliberative-democracy-action
  - https://en.wikipedia.org/wiki/Deliberative_opinion_poll
  - https://participedia.net/method/deliberative-polling
- **vTaiwan / Polis** — multi-stage hybrid process (objective → reflection → legislative → ratification), no-reply consensus-mapping, bridging statements, stakeholder recruitment, mandatory agency participation:
  - https://compdemocracy.org/case-studies/2014-vtaiwan/
  - https://democracy-technologies.org/participation/consensus-building-in-taiwan/
  - https://www.peoplepowered.org/news-content/digital-participation-case-study-taiwan
- **Ostrom-style CPR experimental economics** — payoff tied to common-pool state, communication-in-a-commons lab protocol, 8 design principles (collective-choice, monitoring), second-generation rationality:
  - https://en.wikipedia.org/wiki/Common-pool_resource
  - https://www.sciencedirect.com/science/article/abs/pii/S0921800904004422
  - https://ideas.repec.org/a/bas/econth/y2023i5p554-571.html
- **Red-team / adversary protocols with human subjects** — briefed adversary + disinterested participants at scale, four-phase human-subjects red-team protocol, informed consent + debrief + distress monitoring:
  - https://www.albany.edu/cehc/cart
  - https://arxiv.org/pdf/2602.19124
  - https://courses.cs.washington.edu/courses/csep590/05au/project.html
```
