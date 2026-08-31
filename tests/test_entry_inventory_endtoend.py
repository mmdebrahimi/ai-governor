"""Full-size end-to-end exercise of the decision instrument.

Every other test in `test_decisions.py` exercises 2-4 decisions. That is right for unit-testing a
rule, and it says nothing about whether the instrument is USABLE at the size a real inventory
reaches. The entry-phase inventory is 19 decisions, and that is where the pairwise parts
of the design (coupling candidates, capability derivation) either hold up or fall over.

> **The fixture below is SYNTHETIC and is not elicited data.** It exists to exercise the
> derivation at realistic size and shape. It must never be imported by
> `aigov.instances.land_enterprise`, and no number in it is a claim about any real enterprise.
> The no-invented-numbers rail governs the INSTANCE; a test fixture is allowed to have numbers
> precisely because it is labelled as fiction.

What the fixture is designed to stress, beyond just being big:

- **A tacit fact shared by many decisions.** "what we will actually tolerate losing" appears in
  six decisions. If shared tacit context couples pairwise, this alone is 15 pairs.
- **A transferable record shared by many decisions.** "cash available on hand" also appears in
  several. It must couple NOTHING - that distinction is the fix for the second historical defect
  and it needs to hold at size, not just in a two-decision unit test.
- **A mix of answered and deliberately unanswered fields**, so the gap-reporting paths are live.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from aigov.decisions import (  # noqa: E402
    CouplingRecord, DecisionRecord, FactKind, Reversibility, Sourcing,
    build_inventory, coupling_candidates, render_report,
)
from aigov.instances.land_enterprise import ENTRY_CANDIDATES  # noqa: E402

# --- shared facts, by how expensive they are to move to someone else -------------------------

TOLERANCE = "what we will actually tolerate losing"          # tacit  -> should couple
PARTNER_READ = "how we read a counterparty from past deals"  # tacit  -> should couple
RETURN_BAR = "the return we hold out for"                    # org    -> should couple
CASH = "cash available on hand"                              # record -> must couple NOTHING
FX = "published fx and repatriation rules"                   # record -> must couple NOTHING

_KIND = {
    TOLERANCE: FactKind.TACIT_CONTEXT,
    PARTNER_READ: FactKind.TACIT_CONTEXT,
    RETURN_BAR: FactKind.ORGANIZATION_SPECIFIC_CONTEXT,
    CASH: FactKind.TRANSFERABLE_RECORD,
    FX: FactKind.TRANSFERABLE_RECORD,
}

#: decision id -> facts it turns on. Deliberately overlapping.
_FACTS = {
    "E01": [TOLERANCE],
    "E02a": [PARTNER_READ],
    "E02b": [TOLERANCE],
    "E03": [TOLERANCE, RETURN_BAR],
    "E04": [PARTNER_READ, RETURN_BAR],
    "E05": [RETURN_BAR],
    "E06": [PARTNER_READ],
    "E07": [PARTNER_READ],
    "E08": [PARTNER_READ, RETURN_BAR],
    "E09": [TOLERANCE],
    "E10": [TOLERANCE, CASH, RETURN_BAR],
    "E11": [CASH],
    "E12": [FX, CASH],
    "E13": [PARTNER_READ],
    "E14": [],
    "E15": [TOLERANCE],
    "E16": [TOLERANCE],
    "E17": [],
    "E18": [],
    "E19a": [TOLERANCE],
    "E19b": [],
    "E20": [],
    "E21a": [TOLERANCE],
    "E21b": [CASH],
    "E22": [CASH],
    "E23": [FX],
}

#: decision id -> (freq/yr, cost to buy the call once, cost/yr to hold it, market exists?)
_COSTS = {
    "E01": (8, 6_000, 40_000, True),
    "E02a": (8, 5_000, 55_000, True),  # market cheaper + private info -> HYBRID
    "E02b": (8, 30_000, 45_000, True), # buying the family's own risk appetite is dear -> INTERNALIZE
    "E03": (1, 25_000, 90_000, True),
    "E04": (5, 12_000, 60_000, True),
    "E05": (5, 7_000, 45_000, True),
    "E06": (6, 9_000, 80_000, True),   # market cheaper + private info -> HYBRID
    "E07": (1, 18_000, 70_000, True),
    "E08": (1, 15_000, 65_000, True),
    "E09": (1, 20_000, 75_000, True),
    "E10": (1, 30_000, 110_000, False),   # no market -> forced INTERNALIZE
    "E11": (1, 10_000, 50_000, True),
    "E12": (1, 22_000, 60_000, True),
    "E13": (6, 4_000, 30_000, True),
    "E14": (1, 35_000, 25_000, True),     # cheap to hold -> INTERNALIZE on arithmetic
    "E15": (1, 28_000, 85_000, True),
    "E16": (1, 12_000, 55_000, True),
    "E17": (1, 8_000, 20_000, False),     # no market -> forced INTERNALIZE
    "E18": (1, 14_000, 95_000, True),
    "E19a": (1, 20_000, 60_000, True),   # market cheaper + private info -> HYBRID
    "E19b": (1, 10_000, 30_000, True),
    "E20": (1, 15_000, 50_000, True),
    "E21a": (1, 25_000, 15_000, False),  # no market -> forced INTERNALIZE
    "E21b": (1, 18_000, 40_000, True),
    "E22": (1, 30_000, 80_000, True),
    "E23": (1, 12_000, 40_000, True),
}

#: decisions where the family knows something the market cannot acquire -> HYBRID, not MARKET.
_PRIVATE = {
    "E01": ("what our own development history says about this kind of jurisdiction",),
    "E02a": ("which local workarounds we have seen fail",),
    "E02b": ("what this family will actually build on",),
    "E06": ("how this partner behaved in an unrelated prior dealing",),
    "E07": ("which rights we have previously needed and been refused",),
    "E13": ("which partner claims have proven unreliable before",),
    "E19a": ("what this family actually wants standing on the land in thirty years",),
}

_ROLES = {
    "E01": "principal", "E02a": "principal", "E02b": "principal", "E03": "principal", "E04": "principal",
    "E05": "operating lead", "E06": "principal", "E07": "principal", "E08": "principal",
    "E09": "principal", "E10": "principal", "E11": "principal", "E12": "principal",
    "E13": "operating lead", "E14": "operating lead", "E15": "principal",
    "E16": "operating lead", "E17": "principal",
    "E19a": "principal", "E19b": "operating lead", "E20": "operating lead",
    "E21a": "principal", "E21b": "principal",
    "E22": "principal", "E23": "principal",
    # E18 deliberately left unowned so the unowned-reporting path stays live.
}

_REVERSIBILITY = {
    "E01": Reversibility.REVERSIBLE, "E02a": Reversibility.REVERSIBLE,
    "E02b": Reversibility.COSTLY,
    "E03": Reversibility.COSTLY, "E04": Reversibility.COSTLY,
    "E05": Reversibility.COSTLY, "E06": Reversibility.COSTLY,
    "E07": Reversibility.IRREVERSIBLE, "E08": Reversibility.COSTLY,
    "E09": Reversibility.IRREVERSIBLE, "E10": Reversibility.COSTLY,
    "E11": Reversibility.COSTLY, "E12": Reversibility.IRREVERSIBLE,
    "E13": Reversibility.REVERSIBLE, "E14": Reversibility.REVERSIBLE,
    "E15": Reversibility.COSTLY, "E16": Reversibility.REVERSIBLE,
    "E17": Reversibility.COSTLY,
    "E19a": Reversibility.IRREVERSIBLE, "E19b": Reversibility.REVERSIBLE,
    "E20": Reversibility.COSTLY,
    "E21a": Reversibility.COSTLY, "E21b": Reversibility.COSTLY,
    "E22": Reversibility.IRREVERSIBLE,
    "E23": Reversibility.COSTLY,
    # E18 deliberately left unanswered so the unassured-reporting path stays live.
}


def test_every_instance_decision_has_a_fixture_entry():
    """Adding a decision upstream must fail here, once, and say what is missing.

    This fixture has been hand-patched three times as the inventory grew, each time surfacing as a
    scatter of KeyErrors across unrelated tests. One explicit guard is cheaper to read than seven
    incidental failures.
    """
    missing = {
        "_FACTS": [d.id for d in ENTRY_CANDIDATES if d.id not in _FACTS],
        "_COSTS": [d.id for d in ENTRY_CANDIDATES if d.id not in _COSTS],
    }
    assert not any(missing.values()), (
        f"decisions added to aigov.instances.land_enterprise without fixture entries: {missing}. "
        f"Add them to the dicts above; _PRIVATE / _ROLES / _REVERSIBILITY are optional by design."
    )


def answered_entry_inventory() -> tuple:
    """Every entry decision, fully answered. SYNTHETIC - see the module docstring."""
    out = []
    for d in ENTRY_CANDIDATES:
        freq, ext, internal, market = _COSTS[d.id]
        facts = _FACTS[d.id]
        out.append(DecisionRecord(
            id=d.id,
            question=d.question,
            frequency_per_year=freq,
            external_engagement_cost=ext,
            internal_annual_cost=internal,
            external_market_exists=market,
            private_information=_PRIVATE.get(d.id, ()),
            information_needs=frozenset(facts),
            fact_kinds=tuple((f, _KIND[f]) for f in facts),
            accountable_role=_ROLES.get(d.id, ""),
            atomic=True,
            reversibility=_REVERSIBILITY.get(d.id),
        ))
    return tuple(out)


# ------------------------------------------------------------------------------------------
# The scaling question the small tests cannot answer
# ------------------------------------------------------------------------------------------

def test_every_entry_decision_gets_a_sourcing_verdict_at_full_size():
    ds = answered_entry_inventory()
    report = build_inventory(ds)
    assert len(report.verdicts) == len(ENTRY_CANDIDATES)
    assert not report.undecided, "every cost field is answered, so nothing may be UNDECIDABLE"


def test_no_market_forces_internalize_regardless_of_cost():
    ds = {d.id: d for d in answered_entry_inventory()}
    report = build_inventory(tuple(ds.values()))
    by_id = {v.decision_id: v.sourcing for v in report.verdicts}
    assert by_id["E10"] is Sourcing.INTERNALIZE
    assert by_id["E17"] is Sourcing.INTERNALIZE


def test_private_information_produces_hybrid_not_market():
    """The historical defect: private info was recorded, printed, then ignored."""
    report = build_inventory(answered_entry_inventory())
    by_id = {v.decision_id: v.sourcing for v in report.verdicts}
    for did in ("E02a", "E06", "E13"):
        assert by_id[did] is Sourcing.HYBRID, f"{did} has private info and a cheaper market"


def test_transferable_records_couple_nothing_even_when_widely_shared():
    """CASH is shared by E10/E11/E12 and FX by E12. Neither may generate a coupling candidate."""
    pairs = coupling_candidates(answered_entry_inventory())
    for c in pairs:
        assert CASH not in c.shared_facts
        assert FX not in c.shared_facts


def test_sourcing_verdict_prunes_the_pairwise_blowup():
    """The coupling question does NOT scale with the size of the inventory.

    Naive reading of the design says pairwise, so 18 decisions sharing three tacit facts should
    produce sum(C(n,2)) coupling questions - 40 on this fixture - each one asked separately. That
    would be a usability wall reached mid-session with the user's answers already in.

    It does not happen, because `coupling_candidates` pairs only over RETAINED decisions
    (INTERNALIZE or HYBRID). You are not asked whether two decisions must be made together when
    you have already decided to buy both. MARKET and UNDECIDABLE are excluded at the source.

    This test pins BOTH halves: the naive bound, and the fact that the real count is far under it
    because of the pruning. A regression that removed the retained-filter would blow past the
    pinned count and fail here rather than in front of the user.
    """
    ds = answered_entry_inventory()
    report = build_inventory(ds)
    retained = {v.decision_id for v in report.verdicts
                if v.sourcing in (Sourcing.INTERNALIZE, Sourcing.HYBRID)}

    naive = sum(
        math.comb(sum(1 for f in _FACTS.values() if fact in f), 2)
        for fact in (TOLERANCE, PARTNER_READ, RETURN_BAR)
    )
    pairs = coupling_candidates(ds)

    assert pairs, "the fixture must generate some coupling candidates or it tests nothing"
    assert len(pairs) < naive, "the retained-filter must prune below the naive pairwise bound"
    for c in pairs:
        assert c.a in retained and c.b in retained, "only retained decisions may be paired"

    # Pinned measurement. Update deliberately if the fixture changes; a silent jump is a defect.
    assert (naive, len(pairs)) == (61, 16)


def test_unanswered_role_and_consequence_are_reported_not_guessed():
    report = build_inventory(answered_entry_inventory())
    assert report.unowned == ("E18",)
    assert report.unassured == ("E18",)


def test_capabilities_derive_only_from_affirmed_pairs_at_full_size():
    ds = answered_entry_inventory()
    pairs = coupling_candidates(ds)
    affirmed = tuple(CouplingRecord(a=c.a, b=c.b, coupled=True) for c in pairs)
    report = build_inventory(ds, affirmed)
    assert report.capabilities, "affirming every candidate must yield at least one capability"
    grouped = {i for cap in report.capabilities for i in cap.decision_ids}
    assert "E14" not in grouped, "a decision sharing no expensive fact joins no capability"
    assert "E11" not in grouped, "a decision sharing only a transferable record joins no capability"


def test_full_size_report_renders_and_names_every_decision():
    report = build_inventory(answered_entry_inventory())
    text = render_report(report)
    for d in ENTRY_CANDIDATES:
        assert d.id in text
