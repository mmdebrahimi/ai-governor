"""Seat adapters. The parsing is what decides whether an unread answer becomes a vote."""

import pytest

from aigov.seats import (
    SeatUnavailable,
    _codex_last_message,
    ask_live,
    parse_verdict,
)
from aigov.panel import Seat

ALLOWED = ("SUFFICIENT", "INSUFFICIENT")


# --------------------------------------------------------------------------------------
# parse_verdict -- fail closed
# --------------------------------------------------------------------------------------


def test_plain_verdict_line():
    assert parse_verdict("VERDICT: SUFFICIENT", ALLOWED) == "SUFFICIENT"


def test_verdict_after_reasoning():
    text = "Considering the criterion at length.\n\nVERDICT: INSUFFICIENT"
    assert parse_verdict(text, ALLOWED) == "INSUFFICIENT"


def test_markdown_bold_verdict_is_read():
    assert parse_verdict("**VERDICT: SUFFICIENT**", ALLOWED) == "SUFFICIENT"


def test_heading_style_verdict_is_read():
    assert parse_verdict("## VERDICT: INSUFFICIENT", ALLOWED) == "INSUFFICIENT"


def test_lowercase_verdict_is_read():
    assert parse_verdict("verdict: sufficient", ALLOWED) == "SUFFICIENT"


def test_last_verdict_wins_when_a_model_reconsiders():
    """A model that changes its mind mid-answer means the final line, not the first."""
    text = "VERDICT: SUFFICIENT\n\nOn reflection that was wrong.\n\nVERDICT: INSUFFICIENT"
    assert parse_verdict(text, ALLOWED) == "INSUFFICIENT"


def test_trailing_prose_after_the_token_is_ignored():
    assert parse_verdict("VERDICT: INSUFFICIENT because it drifts", ALLOWED) == "INSUFFICIENT"


def test_token_outside_the_allowed_set_is_not_a_verdict():
    assert parse_verdict("VERDICT: MAYBE", ALLOWED) is None


def test_absent_verdict_returns_none():
    assert parse_verdict("I think the criterion is basically fine.", ALLOWED) is None


def test_empty_verdict_returns_none():
    assert parse_verdict("VERDICT:", ALLOWED) is None


def test_the_word_verdict_mid_sentence_is_not_a_verdict_line():
    assert parse_verdict("My verdict: it depends on the reading.", ALLOWED) is None


def test_a_mentioned_but_undeclared_option_is_not_counted():
    """The failure that matters: prose naming both options must not resolve to either."""
    text = "This is arguably SUFFICIENT, though many would call it INSUFFICIENT."
    assert parse_verdict(text, ALLOWED) is None


# --------------------------------------------------------------------------------------
# codex stream parsing
# --------------------------------------------------------------------------------------


def test_codex_last_message_extracts_final_agent_message():
    stream = "\n".join([
        '{"type":"item.started","item":{"type":"agent_message","text":"partial"}}',
        '{"type":"item.completed","item":{"type":"reasoning","text":"thinking"}}',
        '{"type":"item.completed","item":{"type":"agent_message","text":"first"}}',
        '{"type":"item.completed","item":{"type":"agent_message","text":"final"}}',
    ])
    assert _codex_last_message(stream) == "final"


def test_codex_parser_survives_non_json_lines():
    stream = 'not json\n{"type":"item.completed","item":{"type":"agent_message","text":"ok"}}\n'
    assert _codex_last_message(stream) == "ok"


def test_codex_parser_returns_empty_when_no_agent_message():
    assert _codex_last_message('{"type":"item.completed","item":{"type":"reasoning"}}') == ""


# --------------------------------------------------------------------------------------
# dispatch
# --------------------------------------------------------------------------------------


def test_unregistered_seat_raises_rather_than_guessing_an_adapter():
    with pytest.raises(SeatUnavailable):
        ask_live(Seat(id="S-unknown", model="m", operator="o"), "Q?")
