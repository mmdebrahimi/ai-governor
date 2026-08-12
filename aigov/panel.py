"""The advisory panel — heterogeneous model seats that ADVISE and never ratify.

WHY THIS IS NOT `intake.Panel`. That one is a SORTITION panel: citizens drawn by lot, whose
answers carry democratic legitimacy precisely because nobody selected them. Seating a language
model there would let a model vote on what only people can legitimately ratify. The two objects
are kept apart deliberately, and `PanelReading` below is built so it CANNOT be mistaken for a
ratification (see `ratified_by`).

WHAT THE RESEARCH FORCED (research_outputs/aigov-v15-persona-panels-and-model-diversity.md).
Three findings are encoded here as structure rather than advice, because advice in a docstring is
not a control:

  1. PERSONAS DO NOT CHANGE JUDGMENT. 162 personas x 4 model families x 2,410 questions showed no
     improvement over no persona at all, and expert personas make answers SOUND expert while
     damaging factual accuracy. So a `Seat` has no persona field, and `seat_errors` rejects one.
     Seats differ by MODEL, by what they can SEE, and by what they answer for -- never by
     personality.

  2. CONSENSUS IS SOCIAL, NOT EPISTEMIC. Across heterogeneous debates on six benchmarks, roughly
     one divergent case in four had the MINORITY holding the correct answer. So a divided panel is
     never collapsed to its majority: `DIVIDED` is a terminal reading that escalates, and every
     dissenting position is carried in the output rather than averaged away.

  3. DELIBERATION MUST BE BASELINED, NOT ASSUMED. Much of the measured benefit attributed to debate
     is explained by voting; with identical debaters every multi-agent method UNDERPERFORMED a
     single agent. So v1 elicits INDEPENDENTLY and cross-talk is unrepresentable: `elicit` hands
     each seat only `(seat, question)`, with no channel through which one seat's answer could reach
     another. Deliberation is a later increment that must beat this baseline to earn its place.

WHY TWO SEATS CANNOT VOTE. A strict majority of n is n // 2 + 1. For n = 2 that is 2 -- unanimity.
So on a two-seat panel "the majority agreed" and "both agreed" are the same statement, and calling
it a vote claims an independence check that was never performed. `MIN_VOTING_PANEL` is COMPUTED
from that arithmetic below rather than asserted, on the same discipline as I11: a threshold that
appears in a verdict has to come from somewhere.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Optional

#: Field names that would smuggle persona differentiation back in. Rejected at seat construction.
_PERSONA_FIELDS = frozenset({
    "persona", "personality", "character", "role", "role_play", "backstory",
    "temperament", "voice", "tone", "style", "archetype",
})


def strict_majority(n: int) -> int:
    """Votes needed to carry a strict majority of `n`."""
    return n // 2 + 1


#: The smallest panel on which a majority is genuinely weaker than unanimity -- i.e. the smallest
#: panel where aggregating adds information that "did they all agree?" does not already carry.
#: DERIVED, not chosen: it is the first n for which strict_majority(n) < n.
MIN_VOTING_PANEL = next(n for n in range(1, 64) if strict_majority(n) < n)


class NotRatifiableError(TypeError):
    """Raised when advisory output is used where a ratified artifact is required."""


class Concurrence(Enum):
    """What the seats did. Never what the polity decided."""

    CONCURRENT = "concurrent"          # every seat reached the same verdict
    DIVIDED = "divided"                # seats disagree -- escalate, do not collapse
    INSUFFICIENT_SEATS = "insufficient_seats"   # fewer seats than any reading needs
    NO_READING = "no_reading"          # no seat returned a usable answer


@dataclass(frozen=True)
class Seat:
    """One advisor. Distinguished by model, by visibility, and by what it answers for.

    `visibility` is load-bearing and is the second decorrelation lever: two seats given different
    evidence can disagree about the WORLD rather than merely about wording, and that disagreement
    is the signal the panel exists to surface. Two seats identical in both model and visibility are
    not two seats -- `seat_errors` rejects that pair.
    """

    id: str
    model: str
    #: The organisation that trained the model. Error reduction is highest across DIFFERENT
    #: organisations, so this is recorded to make homogeneity visible rather than implicit.
    operator: str
    #: What this seat was allowed to see. Empty == the question only.
    visibility: frozenset = frozenset()
    #: What this seat's answers are scored against later. Accountability is a role, never a person.
    answers_for: str = ""

    def fingerprint(self) -> str:
        payload = (self.id, self.model, self.operator, sorted(self.visibility), self.answers_for)
        return hashlib.sha256(json.dumps(payload).encode("utf-8")).hexdigest()[:16]


@dataclass(frozen=True)
class SeatOpinion:
    """One seat's independent answer. `raw` keeps the untruncated response for audit."""

    seat_id: str
    verdict: str
    reasoning: str = ""
    raw: str = ""
    #: Set when the seat failed to answer (timeout, parse failure, refusal).
    failed: bool = False


@dataclass(frozen=True)
class PanelReading:
    """What the panel OBSERVED. Advisory input to a decision; never the decision.

    This type deliberately has no `ratified_by`. Accessing that attribute raises rather than
    returning a falsy default, so a caller that duck-types this object into a ratification path
    fails loudly instead of silently admitting model output as authority.
    """

    question: str
    opinions: tuple
    concurrence: Concurrence
    #: Verdicts held by fewer seats than the plurality, kept verbatim. Never averaged away: the
    #: minority is right in roughly one divergent case in four.
    dissent: tuple = ()
    reason: str = ""

    @property
    def ratified_by(self):
        raise NotRatifiableError(
            "a PanelReading is advisory model output and carries no ratification; "
            "seats advise, the polity ratifies"
        )

    def is_actionable_alone(self) -> bool:
        """Always False. Recorded as a method so the answer is visible at every call site."""
        return False

    def caveat(self) -> str:
        if self.concurrence is Concurrence.CONCURRENT and len(self.opinions) < MIN_VOTING_PANEL:
            return ("{} seats agreed, which on a panel this small is unanimity rather than a "
                    "majority -- no independence was tested. Agreement here is weak evidence."
                    .format(len(self.opinions)))
        if self.concurrence is Concurrence.CONCURRENT:
            return ("seats agreed, but agreement among models is social convergence and is a poor "
                    "proxy for accuracy -- correlated training makes joint error ordinary")
        if self.concurrence is Concurrence.DIVIDED:
            return ("seats divided -- the dissenting position is retained because the minority "
                    "holds the correct answer in roughly one divergent case in four")
        return ""


def seat_errors(seats) -> list:
    """The bench is itself an artifact that can be wrong. Check it before trusting a reading."""
    errs = []
    seats = tuple(seats)
    if not seats:
        return ["[PANEL] no seats"]

    seen_ids = set()
    for s in seats:
        if s.id in seen_ids:
            errs.append("[PANEL] duplicate seat id {!r}".format(s.id))
        seen_ids.add(s.id)
        if not s.model.strip():
            errs.append("[PANEL] seat {!r} names no model - a seat is its model, not its label"
                        .format(s.id))
        if not s.operator.strip():
            errs.append("[PANEL] seat {!r} names no operator - decorrelation is claimed across "
                        "organisations, so the organisation has to be recorded".format(s.id))
        for bad in sorted(_PERSONA_FIELDS & set(vars(s).keys() if hasattr(s, "__dict__") else ())):
            errs.append("[PANEL] seat {!r} carries a persona field {!r}; persona prompts change "
                        "style but not judgment, and degrade accuracy on knowledge tasks"
                        .format(s.id, bad))

    # Two seats identical in BOTH model and visibility are one seat counted twice.
    for i, a in enumerate(seats):
        for b in seats[i + 1:]:
            if a.model == b.model and a.visibility == b.visibility:
                errs.append("[PANEL] seats {!r} and {!r} share a model and see the same evidence - "
                            "identical debaters underperform a single agent, so this is one seat "
                            "counted twice".format(a.id, b.id))

    if len({s.operator for s in seats}) == 1 and len(seats) > 1:
        errs.append("[PANEL] every seat is operated by {!r}; error reduction is highest ACROSS "
                    "organisations, and a single-operator bench reads as corroboration while "
                    "carrying one organisation's correlated error"
                    .format(seats[0].operator))
    return errs


def elicit(seats, question: str, ask: Callable[[Seat, str], SeatOpinion]) -> PanelReading:
    """Put ONE question to every seat independently and report what came back.

    `ask` receives only `(seat, question)`. There is deliberately no parameter through which one
    seat's answer could reach another, so v1 cannot deliberate even by mistake -- the independent
    baseline has to exist before deliberation can be shown to beat it.
    """
    seats = tuple(seats)
    opinions = []
    for s in seats:
        try:
            opinions.append(ask(s, question))
        except Exception as exc:                      # a dead seat is a missing seat, not a verdict
            opinions.append(SeatOpinion(seat_id=s.id, verdict="", failed=True, raw=repr(exc)))
    return read(question, tuple(opinions))


def read(question: str, opinions) -> PanelReading:
    """Classify a set of opinions. Pure -- no model calls, so it is testable without a network."""
    opinions = tuple(opinions)
    live = tuple(o for o in opinions if not o.failed and o.verdict.strip())

    if not live:
        return PanelReading(question, opinions, Concurrence.NO_READING,
                            reason="no seat returned a usable verdict")

    tally = {}
    for o in live:
        tally.setdefault(o.verdict.strip(), []).append(o.seat_id)

    if len(tally) == 1:
        if len(live) < MIN_VOTING_PANEL:
            reason = ("{} seats concurred; a strict majority of {} is {}, which equals unanimity, "
                      "so this reading tests no independence"
                      .format(len(live), len(live), strict_majority(len(live))))
        else:
            reason = "{} seats concurred".format(len(live))
        return PanelReading(question, opinions, Concurrence.CONCURRENT, reason=reason)

    top = max(len(v) for v in tally.values())
    dissent = tuple(sorted(
        "{} (held by {})".format(v, ", ".join(sorted(ids)))
        for v, ids in tally.items() if len(ids) < top
    ))
    return PanelReading(
        question, opinions, Concurrence.DIVIDED, dissent=dissent,
        reason="seats divided across {} distinct verdicts; NOT collapsed to the plurality"
               .format(len(tally)),
    )
