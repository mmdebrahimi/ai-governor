# Result — 2026-08-12-1100-advance-entry-derivation-proof

**Terminal reason:** genuine plateau. The one eligible family is still externally gated on user
elicitation; the adjacent reversible work (proving the derivation at full size) is now done.

| | |
|---|---|
| planned / executed steps | ~12 / 16 |
| family pivots (spillover) | 0 — no second eligible family exists |
| gates hit | none (no money, destructive, or genuinely-irreversible action reached) |
| tests | 402 → **410 passed**, 0 regressions |
| forecast | 1 recorded, 1 scored, **hit-rate 0.0** |

## Delivered

`tests/test_entry_inventory_endtoend.py` — 8 tests exercising the instrument at full size on a
synthetic fully-answered 18-decision entry inventory. Closes a real coverage hole: every prior
test worked on 2–4 decisions.

Pinned by the new tests: no-market forces INTERNALIZE regardless of cost · private information
produces HYBRID rather than MARKET · widely-shared transferable records couple nothing · the
retained-filter prunes coupling questions 40 → 7 · unanswered role and consequence are reported
rather than guessed · capabilities derive only from affirmed pairs · the full-size report renders.

## Bar status: still 0 of 4

The family bar needs the user's answers. Nothing in this run moved it, and nothing could — this
run de-risked the machinery the answers will be fed into, which is a different thing and is
reported as such.

## Wall classification

**External, cheap to close.** 1–2 hrs of the user's time on the worksheet. No device, partner,
dataset or spend.

---
single-session; not resumable — bounded attempts per active session only; a re-run after the lock
clears is a NEW session with a fresh budget; repeated re-runs are not globally bounded.
