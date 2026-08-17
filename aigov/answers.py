"""Read elicited answers from a file and turn them into `DecisionRecord`s.

This is the missing half of the inventory. `aigov.decisions` can derive capabilities from
answered decisions, and `aigov.instances.*` can pose the questions, but until now there was no
way to get an answer from the person who has it INTO the instrument. That gap meant every real
session would end with answers on paper and a hand-transcription step nobody had specified.

**Design constraints, in the order they bind:**

1. **The answers must live OUTSIDE this repository.** The repo is public. Frequencies, costs,
   jurisdictions and role assignments for a real family enterprise are exactly what the standing
   privacy rail keeps out of it. `load_answers` therefore REFUSES a path inside the repo tree
   unless the caller explicitly overrides — see `AnswersInsideRepo`. The refusal is the feature.
2. **An omitted field is UNANSWERED, never a default.** This mirrors `DecisionRecord`: `None` is a
   reportable state. Nothing here fills a blank in, and a file containing only ids is legal — it
   simply produces an inventory that is honest about knowing nothing yet.
3. **The file speaks the user's language, not the code's.** Keys are the worksheet questions
   (`times_per_year`, `cost_to_buy_the_call_once`), not the dataclass field names. A person
   filling this in should not have to learn `external_engagement_cost`.

Format is TOML because it is in the standard library from 3.11 (this repo carries no third-party
dependencies), `tomllib` is READ-ONLY — which is the correct capability, since this module must
never write a user's answers anywhere — and it handles multi-line strings and typed scalars
without a schema language.
"""

from __future__ import annotations

import tomllib
from pathlib import Path

from aigov.decisions import DecisionRecord, FactKind, Reversibility

#: Plain-language values a person would write, mapped to the enum. The instrument's three kinds
#: are a real distinction (see `FactKind`), but "organization_specific_context" is not a phrase
#: anyone uses about their own business.
FACT_KINDS = {
    "written-down": FactKind.TRANSFERABLE_RECORD,
    "how-we-operate": FactKind.ORGANIZATION_SPECIFIC_CONTEXT,
    "from-experience": FactKind.TACIT_CONTEXT,
}

#: "What happens if you get it wrong once?" — the worksheet asks for one of these three words.
CONSEQUENCES = {
    "recoverable": Reversibility.REVERSIBLE,
    "expensive": Reversibility.COSTLY,
    "permanent": Reversibility.IRREVERSIBLE,
}

#: answers-file key -> DecisionRecord field. Everything is optional.
_SCALARS = {
    "times_per_year": "frequency_per_year",
    "cost_to_buy_the_call_once": "external_engagement_cost",
    "cost_per_year_to_hold_it": "internal_annual_cost",
    "anyone_sells_this": "external_market_exists",
    "who_answers": "accountable_role",
    "one_decision": "atomic",
    "money_at_stake": "stake_per_decision",
}

#: Keys accepted but deliberately ignored — `question` is copied into the file so the person
#: filling it in can see what they are answering. Reading it back would let a typo in a comment
#: silently change the inventory.
_IGNORED = frozenset({"question", "phase", "notes"})

_LIST_KEYS = frozenset({"what_only_we_know", "must_know_first"})
_KNOWN = frozenset(_SCALARS) | _IGNORED | _LIST_KEYS | {"if_wrong_once"}


class AnswersError(ValueError):
    """A problem with the answers file that the person filling it in can act on."""


class AnswersInsideRepo(AnswersError):
    """The answers file is inside the public repository. Refused on privacy grounds."""


def _repo_root(start: Path) -> Path | None:
    for parent in [start, *start.parents]:
        if (parent / ".git").exists():
            return parent
    return None


def _check_outside_repo(path: Path) -> None:
    """Refuse an answers file that sits inside the public repo tree.

    Fails CLOSED on the privacy question: if the file is inside a git repo that also contains this
    module, loading it would invite someone to commit real financial and jurisdictional detail to a
    public remote. The check is deliberately about LOCATION, not about `.gitignore` — an ignore
    rule is one `git add -f` away from not protecting anything.
    """
    here = _repo_root(Path(__file__).resolve())
    if here is None:
        return
    try:
        resolved = path.resolve()
    except OSError:
        return
    if resolved == here or here in resolved.parents:
        raise AnswersInsideRepo(
            f"{resolved} is inside the public repository at {here}.\n"
            "Real frequencies, costs, roles and jurisdictions must not be stored here.\n"
            "Move the answers file somewhere private (a folder outside this repo, or a private "
            "repo) and point --answers at it there.\n"
            "If you are certain this file contains nothing real - a fixture, a worked example - "
            "pass allow_inside_repo=True."
        )


def _facts(raw, decision_id: str):
    """`must_know_first` -> (information_needs, fact_kinds).

    Accepts either a bare string (fact whose kind is not yet classified - legal, and reported as
    an unclassified fact) or a table with `fact` and `kind`.
    """
    needs, kinds = [], []
    for i, item in enumerate(raw, 1):
        if isinstance(item, str):
            needs.append(item)
            continue
        if not isinstance(item, dict) or "fact" not in item:
            raise AnswersError(
                f"[{decision_id}] must_know_first entry {i} must be a string, or a table with a "
                f"'fact' key and optionally a 'kind' key. Got: {item!r}"
            )
        fact = item["fact"]
        needs.append(fact)
        kind = item.get("kind")
        if kind is None:
            continue
        if kind not in FACT_KINDS:
            raise AnswersError(
                f"[{decision_id}] fact {fact!r} has kind {kind!r}. Use one of: "
                f"{', '.join(sorted(FACT_KINDS))}."
            )
        kinds.append((fact, FACT_KINDS[kind]))
    return frozenset(needs), tuple(kinds)


def _record(decision_id: str, body: dict, question: str) -> DecisionRecord:
    unknown = set(body) - _KNOWN
    if unknown:
        raise AnswersError(
            f"[{decision_id}] unrecognised key(s): {', '.join(sorted(unknown))}. "
            f"Known keys: {', '.join(sorted(_KNOWN - _IGNORED))}."
        )

    fields = {}
    for key, field in _SCALARS.items():
        if key in body:
            fields[field] = body[key]

    if "if_wrong_once" in body:
        word = body["if_wrong_once"]
        if word not in CONSEQUENCES:
            raise AnswersError(
                f"[{decision_id}] if_wrong_once is {word!r}. Use one of: "
                f"{', '.join(sorted(CONSEQUENCES))}."
            )
        fields["reversibility"] = CONSEQUENCES[word]

    private = body.get("what_only_we_know", ())
    if isinstance(private, str):
        private = (private,)

    needs, kinds = _facts(body.get("must_know_first", ()), decision_id)

    return DecisionRecord(
        id=decision_id,
        question=question,
        private_information=tuple(private),
        information_needs=needs,
        fact_kinds=kinds,
        **fields,
    )


def parse_answers(text: str, questions: dict) -> tuple:
    """Parse answers-file TEXT against a `{decision_id: question}` map.

    `questions` is the authority for the wording - the answers file may carry a `question` key for
    the reader's benefit, but it is never read back (see `_IGNORED`).
    """
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        raise AnswersError(f"the answers file is not valid TOML: {exc}") from exc

    unknown = [k for k, v in data.items() if isinstance(v, dict) and k not in questions]
    if unknown:
        raise AnswersError(
            f"answers given for decision(s) not in the inventory: {', '.join(sorted(unknown))}. "
            f"Known ids: {', '.join(sorted(questions))}."
        )

    out = []
    for did, question in questions.items():
        body = data.get(did)
        if body is None:
            out.append(DecisionRecord(id=did, question=question))
            continue
        out.append(_record(did, body, question))
    return tuple(out)


def load_answers(path, questions: dict, *, allow_inside_repo: bool = False) -> tuple:
    """Read an answers file from disk. REFUSES a path inside the public repo by default."""
    path = Path(path)
    if not allow_inside_repo:
        _check_outside_repo(path)
    if not path.exists():
        raise AnswersError(f"no answers file at {path}")
    return parse_answers(path.read_text(encoding="utf-8"), questions)


def answered_ids(records) -> tuple:
    """Ids whose four sourcing inputs are all present - i.e. that can get a verdict."""
    return tuple(r.id for r in records if not r.missing_fields())


def render_template(decisions, phase_of=None) -> str:
    """Emit a blank answers file for `decisions`, ready to be filled in.

    Every field is commented out. An uncommented-but-blank field would be a lie: TOML has no
    "unanswered" scalar, so the only honest way to say "not yet" is for the key to be absent.
    """
    lines = [
        "# ANSWERS - family land enterprise, venture-entry inventory",
        "#",
        "# KEEP THIS FILE OUTSIDE THE PUBLIC REPOSITORY. It will hold real costs, roles and",
        "# jurisdictions. The loader refuses to read it from inside the repo tree.",
        "#",
        "# Uncomment a line and fill it in as you answer. A key you leave commented out is",
        "# UNANSWERED, which is a real state - it gets reported as a named gap, never guessed.",
        "#",
        "# Costs are in whatever single currency you choose; the instrument only compares them",
        "# to each other. Use the same one throughout.",
        "#",
        "# if_wrong_once   : recoverable | expensive | permanent",
        "# kind of a fact  : written-down | how-we-operate | from-experience",
        "#   written-down    = hand over the file and they have it",
        "#   how-we-operate  = specific to us, transferable but only by explaining",
        "#   from-experience = known from doing it, never written down  <- the expensive kind",
        "",
    ]
    for d in decisions:
        phase = f"  ({phase_of(d.id)})" if phase_of else ""
        lines += [
            f"# {'-' * 86}",
            f"# {d.id}{phase}  {d.question}",
            f"# {'-' * 86}",
            f"[{d.id}]",
            f'question = "{d.question.replace(chr(34), chr(39))}"',
            "",
            "# How many times a year does this actually come up?",
            "# times_per_year = 0",
            "",
            "# Pay an outsider to make this ONE call: their fee, plus finding, briefing, checking.",
            "# cost_to_buy_the_call_once = 0",
            "",
            "# Per year to keep this in-house: their time, tools, and attention taken off other work.",
            "# cost_per_year_to_hold_it = 0",
            "",
            "# Can you actually buy this judgement from anyone? If nobody sells it, that settles it.",
            "# anyone_sells_this = true",
            "",
            "# What do you know about this that an outside expert could not find out?",
            '# what_only_we_know = ["", ""]',
            "",
            "# What has to be KNOWN before you can make this call? Facts, not sources.",
            "# must_know_first = [",
            '#   { fact = "", kind = "from-experience" },',
            "# ]",
            "",
            "# Who ANSWERS for this - the role, never a person's name. Leave out if nobody does yet.",
            '# who_answers = ""',
            "",
            "# If you get it wrong once: recoverable | expensive | permanent",
            '# if_wrong_once = "expensive"',
            "",
            "# Is this ONE decision, or several wearing one sentence?",
            "# one_decision = true",
            "",
        ]
    return "\n".join(lines)


__all__ = [
    "AnswersError", "AnswersInsideRepo", "FACT_KINDS", "CONSEQUENCES",
    "parse_answers", "load_answers", "answered_ids", "render_template",
]
