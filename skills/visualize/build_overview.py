#!/usr/bin/env python3
"""Draw a one-page overview of a project's tickets as a self-contained HTML file.

Reads ticket files (one markdown file per ticket), works out which are done,
in progress, ready or waiting, and lays them out left to right in the order
they unblock each other. Standard library only. Nothing leaves the machine.

Usage:
  build_overview.py TICKETS_DIR [TICKETS_DIR ...] --out FILE
      [--title TEXT] [--goal TEXT] [--later "Name: one line" ...]
      [--assume NN=state ...] [--note TEXT]

A TICKETS_DIR holds files named NN-something.md. If its parent folder has a
spec.md, that spec's first heading names the slice.
"""

from __future__ import annotations

import argparse
import html
import re
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

STATES = ["ready", "claimed", "built", "explained", "done"]
STEP_LABEL = {
    "claimed": "being built",
    "built": "built, to be explained",
    "explained": "explained, to be packaged",
}
CARD_H, GAP_X, GAP_Y, PAD = 112, 44, 16, 12
MAP_WIDTH, MAX_CARD_W, MIN_CARD_W = 1100, 220, 140


@dataclass
class Ticket:
    """One ticket as read from its file."""

    number: str
    title: str
    progress: str = "ready"
    stakes: str = ""
    blocked_by: list[str] = field(default_factory=list)
    outside_blocker: str = ""
    level: int = 0
    row: int = 0

    @property
    def is_done(self) -> bool:
        return self.progress == "done"


@dataclass
class Slice:
    """A batch of tickets that together deliver one working thing."""

    name: str
    tickets: list[Ticket]


def read_ticket(path: Path) -> Ticket | None:
    """Read one ticket file. Returns None when the file is not a ticket."""
    text = path.read_text(encoding="utf-8", errors="replace")
    heading = re.search(r"^#\s+(\d+)\s*[:.\-]?\s*(.+)$", text, re.MULTILINE)
    if not heading:
        return None
    ticket = Ticket(number=heading.group(1).zfill(2), title=heading.group(2).strip())
    progress = re.search(r"^\**Progress:?\**:?\s*([a-z]+)", text, re.MULTILINE | re.IGNORECASE)
    if progress and progress.group(1).lower() in STATES:
        ticket.progress = progress.group(1).lower()
    stakes = re.search(r"^\**Stakes:?\**:?\s*([a-z]+)", text, re.MULTILINE | re.IGNORECASE)
    if stakes:
        ticket.stakes = stakes.group(1).lower()
    blocked = re.search(r"^\**Blocked by:?\**:?\s*(.+)$", text, re.MULTILINE | re.IGNORECASE)
    if blocked:
        ticket.blocked_by, ticket.outside_blocker = split_blockers(blocked.group(1))
    return ticket


def split_blockers(line: str) -> tuple[list[str], str]:
    """Split a 'Blocked by' line into ticket numbers and any other blocker in words."""
    numbers = [n.zfill(2) for n in re.findall(r"\b(\d{1,3})\b", line)]
    rest = re.sub(r"\b\d{1,3}\b", "", line)
    rest = re.sub(r"\b(and|none|nothing|can start immediately)\b", "", rest, flags=re.IGNORECASE)
    rest = rest.strip(" ,.;()*")
    return numbers, rest


def slice_name(tickets_dir: Path) -> str:
    """Name a slice from the spec beside its tickets, or from its folder."""
    spec = tickets_dir.parent / "spec.md"
    if spec.exists():
        heading = re.search(r"^#\s+(.+)$", spec.read_text(encoding="utf-8", errors="replace"), re.MULTILINE)
        if heading:
            return heading.group(1).strip()
    folder = tickets_dir.parent.name if tickets_dir.name in {"issues", "tickets"} else tickets_dir.name
    return folder.replace("-", " ").replace("_", " ").strip().capitalize() or "Tickets"


def read_slice(tickets_dir: Path) -> Slice:
    """Read every ticket in one folder, in number order."""
    tickets = [t for p in sorted(tickets_dir.glob("*.md")) if (t := read_ticket(p))]
    return Slice(name=slice_name(tickets_dir), tickets=tickets)


def place(tickets: list[Ticket]) -> None:
    """Give each ticket a column (how many blockers deep it sits) and a row."""
    by_number = {t.number: t for t in tickets}

    def depth(ticket: Ticket, seen: frozenset[str]) -> int:
        known = [by_number[n] for n in ticket.blocked_by if n in by_number and n not in seen]
        return 0 if not known else 1 + max(depth(b, seen | {ticket.number}) for b in known)

    for ticket in tickets:
        ticket.level = depth(ticket, frozenset())
    # within a column, sit each ticket near the tickets it waits for, so arrows cross less
    for level in sorted({t.level for t in tickets}):
        column = [t for t in tickets if t.level == level]

        def pull(ticket: Ticket) -> tuple[float, str]:
            rows = [by_number[n].row for n in ticket.blocked_by if n in by_number]
            return (sum(rows) / len(rows) if rows else 0.0, ticket.number)

        for row, ticket in enumerate(sorted(column, key=pull)):
            ticket.row = row


def card_width(tickets: list[Ticket]) -> int:
    """Narrow the cards so every column fits on one screen."""
    columns = max(t.level for t in tickets) + 1
    fit = (MAP_WIDTH - PAD * 2 - (columns - 1) * GAP_X) // columns
    return max(MIN_CARD_W, min(MAX_CARD_W, fit))


def status_of(ticket: Ticket, by_number: dict[str, Ticket]) -> str:
    """One of: done, doing, ready, waiting."""
    if ticket.is_done:
        return "done"
    if ticket.progress in STEP_LABEL:
        return "doing"
    blockers_done = all(by_number[n].is_done for n in ticket.blocked_by if n in by_number)
    return "ready" if blockers_done and not ticket.outside_blocker else "waiting"


def status_line(ticket: Ticket, status: str) -> str:
    """The short line under a card's title."""
    if status == "done":
        return "Done"
    if status == "doing":
        return STEP_LABEL[ticket.progress].capitalize()
    if status == "ready":
        return "Ready to start"
    waits = ", ".join(ticket.blocked_by)
    if ticket.outside_blocker:
        waits = (waits + " + " if waits else "") + "something outside"
    return "Waits for " + waits


def card_xy(ticket: Ticket, width: int) -> tuple[int, int]:
    return PAD + ticket.level * (width + GAP_X), PAD + ticket.row * (CARD_H + GAP_Y)


def draw_map(tickets: list[Ticket]) -> str:
    """The dependency map for one slice: cards joined by arrows."""
    by_number = {t.number: t for t in tickets}
    columns = max(t.level for t in tickets) + 1
    rows = max(t.row for t in tickets) + 1
    card_w = card_width(tickets)
    width = PAD * 2 + columns * card_w + (columns - 1) * GAP_X
    height = PAD * 2 + rows * CARD_H + (rows - 1) * GAP_Y
    arrows, cards = [], []
    for ticket in tickets:
        x, y = card_xy(ticket, card_w)
        for number in ticket.blocked_by:
            if number not in by_number:
                continue
            blocker = by_number[number]
            bx, by = card_xy(blocker, card_w)
            x1, y1, x2, y2 = bx + card_w, by + CARD_H // 2, x, y + CARD_H // 2
            bend = x2 - GAP_X // 2
            kinds = ("live " if blocker.is_done else "") + ("far" if ticket.level - blocker.level > 1 else "")
            arrows.append(f'<path class="arrow {kinds}" d="M{x1},{y1} C{bend},{y1} {bend},{y2} {x2 - 6},{y2}"/>')
        status = status_of(ticket, by_number)
        stakes = '<span class="stakes">high stakes</span>' if ticket.stakes == "high" else ""
        cards.append(
            f'<div class="card {status}" style="left:{x}px;top:{y}px;width:{card_w}px">'
            f'<div class="num">{html.escape(ticket.number)}{stakes}</div>'
            f'<div class="name">{html.escape(ticket.title)}</div>'
            f'<div class="state">{html.escape(status_line(ticket, status))}</div></div>'
        )
    return (
        f'<div class="scroll"><div class="map" style="width:{width}px;height:{height}px">'
        f'<svg width="{width}" height="{height}" aria-hidden="true">'
        '<defs><marker id="tip" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">'
        '<path d="M0,0 L8,4 L0,8 z"/></marker></defs>' + "".join(arrows) + "</svg>" + "".join(cards) + "</div></div>"
    )


def bar(done: int, doing: int, total: int) -> str:
    """A progress bar: done in solid, in progress in stripes."""
    if total == 0:
        return ""
    return (
        '<div class="bar" role="img" '
        f'aria-label="{done} of {total} done, {doing} in progress">'
        f'<span class="b-done" style="width:{100 * done / total:.1f}%"></span>'
        f'<span class="b-doing" style="width:{100 * doing / total:.1f}%"></span></div>'
    )


def counts(tickets: list[Ticket]) -> tuple[int, int, int]:
    by_number = {t.number: t for t in tickets}
    states = [status_of(t, by_number) for t in tickets]
    return states.count("done"), states.count("doing"), len(tickets)


def next_up(tickets: list[Ticket]) -> str:
    """The sentence under a slice's title: what is happening now, or what is next."""
    by_number = {t.number: t for t in tickets}
    doing = [t for t in tickets if status_of(t, by_number) == "doing"]
    if doing:
        t = doing[0]
        return f"You are here: ticket {t.number}, {STEP_LABEL[t.progress]}."
    ready = [t for t in tickets if status_of(t, by_number) == "ready"]
    if ready:
        return "Next up: ticket " + ", ".join(t.number for t in ready[:4]) + "."
    if tickets and all(t.is_done for t in tickets):
        return "All tickets in this slice are done."
    return "Nothing can start yet: every remaining ticket is waiting."


STYLE = """
:root{--paper:#EDF1EF;--card:#FAFCFB;--ink:#16211D;--ink2:#4A5B55;--rule:#C9D5D0;
--done:#0F6E5C;--done-t:#DCEEE8;--doing:#A8700B;--doing-t:#F7EDD7;--ready:#2C5F9E;--ready-t:#E1EBF7;
--wait:#7A8A84;--wait-t:#EEF1F0;--high:#7B3F86}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--paper:#141A18;--card:#1D2522;--ink:#E6ECE9;
--ink2:#A9B7B1;--rule:#34413C;--done:#5FC7B0;--done-t:#17352E;--doing:#E2B257;--doing-t:#3A2E12;
--ready:#8AB4EA;--ready-t:#1B2A40;--wait:#8B9A94;--wait-t:#222B28;--high:#C99AD2}}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:1200px;margin:0 auto;padding:28px 16px 64px}
h1{font-size:28px;margin:0 0 4px;text-wrap:balance}
h2{font-size:20px;margin:0 0 2px}
.goal{color:var(--ink2);margin:0 0 18px;max-width:70ch}
.top{display:flex;gap:14px;flex-wrap:wrap;margin:14px 0 8px}
.tile{background:var(--card);border:1px solid var(--rule);border-radius:10px;padding:12px 16px;min-width:130px}
.tile b{display:block;font-size:26px;line-height:1.1;font-variant-numeric:tabular-nums}
.tile span{color:var(--ink2);font-size:13px}
.bar{display:flex;height:14px;border-radius:7px;overflow:hidden;background:var(--wait-t);border:1px solid var(--rule);margin:8px 0}
.b-done{background:var(--done)}
.b-doing{background:repeating-linear-gradient(45deg,var(--doing),var(--doing) 6px,var(--doing-t) 6px,var(--doing-t) 12px)}
.slice{background:var(--card);border:1px solid var(--rule);border-radius:12px;padding:18px;margin:18px 0}
.slice .sub{color:var(--ink2);font-size:14px;margin:0}
.here{font-weight:600;margin:6px 0 0}
.scroll{overflow-x:auto;margin-top:12px}
.map{position:relative}
.map svg{position:absolute;inset:0}
.arrow{fill:none;stroke:var(--wait);stroke-width:1.5;stroke-dasharray:4 4;marker-end:url(#tip)}
.arrow.live{stroke:var(--done);stroke-dasharray:none}
.arrow.far{opacity:.45}
marker path{fill:var(--wait)}
.card{position:absolute;height:112px;border-radius:10px;padding:8px 10px;border:1.5px solid;overflow:hidden}
.card .num{font-size:12px;font-weight:700;letter-spacing:.04em;display:flex;justify-content:space-between}
.card .name{font-size:13.5px;line-height:1.25;font-weight:600;margin:2px 0;
display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.card .state{font-size:12px;position:absolute;left:10px;right:10px;bottom:7px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.card.done{background:var(--done-t);border-color:var(--done)} .card.done .num,.card.done .state{color:var(--done)}
.card.doing{background:var(--doing-t);border-color:var(--doing);box-shadow:0 0 0 3px var(--doing-t)} .card.doing .num,.card.doing .state{color:var(--doing)}
.card.ready{background:var(--ready-t);border-color:var(--ready)} .card.ready .num,.card.ready .state{color:var(--ready)}
.card.waiting{background:var(--wait-t);border-color:var(--rule);border-style:dashed} .card.waiting .num,.card.waiting .state{color:var(--wait)}
.stakes{color:var(--high);font-weight:700;text-transform:uppercase;font-size:10px}
.key{display:flex;gap:16px;flex-wrap:wrap;font-size:13px;color:var(--ink2);margin:10px 0 0}
.key i{display:inline-block;width:12px;height:12px;border-radius:3px;border:1.5px solid;vertical-align:-1px;margin-right:5px}
.later{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin-top:10px}
.later div{border:1.5px dashed var(--rule);border-radius:10px;padding:10px 12px;color:var(--ink2);font-size:14px}
.later b{display:block;color:var(--ink)}
.note{background:var(--doing-t);border-left:4px solid var(--doing);padding:10px 14px;border-radius:6px;margin:14px 0;font-size:14px}
footer{color:var(--ink2);font-size:13px;margin-top:22px}
"""

KEY = (
    '<div class="key">'
    '<span><i style="background:var(--done-t);border-color:var(--done)"></i>Done</span>'
    '<span><i style="background:var(--doing-t);border-color:var(--doing)"></i>In progress</span>'
    '<span><i style="background:var(--ready-t);border-color:var(--ready)"></i>Ready to start</span>'
    '<span><i style="background:var(--wait-t);border-color:var(--rule);border-style:dashed"></i>Waiting on another ticket</span>'
    "<span>Arrows point from a ticket to the tickets it unblocks.</span></div>"
)


def render(title: str, goal: str, slices: list[Slice], later: list[str], note: str) -> str:
    """Build the whole page."""
    everything = [t for s in slices for t in s.tickets]
    done = sum(counts(s.tickets)[0] for s in slices)
    doing = sum(counts(s.tickets)[1] for s in slices)
    total = len(everything)
    left = total - done - doing
    parts = [
        f"<h1>{html.escape(title)}</h1>",
        f'<p class="goal">{html.escape(goal)}</p>' if goal else "",
        '<div class="top">'
        f'<div class="tile"><b>{done} of {total}</b><span>tickets done</span></div>'
        f'<div class="tile"><b>{doing}</b><span>in progress</span></div>'
        f'<div class="tile"><b>{left}</b><span>not started</span></div>'
        f'<div class="tile"><b>{len(slices)}{" + " + str(len(later)) if later else ""}</b>'
        f'<span>slices planned{" + later" if later else ""}</span></div></div>',
        bar(done, doing, total),
        f'<div class="note">{html.escape(note)}</div>' if note else "",
    ]
    for one in slices:
        s_done, s_doing, s_total = counts(one.tickets)
        parts.append(
            f'<section class="slice"><h2>{html.escape(one.name)}</h2>'
            f'<p class="sub">{s_done} of {s_total} tickets done</p>'
            + bar(s_done, s_doing, s_total)
            + f'<p class="here">{html.escape(next_up(one.tickets))}</p>'
            + (draw_map(one.tickets) if one.tickets else "")
            + KEY
            + "</section>"
        )
    if later:
        boxes = []
        for item in later:
            name, _, detail = item.partition(":")
            boxes.append(f"<div><b>{html.escape(name.strip())}</b>{html.escape(detail.strip())}</div>")
        parts.append(
            '<section class="slice"><h2>Later, not yet cut into tickets</h2>'
            '<p class="sub">Planned in the spec. Each gets its own tickets when its turn comes.</p>'
            f'<div class="later">{"".join(boxes)}</div></section>'
        )
    parts.append(f"<footer>Drawn from the ticket files on {date.today():%d %B %Y}. Run the skill again to refresh.</footer>")
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f"<title>{html.escape(title)}</title><style>{STYLE}</style></head>"
        f'<body><main>{"".join(parts)}</main></body></html>'
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("tickets_dirs", nargs="+", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--title", default="Project overview")
    parser.add_argument("--goal", default="")
    parser.add_argument("--later", action="append", default=[], help='a later slice, as "Name: one line"')
    parser.add_argument("--assume", action="append", default=[], help="NN=state, for a ticket with no Progress line")
    parser.add_argument("--note", default="")
    args = parser.parse_args()

    slices = [read_slice(d) for d in args.tickets_dirs if d.is_dir()]
    slices = [s for s in slices if s.tickets]
    if not slices:
        parser.exit(1, "No ticket files found. A ticket is a .md file whose first heading starts with a number.\n")
    assumed = dict(item.split("=", 1) for item in args.assume)
    for one in slices:
        for ticket in one.tickets:
            if ticket.number in assumed and assumed[ticket.number] in STATES:
                ticket.progress = assumed[ticket.number]
        place(one.tickets)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(render(args.title, args.goal, slices, args.later, args.note), encoding="utf-8")
    done = sum(counts(s.tickets)[0] for s in slices)
    total = sum(len(s.tickets) for s in slices)
    print(f"Wrote {args.out}: {len(slices)} slice(s), {total} tickets, {done} done.")


if __name__ == "__main__":
    main()
