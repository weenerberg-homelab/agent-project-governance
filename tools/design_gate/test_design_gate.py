"""Tests for C1 and C3 on a synthetic package. Standard library only:

python3 -m unittest tools/design_gate/test_design_gate.py
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent

BRIEF = "# Brief\n\n## 3. Purpose\n\nx\n\n## 4. Primary tasks\n\nx\n\n## 8. Non-goals\n\nx\n"
MANIFEST = (
    "package:\n  id: demo\nartifacts:\n  canonicalCommit: {commit}\n  viewport: 360x800\n  fixture: fixture.json\n"
)
SPEC = textwrap.dedent(
    """\
    # Page specification

    ## 1. Regions

    | Region | Element | Component | Category | Reusable |
    |---|---|---|---|---|
    | **R1** | `header` | Head | primitive | no |
    | **R2** | `ul.list` | List | {cat} | no |

    ## 2. Interactions

    | | Trigger | Result | Keyboard equivalent | Cancel |
    |---|---|---|---|---|
    | I-1 | Tap | Opens | Enter | Escape |
    | I-2 | Tap | Saves | {kb} | — |

    ## 3. States

    | State | Inspected at |
    |---|---|
    | Empty | `S-B` |
    | Full | `#view-full` |
    """
)
AC = textwrap.dedent(
    """\
    # Acceptance criteria

    | Id | Criterion | Points at |
    |---|---|---|
    | AC-S1 | The head shows | R1; S-A |
    | AC-B1 | The list saves | {ref} |
    """
)
HTML = '<!doctype html><section id="view-full"></section><p class="state-label">S-B · empty</p>'
COVERAGE = textwrap.dedent(
    """\
    # coverage.md

    | | |
    |---|---|
    | **Specification** | `main` at `{commit}` |

    | Id | Requirement | Source (at `{commit}`) | Where visible | Verdict | Product Owner's answer |
    |---|---|---|---|---|---|
    | SR-01 | Shows the head | PR §1 | R1 | satisfied | — |
    | SR-02 | Out of V1 | PR §2 | — | not applicable — out of V1 | — |
    | SR-03 | Lists items | PR §3 | — | {v3} | {a3} |
    """
)


def run(script: str, pkg: Path) -> subprocess.CompletedProcess:
    extra = ["--main", "main"] if script.startswith("c3") else []
    return subprocess.run([sys.executable, str(HERE / script), str(pkg), *extra], capture_output=True, text=True)


class Gate(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.pkg = Path(self.tmp.name)
        subprocess.run(["git", "init", "-q", "-b", "main", str(self.pkg)], check=True)
        (self.pkg / "README").write_text("x")
        subprocess.run(["git", "-C", str(self.pkg), "add", "."], check=True)
        subprocess.run(
            ["git", "-C", str(self.pkg), "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "x"], check=True
        )
        self.commit = subprocess.run(
            ["git", "-C", str(self.pkg), "rev-parse", "--short", "HEAD"], capture_output=True, text=True
        ).stdout.strip()

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def write(self, *, cat="domain", kb="Enter", ref="R2; S-B", v3="satisfied", a3="—") -> None:
        p = self.pkg
        (p / "page-brief.md").write_text(BRIEF)
        (p / "page.manifest.yaml").write_text(MANIFEST.format(commit=self.commit))
        (p / "fixture.json").write_text("{}")
        (p / "page-spec.md").write_text(SPEC.format(cat=cat, kb=kb))
        (p / "acceptance-criteria.md").write_text(AC.format(ref=ref))
        (p / "canonical.html").write_text(HTML)
        (p / "coverage.md").write_text(COVERAGE.format(commit=self.commit, v3=v3, a3=a3))

    def test_clean_package_passes(self) -> None:
        self.write()
        c1, c3 = run("c1_structure.py", self.pkg), run("c3_coverage.py", self.pkg)
        self.assertEqual(c1.returncode, 0, c1.stdout)
        self.assertEqual(c3.returncode, 0, c3.stdout)

    def test_c1_catches_each_fault(self) -> None:
        for kw, expect in (
            ({"cat": ""}, "R2: category"),
            ({"kb": "—"}, "no keyboard equivalent"),
            ({"ref": "R9"}, "dangling — R9"),
            ({"ref": "S-Q"}, "dangling — S-Q"),
            ({"ref": "nothing here"}, "points at nothing"),
        ):
            with self.subTest(kw=kw):
                self.write(**kw)
                out = run("c1_structure.py", self.pkg)
                self.assertEqual(out.returncode, 1, out.stdout)
                self.assertIn(expect, out.stdout)

    def test_c3_routes_and_fails(self) -> None:
        for v3, a3, code, expect in (
            ("NOT COVERED", "—", 1, "with no Product Owner answer"),
            ("NOT COVERED", "card `abc` Q1 (a)", 0, ""),
            ("partial", "—", 1, "partial"),
            ("looks fine", "—", 2, "not recognised"),
        ):
            with self.subTest(v3=v3, a3=a3):
                self.write(v3=v3, a3=a3)
                out = run("c3_coverage.py", self.pkg)
                self.assertEqual(out.returncode, code, out.stdout)
                self.assertIn(expect, out.stdout)

    def test_c3_rejects_a_commit_not_on_main(self) -> None:
        self.write()
        cov = self.pkg / "coverage.md"
        cov.write_text(cov.read_text().replace(self.commit, "deadbee"))
        out = run("c3_coverage.py", self.pkg)
        self.assertNotEqual(out.returncode, 0, out.stdout)


if __name__ == "__main__":
    unittest.main()
