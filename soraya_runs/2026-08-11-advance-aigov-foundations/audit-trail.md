# Audit trail — soraya --advance (aigov), 2026-08-11

Gate mode: money-only (default). **Every executed step classified `auto`.** No money, no publish/send, no
recursive delete. Pre-planned estimate ~50 steps; SELF-EXTENDED to ~87 on best judgement (the schema repair
and the F6 spillover were not in the initial estimate). Extension recorded here, not silent.

## Batch A — make the code-owned eligibility gate operational
| # | Step | Class | Outcome |
|---|---|---|---|
| A0 | Rehydrate checkpoint; check run lock | auto | no active run |
| A1 | Run `advance_ranker.rank` | auto | **`blocked:no-accepted-families`** — the whole portfolio was invisible to the gate |
| A2 | Read `references/umbrella-ledger-schema.md` | auto | canonical 5 columns: Family slug / Status / Success-criteria pointer / Critical-path role / blocked_by |
| A3 | Fix mis-placed run dir + self-init account (I had passed `base='.'`) | auto | both relocated under `soraya_runs/`; count was never wrong (`Path('.').parent == '.'`) |
| A4 | Rewrite umbrella `## Project Families` to the canonical schema + `blocked_by` edges | auto (Edit+mirror) | gate now `portfolio_status: ok` |
| A5 | Add `N/M` MVP fractions to 3 family `### Progress proxy` sections | auto (Edit+mirror) | `terminal_met` now machine-readable |
| A6 | Re-run gate | auto | top eligible = **aigov-foundations** (depth 0, terminal unmet) |

## Batch B — advance aigov-foundations to its bar
| # | Step | Class | Outcome |
|---|---|---|---|
| B1 | WebSearch V1 (Arrow, G–S, Sen, McKelvey–Schofield, Black, Ashby) | auto | 5 walls CITED; **3 corrections** |
| B2 | WebSearch V2 (Henry George / LVT) | auto | **H2 FALSIFIED**; source corrected to Arnott & Stiglitz QJE 93(4) 1979 |
| B3 | WebSearch V4 (Fuller) | auto | implementation matches **8/8**; 2 caveats added |
| B4 | WebSearch V5 (OST Art. II/VI, US 2015, LUX 2017) | auto | K7 survives; **new: Art. VI ⇒ derivative authority** |
| B5 | WebSearch V12 (contested set) | auto | 3/4 contested in 3 different ways; **Milgram flag corrected**; LtG not checked |
| B6 | Write 5 memos to `research_outputs/` | auto | bar 0/5 → 5/5 |
| B7 | Apply findings to code + docs (charter C25, canon-map corrections) | auto | fraction 0.7083 → 0.68 (honest fall) |

## Batch C — SPILLOVER into F6 (aigov-collective-choice)
| # | Step | Class | Outcome |
|---|---|---|---|
| C1 | Classify the port with `action_gate` | auto | `auto`, not blocked |
| C2 | Vendor the organ into `aigov/choice/` | auto | **missed `prototypes/`** → 14 collection errors |
| C3 | Vendor `prototypes/`; re-run | auto | **193/193** from the new root |
| C4 | Detached `git worktree` at HEAD to separate committed from working-tree state | auto | **HEAD = 132 tests / 11 files**; working tree = 193 / 17; worktree removed + pruned |
| C5 | Flip charter C15 PENDING → ENFORCED | auto | fraction 0.68 → 0.72 |
| C6 | Rewrite a test that hard-coded C15 as the pending example | auto | tests the mechanism, not the inventory |
| C7 | Seed `aigov-collective-choice` ledger; record self-init | auto | 5/25 |
| C8 | Final verification | auto | root 89 + organ 193 = **282 green**; all 4 bars MET |

## Terminal
`--advance` step-8 checklist: all four ACCEPTED families terminal-met; remaining families are PROPOSED
(not rankable); self-budget ~87/100. **Terminal reason: budget + no unmet accepted family.** Not a hard gate,
not an authority fork.
