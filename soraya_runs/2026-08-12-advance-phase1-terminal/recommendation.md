# Recommendation

1. **The real phase-1 gap is now named: the proposal layer + the certification domain.**
   `Governor.propose` must stop hard-coding instrument names, and non-steering certification must be
   extended to a second domain. The second is genuine design work - the fail-safe gate reasons over
   a resource menu, and a fab-slot lottery is not that shape. Do NOT widen `CERTIFIABLE_INSTRUMENTS`
   by list edit; that certifies something the gate cannot reason about.
2. **When D3 starts proposing, INVERT the two pinned tests** in `tests/test_registry_phase1.py`
   (`test_D3_PROPOSES_NOTHING_the_blocker_this_run_found`, `test_the_certifiable_domain_is_a_single_
   instrument`). Deleting them loses the record of why they existed.
3. **Run the decision-inventory session** (needs the user, 1-2 hrs) - `docs/decision-inventory-
   protocol.md`. Still the only item touching real money and real land.
4. **Ratify or reject the three forks** marked AWAITING RATIFICATION in the umbrella flow-down.
   15 minutes of your judgment; they are load-bearing and unsigned.
5. **Run /idea-anchor** with `docs/idea-anchor-prompt-v3-2026-08-11.md` (user-confirmed skill).
6. Coverage lenses stay blocked on a criterion the panel found insufficient. A10 stays
   authority-gated by design.
