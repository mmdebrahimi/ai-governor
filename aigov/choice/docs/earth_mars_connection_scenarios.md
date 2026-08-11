# Earth↔Mars Connection Scenarios (short / mid / long term)

Context note for the governance project: the Earth↔Mars *connection* sets the load-bearing assumptions of
the whole design (intermittent connectivity, no trusted external authority, autonomy-forced governance).
This memo frames how the connection evolves and what each phase means for the governance system we built.

## The two physics constants that govern everything
- **Light-time latency:** one-way 3–22 min (round-trip 6–44 min) by orbital geometry. **No real-time
  control, ever.** Plus a **~2-week comms blackout every ~26 months** at solar conjunction.
- **Launch-window cadence:** transfer windows every **~26 months** (synodic period). Resupply is a
  **batch, not a stream** — miss a window, wait two years.

Together these **mandate local autonomous governance** — the physical justification for the whole project.

## Connection across four channels × three horizons
"Connection" = four channels — **Bits** (comms), **Atoms** (transport), **Authority** (governance),
**Value** (economy) — each weakening Earth's grip and forcing Mars autonomy over time.

| Channel | Short (now–~2035) | Mid (~2035–2060) | Long (2060+) |
|---|---|---|---|
| Bits | DSN + relay; no/few humans; latency tolerable | Relay constellation; latency *operationally absorbed*; Mars runs own ops | Mars-local internet; Earth a high-latency peer; info divergence |
| Atoms | Robotic cargo; 100% Earth-made | First crews; ISRU propellant/water; still import-dependent (electronics/meds/spares) | Resupply optional for survival; Earth ships high-value/low-mass only |
| Authority | Earth mission-control owns every decision | **Latency-forced split:** Earth=strategy/funds, Mars=all operational decisions | Mars self-governs; Earth authority → influence. **Our governance system is the live mechanism** |
| Value | Cost center (science/prestige) | Earth→Mars subsidy; Mars→Earth value = data/IP | Mars exports bits/services, never bulk goods |

## The arc: umbilical → tether → handshake
- **Short = umbilical** — Mars is an instrument; no governance needed (remote operation).
- **Mid = tether** — latency physically severs *operational* control from Earth while strategic/financial
  control remains. *Authority de-syncs from physics.* **The dangerous, under-designed phase — the project's
  real target.**
- **Long = handshake** — two self-governing nodes; the Earth-tested governance is the colony's constitution.

## Best / worst case on the load-bearing uncertainties
| Uncertainty | Best | Worst |
|---|---|---|
| Transit time (mid) | nuclear-thermal ~3–4 mo → tighter coupling | chemical ~7–9 mo → autonomy forced earlier/harder |
| Self-sufficiency | ISRU+local mfg closes the loop → real independence | permanent import-dependence → Earth keeps a **survival veto** ("no external authority" breaks) |
| Authority transition | negotiated, pre-designed handover (what this project enables) | unplanned rupture across 20-min latency → legitimacy crisis |

## Implications for the governance project
1. **"No trusted external authority" is true LONG-term, FALSE mid-term** if Earth controls resupply → an
   unmodeled adversary: **the resupplier as coercer** (survival veto). → added to the voting threat model.
2. **"Intermittent connectivity" is concrete:** the conjunction blackout is the hard case — governance must
   complete full cycles with **zero Earth contact**. The caretaker/min-survival fallback (M1) is the right
   primitive.
3. **The mid-term "tether" phase is the real target** — design tether-phase governance now, before the
   latency-forced split happens for real.
4. **New work:** a `connection-model` family parameterizing latency / resupply-cadence / import-dependence
   as governance-sim inputs (built as `governance/connection.py`).
