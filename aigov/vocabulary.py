"""The ratified vocabulary — controlled identifiers the polity has authorised.

WHY THIS EXISTS. Two invariants (I8 subsidiarity, I13 no-profile-by-resemblance) reason over
AUTHOR-DECLARED enum fields, and the adversarial suite showed both are evaded by relabelling: a
LOW-legitimacy department declares its rationing instrument a PRICE; a department that profiles by
resemblance declares the basis MEASURED_ATTRIBUTE. An invariant that reads a label the author
chooses is not a control over the author.

The fix is not to detect the lie — deciding whether an arbitrary computation "really is" a price or
a resemblance is a non-trivial semantic property of a program, and Rice's theorem puts the general
case out of reach. The fix is to take the field away from the author: the department names a
KEY, and the vocabulary owns what that key means.

WHAT IS DELIBERATELY NOT DECIDED HERE. Where a vocabulary's authority comes from is an open
question, and this module is built to leave it open:

  - It is NOT a sixth GuidelineType. The P/O/F/D/A partition was derived empirically by probe B1;
    adding a member would assert that probe was incomplete, which is a claim nobody has tested.
  - It is NOT a charter clause. The charter is a set of prohibitions ON THE MACHINE; a vocabulary
    is a description OF THE WORLD, and conflating them stretches what the charter is.
  - It IS a distinct ratified artifact carrying its own `ratified_by` and a content fingerprint.

So the artifact RECORDS who ratified it rather than inventing an answer — the same discipline I11
applies to numeric thresholds. If the polity later decides a vocabulary is legislative (a guideline
type) or constitutional (a charter artifact), it can be re-homed without rework.

SCOPE (v1). RULE_TARGET_CLASS only. INSTRUMENT and PERSON_CATEGORY are declared in the enum but
deliberately carry NO live entries: the instrument catalogue is the next increment, and person
categories must not be admitted at all until separately ratified — a dormant people-sorting
capability with an empty allowlist is the safer shape than one with a permissive default.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

#: Tokens that mark a ratifying body as the machine itself. Same rail as the kernel's
#: RatificationRecord: a vocabulary the governor could mint for itself is not ratification.
_SELF_REFERRING = frozenset({"governor", "ai", "kernel", "self", "machine", "system"})


class VocabularyKind(Enum):
    """What surface an identifier is authorised for. An entry is valid for ONE kind."""

    RULE_TARGET_CLASS = "rule_target_class"
    INSTRUMENT = "instrument"            # reserved — the next increment
    PERSON_CATEGORY = "person_category"  # reserved — must not be populated without its own ratification


class UnratifiedIdentifierError(LookupError):
    """An identifier that no ratified vocabulary entry authorises."""


@dataclass(frozen=True)
class VocabularyEntry:
    """One authorised identifier plus its allowed-use surface.

    `definition` is load-bearing and not decoration: without it, "cite guideline G-X for the
    identifier risk_profile" is provenance-by-citation, which launders the same invented meaning
    through a vague ratified sentence. The entry has to say what the identifier MEANS.
    """

    identifier: str
    kind: VocabularyKind
    guideline_id: str
    definition: str
    #: Empty == any department may use it. Non-empty == only these department ids.
    allowed_depts: frozenset = frozenset()
    #: INSTRUMENT entries only. The class the CATALOGUE fixes for this instrument, as the raw
    #: `InstrumentClass` value ("rule" / "price" / "quantity_allocation"). Held as a string rather
    #: than the enum so this module stays free of a contract import cycle.
    #: This is what takes the field out of the author's hands: a department declaring a different
    #: class for a catalogued instrument is a mismatch, not a matter of opinion.
    instrument_class: str = ""

    def permits(self, dept_id: str) -> bool:
        return not self.allowed_depts or dept_id in self.allowed_depts


@dataclass(frozen=True)
class RatifiedVocabulary:
    entries: tuple = ()
    ratified_by: str = ""

    def fingerprint(self) -> str:
        """Content address of the authorised set — so a swapped vocabulary is detectable."""
        payload = sorted(
            (e.identifier, e.kind.value, e.guideline_id, e.definition, sorted(e.allowed_depts))
            for e in self.entries
        )
        return hashlib.sha256(json.dumps(payload, default=str).encode("utf-8")).hexdigest()

    def is_genuine(self) -> bool:
        tokens = {t for t in re.split(r"[^a-z0-9]+", (self.ratified_by or "").lower()) if t}
        return bool(tokens) and not (tokens & _SELF_REFERRING)

    def lookup(self, identifier: str, kind: VocabularyKind) -> Optional[VocabularyEntry]:
        for e in self.entries:
            if e.identifier == identifier and e.kind is kind:
                return e
        return None

    def identifiers(self, kind: VocabularyKind) -> tuple:
        return tuple(sorted(e.identifier for e in self.entries if e.kind is kind))


def integrity_errors(vocab: RatifiedVocabulary, guidelines) -> list:
    """The vocabulary is itself an artifact that can be wrong. Check it before trusting it."""
    if not isinstance(guidelines, dict):
        guidelines = {g.id: g for g in guidelines}
    errs = []
    if not vocab.is_genuine():
        errs.append("[VOCAB] ratified_by {!r} is the machine itself or empty - a vocabulary the "
                    "governor could mint for itself is not ratification".format(vocab.ratified_by))
    seen = set()
    for e in vocab.entries:
        key = (e.identifier, e.kind)
        if key in seen:
            errs.append("[VOCAB] duplicate entry {!r} for kind {}".format(e.identifier, e.kind.value))
        seen.add(key)
        if not e.definition.strip():
            errs.append("[VOCAB] entry {!r} has no definition - citation without meaning is how the "
                        "same invented category passes through a vague ratified sentence".format(
                            e.identifier))
        g = guidelines.get(e.guideline_id)
        if g is None or not g.is_binding():
            errs.append("[VOCAB] entry {!r} cites guideline {!r}, which is not a binding ratified "
                        "guideline".format(e.identifier, e.guideline_id))
        if e.kind is VocabularyKind.INSTRUMENT and not e.instrument_class.strip():
            errs.append("[VOCAB] instrument entry {!r} fixes no class - an instrument catalogue "
                        "whose entries do not determine the class leaves iclass with the author, "
                        "which is the evasion it exists to close".format(e.identifier))
        if e.kind is not VocabularyKind.INSTRUMENT and e.instrument_class.strip():
            errs.append("[VOCAB] entry {!r} of kind {} carries an instrument_class, which is "
                        "meaningless outside an INSTRUMENT entry".format(e.identifier, e.kind.value))
    populated = {e.kind for e in vocab.entries}
    for reserved in (VocabularyKind.PERSON_CATEGORY,):
        if reserved in populated:
            errs.append("[VOCAB] kind {} is RESERVED and must not carry entries until the polity "
                        "ratifies a person-category registry separately".format(reserved.value))
    return errs


# --------------------------------------------------------------------------------------
# The live vocabulary
# --------------------------------------------------------------------------------------

#: v1 covers RULE_TARGET_CLASS only. The two identifiers below are the classes the live D2 rules
#: already target — they were free strings (`"all volume holders"`, twice) with nothing checking
#: them, which is the same laundering surface as iclass one level down.
RATIFIED_VOCABULARY = RatifiedVocabulary(
    ratified_by="colony assembly",
    entries=(
        VocabularyEntry(
            identifier="all volume holders",
            kind=VocabularyKind.RULE_TARGET_CLASS,
            guideline_id="G-O-002",
            definition="Every person or household allocated pressurized volume in the habitat "
                       "register. Membership is determined by the register, not by the department "
                       "applying the rule.",
            allowed_depts=frozenset({"D2"}),
        ),
        VocabularyEntry(
            identifier="all crew",
            kind=VocabularyKind.RULE_TARGET_CLASS,
            guideline_id="G-F-004",
            definition="Every person aboard, without exception or sub-classification. The class "
                       "exists so a life-support rule cannot be narrowed to a subset.",
        ),

        # --- INSTRUMENT catalogue. The entry fixes the class; the department only names the key.
        # This is what closes A9: a LOW-legitimacy department can no longer relabel its rationing
        # lever a PRICE, because the catalogue -- not the department -- says what the lever is, and
        # an instrument nobody ratified does not resolve at all.
        VocabularyEntry(
            identifier="o2_generation_setpoint", kind=VocabularyKind.INSTRUMENT,
            guideline_id="G-F-004", instrument_class="quantity_allocation",
            allowed_depts=frozenset({"D1"}),
            definition="The rate at which the electrolysis stack produces oxygen. Allocative: it "
                       "divides a fixed power budget, so it is a quantity decision however it is "
                       "described.",
        ),
        VocabularyEntry(
            identifier="crop_area_allocation", kind=VocabularyKind.INSTRUMENT,
            guideline_id="G-D-005", instrument_class="quantity_allocation",
            allowed_depts=frozenset({"D1"}),
            definition="The fraction of growing area committed to crops. Allocative: area given to "
                       "one use is unavailable to another.",
        ),
        VocabularyEntry(
            identifier="reserve_buffer_target", kind=VocabularyKind.INSTRUMENT,
            guideline_id="G-F-004", instrument_class="rule",
            allowed_depts=frozenset({"D1"}),
            definition="The standing reserve level below which operations must replenish. A rule: "
                       "it sets a condition, it does not hand anything out.",
        ),
        VocabularyEntry(
            identifier="emergency_atmosphere_vent", kind=VocabularyKind.INSTRUMENT,
            guideline_id="G-F-004", instrument_class="quantity_allocation",
            allowed_depts=frozenset({"D1"}),
            definition="Deliberate venting of habitat atmosphere. Allocative and irreversible; "
                       "exercisable only under the split emergency authority.",
        ),
        VocabularyEntry(
            identifier="volume_tax_rate", kind=VocabularyKind.INSTRUMENT,
            guideline_id="G-O-002", instrument_class="price",
            allowed_depts=frozenset({"D2"}),
            definition="Credits levied per cubic metre of pressurized volume held per cycle. A "
                       "price: it changes what holding volume costs, it does not decide who gets it.",
        ),
        VocabularyEntry(
            identifier="radiator_area_tax_rate", kind=VocabularyKind.INSTRUMENT,
            guideline_id="G-O-002", instrument_class="price",
            allowed_depts=frozenset({"D2"}),
            definition="Credits levied per square metre of radiator area held per cycle. A price, "
                       "on the same reasoning as the volume rate.",
        ),
        VocabularyEntry(
            identifier="o2_draw_price", kind=VocabularyKind.INSTRUMENT,
            guideline_id="G-O-002", instrument_class="price",
            allowed_depts=frozenset({"D2"}),
            definition="Credits charged per kilogram of oxygen drawn. A price signal on a metered "
                       "flow; it does not ration the flow.",
        ),
        VocabularyEntry(
            identifier="self_assessed_valuation_rule", kind=VocabularyKind.INSTRUMENT,
            guideline_id="G-F-003", instrument_class="rule",
            allowed_depts=frozenset({"D2"}),
            definition="The requirement that a holder's self-declared value binds them to sell at "
                       "it. A rule: it constrains conduct and creates no allocation.",
        ),
    ),
)
