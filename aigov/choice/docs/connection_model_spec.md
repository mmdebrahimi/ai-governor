# Connection Model — Spec (family `mars-gov-connection-model`)

Parameterizes the Earth↔Mars connection as **governance-sim inputs** (latency · blackout · resupply ·
import-dependence), and makes the **resupplier-as-coercer survival veto** checkable. Code:
`governance/connection.py`. Background: `docs/earth_mars_connection_scenarios.md`.

## Physics-grounded constants
- Synodic cadence **26 cycles** (~26 months) — resupply windows + conjunction blackouts.
- Conjunction blackout **2 cycles** — `earth_contact=False` → governance must run with **zero Earth
  contact** (the M1 caretaker/min-survival primitive is the relevant mechanism).
- Round-trip light-time **6–44 min**, oscillating over the synodic cycle. No real-time control, ever.
- Local crop capacity grows from **0.30 → demand** as greenhouses build out (`+0.02/cycle`); demand ≈ 0.618
  kg/capita/day (from `models.resource_sim`). **Self-sufficiency at cycle 53.**

## The umbilical → tether → handshake arc
`connection_at(cycle).phase`:
- **umbilical** (cycle 0) — fully Earth-dependent.
- **tether** (import-dependent, cycles 1–52) — local capacity below demand; Earth resupply required.
- **handshake** (cycle ≥ 53) — self-sufficient; resupply optional.

## The resupplier-as-coercer veto (the load-bearing output)
`resupplier_veto_survivable(cycle)` = `self_sufficient(cycle)`. While **False** (import-dependent phase),
whoever controls resupply holds a **survival veto** over governance — withholding a window starves the
colony regardless of the in-colony voting mechanism. This **breaks the "no trusted external authority"
premise** for ~53 cycles, then voids at self-sufficiency. Quantified, not asserted:
`import_needed_pc(cycle)` is the per-capita food the colony cannot produce locally — the exact size of the
coercion lever. Mitigation is **self-sufficiency** (close the food/O2 loop) + a strategic reserve that
survives ≥1 missed window — NOT cryptography.

## Governance-design implications (closed by this family)
1. The voting threat model now lists **resupplier-as-coercer** as an adversary (mid-term only).
2. The blackout case validates the **caretaker/min-survival** fallback — full cycles with no Earth contact.
3. The mid-term **tether** phase is the project's real target; this model dates *when* the survival veto is
   live so governance design can account for it.

## API
- `is_blackout(cycle)` · `round_trip_latency_min(cycle)` · `crop_capacity_pc(cycle)` ·
  `import_needed_pc(cycle)` · `imported_food_pc(cycle, withheld=)` · `self_sufficient(cycle)` ·
  `self_sufficiency_cycle()` · `resupplier_veto_survivable(cycle)` · `connection_at(cycle)` · `timeline(n)`.

## Deferred (phase-2)
Wire the connection timeline into `run_sandbox` (drive `imported_food_pc` per cycle + a blackout flag);
strategic-reserve buffer sizing; stochastic window slippage; the latency→decision-cadence coupling
(how 6–44 min round-trip bounds Earth-in-the-loop ratification during the tether phase).
