"""Put one question to the live two-seat bench and write the reading as an auditable artifact.

    python scripts/run_panel.py <question-file> [--out panel_runs/<name>.md] [--allow A,B]

Seats are called CONCURRENTLY but never see each other: each thread gets `(seat, question)` and
nothing else, so parallelism buys wall-clock without creating a channel between them.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from aigov.panel import Concurrence, read, seat_errors           # noqa: E402
from aigov.seats import CLAUDE_SEAT, GPT_SEAT, ask_live          # noqa: E402


def run(question: str, seats, allowed):
    problems = seat_errors(seats)
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(seats)) as pool:
        futures = {pool.submit(ask_live, s, question): s for s in seats}
        opinions = []
        for fut in concurrent.futures.as_completed(futures):
            seat = futures[fut]
            try:
                opinions.append(fut.result())
            except Exception as exc:
                from aigov.panel import SeatOpinion
                opinions.append(SeatOpinion(seat_id=seat.id, verdict="", failed=True,
                                            raw=repr(exc)))
    order = {s.id: i for i, s in enumerate(seats)}
    opinions.sort(key=lambda o: order.get(o.seat_id, 99))
    return read(question, tuple(opinions)), problems


def render(reading, problems, seats) -> str:
    out = ["# Panel reading — {}".format(date.today().isoformat()), ""]
    out.append("**Concurrence:** `{}`  ".format(reading.concurrence.value))
    out.append("**Reason:** {}  ".format(reading.reason))
    if reading.caveat():
        out.append("**Caveat:** {}".format(reading.caveat()))
    out.append("")
    out.append("| Seat | Model | Operator | Verdict |")
    out.append("|---|---|---|---|")
    by_id = {s.id: s for s in seats}
    for o in reading.opinions:
        s = by_id.get(o.seat_id)
        out.append("| {} | {} | {} | {} |".format(
            o.seat_id, s.model if s else "?", s.operator if s else "?",
            "**FAILED**" if o.failed else "`{}`".format(o.verdict)))
    out.append("")
    if reading.dissent:
        out.append("**Dissent retained (not collapsed):**")
        for d in reading.dissent:
            out.append("- {}".format(d))
        out.append("")
    if problems:
        out.append("**Bench problems:**")
        out.extend("- {}".format(p) for p in problems)
        out.append("")
    out.append("> This is advisory model output. It is not a ratification and is not actionable "
               "alone.")
    out.append("")
    out.append("## Question")
    out.append("")
    out.append("```")
    out.append(reading.question.strip())
    out.append("```")
    for o in reading.opinions:
        out.append("")
        out.append("## Seat `{}` — full response".format(o.seat_id))
        out.append("")
        out.append((o.raw or "(no output)").strip())
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("question_file")
    ap.add_argument("--out")
    ap.add_argument("--allow", default="SUFFICIENT,INSUFFICIENT")
    args = ap.parse_args()

    question = Path(args.question_file).read_text(encoding="utf-8")
    allowed = tuple(a.strip().upper() for a in args.allow.split(",") if a.strip())
    seats = (CLAUDE_SEAT, GPT_SEAT)

    reading, problems = run(question, seats, allowed)
    text = render(reading, problems, seats)

    if args.out:
        p = Path(args.out)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        print("wrote {}".format(p))

    print("concurrence: {}".format(reading.concurrence.value))
    for o in reading.opinions:
        print("  {}: {}".format(o.seat_id, "FAILED" if o.failed else o.verdict))
    if reading.caveat():
        print("caveat: {}".format(reading.caveat()))
    return 0 if reading.concurrence is not Concurrence.NO_READING else 1


if __name__ == "__main__":
    raise SystemExit(main())
