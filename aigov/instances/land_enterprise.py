"""Candidate decision list for the family land enterprise — A DRAFT FOR THE USER TO CORRECT.

> **PRIVACY — STANDING, NON-NEGOTIABLE.** This module lives in a PUBLIC repository. Every
> decision here is a SHAPE ("whether a candidate jurisdiction passes our stability screen"),
> never an instance. **No jurisdiction is named anywhere in this file**, and none may be added:
> the candidate-country list is exactly the kind of specific the standing rail keeps out of this
> repo. Roles are unfilled slots. Amounts, counterparties and holdings never appear.

**Scope, ratified 2026-08-12.** The inventory covers **agri-venture ENTRY and PARTNER SELECTION**
— the decisions faced in roughly the next 12 months getting a farming venture off the ground.
This replaced an earlier draft, which inventoried an *operating* multi-country farm. That draft
was mis-specified against the real situation on two counts:

1. There is no operating farm. The venture is prospective.
2. The stated model is to partner with established in-country agribusinesses. Under a partner-led
   model most operating decisions belong to the PARTNER, not to the family — so inventorying them
   would derive capabilities for work the family will never do.

The operating set is preserved below as `OPERATING_CANDIDATES_DEFERRED`. It is not discarded; it
becomes the live inventory once a venture is actually running, and only for whatever operating
decisions the partnership structure leaves on the family's side.

**What this deliberately is NOT.** Every `DecisionRecord` carries `id` and `question` and NOTHING
ELSE. The four sourcing inputs, private information, information needs, fact kinds, accountable
role, reversibility and atomicity are left `None`/empty ON PURPOSE — they are ELICITED, and
`aigov.decisions` exists to refuse to invent them. Running `build_inventory` over this module
reports 100% `UNDECIDABLE` with every gap named. That is the correct pre-elicitation state.

**Expect a MARKET/HYBRID skew, and read it as correct.** Sourcing compares
`frequency x external_engagement_cost` against `internal_annual_cost`. `COMMITMENT`-phase
decisions happen once, so that product stays small and buying the judgement usually wins.
Capability is retained where private information degrades the market option (HYBRID) or where no
market exists at all. `SCREENING`-phase decisions recur across candidates and are where a genuine
INTERNALIZE verdict is most likely to appear.

**The list carries no structure.** Order is arbitrary; `_READING_GROUPS` is a reading aid for the
correction session only and never reaches the instrument. Structure is COMPUTED from affirmed
couplings — proposing groups here would import the template the anti-mimicry rail exists to stop.
"""

from __future__ import annotations

from aigov.decisions import DecisionRecord

#: Decisions run REPEATEDLY across candidates during the search, so a real frequency exists and a
#: genuine INTERNALIZE verdict is reachable.
SCREENING_IDS = ("E01", "E02", "E04", "E05", "E06", "E13")

#: Decisions taken ONCE for the first venture. Frequency will be about 1, so expect MARKET/HYBRID
#: unless private information or a missing market carries them.
COMMITMENT_IDS = (
    "E03", "E07", "E08", "E09", "E10", "E11", "E12", "E14", "E15", "E16", "E17", "E18",
)

#: Decisions the DRAFTER suspects are COMPOUND — two reasonable people could answer different
#: parts differently, so `aigov.decisions` would refuse a verdict. `atomic` stays `None` in the
#: records; this is a flag for the correction session, never an input to the instrument.
SUSPECTED_COMPOUND_IDS = ("E02", "E15")

#: Reading aid for the correction session ONLY. Never exported into a record.
_READING_GROUPS = {
    "where": ("E01", "E02", "E03"),
    "what shape of asset": ("E04", "E05"),
    "who with": ("E06", "E07", "E08", "E09"),
    "how much and through what": ("E10", "E11", "E12"),
    "what we can see": ("E13", "E14"),
    "what we carry": ("E15", "E16"),
    "who answers for it": ("E17", "E18"),
}


def _d(id_: str, question: str) -> DecisionRecord:
    """A candidate decision: the question only. Every elicited field stays unanswered."""
    return DecisionRecord(id=id_, question=question)


ENTRY_CANDIDATES = (
    # --- where ---
    _d("E01", "Whether a candidate jurisdiction passes our political-stability and personal-safety "
              "screen well enough to put capital into at all."),
    _d("E02", "Whether a candidate jurisdiction's foreign-ownership regime permits a structure we "
              "would actually accept — and if direct ownership is barred, whether the available "
              "workaround is one we are willing to rely on."),
    _d("E03", "Which jurisdiction to commit the first venture to, given we cannot start "
              "everywhere at once."),

    # --- what shape of asset ---
    _d("E04", "Whether to enter by buying into an existing operating business or by building "
              "greenfield."),
    _d("E05", "Whether to hold land, lease it, or contract-farm without holding land at all."),

    # --- who with ---
    _d("E06", "Whether a specific candidate partner passes diligence well enough to proceed with."),
    _d("E07", "What control and information rights to require from a partner, decided separately "
              "from how much of the equity we hold."),
    _d("E08", "How to structure the partner's economic incentive so their upside and ours point "
              "the same way."),
    _d("E09", "What exit mechanism to fix at entry, before we need it."),

    # --- how much and through what ---
    _d("E10", "How much capital to commit to a first venture."),
    _d("E11", "Whether to fund it with family equity alone, or bring in local debt or outside "
              "co-investors."),
    _d("E12", "What holding structure to route the investment through, given repatriation and "
              "treaty considerations."),

    # --- what we can see ---
    _d("E13", "For a given claim a partner makes about the operation, whether we must be able to "
              "verify it independently or can accept it on their report."),
    _d("E14", "Whether to deploy our own instrumentation on an operation we do not run, and how "
              "deep to take it."),

    # --- what we carry ---
    _d("E15", "Which political, currency and production risks to mitigate deliberately and which "
              "to carry ourselves."),
    _d("E16", "Whether to run a bounded pilot before committing at full size."),

    # --- who answers for it ---
    _d("E17", "Who on our side answers for this venture — the role, not the person."),
    _d("E18", "Whether to bring agricultural expertise in-house or rely entirely on the partner "
              "for it."),
)

#: The superseded operating-farm draft. NOT the live inventory. Retained because it becomes
#: relevant once a venture is running — and then only for whichever operating decisions the
#: partnership structure actually leaves on the family's side, which may be very few.
OPERATING_CANDIDATES_DEFERRED = (
    _d("L01", "Whether to acquire a specific parcel that has been offered to us in a "
              "jurisdiction where we already operate."),
    _d("L03", "Whether to sell a parcel we currently hold."),
    _d("L04", "For a given parcel, whether to farm it ourselves or lease it out to an operator."),
    _d("L05", "Whether to renew, renegotiate or end a tenancy or share arrangement as it "
              "comes up for term."),
    _d("L06", "What to plant on a given parcel for the coming season."),
    _d("L07", "Whether to change the established rotation on a given parcel."),
    _d("L08", "Whether to fund an irrigation or drainage improvement on a given parcel."),
    _d("L09", "Whether to convert a parcel from one land use to another (a change measured in "
              "years, not seasons)."),
    _d("L10", "When to harvest a given block once it is within its window."),
    _d("L11", "How much of a major input to commit to in advance of a season, and when to commit."),
    _d("L12", "Whether to move a category of purchasing from our current supplier to another."),
    _d("L13", "For a given machine requirement, whether to buy, lease, or hire it in with an "
              "operator."),
    _d("L14", "Whether to repair or replace a major machine at the point it fails or comes due."),
    _d("L15", "Whether to sell stored output now or continue holding it."),
    _d("L16", "Whether to commit a share of an expected harvest to a forward price before it "
              "is in hand."),
    _d("L17", "Which buyer or channel to direct a given lot to."),
    _d("L18", "For a given recurring work need, whether to fill it with a permanent hire, "
              "seasonal labour, or a contractor."),
    _d("L19", "When a site-level manager leaves, whether to promote from inside or recruit "
              "from outside."),
    _d("L20", "Whether to change the terms on which a site-level manager is rewarded."),
    _d("L21", "Whether to fund a given investment with borrowing rather than from our own cash."),
    _d("L22", "Which of the competing parcel-level investments in front of us to fund this "
              "cycle, given we cannot fund all of them."),
    _d("L23", "Whether to move cash out of the jurisdiction that generated it."),
    _d("L24", "Which currency to hold working capital in for a given operating unit."),
    _d("L25", "Whether to insure a given exposure or carry it ourselves."),
    _d("L26", "How to respond when a jurisdiction changes a rule that binds one of our "
              "operations."),
    _d("L27", "Whether to contest an assessment or ruling rather than pay it."),
    _d("L28", "Whether to obtain or renew a certification that a buyer or market asks for."),
    _d("L29", "Whether to place a family member into an operating role."),
    _d("L30", "For a given period, whether to distribute earnings or retain them in the business."),
    _d("L31", "Whether to change how the holding entities are arranged across jurisdictions."),
)

#: What the instrument runs on. Entry phase only, by ratified scope.
CANDIDATES = ENTRY_CANDIDATES

#: Every entry decision is in the first pass — the whole ratified scope is 18 decisions, which
#: clears the family bar of >=15 without deferring any of it to a second sitting.
FIRST_PASS_IDS = tuple(d.id for d in ENTRY_CANDIDATES)

BY_ID = {d.id: d for d in CANDIDATES}
FIRST_PASS = tuple(BY_ID[i] for i in FIRST_PASS_IDS)


def phase_of(decision_id: str) -> str:
    """SCREENING (recurs across candidates) or COMMITMENT (taken once)."""
    if decision_id in SCREENING_IDS:
        return "SCREENING"
    if decision_id in COMMITMENT_IDS:
        return "COMMITMENT"
    return "UNCLASSIFIED"


__all__ = [
    "CANDIDATES", "ENTRY_CANDIDATES", "OPERATING_CANDIDATES_DEFERRED", "BY_ID", "FIRST_PASS",
    "FIRST_PASS_IDS", "SCREENING_IDS", "COMMITMENT_IDS", "SUSPECTED_COMPOUND_IDS", "phase_of",
]
