# Proposal — the design coordinator generates the design

| | |
|---|---|
| **Status** | **PROPOSED.** Amends `governance/90-design-delivery.md` once approved; not in force before then |
| **Author** | External Product Strategist, acting as design coordinator (Coach Platform, selection package) |
| **Date** | 2026-09-25 |
| **Decided so far** | The Product Owner, 2026-09-25: *"This is the correct way to do it. This is how we will work in the future."* (DC-Q5, DC-F3). Working method only — this document is the process change it implies |

## 1. Evidence

| | External design model (S2–S5 as written) | Coordinator generates (2026-09-25) |
|---|---|---|
| Loop | Coordinator writes a ~600-line prompt → PO pastes it with attachments into the design tool → PO drops the files back → coordinator files and validates them | Coordinator builds, renders and publishes a canvas → PO gives notes → next round |
| Rounds reaching the PO | 3 in 3 days (S2, S4, S5 delta 1) | 14 in one day (rounds 4–17), ending in S7 accepted |
| Failures recorded | Wrong attachment named; the wrong *Layout C* assumed; files handed over without links; prompts edited after the pass had read them (F-4) | Layout defects found by render and fixed before publish: clipped boards, wrapped headers, lost row lines, a sticky header broken by a style change |
| Board rounds | Q39–Q49 cycled without converging (DEC-013's own record) | None needed for design choices: the PO answered in-session questions, each with its on-screen effect stated |

**Inferred:** most of the gain is the removed hand-off, not the model. **Assumed:** the rate holds on a page with less settled content than selection had at S4.

## 2. Proposed changes to `90-design-delivery.md`

| Section | Now | Proposed |
|---|---|---|
| **§3 Roles** | The design model generates; the coordinator *never generates design* | **The coordinator generates the design** on a design canvas. An external design model stays available when the Product Owner asks for one |
| **§5.7 Retained input** | One self-contained prompt per pass | **The generator is the retained input**: the page's markup source and its data, committed with the package as tooling (never product code, never linted as source). Each round's `brief.md` quotes the Product Owner's notes verbatim. Prompts are written only when an external model is used |
| **§6 Stages** | S2 alternatives → S3 choose → S4 high-fidelity → S5 audit and deltas → S6 coverage → S7 visual | **One design loop replaces S2–S5 and S7**: generate → render-check → publish → Product Owner's notes, repeated. It ends when he accepts the design for **each device form**, desktop and phone named separately. **S6 runs after the loop**, on the accepted design |
| **§8 Alternatives** | A number set by the brief, generated once | **Cheap and on demand**: offered as boards on one canvas whenever a question is open — layout, control design, style. The selection package did this for control shapes and for four style schemes |
| **§9 Assumption audit** | ACCEPT / REJECT / MODIFY / IRRELEVANT on the model's report | **Dropped** — the coordinator's assumptions are its own. Each round's README lists them. Spec gaps go to the reconciliation list in DEC-013's three kinds, with **NOT COVERED shown at every visual judgement** |
| **§11 Budgets** | Fixed S5 and S7 delta budgets and a stop rule | **The Product Owner's word ends the loop** (*"it is a wrap"*). There is no count budget; the round log in the manifest shows the cost |
| **New · Render check** | — | **Every round is rendered before it is published**: desktop width and 360px, with no horizontal overflow, measured board heights, and sticky and hover behaviour verified. A defect found is fixed before publishing, not reported. This needs the Product Owner's standing consent, because the canvas type renders only when asked; he gave it on 2026-09-25 (DC-Q6) |
| **New · Canvas hygiene** | — | One canvas per package for the candidate. Explorations go on **separate** canvases, so an accepted candidate is never overwritten. Read the live version before every publish; a save from inside the page is merged, never forced |
| **New · Reconciliation list, kept per round** | — | **Updated every round**, not at the end. Each row carries its kind (CHANGED, ADDED, NOT COVERED), the round that introduced it, and the Product Owner's answer where he gave one. The manifest records the list's state at every visual judgement. An **ADDED or CHANGED row that introduces or changes a computed figure** carries its computation rule, and the figure is rebuilt by a second seat before the freeze (see §14.1 and *Rebuild request* below) |
| **New · NOT COVERED rows** | — | **Shown at every visual judgement until answered, and answered once.** An answered row is not shown again unless the design changes it. A row the Product Owner neither covers nor removes gets **one** design round to cover it; if it still is not covered, it goes back to him as keep-or-remove, and that answer is final. This bounds how often a frozen design can reopen |
| **§14.1 Independence** | Figures rebuilt twice, by different seats | **Unchanged, and now load-bearing.** The coordinator both builds and designs, so **every figure it computes for a design is rebuilt by a second seat before the S8 freeze** (the selection package has three: versatility for unselected players, the order per fixture view, and the best position per fixture). The visual stays the Product Owner's eye |
| **New · Rebuild request** | — | **The coordinator writes the rebuild request** as soon as a computed row lands on the reconciliation list. It is one committed prompt per batch, addressed to the second seat (on Coach Platform, the internal Product Strategist). It carries the rule as the Product Owner decided it, the views to rebuild, the instruction to rebuild before reading the design's figures, and where the result goes: the package's expected-figures file, one commit, one comment on the package pull request. **The Product Owner or the operator hands it over**; the coordinator has no tracker seat. The rebuild runs alongside the rounds. **The freeze waits on it**, and a round that changes a rebuilt figure gets a new request. **On a mismatch** the second seat changes neither design nor specification: the coordinator corrects the design, or takes the rule to the Product Owner |

**The two NOT COVERED rules and the per-round list come from the design coordinator's review of Coach
Platform's DEC-013** (REPORT-008, findings F2–F4, M1–M3). They are written here so every project that
runs this process gets them, not only the one whose decision prompted them.

**Unchanged:** invariants; S8 freeze; S9 page-spec and acceptance criteria; S10 gate; §14.5, under which the built screen is checked against the package; and, on Coach Platform, DEC-013's alignment pass in place of §13's per-change amendment.

## 3. Risks, and what answers each

| Risk | Answer |
|---|---|
| The coordinator checks its own work | The Product Owner judges by eye each round; figures are rebuilt by a second seat at S6 (§14.1); the render check is mechanical |
| The design drifts from the spec without anyone noticing | DEC-013 clause 4: the reconciliation list in three kinds, and NOT COVERED shown at every judgement |
| The generator becomes a second codebase | It is package tooling, like `fixture-expected.md`'s calculator: never imported, never adopted. The Architect builds from the accepted package, not from the generator |
| Per-round cost | Each round is a delta on the generator, not a regeneration. The manifest's round log is the audit |
| Canvas fonts load from Google | The product self-hosts two `woff2` files (cheap under the stack brief); recorded on the round that picks a font |

## 4. For the Product Owner

- **(a)** Approve this as a change to the shared process, `90-design-delivery.md` on governance `main`. Coach Platform follows it on merge, under DEC-011.
- **(b)** Approve it as a Coach Platform variation only — DEC-011 V6 — and leave the shared process as it is.

**Recommendation: (a).** Nothing in it is specific to Coach Platform, and a variation would leave the shared process describing a loop no project runs.
