# Result - soraya --advance, 2026-08-11 (decision inventory)

## What this run answers
"What departments do we need?" - without handing back a list of what other organisations have.

The user ratified (Pending Decision 5, settled this run) that the instrument SHOULD give a final
recommendation, but must reach it by interrogating first. The binding constraint is TRACEABILITY.
This run makes that a PROPERTY rather than a promise: departments are **computed**, not proposed.

    decisions you actually face
      -> internalize-vs-market verdict per decision   (Coase 1937 / Williamson)
      -> cluster the held ones by shared information need   (Galbraith)
      -> departments, each carrying `derived_from`

## The live defect, found by running it
`private_information` was recorded, printed as a "degraded" note, and had **no effect on the
verdict**. Three of four buyable decisions came out MARKET despite depending on knowledge an
outsider cannot acquire at any price. A declared field nothing acted on.

Fixed with `Sourcing.HYBRID` - buy the execution, keep the judgment. Derived (market-cheaper AND
private information present), needs no new number, and forms a department because an unowned
judgment is how a supplier quietly starts making your decisions.

## What the derivation actually produced
On a realistic partial farm inventory, acquisition + cash-phasing + planting collapsed into ONE
department, because they need the same facts (land_price, cash_position, soil_quality,
water_rights). A catalogue would have given Finance + Agriculture + Legal + Sustainability. The
derivation gives two clusters and neither carries a conventional name - by design, since naming a
cluster would import a template through the back door.

## No invented numbers
- The Coase test compares two USER-supplied quantities. No threshold, no weighting, no scoring
  constant anywhere in the module.
- The boundary is EXACT - a test pins that the verdict flips at equal cost with no tolerance band,
  because a band would be a number the instrument chose.
- A missing input yields UNDECIDABLE with the field NAMED. No default. Supplying one would be the
  same act I11 forbids for numeric thresholds.

## Measured
root **257 -> 283** (+26), 0 regressions; vendored organ **193/193**; mutant reverting HYBRID turns
2 tests RED; source restored byte-identical. One test-fixture bug of my own caught and fixed (I had
the Coase direction backwards - a HIGH internal cost means BUY, not HOLD).

## Honest limits
- It cannot tell you whether your inventory is COMPLETE. A decision you never mention produces no
  department and nothing here notices the absence.
- It does not rank decisions or choose a strategy. It converts an elicited inventory into a
  structure; judgment stays with whoever answered.
- The numbers in the demo run are ILLUSTRATIVE. No real inventory exists yet.
