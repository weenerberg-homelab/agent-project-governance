# `tools/design_gate/` — C1 and C3

The design gate's two scripts (`90-design-delivery.md` §14; proposal `2026-09-29_slim-design-gate.md` §5
step 2). C2 is each package's existing render check. G11 is read by the S9 take-in seat.

Two kinds of screen are gated, by how they were designed (`90-design-delivery.md` §6.8 *Exit*, R-44):

| Script | Carries | A finished package (S1–S10) | A prototype screen (Intermediate, R-44) |
|---|---|---|---|
| `c1_structure.py` | G1, G2, G3, G4, G5, G8 | `c1_structure.py <package>` — `page-brief.md`, `page.manifest.yaml`, `page-spec.md`, `acceptance-criteria.md`, `*.html` at the package root | `c1_structure.py <spec-dir> --prototype <prototype.html> --page <id>` — the `page-spec.md` and `acceptance-criteria.md` the build writes when it reaches the screen, read against **that page** of the frozen prototype (`p-<id>`). G1 reads `page-spec.md` when there is no brief; G2 asks that `page-spec.md` names `p-<id>` and the prototype's pin (a `prototype-final-…` tag or a commit) |
| `c3_coverage.py` | G9, G10 | `c3_coverage.py <package> [--main origin/main]` — the package's `coverage.md` | `c3_coverage.py <repo> --screen <id> [--table <file>]` — the **one** requirement-coverage table for the prototype-covered screens (WEE-470 Q1 (a)), only the rows whose *Screen* column names `<id>` (`week` or `p-week`). Default path `_docs/design/v1a-coverage.md` (WEE-479); when it is missing, C3 says where it looked |

Both take `--out <file>` to write the report. For a finished package the coordinator runs them at S9 and
commits their output with the specification. For a prototype screen they run when the build reaches the
screen, over the spec its increment carries — saved as `page-spec.md` and `acceptance-criteria.md` in one
directory if the instruction holds them as documents. Standard library and `git` only.

**Exit codes.** `0` every item passes · `1` at least one FAIL · `2` no FAIL, but items the script could
not decide. An UNRESOLVED item is read at G11, never passed (§14).

## What each check decides

| | Rule |
|---|---|
| **G1** | `page-brief.md` has a heading for purpose, primary task(s) and non-goal(s) |
| **G2** | The manifest names `canonicalCommit` (a hex commit), `viewport` (`WxH`) and `fixture` (a `.json` that exists) |
| **G3** | Every row of a `page-spec.md` table with *Component* and *Category* columns has a component and a category in `primitive`, `page-local`, `domain`, `shared` |
| **G4** | Every row of a table with *Keyboard* and *Cancel* columns has a keyboard equivalent; the cancel cell is not blank (`—` states nothing cancels) |
| **G5** | Every state row names a specimen (`S-X`) or anchor (`#id`) the HTML carries, or a state label's text; a row in a table with a *Why* column is an n/a class and needs its reason. A specimen named beside an existing anchor is that anchor's alias. `S-A` is the primary: present when `canonical.html` or `candidate.html` exists |
| **G8** | Every `AC-*` row's *Points at* (or *Evidence*) cell names something: its region ids exist in the region table (a sub-region's parent counts), its specimens and anchors exist in the HTML; a cell naming only a rule (`§`, `RL-`, `SR-`, `DA-`, a card) passes as *points at a rule* |
| **G9** | Every `coverage.md` row with an id: *satisfied* passes; *not applicable* needs a reason; a verdict naming NOT COVERED, CHANGED, narrowed, removed or deferred needs the Product Owner's answer; a CHANGED or NOT COVERED **Kind** that is not satisfied needs it too; *partial*, *not satisfied*, *open* fail; anything else is UNRESOLVED |
| **G10** | The pinned specification commit (a two-column header row *Specification*, or a *Source* column header) is on `--main`; a source cell citing a draft that is not folded fails; any other commit a source cites must be on `--main` |

## Checked against

| Screen | Head | C1 | C3 |
|---|---|---|---|
| fixture-result, revision 41 (package) | coach-platform `main` `ac815a6` | 0 — 33 regions, 30 interactions, 26 states, 64 criteria | 0 — 133 rows, pins on `main` |
| This week, `p-week` — M9's first screen (`S1`, WEE-456 `build-plan-1`) | `main` `ac815a6`, prototype tag `prototype-final-2026-10-02` | 1 — the page is found in the prototype; `page-spec.md` and `acceptance-criteria.md` are not written yet (R-44: written when the build reaches `S1`) | 1 — the one coverage table is not at `_docs/design/v1a-coverage.md` yet (WEE-479, in progress) |
| selection, revision 6 (package, earlier run) | `81e1b0c` | 0 — 30 regions, 16 interactions, 44 states, 103 criteria | 1 — no `coverage.md` yet |

The counts for fixture-result agree with the S9 take-in's hand check (`WEE-399-T4`: 33 regions, 64
criteria, 133 coverage rows).

`python3 -m unittest tools/design_gate/test_design_gate.py` runs a synthetic package through each fault.
