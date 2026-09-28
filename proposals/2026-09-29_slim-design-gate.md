# Proposal — one design artifact, and a gate of three scripts and one reading

| | |
|---|---|
| **Status** | **PROPOSED** — for the Product Owner. Nothing in `90-design-delivery.md` changes until he approves; the changes are then applied in one pull request, and this document is kept as the record |
| **Author** | Operator (paperclip_trial), from REPORT-009 **R-43** |
| **Date** | 2026-09-29 |
| **Asked by** | The Product Owner, Q145, 2026-09-29 — *"Proposal"* |

## 1. Why now

The design gate the process ends in was sized for the first package, which was also the one the process
was invented on. **Eleven packages are now heading for S9 and S10** on Coach Platform: fixture-result,
this-week, create-fixture, session, players, season-setup, teams-schedule, plan, settings, assessment, and
the accepted app flow. Everything the gate costs, it now costs eleven times over.

| What a package pays after the design is accepted | Now | Evidence |
|---|---|---|
| Artifacts tracking requirements | **Two**: the §7.2 coverage table (S1) **and** the §6.3 reconciliation list (every round) | Both hold one row per requirement, verdict in one, CHANGED/NOT COVERED in the other |
| Coverage verified | **Three times**: the sweep every round (§5.7), S6 on the accepted design (§10), and the independent forward rebuild at S10 (§14.1) | Selection's S10 (WEE-273) cost $43; the S6 re-runs whenever a round moved the design |
| Take-ins on the tracker | **Four**: S1, S8, S9 and S10 | Selection: WEE-135 $25, WEE-171 $55, WEE-182 $21, WEE-231 $26 — plus a card at most of them |
| Gate | **Eleven checks, G1–G11**, run by reading | REPORT-009: *"eight of the eleven gate checks as separate steps"* |

Two packages have run it end to end: selection (the learning case, **$469** of tracker-side design work) and
fixture-result (**$109**). The four take-ins, the double-kept coverage and the eleven read checks are most
of what the second one still paid.

## 2. What stays — REPORT-009's keep list

Nothing below removes any of these:

- **DEC-013's boundary**: the accepted design governs what the user sees and does; invariants and rules of
  computation stay binding.
- **The second-seat rebuild of every computed figure before the freeze** (§14.1), which found real errors
  on both packages.
- **The render check and the NOT COVERED sweep as scripts, every round** (§5.7).
- **The Product Owner's eye ends the loop** (§11), and his acceptance makes a package DECIDED.

## 3. The proposal

### 3.1 One artifact: `coverage.md` replaces the coverage table and the reconciliation list

One row per applicable requirement, built at S1 from the accepted specification (never from a brief), and
kept current every round by the sweep script:

| Requirement | Source, section and commit | Where visible | Verdict | PO answer |
|---|---|---|---|---|
| id | folded accepted spec at a commit | region id or specimen | **satisfied** · **CHANGED** · **NOT COVERED** · **not applicable** (reason) | card and date, where he gave one |

Plus **ADDED** rows for what the design does that the specification does not. The alignment pass reads its
CHANGED, NOT COVERED and ADDED rows — exactly what it reads from `reconciliation-list.md` today. A computed
figure's row carries its rule, and the second-seat rebuild is still required for it (§14.1, unchanged).

### 3.2 S6 is the loop's last sweep, not a stage

The sweep already runs every round. **At the design's acceptance, the last sweep report is S6's forward and
reverse result**, and the arithmetic is the second-seat rebuild the freeze already waits on. S6 disappears
as a separate pass; the stage name stays so records citing it resolve.

### 3.3 Two take-ins, not four

| Take-in | Now | Proposed |
|---|---|---|
| S1 | Brief, design space, **independent forward coverage built from the specification** | **Unchanged** — the independent build moves *here*, where a stale requirement list is cheapest to catch |
| S8, S9, S10 | Three separate take-ins, most with a card | **One**, at S9: the freeze commit, `page-spec.md`, `acceptance-criteria.md` and the gate result together, **one card** to accept the package |

### 3.4 The gate: three scripts and one reading

| | Replaces | How |
|---|---|---|
| **C1 — structure** (script) | G1, G2, G3, G4, G5, G8 | Checks that the brief states purpose, tasks and non-goals; the manifest names viewport, fixture and commit; every region in the canonical HTML carries a component id and category; every interactive component has a behaviour row with keyboard and cancel; every state class has a named specimen or an n/a reason; every acceptance criterion points at an id that exists |
| **C2 — render** (the existing render check) | G6, G7 | Device forms rendered, no horizontal overflow, the keyboard-reach and visible-focus table, and a lint for colour-only meaning |
| **C3 — coverage** (script) | G9, G10 | Every applicable `coverage.md` row is satisfied, or CHANGED/NOT COVERED with a PO answer; every source cites a folded specification at a commit on `main`, never a draft amendment |
| **G11 — the decisive reading** (a seat, kept) | G11 | *Do the rendered states and the figures satisfy the accepted rules, with nothing left for an implementer to invent?* The one check no script can do, read by the S9 take-in seat |

The three scripts live **once, in the governance repository** (`tools/design_gate/`), not re-written per
package. A package passes them before its S9 take-in; the take-in reads their output and does G11.

## 4. What it saves, estimated

| Per package | Now | Proposed |
|---|---|---|
| Take-ins | 4 | **2** |
| Cards to the Product Owner after acceptance | 2–3 | **1** |
| Coverage artifacts | 2, kept by hand in step | **1**, kept by the sweep |
| Gate checks read by a seat | 11 | **1** (G11) |
| Tracker-side design cost | $109 (fixture-result) | **≈ $50–70**, inferred from dropping two take-ins and S6 |

Across the eleven packages in flight: **about 22 fewer take-ins, 11–22 fewer cards, and ≈ $0.4–0.6 k**.
**Assumed:** simpler screens (hubs, lists) sit at the low end. **Unverified:** C1 depends on the canonical
HTML carrying component ids consistently — true of the two finished packages, to be checked on the rest.

## 5. How it is applied

1. On approval, one governance pull request (the Product Owner merges; no agent seat): §5, §6, §6.3, §7.2,
   §10 and §14 of `90-design-delivery.md`, the coordinator template, and the `design-delivery` skill.
2. `tools/design_gate/` — C1 and C3 — written by the coordinator (the gate scripts are its to own, like
   the sweep), reviewed by a second seat, landed in the same repository.
3. **Packages in flight** convert at their next revision: the coordinator merges the two files into
   `coverage.md`. **Fixture-result** (S9, gate not yet run) is the first to use the new gate.
4. The host watcher stops opening a separate S8 take-in; the S9 take-in carries the freeze.

## 6. Decide

- **(a) Approve** — applied as §5 says.
- **(b) Approve §3.1–§3.3 only** — one artifact and two take-ins, keeping the eleven read checks.
- **(c) Reject** — the gate stays as it is.
