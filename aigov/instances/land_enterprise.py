"""Candidate decision list for the family land enterprise — A DRAFT FOR THE USER TO CORRECT.

> **PRIVACY — STANDING, NON-NEGOTIABLE.** This module lives in a PUBLIC repository. Every
> decision here is a SHAPE ("whether to acquire a parcel in a jurisdiction we already operate
> in"), never an instance ("whether to buy X for $Y"). No jurisdiction, crop, counterparty,
> amount, holding or family member is named. Roles are unfilled slots. Nothing below identifies
> the enterprise.

**What this is.** `aigov-land-enterprise` candidate action #1 is *"run the decision-inventory
session, Claude drafting the candidate list for the user to correct"*. This module is that
draft — the half a machine can do, so the session becomes correction rather than composition.

**What this deliberately is NOT.** Every `DecisionRecord` below carries `id` and `question` and
NOTHING ELSE. The four sourcing inputs, the private information, the information needs, the fact
kinds, the accountable role, the reversibility and the atomicity are all left `None`/empty ON
PURPOSE. They are ELICITED fields — `aigov.decisions` exists precisely to refuse to invent them.
A drafted frequency or a guessed cost would be exactly the failure the instrument was built to
prevent, and it would contaminate every verdict downstream. So this draft proposes only the
QUESTIONS; it proposes no answers.

Consequently, running `build_inventory` on this module reports 100% `UNDECIDABLE` with every gap
named. That is the CORRECT pre-elicitation state, not a defect.

**The list carries no structure.** The order is arbitrary and the `_READING_GROUPS` labels below
are a reading aid for the correction session ONLY. They are not exported into any record and
never reach the instrument. Structure is COMPUTED from affirmed couplings — proposing groups here
would import the template one level down, which is the documented failure this whole family
exists to avoid.
"""

from __future__ import annotations

from aigov.decisions import DecisionRecord

#: The recommended FIRST-PASS subset. The family bar is >=15 decisions with all four sourcing
#: inputs answered; a 24-decision first sitting is not tractable in one session. These 16 are the
#: ones drafted as most likely to be both genuinely recurring and genuinely consequential, so the
#: bar is reachable in one sitting with the remainder deferred to a second pass.
FIRST_PASS_IDS = (
    "L01", "L02", "L04", "L06", "L07", "L10", "L11", "L13",
    "L15", "L16", "L18", "L21", "L22", "L23", "L26", "L30",
)

#: Decisions the DRAFTER suspects are COMPOUND — i.e. two reasonable people could answer
#: different parts differently, so `aigov.decisions` would refuse them a verdict. `atomic` is an
#: elicited field and is left `None` in the records; this tuple is a flag for the correction
#: session ("consider splitting these"), never an input to the instrument.
SUSPECTED_COMPOUND_IDS = ("L22", "L26", "L31")

#: Reading aid for the correction session ONLY — never exported into a record, never seen by
#: `build_inventory`. See the module docstring.
_READING_GROUPS = {
    "land and tenure": ("L01", "L02", "L03", "L04", "L05"),
    "what the land does": ("L06", "L07", "L08", "L09", "L10"),
    "inputs and equipment": ("L11", "L12", "L13", "L14"),
    "selling the output": ("L15", "L16", "L17"),
    "people": ("L18", "L19", "L20"),
    "capital and cross-border cash": ("L21", "L22", "L23", "L24"),
    "risk, tax and compliance": ("L25", "L26", "L27", "L28"),
    "ownership and family": ("L29", "L30", "L31"),
}


def _d(id_: str, question: str) -> DecisionRecord:
    """A candidate decision: the question only. Every elicited field stays unanswered."""
    return DecisionRecord(id=id_, question=question)


CANDIDATES = (
    # --- land and tenure ---
    _d("L01", "Whether to acquire a specific parcel that has been offered to us in a "
              "jurisdiction where we already operate."),
    _d("L02", "Whether to begin operating in a jurisdiction we are not currently in."),
    _d("L03", "Whether to sell a parcel we currently hold."),
    _d("L04", "For a given parcel, whether to farm it ourselves or lease it out to an operator."),
    _d("L05", "Whether to renew, renegotiate or end a tenancy or share arrangement as it "
              "comes up for term."),

    # --- what the land does ---
    _d("L06", "What to plant on a given parcel for the coming season."),
    _d("L07", "Whether to change the established rotation on a given parcel."),
    _d("L08", "Whether to fund an irrigation or drainage improvement on a given parcel."),
    _d("L09", "Whether to convert a parcel from one land use to another (a change measured in "
              "years, not seasons)."),
    _d("L10", "When to harvest a given block once it is within its window."),

    # --- inputs and equipment ---
    _d("L11", "How much of a major input to commit to in advance of a season, and when to commit."),
    _d("L12", "Whether to move a category of purchasing from our current supplier to another."),
    _d("L13", "For a given machine requirement, whether to buy, lease, or hire it in with an "
              "operator."),
    _d("L14", "Whether to repair or replace a major machine at the point it fails or comes due."),

    # --- selling the output ---
    _d("L15", "Whether to sell stored output now or continue holding it."),
    _d("L16", "Whether to commit a share of an expected harvest to a forward price before it "
              "is in hand."),
    _d("L17", "Which buyer or channel to direct a given lot to."),

    # --- people ---
    _d("L18", "For a given recurring work need, whether to fill it with a permanent hire, "
              "seasonal labour, or a contractor."),
    _d("L19", "When a site-level manager leaves, whether to promote from inside or recruit "
              "from outside."),
    _d("L20", "Whether to change the terms on which a site-level manager is rewarded."),

    # --- capital and cross-border cash ---
    _d("L21", "Whether to fund a given investment with borrowing rather than from our own cash."),
    _d("L22", "Which of the competing parcel-level investments in front of us to fund this "
              "cycle, given we cannot fund all of them."),
    _d("L23", "Whether to move cash out of the jurisdiction that generated it."),
    _d("L24", "Which currency to hold working capital in for a given operating unit."),

    # --- risk, tax and compliance ---
    _d("L25", "Whether to insure a given exposure or carry it ourselves."),
    _d("L26", "How to respond when a jurisdiction changes a rule that binds one of our "
              "operations."),
    _d("L27", "Whether to contest an assessment or ruling rather than pay it."),
    _d("L28", "Whether to obtain or renew a certification that a buyer or market asks for."),

    # --- ownership and family ---
    _d("L29", "Whether to place a family member into an operating role."),
    _d("L30", "For a given period, whether to distribute earnings or retain them in the business."),
    _d("L31", "Whether to change how the holding entities are arranged across jurisdictions."),
)

#: Index for the correction session.
BY_ID = {d.id: d for d in CANDIDATES}

FIRST_PASS = tuple(BY_ID[i] for i in FIRST_PASS_IDS)

__all__ = [
    "CANDIDATES", "BY_ID", "FIRST_PASS", "FIRST_PASS_IDS", "SUSPECTED_COMPOUND_IDS",
]
