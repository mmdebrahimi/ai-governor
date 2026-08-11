# AI Government (`aigov`)

A constitutionally-bounded **AI Governor** plus pluggable **departments** that convert democratically-ratified
guidelines into a running, auditable institutional framework — designed and **TESTED in simulation before any
colony exists**. First instance: a Mars colony, electorate 100–1000.

**Status (2026-08-11):** three authority forks **ratified** — the AI is an *administrative organ* under human
sovereignty (never selects the objective, never amends its own constraints, never holds the exception); V1 scale
is **colony 100–1000**; the deliverable is a **runnable governed simulation**.

| Family | Bar | State |
|---|---|---|
| `aigov-foundations` (F0) | 5/5 | ✅ 5 cited memos; **one falsification** revised a committed design bound |
| `aigov-constitution` (F1) | 4/4 | ✅ 25-clause charter, four non-negotiable invariants, measured fraction **0.72** |
| `aigov-dept-contract` (F3) | 6/6 | ✅ contract + validator I1–I11 + mutation-proof |
| `aigov-collective-choice` (F6) | 4/4 | ✅ Mars_Governance organ vendored at full strength (193/193) |
| `aigov-guideline-intake` (F2) | 3/3 | ✅ sortition + quadratic budget + median elicitation, fail-closed |
| `aigov-twin` (F4) | 3/3 | ✅ the world: observability enforced, baselines reproduced, **can fail** |
| `aigov-kernel` (F5) | 3/3 | ✅ **the runtime — `apply()` cannot act un-gated** |

```bash
python -m pytest tests/ -q                      # 182 passed
cd aigov/choice && python -m pytest tests/ -q   # 193 passed (vendored collective-choice organ)
python -m aigov.render_charter                  # regenerate docs/charter.md from the enforcing code
```

The AI Governor now exists as a runnable object. Still missing: the **independent audit organ** (F9), the **adversarial suite** (F10) and the integrated ≥12-cycle run (F11). The kernel can non-steering-certify exactly **one** instrument today and refuses all others — a stated limit, not a gap. Nothing here is governance-validated — see **Honesty rails** below.

## Read in this order

| # | Document | What it settles |
|---|---|---|
| 1 | [`docs/idea-anchor-DRAFT-2026-08-11.md`](docs/idea-anchor-DRAFT-2026-08-11.md) | The framing + the 3 authority forks (**ratified 2026-08-11**) + the blunt critique |
| 2 | [`docs/foundations-canon-map.md`](docs/foundations-canon-map.md) | The 12 formal **walls** that bound what may be promised, the 6 literatures, the 8 framework forks (**V1/V2/V4/V5/V12 promoted to cited tier**) |
| 3 | [`docs/department-ontology.md`](docs/department-ontology.md) | The 16 departments derived from function + **the Department Contract (I1–I11)** — the anti-theater primitive |
| 4 | [`docs/decomposition-flowdown.md`](docs/decomposition-flowdown.md) | 12 families, requirements flow-down, critical path, VOI-ranked first moves |
| 5 | [`plans/AI_Governor_Phase1_Technical_Plan.md`](plans/AI_Governor_Phase1_Technical_Plan.md) | The ordered ~78-step path to the phase-1 bar, gate-classified |

## Project ledgers

| Ledger | Role | Gate |
|---|---|---|
| `project_state/aigov.md` | **umbrella** — families, flow-down, mission terminal | — |
| `project_state/aigov-foundations.md` | F0 — canon → audit-tier evidence | A |
| `project_state/aigov-constitution.md` | F1 — D0 charter + machine limits | A |
| `project_state/aigov-dept-contract.md` | F3 — the department SDK | B |
| `project_state/aigov-guideline-intake.md` | F2 — where intent becomes machine-binding | B |
| `project_state/aigov-collective-choice.md` | F6 — the sovereign channel (D3) | B |
| `project_state/aigov-twin.md` | F4 — the world departments act on (D14) | C |
| `project_state/aigov-kernel.md` | F5 — the runtime | D |

Six further families are *proposed* in the decomposition and seeded when their gate clears (anti-sprawl:
seeding a blocked family produces a stale artifact and spends a self-init slot for nothing). Next up:
`aigov-adversarial` (F10) and `aigov-audit-arbitration` (F9), both unblocked by the kernel.

## The two claims this project rests on

1. **Hayek's objection is weakest exactly where this starts and strongest exactly where it aspires to end.**
   A closed life-support loop (O₂, water, power, thermal, pressure) is genuinely centrally plannable — few state
   variables, measurable, causally tight, failure = death. A terrestrial economy is not. So the honest
   architecture is a **subsidiarity engine**: centrally run only the hard physical commons; everywhere else
   maintain the conditions for decentralized discovery. Scaling colony → city → nation means the centrally-run
   share *shrinks*.
2. **The AI never decides.** Arrow and Gibbard–Satterthwaite mean there is no correct preference aggregation to
   discover — an optimizing AI sovereign would merely hide a contested value choice inside a weight vector.
   The governor generates options, simulates, drafts, executes ratified rules, and audits. Humans hold all
   binding authority. Invariants I1 and I9 exist to make that structural rather than stylistic.

## Reuse (verified, not assumed)

`C:\Users\Farshad\PythonProjects\Space_Reflectors_Project\Mars_Governance` — 9-family governance umbrella with
`ai_advisor.py` (curated option menus), `binding_elections.py` (ratify gates execution), `fail_safe_gate.py`
(fail-closed escalation; 0 silent mis-certifications across 500-panel ensembles), `panel_agnostic.py`,
`exogenous_preferences.py` (anti-steering), `connection.py` (resupplier-as-coercer), `civic_education.py`,
`resource_sim.py`. **Re-run 2026-08-11: `193 passed in 27.14s`.** Ten of the sixteen departments already have a
tested primitive to bind against.

## Honesty rails (non-negotiable)

- Inherited `mars-governance` **D7**: every "confirmed" result here is **MODEL-COHERENT**, not
  governance-validated. Nothing may be reported as validated governance on the strength of a green test suite.
- `docs/foundations-canon-map.md` is **model recall**, discovery-tier. No claim in it bears design weight until
  promoted through `/research` + `/research-verify`.
- Any charter clause enforced only by the governor's own compliance is labelled **`aspirational`**, never
  `enforced` (same class as Soraya's own T1=(c)/OT1 residual: in-process constraints are discipline, not
  enforcement).

## The three invented-number channels, structurally closed

The recurring failure mode of an "advisory" AI is that it supplies a number nobody asked it for, and the
number then binds. Three distinct channels are now closed by construction rather than by intention:

| Channel | Where it would leak | What closes it |
|---|---|---|
| An invented **threshold** | a department restating a policy level | contract invariant **I11** + departments READ levels via `level_of()`; a source-scan test forbids literals |
| An invented **level** | the governor filling in what a vague guideline omitted | intake **G1/G2** — a binding type-F guideline is unconstructible without a panel-supplied level |
| An invented **state reading** | treating a latent quantity as measured | twin **DT1** — `read()` refuses `LATENT`, and `ESTIMATED` values carry method + error bar |

A fourth would be an invented **procedural** constant: the intake's polarization tolerance is therefore
derived by simulation (`calibrate_polarization()`), and `compile_guidelines` refuses an `AI_SUPPLIED` one.
