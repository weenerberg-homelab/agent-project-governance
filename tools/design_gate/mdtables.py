"""Markdown table reading shared by the design-gate scripts (90-design-delivery.md §14).

Standard library only. A table is a run of lines starting with `|`, whose second line is the
separator row. Cells are split on unescaped `|` outside backticks.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Table:
    path: Path
    line: int  # 1-based line of the header row
    header: list[str]
    rows: list[tuple[int, list[str]]] = field(default_factory=list)  # (line, cells)
    section: str = ""  # the nearest heading above the table

    def col(self, *names: str) -> int | None:
        """Index of the first header cell containing any of `names` (case-insensitive)."""
        for i, h in enumerate(self.header):
            low = plain(h).lower()
            if any(n.lower() in low for n in names):
                return i
        return None


def split_row(line: str) -> list[str]:
    cells, cur, tick = [], [], False
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|") and not body.endswith("\\|"):
        body = body[:-1]
    i = 0
    while i < len(body):
        ch = body[i]
        if ch == "\\" and i + 1 < len(body) and body[i + 1] == "|":
            cur.append("|")
            i += 2
            continue
        if ch == "`":
            tick = not tick
        if ch == "|" and not tick:
            cells.append("".join(cur).strip())
            cur = []
        else:
            cur.append(ch)
        i += 1
    cells.append("".join(cur).strip())
    return cells


SEP = re.compile(r"^\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")


def tables(path: Path) -> list[Table]:
    lines = path.read_text(encoding="utf-8").splitlines()
    out: list[Table] = []
    heading = ""
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("#"):
            heading = ln.lstrip("#").strip()
        if ln.lstrip().startswith("|") and i + 1 < len(lines) and SEP.match(lines[i + 1].strip()):
            t = Table(path, i + 1, split_row(ln), section=heading)
            j = i + 2
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                t.rows.append((j + 1, split_row(lines[j])))
                j += 1
            out.append(t)
            i = j
            continue
        i += 1
    return out


def plain(cell: str) -> str:
    """The cell without markdown emphasis or code ticks."""
    return re.sub(r"[*`_]", "", cell).strip()


def empty(cell: str) -> bool:
    return plain(cell) in ("", "—", "-", "–")


class Report:
    """PASS / FAIL / UNRESOLVED lines, and the exit code: 1 on any FAIL, 2 on UNRESOLVED only."""

    def __init__(self, title: str) -> None:
        self.title = title
        self.lines: list[tuple[str, str, str]] = []  # (check, verdict, text)

    def add(self, check: str, verdict: str, text: str) -> None:
        self.lines.append((check, verdict, text))

    def render(self) -> str:
        out = [f"## {self.title}", ""]
        for check in dict.fromkeys(c for c, _, _ in self.lines):
            rows = [(v, t) for c, v, t in self.lines if c == check]
            worst = (
                "FAIL"
                if any(v == "FAIL" for v, _ in rows)
                else "UNRESOLVED"
                if any(v == "UNRESOLVED" for v, _ in rows)
                else "PASS"
            )
            out.append(f"### {check} — **{worst}**")
            out.append("")
            for v, t in rows:
                if v != "PASS" or len(rows) == 1:
                    out.append(f"- {v}: {t}")
            passes = sum(1 for v, _ in rows if v == "PASS")
            if len(rows) > 1:
                out.append(f"- {passes} of {len(rows)} checked items pass")
            out.append("")
        return "\n".join(out)

    def code(self) -> int:
        verdicts = {v for _, v, _ in self.lines}
        return 1 if "FAIL" in verdicts else 2 if "UNRESOLVED" in verdicts else 0
