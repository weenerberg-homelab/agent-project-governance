"""C1 — structure. Carries G1, G2, G3, G4, G5 and G8 of 90-design-delivery.md §14.

    python3 tools/design_gate/c1_structure.py <package-dir> [--out report.md]

Reads the package's `page-brief.md`, `page.manifest.yaml`, `page-spec.md`, `acceptance-criteria.md` and
the rendered HTML at the package root. Standard library only.

Exit 0: every check passes. Exit 1: at least one FAIL. Exit 2: no FAIL, but at least one item the script
could not decide — an UNRESOLVED item is read at G11 by the S9 take-in, never passed (§14).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mdtables import Report, Table, empty, plain, tables  # noqa: E402

CATEGORIES = {"primitive", "page-local", "domain", "shared"}
REGION = re.compile(r"(?<![\w.-])R\d+(?:\.\d+)*(?![\w-])")
SPECIMEN = re.compile(r"(?<![\w-])S-[A-Z]{1,2}(?![\w-])")
ANCHOR = re.compile(r"(?<![\w&])#([A-Za-z][\w-]*)")
RULE = re.compile(r"§|\b(?:RL|SR|DA|DI|INV|AC|AF|AP|DC-Q|DC-F|WEE|Q|F|FR|SA|DEC)-?\w*\d|\bcard\b|\bpage-spec\b", re.I)


def region_id(cell: str) -> str:
    m = REGION.search(plain(cell))
    return m.group(0) if m else ""


def html_text(pkg: Path) -> str:
    return "\n".join(p.read_text(encoding="utf-8") for p in sorted(pkg.glob("*.html")))


def has_specimen(s: str, html: str, pkg: Path) -> bool:
    """A specimen id is present when the HTML names it. `S-A` is the primary by convention (process §5.2):
    the canonical page itself, present when `canonical.html` or `candidate.html` exists."""
    if re.search(rf"(?<![\w-]){re.escape(s)}(?![\w-])", html):
        return True
    return s == "S-A" and any((pkg / f).exists() for f in ("canonical.html", "candidate.html"))


def state_labels(html: str) -> list[str]:
    return [re.sub(r"<[^>]+>", "", m).strip().lower() for m in re.findall(r'class="state-label"[^>]*>(.*?)</', html)]


def g1(pkg: Path, r: Report) -> None:
    brief = pkg / "page-brief.md"
    if not brief.exists():
        r.add("G1 purpose, tasks, non-goals", "FAIL", "`page-brief.md` is missing")
        return
    heads = [
        ln.lstrip("#").strip().lower() for ln in brief.read_text(encoding="utf-8").splitlines() if ln.startswith("#")
    ]
    for label, pat in (
        ("purpose", r"\bpurpose\b"),
        ("primary tasks", r"\bprimary tasks?\b"),
        ("non-goals", r"\bnon-goals?\b"),
    ):
        hit = next((h for h in heads if re.search(pat, h)), None)
        r.add(
            "G1 purpose, tasks, non-goals",
            "PASS" if hit else "FAIL",
            f"{label}: " + (f"heading *{hit}*" if hit else "no heading in `page-brief.md`"),
        )


def g2(pkg: Path, r: Report) -> None:
    man = pkg / "page.manifest.yaml"
    if not man.exists():
        r.add("G2 identified and recoverable", "FAIL", "`page.manifest.yaml` is missing")
        return
    text = man.read_text(encoding="utf-8")
    commit = re.search(r"^\s*canonicalCommit:\s*['\"]?([0-9a-f]{7,40})\b", text, re.M)
    r.add(
        "G2 identified and recoverable",
        "PASS" if commit else "FAIL",
        f"canonicalCommit: {commit.group(1) if commit else 'absent or not a commit'}",
    )
    fixture = re.search(r"^\s*fixture:\s*['\"]?([\w./-]+\.json)", text, re.M)
    if fixture:
        ok = (pkg / fixture.group(1)).exists()
        r.add(
            "G2 identified and recoverable",
            "PASS" if ok else "FAIL",
            f"fixture: {fixture.group(1)}" + ("" if ok else " — file not found"),
        )
    else:
        r.add("G2 identified and recoverable", "FAIL", "fixture: not named in the manifest")
    vp = re.search(r"^\s*viewport:\s*['\"]?(\d{3,4}x\d{3,4})\b", text, re.M)
    r.add(
        "G2 identified and recoverable",
        "PASS" if vp else "FAIL",
        f"viewport: {vp.group(1) if vp else 'absent or not WxH'}",
    )


def region_tables(spec: list[Table]) -> list[Table]:
    return [t for t in spec if t.col("component") is not None and t.col("category") is not None]


def g3(spec: list[Table], r: Report) -> set[str]:
    ids: set[str] = set()
    found = region_tables(spec)
    if not found:
        r.add("G3 regions map to components", "FAIL", "`page-spec.md` has no table with Component and Category columns")
        return ids
    for t in found:
        ci, ki = t.col("component"), t.col("category")
        for line, cells in t.rows:
            rid = region_id(cells[0]) if cells else ""
            if rid:
                ids.add(rid)
            name = rid or plain(cells[0])[:40]
            if len(cells) <= max(ci, ki):
                r.add(
                    "G3 regions map to components", "UNRESOLVED", f"`page-spec.md:{line}` {name}: row has too few cells"
                )
                continue
            cat = plain(cells[ki]).lower()
            if empty(cells[ci]):
                r.add("G3 regions map to components", "FAIL", f"`page-spec.md:{line}` {name}: no component")
            elif cat not in CATEGORIES:
                r.add(
                    "G3 regions map to components",
                    "FAIL" if empty(cells[ki]) else "UNRESOLVED",
                    f"`page-spec.md:{line}` {name}: category *{cat or 'none'}*",
                )
            else:
                r.add("G3 regions map to components", "PASS", name)
    return ids


def g4(spec: list[Table], r: Report) -> None:
    found = [t for t in spec if t.col("keyboard") is not None and t.col("cancel") is not None]
    if not found:
        r.add(
            "G4 behaviour with keyboard and cancel",
            "FAIL",
            "`page-spec.md` has no interactions table with Keyboard and Cancel columns",
        )
        return
    for t in found:
        kb, cc = t.col("keyboard"), t.col("cancel")
        for line, cells in t.rows:
            name = plain(" ".join(cells[:2]))[:60]
            if len(cells) <= max(kb, cc):
                r.add(
                    "G4 behaviour with keyboard and cancel",
                    "UNRESOLVED",
                    f"`page-spec.md:{line}` {name}: row has too few cells",
                )
            elif empty(cells[kb]):
                r.add(
                    "G4 behaviour with keyboard and cancel",
                    "FAIL",
                    f"`page-spec.md:{line}` {name}: no keyboard equivalent",
                )
            elif plain(cells[cc]) == "":
                r.add(
                    "G4 behaviour with keyboard and cancel",
                    "FAIL",
                    f"`page-spec.md:{line}` {name}: cancel cell empty (write — where nothing cancels)",
                )
            else:
                r.add("G4 behaviour with keyboard and cancel", "PASS", name)


def g5(spec: list[Table], html: str, pkg: Path, r: Report) -> None:
    ids = set(re.findall(r'\sid="([^"]+)"', html))
    found = [
        t
        for t in spec
        if plain(t.header[0]).lower().startswith("state") or (t.col("class") is not None and t.col("why") is not None)
    ]
    if not found:
        r.add("G5 states inspectable", "FAIL", "`page-spec.md` has no state table")
        return
    for t in found:
        where = t.col("inspect", "where")
        why = t.col("why", "reason")
        for line, cells in t.rows:
            name = plain(cells[0])[:60]
            if where is None and why is not None:
                r.add(
                    "G5 states inspectable",
                    "FAIL" if empty(cells[why]) else "PASS",
                    f"`page-spec.md:{line}` {name}: n/a" + (" with no reason" if empty(cells[why]) else ""),
                )
                continue
            cell = cells[where] if where is not None and where < len(cells) else ""
            specs = set(SPECIMEN.findall(cell))
            anchors = set(ANCHOR.findall(cell))
            if (
                not specs
                and not anchors
                and any(plain(cell).lower() and plain(cell).lower() in lab for lab in state_labels(html))
            ):
                r.add("G5 states inspectable", "PASS", f"{name} (state label)")
                continue
            if not specs and not anchors:
                r.add(
                    "G5 states inspectable",
                    "UNRESOLVED",
                    f"`page-spec.md:{line}` {name}: names no specimen or anchor — *{plain(cell)[:80]}*",
                )
                continue
            missing = [f"#{a}" for a in sorted(anchors) if a not in ids]
            if not (anchors and not missing):
                # A specimen named beside an existing anchor is that anchor's alias (`#view-before` (S-I)).
                missing += [s for s in sorted(specs) if not has_specimen(s, html, pkg)]
            r.add(
                "G5 states inspectable",
                "FAIL" if missing else "PASS",
                f"`page-spec.md:{line}` {name}" + (f": not in the HTML — {', '.join(missing)}" if missing else ""),
            )


def g8(pkg: Path, regions: set[str], html: str, r: Report) -> None:
    ac = pkg / "acceptance-criteria.md"
    if not ac.exists():
        r.add("G8 criteria point at something that exists", "FAIL", "`acceptance-criteria.md` is missing")
        return
    ids = set(re.findall(r'\sid="([^"]+)"', html))
    n = 0
    for t in tables(ac):
        pt = t.col("points at", "evidence")
        for line, cells in t.rows:
            aid = plain(cells[0])
            if not re.fullmatch(r"AC-[A-Z]+\d+", aid):
                continue
            n += 1
            refs = cells[pt] if pt is not None and pt < len(cells) else " ".join(cells[2:])
            regs = set(REGION.findall(plain(refs)))
            specs = set(SPECIMEN.findall(refs))
            anchors = set(ANCHOR.findall(refs))
            if not (regs or specs or anchors or RULE.search(refs)):
                r.add(
                    "G8 criteria point at something that exists",
                    "FAIL",
                    f"`acceptance-criteria.md:{line}` {aid}: points at nothing",
                )
                continue
            missing = [x for x in sorted(regs) if x not in regions and x.split(".")[0] not in regions]
            missing += [s for s in sorted(specs) if not has_specimen(s, html, pkg)]
            missing += [f"#{a}" for a in sorted(anchors) if a not in ids]
            r.add(
                "G8 criteria point at something that exists",
                "FAIL" if missing else "PASS",
                f"`acceptance-criteria.md:{line}` {aid}" + (f": dangling — {', '.join(missing)}" if missing else ""),
            )
    if n == 0:
        r.add("G8 criteria point at something that exists", "FAIL", "no `AC-*` rows found")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("package", type=Path)
    ap.add_argument("--out", type=Path)
    a = ap.parse_args()
    pkg = a.package.resolve()
    r = Report(f"C1 — structure · `{pkg.name}`")
    spec_path = pkg / "page-spec.md"
    spec = tables(spec_path) if spec_path.exists() else []
    html = html_text(pkg)
    g1(pkg, r)
    g2(pkg, r)
    regions = g3(spec, r) if spec else set()
    if not spec:
        r.add("G3 regions map to components", "FAIL", "`page-spec.md` is missing")
    else:
        g4(spec, r)
        g5(spec, html, pkg, r)
    g8(pkg, regions, html, r)
    text = r.render()
    print(text)
    if a.out:
        a.out.write_text(text + "\n", encoding="utf-8")
    return r.code()


if __name__ == "__main__":
    sys.exit(main())
