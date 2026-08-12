"""The decision inventory — what an organisation must RETAIN, derived from what it decides.

WHY THIS EXISTS. Asked "what departments do we need?", the tempting answer is a list of what
governments and companies usually have: finance, operations, legal, HR. That answer is the
documented standard failure of institutional reform — adopting the outward FORM of something that
works elsewhere while the function never arrives (Andrews/Pritchett/Woolcock, isomorphic mimicry).
An AI is very good at producing that list, which makes it very good at that failure.

The user ratified a specific resolution to this (Pending Decision 5, 2026-08-11): the instrument
SHOULD give a final recommendation, but must reach it by interrogating first. The binding
constraint is therefore **traceability** — the recommendation has to be derivable from what was
elicited about THIS situation, not from a template.

    decisions the user actually faces
      -> per-decision internalize-vs-market verdict     (Coase 1937 / Williamson)
      -> pairs worth asking about, from EXPENSIVE shared facts only   (Galbraith)
      -> an ELICITED yes/no per pair
      -> retained capabilities, but ONLY where every internal pair was affirmed

WHY "CAPABILITY" AND NOT "DEPARTMENT". A group of decisions that must be made together may need
one part-time person, a standing committee, a recurring meeting, or eventually a department.
Calling the output a department picks the organisational form before anyone has decided it, which
is the same import-the-template failure one level down. Form is a separate, later, human step.

THE CHAINING DEFECT THIS FILE WAS BUILT WITH, AND NO LONGER HAS. The first version computed
connected components over "shares at least one information need". Running it showed the damage:
four decisions A(refinance)-B(renovate)-C(pick contractor)-D(contractor bonus), where A and D share
nothing whatever, collapsed into one unit because B and C bridged them. Worse, a result previously
reported as a non-obvious insight — acquisition, cash-phasing and planting forming one capability —
was partly this artifact: cash-phasing and planting share ZERO facts and were joined only through
acquisition. A test PINNED the chaining as desired behaviour, with a docstring arguing it was
correct.

Two changes remove it. Grouping now runs over AFFIRMED COUPLINGS rather than shared facts, and a
group becomes a capability only if it is COMPLETE — every pair inside it independently affirmed. An
incomplete group is not a smaller capability, it is NOT a capability: its links are reported for a
human to group. So A-B affirmed and B-C affirmed no longer implies A-C.

NO INVENTED NUMBERS. The Coase test compares two quantities the USER supplies. There is no
threshold, no weighting, no scoring constant, and no capacity limit anywhere in this file. Where an
input is missing the verdict is `UNDECIDABLE` and the missing field is NAMED, because guessing it
would be the same class of act invariant I11 forbids for numeric thresholds. Maximal-clique
enumeration was considered and rejected for exactly this reason: it is exponential in the worst
case, and bounding it would require a constant nobody ratified.

ACCOUNTABILITY IS A ROLE, NEVER A PERSON. Every decision carries an accountable ROLE — including
MARKET ones, because somebody internal still selects the supplier, briefs them, and inspects the
result, and an unowned bought-in judgment is how a supplier quietly ends up deciding for you. An
unfilled slot is REPORTED alongside the undecided, never blocking and never filled with a guess.

WHAT THIS DELIBERATELY DOES NOT DO. It does not rank decisions, choose a strategy, name a
capability, or say which matters most. It converts an elicited inventory into a structure. Judgment
stays with the people who answered the questions.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional

# --------------------------------------------------------------------------------------
# Verdicts
# --------------------------------------------------------------------------------------


class Sourcing(Enum):
    """Where a recurring decision should be made from."""

    #: Hold the capability in-house. Either the market is cheaper to leave, or there is no market.
    INTERNALIZE = "internalize"
    #: Buy it per-transaction. Cheaper than holding the capability, and no private information
    #: blocks an outsider from doing it well.
    MARKET = "market"
    #: Buy the EXECUTION, hold the JUDGMENT. The market is cheaper on price, but the decision
    #: depends on things only the owner knows, so an outsider can do the work and cannot make the
    #: call.
    #:
    #: This state exists because the first run of this module was wrong. Private information was
    #: recorded, printed as a "degraded" note, and then had no effect on the verdict — a declared
    #: field nothing acted on. Williamson's point is that asset specificity DRIVES internalization
    #: rather than annotating it. Hybrid is derived, not invented: market-cheaper AND private
    #: information present.
    HYBRID = "hybrid"
    #: The inputs needed to decide are missing. NOT a default, NOT a guess — a named gap.
    UNDECIDABLE = "undecidable"


class Reversibility(Enum):
    REVERSIBLE = "reversible"
    COSTLY = "costly"
    IRREVERSIBLE = "irreversible"


class Assurance(Enum):
    """How independently a decision must be CHECKED before it becomes final.

    Assurance is ORTHOGONAL to sourcing, and conflating the two is a real modelling error: brain
    surgery is about as high-consequence as a decision gets and is still bought from outside. What
    consequence drives is how hard you check, not who holds the capability.

    This axis exists because `reversibility` was elicited, asked about in the interview, described
    in the protocol as a question that "changes the answer" — and then fed no verdict at all. That
    is the same declared-field-nothing-acts-on shape that made `private_information` a live defect
    in this module. A field that changes nothing should either drive something or stop being asked.
    """

    #: Reversible: if you can undo it, the cost of being wrong once IS the undo.
    SELF_CHECK = "self_check"
    #: Costly to unwind: someone who is not making the call looks at it before it commits.
    SECOND_OPINION = "second_opinion"
    #: Irreversible: reviewed by someone independent of the decider AND of any supplier, because a
    #: supplier paid to do the work is not a check on whether the work should happen.
    INDEPENDENT_REVIEW = "independent_review"
    #: Consequence not yet elicited. Not a default — a named gap, as everywhere else here.
    UNDECIDABLE = "undecidable"


#: Consequence -> how hard to check. An ordered 3-value elicited enum mapped onto an ordered
#: 3-value response. NOT a numeric threshold: `stake_per_decision` is deliberately NOT consulted,
#: because turning money-at-stake into a level would need a cutoff nobody ratified.
_ASSURANCE_BY_REVERSIBILITY = {
    Reversibility.REVERSIBLE: Assurance.SELF_CHECK,
    Reversibility.COSTLY: Assurance.SECOND_OPINION,
    Reversibility.IRREVERSIBLE: Assurance.INDEPENDENT_REVIEW,
}


class FactKind(Enum):
    """How expensive a fact is to move to somebody else.

    This is the distinction the first version lacked, and its absence was the second defect:
    "should we acquire this building" and "can we run payroll on Friday" were grouped because both
    need `cash_available` — a number in a spreadsheet that anyone handed the file would have.
    Cheap facts do not couple decisions; they are just data both decisions read.
    """

    #: Written down. Hand over the file and the recipient has it. Couples nothing.
    TRANSFERABLE_RECORD = "transferable_record"
    #: Specific to how this organisation operates. Transferable, but only by explaining it.
    ORGANIZATION_SPECIFIC_CONTEXT = "organization_specific_context"
    #: Known from experience and never written down. The expensive kind.
    TACIT_CONTEXT = "tacit_context"


#: Only these kinds make a shared fact a reason to SUSPECT coupling. A transferable record is
#: shared data, not shared context.
_COUPLING_KINDS = frozenset({FactKind.ORGANIZATION_SPECIFIC_CONTEXT, FactKind.TACIT_CONTEXT})


# --------------------------------------------------------------------------------------
# The elicited record
# --------------------------------------------------------------------------------------


@dataclass(frozen=True)
class DecisionRecord:
    """One recurring decision, in the words of the person who makes it.

    Every field is ELICITED. Nothing here may be inferred by the instrument — that is the whole
    point. `None` means "not yet answered", which is a reportable state, not a zero.
    """

    id: str
    #: The decision as the user states it. "Which parcels do we plant next season, with what?"
    question: str

    #: How many times per year this decision comes up.
    frequency_per_year: Optional[float] = None
    #: What it costs to have an outsider make this decision ONCE — their fee, plus finding them,
    #: briefing them, and checking the result. Williamson's transaction cost, in the user's units.
    external_engagement_cost: Optional[float] = None
    #: What it costs per year to hold the capability in-house — salary, tools, attention.
    internal_annual_cost: Optional[float] = None
    #: Is there anyone to buy this from at all? `False` forces internalization regardless of cost.
    external_market_exists: Optional[bool] = None

    #: Things known to the user that an outsider would not have. Non-empty does NOT silently
    #: adjust the arithmetic — it FLAGS the market option as degraded, because quantifying the
    #: degradation would mean inventing a number.
    private_information: tuple = ()

    #: What must be KNOWN to make this decision.
    information_needs: frozenset = frozenset()
    #: `(fact, FactKind)` pairs. A fact with no kind is UNCLASSIFIED and generates no coupling
    #: candidate — fail closed, because guessing that an unclassified fact is expensive would
    #: manufacture the coupling this module exists to elicit.
    fact_kinds: tuple = ()

    #: The ROLE answerable for this decision. Never a person's name: a role survives the person
    #: leaving, and a name in a persisted artifact is a privacy leak waiting to happen. Empty
    #: means UNFILLED, which is reported, not guessed.
    accountable_role: str = ""

    #: Is this ONE decision, or several wearing one sentence? Elicited, never inferred.
    #: `False` REFUSES to source it: "manage financing" and "should we offer 1.2M for 123 Main St"
    #: are both legitimate English and produce completely different structures from the same
    #: enterprise, so a verdict on a compound question is meaningless rather than approximate.
    #: `None` is merely unasked — it does not block, because the four cost fields are what the
    #: verdict actually consumes.
    atomic: Optional[bool] = None

    #: Context for the humans. Deliberately NOT an input to any verdict — money at stake tells you
    #: how much care a decision deserves, and turning it into a level would need a cutoff nobody
    #: ratified. Consequence drives assurance; stake does not.
    stake_per_decision: Optional[float] = None
    #: Drives ASSURANCE (how hard to check), never sourcing (who holds it).
    reversibility: Optional[Reversibility] = None

    def missing_fields(self) -> tuple:
        """Exactly which answers are still needed for a sourcing verdict."""
        needed = ("frequency_per_year", "external_engagement_cost",
                  "internal_annual_cost", "external_market_exists")
        return tuple(n for n in needed if getattr(self, n) is None)

    def annual_external_cost(self) -> Optional[float]:
        if self.frequency_per_year is None or self.external_engagement_cost is None:
            return None
        return self.frequency_per_year * self.external_engagement_cost

    def kind_of(self, fact: str) -> Optional[FactKind]:
        for f, k in self.fact_kinds:
            if f == fact:
                return k
        return None

    def unclassified_facts(self) -> tuple:
        return tuple(sorted(f for f in self.information_needs if self.kind_of(f) is None))

    def expensive_facts(self) -> frozenset:
        """Facts whose sharing is a REASON to suspect two decisions must be made together."""
        return frozenset(f for f in self.information_needs if self.kind_of(f) in _COUPLING_KINDS)


@dataclass(frozen=True)
class SourcingVerdict:
    decision_id: str
    sourcing: Sourcing
    #: Plain-language derivation, quoting the user's own numbers back. This IS the traceability.
    rationale: str
    annual_external_cost: Optional[float] = None
    internal_annual_cost: Optional[float] = None
    #: True when private information means an outsider could not do this WELL, whatever it costs.
    market_option_degraded: bool = False
    missing: tuple = ()


def classify_sourcing(d: DecisionRecord) -> SourcingVerdict:
    """The Coase test, with the user's numbers and no invented ones.

    Order matters. A missing answer is reported BEFORE any comparison, so an incomplete inventory
    can never be silently completed by a default.
    """
    if d.atomic is False:
        return SourcingVerdict(
            d.id, Sourcing.UNDECIDABLE,
            "this is more than one decision, so no single verdict is meaningful - split it and "
            "re-run. A compound question does not get an approximate answer here; it gets none.",
            missing=("atomic",),
            market_option_degraded=bool(d.private_information))

    missing = d.missing_fields()
    if missing:
        return SourcingVerdict(
            d.id, Sourcing.UNDECIDABLE,
            "cannot be sourced yet - still unanswered: {}. No default is applied; supplying one "
            "would be the instrument inventing the answer it exists to elicit.".format(
                ", ".join(missing)),
            missing=missing,
            market_option_degraded=bool(d.private_information))

    if not d.external_market_exists:
        return SourcingVerdict(
            d.id, Sourcing.INTERNALIZE,
            "no external market exists for this decision, so it is held in-house regardless of "
            "cost - there is nothing to buy.",
            annual_external_cost=d.annual_external_cost(),
            internal_annual_cost=d.internal_annual_cost,
            market_option_degraded=bool(d.private_information))

    ext = d.annual_external_cost()
    internal = d.internal_annual_cost
    degraded = bool(d.private_information)

    if ext > internal:
        why = ("going to the market {:g} times a year at {:g} each costs {:g}, against {:g} to "
               "hold it in-house - cheaper to own.").format(
                   d.frequency_per_year, d.external_engagement_cost, ext, internal)
        return SourcingVerdict(d.id, Sourcing.INTERNALIZE, why, ext, internal, degraded)

    priced = ("going to the market {:g} times a year at {:g} each costs {:g}, against {:g} to "
              "hold it in-house - cheaper to buy.").format(
                  d.frequency_per_year, d.external_engagement_cost, ext, internal)

    if degraded:
        why = (priced + " BUT this decision depends on {} - things an outsider cannot acquire at "
               "any price. So the market can supply the EXECUTION and cannot supply the "
               "JUDGMENT: hire the work, keep the call.".format(
                   ", ".join(d.private_information)))
        return SourcingVerdict(d.id, Sourcing.HYBRID, why, ext, internal, True)

    return SourcingVerdict(d.id, Sourcing.MARKET, priced, ext, internal, False)


# --------------------------------------------------------------------------------------
# Assurance — how hard to check, which is NOT who holds the capability
# --------------------------------------------------------------------------------------


@dataclass(frozen=True)
class AssuranceVerdict:
    decision_id: str
    assurance: Assurance
    rationale: str
    #: True when the checker must also be independent of the SUPPLIER, not merely of the decider.
    supplier_conflicted: bool = False


def classify_assurance(d: DecisionRecord, sourcing: Optional[Sourcing] = None) -> AssuranceVerdict:
    """Derive the checking requirement from consequence alone.

    `sourcing` is accepted only to note a supplier conflict of interest; it never changes the
    LEVEL. That is the whole point of splitting the axes.
    """
    if d.reversibility is None:
        return AssuranceVerdict(
            d.id, Assurance.UNDECIDABLE,
            "cannot set a checking requirement yet - 'what happens if you get it wrong once?' is "
            "unanswered. No default is applied.")

    level = _ASSURANCE_BY_REVERSIBILITY[d.reversibility]
    bought = sourcing in (Sourcing.MARKET, Sourcing.HYBRID)
    conflicted = bought and level is Assurance.INDEPENDENT_REVIEW

    why = {
        Assurance.SELF_CHECK:
            "getting this wrong once is recoverable, so the person making it checks their own work.",
        Assurance.SECOND_OPINION:
            "getting this wrong once is expensive to unwind, so someone who is not making the call "
            "reviews it before it commits.",
        Assurance.INDEPENDENT_REVIEW:
            "getting this wrong once is permanent, so it is reviewed by someone independent of the "
            "person making it.",
    }[level]

    if conflicted:
        why += (" This one is bought in, so the reviewer must ALSO be independent of the supplier - "
                "a supplier paid to do the work is not a check on whether it should happen.")

    return AssuranceVerdict(d.id, level, why, conflicted)


# --------------------------------------------------------------------------------------
# Coupling — asked, not assumed
# --------------------------------------------------------------------------------------


#: The single question that decides whether two decisions must be made together. A yes/no the user
#: supplies. A weighted score was proposed and REJECTED: any scoring expression needs weights, and
#: a weight would be a number the instrument invented.
COUPLING_QUESTION = (
    "Would these two decisions come out materially worse if different people made them and could "
    "only exchange written notes?")


@dataclass(frozen=True)
class CandidateCoupling:
    """A pair worth ASKING about. Not a finding — a question the cheap filter says is worth the
    user's time.

    Shared expensive facts are NECESSARY BUT NOT SUFFICIENT. This filter exists only to keep the
    instrument small: asking every pair is quadratic, and on a 20-decision inventory that is 190
    judgments nobody will make honestly.

    NAMED RESIDUAL: it cannot see a coupling between two decisions that share no RECORDED fact but
    turn on the same unrecorded context. The user may add a pair by hand. The filter is a cost
    control, not a claim about reality, and it is reported as such.
    """

    a: str
    b: str
    shared_facts: tuple

    def prompt(self) -> str:
        return "[{} + {}] {} (both turn on: {})".format(
            self.a, self.b, COUPLING_QUESTION, ", ".join(self.shared_facts))


@dataclass(frozen=True)
class CouplingRecord:
    """The user's ELICITED answer for ONE pair. The only thing that may group decisions."""

    a: str
    b: str
    coupled: bool

    def key(self) -> frozenset:
        return frozenset((self.a, self.b))


@dataclass(frozen=True)
class ConfirmedCapability:
    """A set of decisions that must be made together, where EVERY internal pair was affirmed.

    Completeness is the anti-chaining rail. A set whose members are not all mutually coupled is
    exactly the pathology this module shipped with, so it does not become a smaller capability —
    it does not become a capability at all.
    """

    decision_ids: tuple
    #: The user's own decision questions, verbatim. Traceability, readable by a human.
    derived_from: tuple
    #: Every pair inside, all affirmed. The evidence, not a summary of it.
    affirmed_pairs: tuple

    #: Deliberately NOT auto-named. Naming it "Finance" would import a template through the back
    #: door; the group is what was derived, and the label is the user's to give. So is the
    #: organisational FORM — one person, a committee, or a department.
    label: str = ""

    def size(self) -> int:
        return len(self.decision_ids)


@dataclass(frozen=True)
class UngroupedCouplingLinks:
    """Decisions linked by affirmation but NOT mutually coupled. A human has to group these.

    Reported rather than resolved. Guessing the grouping is precisely the chaining defect, and a
    rule for splitting an incomplete group would need a threshold nobody ratified.
    """

    decision_ids: tuple
    affirmed_pairs: tuple
    missing_pairs: tuple

    def why(self) -> str:
        return ("{} decisions are linked by {} affirmed pair(s), but {} pair(s) were never "
                "affirmed, so they are not all mutually coupled. Grouping them is a human "
                "judgment this instrument will not make for you.").format(
                    len(self.decision_ids), len(self.affirmed_pairs), len(self.missing_pairs))


def coupling_candidates(decisions, verdicts=None) -> list:
    """Pairs worth asking the coupling question about — retained decisions, expensive shared facts.

    MARKET and UNDECIDABLE decisions are excluded: you do not group a capability you buy outright,
    and you must not group one you have not finished thinking about.
    """
    by_id = {d.id: d for d in decisions}
    if verdicts is None:
        verdicts = [classify_sourcing(d) for d in decisions]
    retained = sorted(v.decision_id for v in verdicts
                      if v.sourcing in (Sourcing.INTERNALIZE, Sourcing.HYBRID))

    out = []
    for i, a in enumerate(retained):
        for b in retained[i + 1:]:
            shared = by_id[a].expensive_facts() & by_id[b].expensive_facts()
            if shared:
                out.append(CandidateCoupling(a, b, tuple(sorted(shared))))
    return out


def derive_capabilities(decisions, couplings, verdicts=None):
    """Group ONLY on affirmed couplings, and ONLY where the group is complete.

    Returns `(confirmed, ungrouped)`.

    Components are built over affirmed pairs, then each component is CHECKED for completeness.
    That check is what refuses chaining: with A-B and B-C affirmed but A-C not, the component
    {A,B,C} needs three pairs and has two, so it yields no capability. Completeness is O(pairs) on
    an already-formed component — no clique enumeration, and therefore no capacity constant.
    """
    by_id = {d.id: d for d in decisions}
    if verdicts is None:
        verdicts = [classify_sourcing(d) for d in decisions]
    retained = {v.decision_id for v in verdicts
                if v.sourcing in (Sourcing.INTERNALIZE, Sourcing.HYBRID)}

    affirmed = {}
    for c in couplings:
        if c.coupled and c.a in retained and c.b in retained and c.a != c.b:
            affirmed[c.key()] = (min(c.a, c.b), max(c.a, c.b))

    adjacency = {}
    for a, b in affirmed.values():
        adjacency.setdefault(a, set()).add(b)
        adjacency.setdefault(b, set()).add(a)

    seen, components = set(), []
    for node in sorted(adjacency):
        if node in seen:
            continue
        stack, comp = [node], []
        seen.add(node)
        while stack:
            cur = stack.pop()
            comp.append(cur)
            for nxt in sorted(adjacency[cur]):
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        components.append(tuple(sorted(comp)))

    confirmed, ungrouped = [], []
    for comp in components:
        wanted = [(comp[i], comp[j])
                  for i in range(len(comp)) for j in range(i + 1, len(comp))]
        have = [p for p in wanted if frozenset(p) in affirmed]
        missing = [p for p in wanted if frozenset(p) not in affirmed]
        if missing:
            ungrouped.append(UngroupedCouplingLinks(comp, tuple(have), tuple(missing)))
        else:
            confirmed.append(ConfirmedCapability(
                decision_ids=comp,
                derived_from=tuple(by_id[m].question for m in comp),
                affirmed_pairs=tuple(have)))

    confirmed.sort(key=lambda c: (-c.size(), c.decision_ids))
    ungrouped.sort(key=lambda u: (-len(u.decision_ids), u.decision_ids))
    return confirmed, ungrouped


# --------------------------------------------------------------------------------------
# Accountability — a role or an empty slot, never a name
# --------------------------------------------------------------------------------------


@dataclass(frozen=True)
class AccountabilitySlot:
    """Who ANSWERS for a decision, as a role.

    Applies to every decision regardless of sourcing. A MARKET decision still needs someone
    internal to pick the supplier, brief them, and inspect the result — the critique's point, and
    correct: outsourcing the work does not outsource the accountability.
    """

    decision_id: str
    role: str = ""

    def is_filled(self) -> bool:
        return bool(self.role.strip())


def accountability(decisions) -> list:
    return [AccountabilitySlot(d.id, d.accountable_role) for d in decisions]


# --------------------------------------------------------------------------------------
# The interrogation side
# --------------------------------------------------------------------------------------

#: One question per unanswered field, phrased so a non-specialist can answer it from their own
#: experience rather than having to estimate an abstraction.
_FIELD_QUESTIONS = {
    "frequency_per_year":
        "How many times a year does this actually come up? A rough count of the last two years is "
        "fine - it does not need to be exact, it needs to be yours.",
    "external_engagement_cost":
        "If you handed this to an outside specialist ONCE, what would it cost you all-in - their "
        "fee, plus the time to find them, brief them, and check their work?",
    "internal_annual_cost":
        "What would it cost per year to keep this capability in-house - the person's time, the "
        "tools, and the attention it takes off other things?",
    "external_market_exists":
        "Is there anyone you could actually buy this judgement from? If nobody sells it, that "
        "settles it on its own.",
}

#: Asked of EVERY decision, answered or not. These are the ones that change the answer rather than
#: fill in a field.
_STANDING_QUESTIONS = (
    "What do you know about this that an outside expert could not find out? That is the thing that "
    "makes buying it worse than it looks on price.",
    "What has to be KNOWN before you can make this call? List the facts, not the sources.",
    "For each of those facts, which is it: (a) written down somewhere, so anyone handed the file "
    "would have it; (b) specific to how you operate, so you would have to explain it; or (c) "
    "something you know from experience and have never written down? Only (b) and (c) are reasons "
    "two decisions might have to be made by the same person.",
    "Who ANSWERS for this decision - the role, not the person? If nobody does yet, say so.",
    "What happens if you get it wrong once? Say whether it is recoverable, expensive, or permanent.",
    "Is this ONE decision, or several? Could two reasonable people answer different PARTS of this "
    "question differently? If so it needs splitting before anything here means much.",
)


def interview_questions(d: DecisionRecord) -> list:
    """The exact questions still needed for THIS decision — no generic questionnaire.

    Only unanswered fields generate a question, so a second pass is short. The standing questions
    appear only where their answer is still missing.
    """
    qs = ["[{}] {}".format(d.id, d.question)]
    for f in d.missing_fields():
        qs.append("  - {}".format(_FIELD_QUESTIONS[f]))
    if not d.private_information:
        qs.append("  - {}".format(_STANDING_QUESTIONS[0]))
    if not d.information_needs:
        qs.append("  - {}".format(_STANDING_QUESTIONS[1]))
    elif d.unclassified_facts():
        qs.append("  - {} (unclassified so far: {})".format(
            _STANDING_QUESTIONS[2], ", ".join(d.unclassified_facts())))
    if not d.accountable_role.strip():
        qs.append("  - {}".format(_STANDING_QUESTIONS[3]))
    if d.reversibility is None:
        qs.append("  - {}".format(_STANDING_QUESTIONS[4]))
    if d.atomic is None:
        qs.append("  - {}".format(_STANDING_QUESTIONS[5]))
    return qs


@dataclass(frozen=True)
class InventoryReport:
    verdicts: tuple
    #: How hard each decision must be checked. A SEPARATE axis from `verdicts` — a bought-in
    #: decision can still require independent review.
    assurance: tuple
    #: Groups where every internal pair was affirmed. The only computed structure.
    capabilities: tuple
    #: Linked but not mutually coupled — handed back for a human to group.
    ungrouped: tuple
    #: Pairs the user has not yet answered the coupling question for.
    pending_couplings: tuple
    undecided: tuple
    #: Decisions with no accountable role. Reported, never guessed, never blocking.
    unowned: tuple
    #: Decisions whose consequence is unanswered, so no checking requirement can be set.
    unassured: tuple
    open_questions: tuple

    @property
    def is_complete(self) -> bool:
        return not (self.undecided or self.pending_couplings or self.ungrouped
                    or self.unowned or self.unassured)


def build_inventory(decisions, couplings=()) -> InventoryReport:
    """Everything at once: verdicts, confirmed capabilities, and every gap by name.

    An incomplete inventory still produces what IS settled — the 'degrade, do not block' shape. It
    never hides the gap: undecided decisions, unanswered coupling questions, ungrouped links and
    unowned decisions all come back in the same object, so a partial answer cannot be mistaken for
    a full one.
    """
    verdicts = [classify_sourcing(d) for d in decisions]
    by_verdict = {v.decision_id: v.sourcing for v in verdicts}
    assur = [classify_assurance(d, by_verdict.get(d.id)) for d in decisions]
    couplings = tuple(couplings)
    confirmed, ungrouped = derive_capabilities(decisions, couplings, verdicts)

    answered = {c.key() for c in couplings}
    pending = tuple(c for c in coupling_candidates(decisions, verdicts)
                    if frozenset((c.a, c.b)) not in answered)

    undecided = tuple(v.decision_id for v in verdicts if v.sourcing is Sourcing.UNDECIDABLE)
    unowned = tuple(s.decision_id for s in accountability(decisions) if not s.is_filled())
    unassured = tuple(a.decision_id for a in assur if a.assurance is Assurance.UNDECIDABLE)

    questions = []
    for d in decisions:
        qs = interview_questions(d)
        if len(qs) > 1:
            questions.extend(qs)
    questions.extend(c.prompt() for c in pending)

    return InventoryReport(tuple(verdicts), tuple(assur), tuple(confirmed), tuple(ungrouped),
                           pending, undecided, unowned, unassured, tuple(questions))


def render_report(report: InventoryReport) -> str:
    """Human-readable, with the derivation shown rather than summarised."""
    lines = ["DECISION SOURCING"]
    for v in report.verdicts:
        lines.append("  {:<10} {:<12} {}".format(v.decision_id, v.sourcing.value, v.rationale))

    lines.append("")
    lines.append("ASSURANCE (how hard to check - a SEPARATE question from who holds it)")
    for a in report.assurance:
        lines.append("  {:<10} {:<20} {}".format(a.decision_id, a.assurance.value, a.rationale))

    lines.append("")
    lines.append("RETAINED CAPABILITIES ({} - every internal pair affirmed by you; the "
                 "organisational form is still yours to choose)".format(len(report.capabilities)))
    for i, cap in enumerate(report.capabilities, 1):
        lines.append("  {}. {} decision(s): {}".format(
            i, cap.size(), ", ".join(cap.decision_ids)))
        for q in cap.derived_from:
            lines.append("     <- {}".format(q))

    if report.ungrouped:
        lines.append("")
        lines.append("HUMAN GROUPING REQUIRED ({})".format(len(report.ungrouped)))
        for u in report.ungrouped:
            lines.append("  {}".format(", ".join(u.decision_ids)))
            lines.append("     {}".format(u.why()))
            lines.append("     never affirmed: {}".format(
                ", ".join("{}+{}".format(a, b) for a, b in u.missing_pairs)))

    if report.pending_couplings:
        lines.append("")
        lines.append("COUPLING QUESTIONS UNANSWERED ({} - no group forms until you answer)".format(
            len(report.pending_couplings)))
        for c in report.pending_couplings:
            lines.append("  {} + {} (both turn on: {})".format(
                c.a, c.b, ", ".join(c.shared_facts)))

    if report.undecided:
        lines.append("")
        lines.append("UNANSWERED ({}) - these join no capability until answered".format(
            len(report.undecided)))
        lines.extend("  {}".format(u) for u in report.undecided)

    if report.unowned:
        lines.append("")
        lines.append("NO ACCOUNTABLE ROLE ({}) - including any bought-in decision, which still "
                     "needs someone internal to own the supplier".format(len(report.unowned)))
        lines.extend("  {}".format(u) for u in report.unowned)

    if report.unassured:
        lines.append("")
        lines.append("NO CHECKING REQUIREMENT ({}) - consequence unanswered".format(
            len(report.unassured)))
        lines.extend("  {}".format(u) for u in report.unassured)

    if report.open_questions:
        lines.append("")
        lines.append("QUESTIONS TO ASK")
        lines.extend("  " + q for q in report.open_questions)
    return "\n".join(lines)


__all__ = [n for n in dir() if not n.startswith("_")]
