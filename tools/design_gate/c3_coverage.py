"""C3 — coverage. Carries G9 and G10 of 90-design-delivery.md §14, over a coverage table (§7.2).

    python3 tools/design_gate/c3_coverage.py <package-dir> [--main origin/main] [--out report.md]
    python3 tools/design_gate/c3_coverage.py <repo> --screen <page-id> [--table <file>] [--main origin/main]

Two inputs, by how the screen was designed:

- **A finished package** (S1–S10): the package's own `coverage.md`.
- **A prototype screen** (§6.8 *Exit*, R-44): the **one** requirement-coverage table for the screens the
  prototype covers, filtered to the screen being gated (`--screen`, its prototype page id, e.g. `week` for
  `p-week`). The table carries a *Screen* column; a row belongs to every screen it names. Without
  `--table`, the table is read at `_docs/design/v1a-coverage.md` in the repository (WEE-479, WEE-470 Q1 (a)).

G9: every applicable row is **satisfied**; a **not applicable** row states its reason; a **CHANGED** or
**NOT COVERED** row carries the Product Owner's answer. G10: every table's source is pinned at a commit on
the project's main branch, and no source cites a draft or unfolded amendment as authority.

Standard library and `git` only. Exit 0: pass. Exit 1: at least one FAIL. Exit 2: no FAIL, but at least one
item the script could not decide — read at G11 by the S9 take-in, never passed (§14).
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mdtables import Report, Table, empty, plain, tables  # noqa: E402

HEX = re.compile(r"`([0-9a-f]{7,40})`")
ROW_ID = re.compile(r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-?\d+[a-z]?$")
NEEDS_ANSWER = ("not covered", "changed", "narrowed", "removed", "deferred")
FAILING = ("not satisfied", "partial", "open", "unknown")


def git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)


def on_main(repo: Path, commit: str, main: str) -> bool | None:
    if git(repo, "cat-file", "-e", f"{commit}^{{commit}}").returncode != 0:
        return None
    return git(repo, "merge-base", "--is-ancestor", commit, main).returncode == 0


def verdict(t: Table, line: int, cells: list[str], rid: str, r: Report) -> None:
    vi, ai, ki = t.col("verdict"), t.col("answer", "po choice"), t.col("kind")
    v = plain(cells[vi]).lower() if vi is not None and vi < len(cells) else ""
    answer = cells[ai] if ai is not None and ai < len(cells) else ""
    kind = plain(cells[ki]).lower() if ki is not None and ki < len(cells) else ""
    where = f"`{t.path.name}:{line}` {rid}"
    if not v:
        r.add("G9 every obligation satisfied or routed", "FAIL", f"{where}: no verdict")
    elif v.startswith("not applicable"):
        reason = v[len("not applicable") :].strip(" —-–:()")
        r.add(
            "G9 every obligation satisfied or routed",
            "PASS" if len(reason) > 3 else "FAIL",
            where + ("" if len(reason) > 3 else ": not applicable with no reason"),
        )
    elif v.startswith("satisfied"):
        routed = any(k in v for k in NEEDS_ANSWER)
        r.add(
            "G9 every obligation satisfied or routed",
            "FAIL" if routed and empty(answer) else "PASS",
            where + (f": *{v[:50]}* with no Product Owner answer" if routed and empty(answer) else ""),
        )
    elif any(k in kind for k in ("changed", "not covered")) and empty(answer):
        # Satisfied rows returned above: a CHANGED row the aligned specification now reads is closed.
        r.add(
            "G9 every obligation satisfied or routed",
            "FAIL",
            f"{where}: {kind.upper()}, not satisfied, with no Product Owner answer",
        )
    elif any(k in v for k in NEEDS_ANSWER):
        r.add(
            "G9 every obligation satisfied or routed",
            "FAIL" if empty(answer) else "PASS",
            where + (f": *{v[:50]}* with no Product Owner answer" if empty(answer) else ""),
        )
    elif any(k in v for k in FAILING):
        r.add("G9 every obligation satisfied or routed", "FAIL", f"{where}: *{v[:60]}*")
    else:
        r.add("G9 every obligation satisfied or routed", "UNRESOLVED", f"{where}: verdict not recognised — *{v[:60]}*")


V1A_TABLE = Path("_docs/design/v1a-coverage.md")  # WEE-479 proposes it here; the Architect places it


def screen_match(cell: str, screen: str) -> bool:
    """A Screen cell names the screen by its prototype page id, with or without the `p-` prefix."""
    return re.search(rf"(?<![\w-])(?:p-)?{re.escape(screen)}(?![\w-])", plain(cell)) is not None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("package", type=Path, help="a finished package's directory, or the repository for a prototype screen")
    ap.add_argument("--screen", help="the prototype page id of the screen being gated (e.g. week)")
    ap.add_argument("--table", type=Path, help=f"the one coverage table (default <repo>/{V1A_TABLE})")
    ap.add_argument("--main", default="origin/main", help="the project's main branch ref (default origin/main)")
    ap.add_argument("--out", type=Path)
    a = ap.parse_args()
    pkg = a.package.resolve()
    repo = Path(git(pkg, "rev-parse", "--show-toplevel").stdout.strip() or pkg)
    r = Report(f"C3 — coverage · `{a.screen or pkg.name}`")
    # a package reads its own coverage.md; a prototype screen reads the one table, filtered to its rows
    cov = a.table.resolve() if a.table else (repo / V1A_TABLE if a.screen else pkg / "coverage.md")
    if not cov.exists():
        if a.table:
            why = f"`{cov}` is missing"
        elif a.screen:
            why = (
                f"the one coverage table is not at `{V1A_TABLE}` (WEE-479, WEE-470 Q1 (a)); "
                "pass `--table` if it lives elsewhere"
            )
        else:
            why = (
                f"`coverage.md` is missing in `{pkg.name}` (process §7.2); for a prototype screen pass "
                f"`--screen`, which reads the one table at `{V1A_TABLE}`"
            )
        r.add("G9 every obligation satisfied or routed", "FAIL", why)
        text = r.render()
        print(text)
        if a.out:
            a.out.write_text(text + "\n", encoding="utf-8")
        return r.code()
    all_tables = tables(cov)

    # G10 — the pin. A header-table row naming the specification, or a column header, carries the commit.
    pins: set[str] = set()
    for t in all_tables:
        for h in t.header:
            if "source" in h.lower():
                pins.update(HEX.findall(h))
        if len(t.header) == 2:
            for _, cells in t.rows:
                if cells and "specification" in plain(cells[0]).lower():
                    pins.update(HEX.findall(" ".join(cells[1:])))
    if not pins:
        r.add("G10 cites a folded specification at a commit", "FAIL", f"no specification commit pinned in `{cov.name}`")
    for c in sorted(pins):
        ok = on_main(repo, c, a.main)
        r.add(
            "G10 cites a folded specification at a commit",
            {True: "PASS", False: "FAIL", None: "UNRESOLVED"}[ok],
            f"`{c}`"
            + {True: f" is on `{a.main}`", False: f" is **not** on `{a.main}`", None: " is not in this clone"}[ok],
        )

    # G9 — rows, and G10 — per-row sources.
    n = 0
    for t in all_tables:
        if t.col("verdict") is None:
            continue
        si = t.col("source")
        sc = t.col("screen", "page")
        if a.screen and sc is None:
            r.add(
                "G9 every obligation satisfied or routed",
                "FAIL",
                f"`{cov.name}:{t.line}`: a requirement table with no *Screen* column, so no row can be filtered to `{a.screen}`",
            )
            continue
        for line, cells in t.rows:
            rid = plain(cells[0]) if cells else ""
            if not ROW_ID.match(rid):
                continue
            if a.screen and not (sc < len(cells) and screen_match(cells[sc], a.screen)):
                continue
            n += 1
            verdict(t, line, cells, rid, r)
            if si is not None and si < len(cells):
                src = cells[si]
                low = plain(src).lower()
                if "draft" in low and "folded" not in low:
                    r.add(
                        "G10 cites a folded specification at a commit",
                        "FAIL",
                        f"`{cov.name}:{line}` {rid}: source cites a draft — *{plain(src)[:60]}*",
                    )
                for c in HEX.findall(src):
                    if c not in pins and on_main(repo, c, a.main) is False:
                        r.add(
                            "G10 cites a folded specification at a commit",
                            "FAIL",
                            f"`{cov.name}:{line}` {rid}: `{c}` is not on `{a.main}`",
                        )
    if n == 0:
        r.add(
            "G9 every obligation satisfied or routed",
            "FAIL",
            f"no requirement rows for `{a.screen}` in `{cov.name}`"
            if a.screen
            else "no requirement rows found (no table with a Verdict column)",
        )
    text = r.render()
    print(text)
    if a.out:
        a.out.write_text(text + "\n", encoding="utf-8")
    return r.code()


if __name__ == "__main__":
    sys.exit(main())
