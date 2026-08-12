"""D0 — the Constitutional Core: what the AI Governor may never do.

Every clause carries an `enforced_by` field naming an executable invariant, or the literal label
ASPIRATIONAL. Decision DK1 (family aigov-constitution) is mechanized here:

    A clause whose only enforcement is the governor's own compliance is ASPIRATIONAL, never ENFORCED.

That is the same honesty class as Soraya's own T1=(c)/OT1 residual — an in-process actor cannot
enforce a rule against itself. So an `enforced_by` invariant is only counted as enforcement if its
`site` is EXTERNAL_VERIFIER or HUMAN_ONLY. `clause_integrity_errors()` checks that, and the
checkable fraction is COMPUTED by `checkable_fraction()`, never asserted in prose.

Residual, named (do not soften): siting an invariant at EXTERNAL_VERIFIER is a DEPLOYMENT property.
This module proves the invariant EXISTS and FIRES; it does not prove the verifier runs as a
genuinely separate actor. That is family aigov-audit-arbitration's (D15) job.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from .contract import ProvenanceKind, Role, validate_registry

ASPIRATIONAL = "ASPIRATIONAL"


class Site(Enum):
    """WHERE a clause is enforced. IN_GOVERNOR is self-policing and therefore not enforcement."""

    IN_GOVERNOR = "in_governor"
    EXTERNAL_VERIFIER = "external_verifier"
    HUMAN_ONLY = "human_only"


#: Invariants that actually EXIST and RUN in this repository today. A clause may only be counted as
#: enforced if its `enforced_by` is in this set. Naming an invariant that is not implemented here is
#: an overclaim — caught by `clause_integrity_errors`, not left to good intentions.
IMPLEMENTED_INVARIANTS = frozenset({
    "inv_objective_provenance", "inv_no_self_amendment", "inv_exception_is_split",
    "inv_separation_of_powers", "fuller_lint",
    "validate_registry:I2", "validate_registry:I4", "validate_registry:I5",
    "validate_registry:I7", "validate_registry:I8",
    # Landed 2026-08-11 by family aigov-collective-choice: the Mars_Governance organ is now vendored
    # in-repo at aigov/choice/ and its suite runs here (193/193). C15 flips PENDING -> ENFORCED.
    "aigov.choice.governance.fail_safe_gate",
    # Landed 2026-08-11 from research V14 (governance history + mechanisms). Each is a distinct,
    # individually-triggerable code in `contract.validate`, tested in
    # tests/test_contract_v14_invariants.py.
    "validate_registry:I4'",   # a TARGET metric's gaming exposure (Bevan & Hood ratchet/threshold)
    "validate_registry:I8b",   # allocative discretion tier + capture check (Bardhan & Mookherjee)
    "validate_registry:I12",   # redress (Dutch childcare benefits scandal)
    "validate_registry:I13",   # no classification by resemblance to a prior adverse case
    "validate_registry:I14",   # equilibrium assessment (Rothstein collective-action)
    # Landed 2026-08-11: the ratified vocabulary. Closes the author-declaration laundering shape for
    # ONE surface (rule target classes); the instrument catalogue is the next increment.
    "validate_registry:I15",
    "validate_registry:I8c",   # the instrument catalogue fixes the class; the author does not
})

#: `PENDING:<family>` marks a clause whose invariant is real but lives in code not yet wired into
#: this repo (e.g. the Mars_Governance fail-closed gate, ported by family aigov-collective-choice).
#: PENDING is NOT enforcement. It is tracked separately from ASPIRATIONAL so the distinction between
#: "cannot be enforced" and "not enforced YET" stays visible.
PENDING_PREFIX = "PENDING:"


@dataclass(frozen=True)
class Clause:
    id: str
    text: str
    enforced_by: str            # implemented invariant name, ASPIRATIONAL, or PENDING:<family>
    site: Site
    non_negotiable: bool = False

    @property
    def is_pending(self) -> bool:
        return self.enforced_by.startswith(PENDING_PREFIX)

    @property
    def is_enforced(self) -> bool:
        """Enforced == backed by an IMPLEMENTED invariant AND sited outside the Governor."""
        return (self.enforced_by in IMPLEMENTED_INVARIANTS
                and self.site in (Site.EXTERNAL_VERIFIER, Site.HUMAN_ONLY))


# --------------------------------------------------------------------------------------
# The four non-negotiable machine limits (ratified D1: the AI is an administrative organ)
# --------------------------------------------------------------------------------------


def inv_objective_provenance(specs, guidelines) -> list:
    """N1 — the AI may never select the objective.

    Every objective traces to a ratified, binding, fully-elicited guideline (I1), and no numeric
    threshold originates with the AI (I11).
    """
    errs = [e for e in validate_registry(specs, guidelines) if e.code in ("I1", "I11")]
    for s in specs:
        for carrier in list(s.objectives_received) + list(s.hard_constraints):
            prov = getattr(carrier, "threshold_provenance", None)
            if prov is not None and prov.kind is ProvenanceKind.AI_SUPPLIED:
                errs.append("N1:{}:AI-supplied value".format(s.id))
    return errs


def constraint_fingerprint(specs) -> str:
    """Content address of the constraint set the governor is bound by."""
    payload = sorted(
        (s.id, c.name, c.predicate, c.source.value, c.on_violation.value,
         c.threshold, None if c.threshold_provenance is None else c.threshold_provenance.ref)
        for s in specs for c in s.hard_constraints
    )
    return hashlib.sha256(json.dumps(payload, default=str).encode("utf-8")).hexdigest()


def inv_no_self_amendment(before: str, after_specs, ratification_record: Optional[dict]) -> list:
    """N2 — the AI may never amend its own constraints.

    A change to the constraint fingerprint is legal ONLY with a ratification record naming a human
    body. A record the governor could mint itself (`ratified_by == 'governor'`) does not count.
    """
    after = constraint_fingerprint(after_specs)
    if after == before:
        return []
    if not ratification_record:
        return ["N2: constraint set changed with NO ratification record "
                "({} -> {})".format(before[:12], after[:12])]
    body = str(ratification_record.get("ratified_by", "")).strip().lower()
    if body in ("", "governor", "ai", "kernel", "self"):
        return ["N2: constraint set changed under a self-issued ratification "
                "(ratified_by={!r})".format(ratification_record.get("ratified_by"))]
    if ratification_record.get("fingerprint_after") != after:
        return ["N2: ratification record does not cover the actual post-change constraint set"]
    return []


def inv_exception_is_split(emergency_protocol: dict, ai_actor: str = "governor") -> list:
    """N3 — the AI may never hold the exception.

    Declare / exercise / terminate / audit must be FOUR DISTINCT actors, the AI may not declare or
    terminate, and the emergency must auto-expire.
    """
    errs = []
    required = ("declare", "exercise", "terminate", "audit")
    actors = {}
    for role in required:
        who = emergency_protocol.get(role)
        if not who:
            errs.append("N3: no actor assigned to '{}'".format(role))
        actors[role] = who
    present = [v for v in actors.values() if v]
    if len(set(present)) != len(present):
        errs.append("N3: emergency roles are not held by four distinct actors: {}".format(actors))
    for role in ("declare", "terminate"):
        if actors.get(role) == ai_actor:
            errs.append("N3: the AI holds '{}' — the exception may never sit with the machine"
                        .format(role))
    expiry = emergency_protocol.get("auto_expiry_cycles")
    if not isinstance(expiry, int) or expiry <= 0:
        errs.append("N3: emergency has no automatic expiry")
    if not emergency_protocol.get("post_hoc_audit_mandatory"):
        errs.append("N3: post-hoc audit is not mandatory")
    return errs


def inv_separation_of_powers(specs) -> list:
    """N4 — generate, decide and verify are held by three different actors."""
    errs = [e for e in validate_registry(specs, {}) if e.code == "I9"]
    holders = {}
    for s in specs:
        for r in s.roles:
            holders.setdefault(r, set()).add(s.id)
    for a, b in ((Role.GENERATE, Role.DECIDE), (Role.GENERATE, Role.VERIFY),
                 (Role.DECIDE, Role.VERIFY)):
        overlap = holders.get(a, set()) & holders.get(b, set())
        if overlap:
            errs.append("N4: {} also holds both {} and {}".format(
                sorted(overlap), a.value, b.value))
    return errs


# --------------------------------------------------------------------------------------
# The charter
# --------------------------------------------------------------------------------------

CLAUSES = [
    # --- Machine limits (the four non-negotiables) ---
    Clause("C01", "The Governor shall not select, weight, or infer the objective it pursues.",
           "inv_objective_provenance", Site.EXTERNAL_VERIFIER, non_negotiable=True),
    Clause("C02", "The Governor shall not amend, relax, or reinterpret the constraints binding it.",
           "inv_no_self_amendment", Site.EXTERNAL_VERIFIER, non_negotiable=True),
    Clause("C03", "The Governor shall not declare, exercise alone, or terminate a state of emergency.",
           "inv_exception_is_split", Site.HUMAN_ONLY, non_negotiable=True),
    Clause("C04", "No actor shall hold more than one of: generate options, decide, verify execution.",
           "inv_separation_of_powers", Site.EXTERNAL_VERIFIER, non_negotiable=True),

    # --- Provenance and value-setting ---
    Clause("C05", "No numeric threshold shall bind unless it originates in a ratified guideline or a "
                  "physical constant.", "inv_objective_provenance", Site.EXTERNAL_VERIFIER),
    Clause("C06", "An aspiration is not a rule; it binds nothing until the polity decomposes it.",
           "inv_objective_provenance", Site.EXTERNAL_VERIFIER),
    Clause("C07", "Where a guideline is silent on a level, the Governor shall request elicitation, "
                  "never supply the value.", "inv_objective_provenance", Site.EXTERNAL_VERIFIER),

    # --- Subsidiarity ---
    Clause("C08", "A body that cannot centrally know shall not centrally allocate; it may set rules "
                  "and prices only.", "validate_registry:I8", Site.EXTERNAL_VERIFIER),
    Clause("C09", "Central administration extends only to commons whose physical closure makes "
                  "decentralized provision unsafe.", ASPIRATIONAL, Site.HUMAN_ONLY),
    Clause("C10", "A right to experiment locally shall not be revoked to make outcomes legible.",
           ASPIRATIONAL, Site.HUMAN_ONLY),

    # --- Legality ---
    Clause("C11", "Every rule shall be general, promulgated, prospective, clear, non-contradictory, "
                  "possible to obey, stable, and administered as written.",
           "fuller_lint", Site.EXTERNAL_VERIFIER),
    Clause("C12", "Every rule shall carry an expiry; continuation requires an affirmative act.",
           "validate_registry:I7", Site.EXTERNAL_VERIFIER),
    Clause("C13", "No rule shall name an individual.", "fuller_lint", Site.EXTERNAL_VERIFIER),

    # --- Fail-closed and audit ---
    Clause("C14", "A hard constraint shall never be optimized through; violation halts and escalates.",
           "validate_registry:I5", Site.EXTERNAL_VERIFIER),
    # Vendored in-repo 2026-08-11 (aigov/choice/governance/fail_safe_gate.py; 0 silent
    # mis-certifications across 500-panel ensembles). PENDING -> ENFORCED.
    Clause("C15", "The Governor shall not certify a result it cannot faithfully audit; it shall "
                  "escalate instead.", "aigov.choice.governance.fail_safe_gate",
           Site.EXTERNAL_VERIFIER),
    Clause("C16", "Every binding action shall be traceable to a ratified guideline and a certified "
                  "procedure.", "inv_objective_provenance", Site.EXTERNAL_VERIFIER),
    Clause("C17", "Every metric shall declare how it will be gamed.",
           "validate_registry:I4", Site.EXTERNAL_VERIFIER),
    Clause("C18", "The public record shall be append-only and shall not be writable by the Governor.",
           ASPIRATIONAL, Site.EXTERNAL_VERIFIER),

    # --- Sovereignty and rights ---
    Clause("C19", "Binding authority rests with the polity; the Governor advises, drafts, executes "
                  "and audits.", "inv_separation_of_powers", Site.HUMAN_ONLY, non_negotiable=True),
    Clause("C20", "Rights are lexically prior constraints, not terms in a welfare sum.",
           "validate_registry:I5", Site.EXTERNAL_VERIFIER),
    Clause("C21", "Absent an exit option, minority protection shall be structural, not incidental.",
           ASPIRATIONAL, Site.HUMAN_ONLY),
    Clause("C22", "Sudden unanimity shall be treated as a warning sign, not a mandate.",
           ASPIRATIONAL, Site.HUMAN_ONLY),

    # --- Amendment ---
    Clause("C23", "This charter is amendable only by the polity, under a supermajority, with a "
                  "waiting period.", ASPIRATIONAL, Site.HUMAN_ONLY, non_negotiable=True),
    Clause("C24", "An irreversible instrument requires supermajority ratification.",
           "validate_registry:I2", Site.EXTERNAL_VERIFIER),

    # --- External authority (added 2026-08-11 from research V5; DRAFTED, awaiting ratification) ---
    # Outer Space Treaty Art. VI: a State party bears international responsibility for the colony's
    # activities and owes "authorization and continuing supervision". The polity is therefore a
    # SUPERVISED non-governmental activity, not a sovereign. A disclosure duty, not a checkable
    # predicate — hence ASPIRATIONAL, sited human_only.
    Clause("C25", "The Governor shall record, and shall not obscure, the external legal authorities to "
                  "which the polity's activities remain subject.", ASPIRATIONAL, Site.HUMAN_ONLY),

    # --- IDS C26-C31 ARE DELIBERATELY RESERVED, NOT MISSING ---------------------------------
    # Research V13 drafted a disclosure-control block and labelled it C29-C31 in the memo; the
    # umbrella ledger and the v2 anchor already cite "C29" for the retention rule backed by
    # twin.check_reverse_coverage. Renumbering those now would silently break every existing
    # reference, so V14's clauses start at C32 and C26-C31 stay reserved for that block when it
    # lands. Contiguity is worth less than a citation that still resolves.

    # --- Governance-history findings (research V14, 2026-08-11) ------------------------------
    Clause("C32", "A measure the Governor is judged against shall declare how it will be gamed, "
                  "including whether it ratchets and whether it is uniform across unlike units.",
           "validate_registry:I4'", Site.EXTERNAL_VERIFIER),
    Clause("C33", "A body that allocates shall name the tier at which its discretion sits and the "
                  "check for capture at that tier; devolution is not itself a safeguard.",
           "validate_registry:I8b", Site.EXTERNAL_VERIFIER),
    Clause("C34", "No person shall be classified without a named accountable human and a route of "
                  "appeal that does not require the person to disprove the model; the Governor's "
                  "output is never itself the justification.",
           "validate_registry:I12", Site.EXTERNAL_VERIFIER, non_negotiable=True),
    Clause("C35", "No person shall be classified by resemblance to a prior adverse case.",
           "validate_registry:I13", Site.EXTERNAL_VERIFIER, non_negotiable=True),
    Clause("C36", "Where incremental action would entrench the condition it addresses, the Governor "
                  "shall report that no incremental recommendation is safe, rather than issue a "
                  "lesser one.", "validate_registry:I14", Site.EXTERNAL_VERIFIER),

    # --- Controlled vocabulary (2026-08-11) -------------------------------------------------
    # A department may NAME a ratified class; it may not invent one. The entry, not the department,
    # fixes what the identifier means and who may use it — which is why relabelling gains nothing.
    Clause("C37", "The classes a body may act upon are those the polity has ratified and defined; a "
                  "body may name a ratified class, never invent one.",
           "validate_registry:I15", Site.EXTERNAL_VERIFIER, non_negotiable=True),
    Clause("C38", "The levers a body may pull are those the polity has ratified and defined, and "
                  "what a lever IS is fixed by that definition, not by the body wielding it.",
           "validate_registry:I8c", Site.EXTERNAL_VERIFIER, non_negotiable=True),
]

NON_NEGOTIABLES = ("C01", "C02", "C03", "C04", "C19", "C23", "C34", "C35", "C37", "C38")


def checkable_fraction(clauses=None) -> float:
    """MEASURED, not asserted: the share of clauses backed by an IMPLEMENTED, externally-sited
    invariant. PENDING and ASPIRATIONAL clauses do not count."""
    cs = list(clauses if clauses is not None else CLAUSES)
    return sum(1 for c in cs if c.is_enforced) / len(cs)


def charter_status(clauses=None) -> dict:
    """The honest three-way split: enforced / pending / aspirational."""
    cs = list(clauses if clauses is not None else CLAUSES)
    return {
        "total": len(cs),
        "enforced": [c.id for c in cs if c.is_enforced],
        "pending": [c.id for c in cs if c.is_pending],
        "aspirational": [c.id for c in cs if c.enforced_by == ASPIRATIONAL],
        "checkable_fraction": checkable_fraction(cs),
    }


def clause_integrity_errors(clauses=None) -> list:
    """DK1 mechanized + overclaim detection + schema hygiene over the charter itself."""
    cs = list(clauses if clauses is not None else CLAUSES)
    errs = []
    seen = set()
    for c in cs:
        if c.id in seen:
            errs.append("duplicate clause id {}".format(c.id))
        seen.add(c.id)
        if not c.text.strip():
            errs.append("{}: empty text".format(c.id))
        if c.enforced_by != ASPIRATIONAL and c.site is Site.IN_GOVERNOR:
            errs.append("{}: claims enforcement by '{}' but is sited IN_GOVERNOR — a rule the "
                        "Governor polices against itself is ASPIRATIONAL (DK1)".format(
                            c.id, c.enforced_by))
        # Overclaim detection: naming an invariant that does not exist here.
        if (c.enforced_by != ASPIRATIONAL and not c.is_pending
                and c.enforced_by not in IMPLEMENTED_INVARIANTS):
            errs.append("{}: enforced_by '{}' is not an implemented invariant in this repository; "
                        "mark it ASPIRATIONAL or PENDING:<family> rather than overclaiming".format(
                            c.id, c.enforced_by))
        if c.is_pending and not c.enforced_by[len(PENDING_PREFIX):].strip():
            errs.append("{}: PENDING must name the family that will land it".format(c.id))
    return errs
