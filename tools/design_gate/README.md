# `tools/design_gate/` — C1 and C3

The design gate's two scripts (`90-design-delivery.md` §14; proposal `2026-09-29_slim-design-gate.md` §5
step 2). C2 is each package's existing render check. G11 is read by the S9 take-in seat.

| Script | Carries | Reads |
|---|---|---|
| `c1_structure.py <package>` | G1, G2, G3, G4, G5, G8 | `page-brief.md`, `page.manifest.yaml`, `page-spec.md`, `acceptance-criteria.md`, `*.html` at the package root |
| `c3_coverage.py <package> [--main origin/main]` | G9, G10 | `coverage.md`, and `git` for the pinned commits |

Both take `--out <file>` to write the report. The coordinator runs them at S9 and commits their output
with the specification (`page-spec.md` and `acceptance-criteria.md`). Standard library and `git` only.

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

| Package | Head | C1 | C3 |
|---|---|---|---|
| fixture-result, revision 41 | `94d4226` | 0 — 33 regions, 30 interactions, 26 states, 64 criteria | 0 — 133 rows, pin `9770520` |
| selection, revision 6 | `81e1b0c` | 0 — 30 regions, 16 interactions, 44 states, 103 criteria | 1 — no `coverage.md` yet (converts at its next revision, proposal §5 step 3) |

The counts for fixture-result agree with the S9 take-in's hand check (`WEE-399-T4`: 33 regions, 64
criteria, 133 coverage rows).

`python3 -m unittest tools/design_gate/test_design_gate.py` runs a synthetic package through each fault.
