"""Real seat adapters — the subprocess boundary between the panel and two vendor CLIs.

Kept OUT of `panel.py` on purpose: classification has to be testable without a network, and the
panel tests prove `read()` works with no I/O at all. Everything fragile lives here.

BOTH seats run under an existing subscription, so a call costs tokens and not dollars. That is why
this module never provisions, never authenticates, and never reads an API key: an adapter that
could reach a metered endpoint would turn every panel question into a spend decision.

A seat that cannot be parsed is a MISSING seat, never a verdict. `parse_verdict` fails closed --
an unparseable answer returns None and the opinion is marked failed, because guessing what a model
"probably meant" is how an unread answer becomes a vote.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from typing import Optional

from .panel import Seat, SeatOpinion

#: Every seat is asked for this line. One token, greppable, position-independent.
VERDICT_PREFIX = "VERDICT:"

DEFAULT_TIMEOUT = 420


class SeatUnavailable(RuntimeError):
    """The CLI backing a seat is not installed or not on PATH."""


def parse_verdict(text: str, allowed) -> Optional[str]:
    """Pull the declared verdict out of a free-text answer. Fail closed.

    Scans every line rather than only the first: models routinely lead with reasoning and put the
    verdict at the end. The LAST declared verdict wins -- a model that reconsiders mid-answer means
    the final line, and taking the first would record a position it walked away from.
    """
    allowed = {a.strip().upper() for a in allowed}
    found = None
    for line in text.splitlines():
        s = line.strip().lstrip("*# ").strip()
        if not s.upper().startswith(VERDICT_PREFIX):
            continue
        token = s[len(VERDICT_PREFIX):].strip().strip("*`_.").strip().upper()
        token = token.split()[0] if token else ""
        if token in allowed:
            found = token
    return found


def _run(argv, payload: str, timeout: int) -> str:
    """Run a CLI with `payload` on stdin. Returns stdout; raises on non-zero exit."""
    proc = subprocess.run(argv, input=payload, capture_output=True, text=True,
                          timeout=timeout, encoding="utf-8", errors="replace")
    if proc.returncode != 0:
        raise RuntimeError("{} exited {}: {}".format(argv[0], proc.returncode,
                                                     (proc.stderr or "")[-400:]))
    return proc.stdout


def _codex_last_message(stdout: str) -> str:
    """Extract the final agent_message from codex's JSONL stream."""
    last = ""
    for line in stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("type") == "item.completed":
            item = obj.get("item") or {}
            if item.get("type") == "agent_message":
                last = item.get("text") or last
    return last


def ask_codex(seat: Seat, question: str, allowed=("SUFFICIENT", "INSUFFICIENT"),
              timeout: int = DEFAULT_TIMEOUT) -> SeatOpinion:
    """The GPT seat, via the Codex CLI.

    Resolved through `shutil.which` because on Windows `codex` is a .CMD shim that
    `subprocess.run(["codex", ...])` cannot execute directly.
    """
    exe = shutil.which("codex")
    if not exe:
        raise SeatUnavailable("codex not on PATH")
    out = _run([exe, "exec", "--skip-git-repo-check", "--json", "-"], question, timeout)
    text = _codex_last_message(out)
    verdict = parse_verdict(text, allowed)
    return SeatOpinion(seat_id=seat.id, verdict=verdict or "", reasoning=text,
                       raw=text, failed=verdict is None)


def ask_claude(seat: Seat, question: str, allowed=("SUFFICIENT", "INSUFFICIENT"),
               timeout: int = DEFAULT_TIMEOUT) -> SeatOpinion:
    """The Claude seat, via a FRESH `claude -p` session.

    A fresh session is the whole point: asking the same conversation that authored the artifact is
    self-validation, not a second opinion. This seat sees the question and nothing else.
    """
    exe = shutil.which("claude")
    if not exe:
        raise SeatUnavailable("claude not on PATH")
    # Prompt goes on stdin, not argv: the questions are long and multi-line, and Windows argv
    # quoting mangles them.
    out = _run([exe, "-p"], question, timeout)
    verdict = parse_verdict(out, allowed)
    return SeatOpinion(seat_id=seat.id, verdict=verdict or "", reasoning=out,
                       raw=out, failed=verdict is None)


#: The live two-seat bench. Different models, different organisations, same evidence -- so any
#: disagreement is attributable to the models rather than to what they were shown.
CLAUDE_SEAT = Seat(id="S-claude", model="claude-opus-5", operator="anthropic",
                   answers_for="governance-instrument review")
GPT_SEAT = Seat(id="S-gpt", model="gpt-5.5", operator="openai",
                answers_for="governance-instrument review")

ASK = {CLAUDE_SEAT.id: ask_claude, GPT_SEAT.id: ask_codex}


def ask_live(seat: Seat, question: str) -> SeatOpinion:
    """Dispatch to the adapter for `seat`. The `ask` callable `panel.elicit` expects."""
    fn = ASK.get(seat.id)
    if fn is None:
        raise SeatUnavailable("no adapter registered for seat {!r}".format(seat.id))
    return fn(seat, question)
