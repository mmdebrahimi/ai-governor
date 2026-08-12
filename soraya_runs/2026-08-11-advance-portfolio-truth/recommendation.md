# Recommendation

1. **Decide the polarization-threshold fix.** Drafted position: the tolerance must be derived at
   the ACTUAL panel size in use, not fixed at 16 - this is a scope error, not a judgment call, and
   `calibrate_polarization(panel_size=n)` already exists. Cheapest correct shape: precompute a
   small per-panel-size table at import, keep provenance GUIDELINE (still derived, so intake G2 is
   unaffected), and pin it with a test. Alternative if a single number is wanted: set a MINIMUM
   panel size of 12 and keep 0.900, which removes the n=8 false-escalation but leaves the n>=24
   missed-escalation exposure unaddressed. Prefer the table.
2. **Answer the anti-mimicry authority fork** (umbrella Pending Decisions) - still the single
   highest-value open item; everything downstream inherits it.
3. **Run the decision-elicitation probe** (needs the user, ~1 hour, no code).
4. **Close A8 cheaply** - re-validate the registry each cycle, or deep-copy specs at admission so
   the caller cannot mutate an admitted registry. The second is strictly better and small.
5. **A9/A10 need behavioural classification**, not more declaration checks - a genuinely larger
   piece of work, and A10 is the MEANING channel the anchor already names as unsolved.
6. **Ledger op still owed:** record the threshold finding as a Hypothesis row via
   `/project-state aigov --append-hypothesis "..."` (hard-routed table; logged in the Action Log
   this run rather than hand-edited).
7. Uncommitted: 5 prior files + two increments.
