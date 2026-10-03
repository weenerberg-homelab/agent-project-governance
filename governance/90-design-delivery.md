# Design delivery — the process, the package and the gate

**Status:** accepted on merge · **Applies to:** any project designing screens · **Amends:** the Product
Strategist section of `10-agents_workflow.md`, which this file's §3.1 depends on · **Amended
2026-09-25:** the design coordinator generates the design (`proposals/2026-09-25_design-coordinator-generates.md`,
approved (a) by the Product Owner)

This process was reduced from two much larger UX operating documents and then corrected twice against
independent review. Its worked examples come from the first project to use it; the rules are general
and the examples are labelled as examples.

---

## 1. What this is

A process for turning a product requirement into a screen that a software agent can implement without
making design decisions of its own, **and, before the screens, for designing the flow between them**
(S0, §6.7). A package per screen makes each screen right and leaves the path between screens decided by
nobody; on Coach Platform that path was written in `design-intent.md` §2 and never designed, and the
Product Owner found the deployed flow poor once the first screens were good (2026-09-28).

It is written for a small product built by a mixed team of one human Product Owner and several agents.
**The design coordinator generates the design** on a design canvas, round by round, and the Product
Owner judges each round by eye. An **external design model** — no memory between sessions, no access to
the product's records — stays available when the Product Owner asks for one; §5.7 and §9 say what
changes then.

**Which parts apply depends on the project's phase** (`20-development_iteration.md`, *Development
phases*). In **Exploratory** the work is one clickable prototype (§6.8) and the per-screen stages S1–S10
do not run. From **Intermediate** the stage table in §6 applies to each screen, and in **Finalization**
it applies strictly.

### What it is not

- Not a visual style guide.
- Not a replacement for the requirements or for `design-intent.md`. Those say what the product does and
  what a design must satisfy; this says how a screen gets built, checked and frozen.
- Not a design system, and not a second home for decisions that already have one. §12.5 names the
  authoritative home for each kind.

---

## 2. The problem it solves

Four failures from the first project to use this process, stated narrowly, from what its record
supports. They are why each control below exists.

**A design space went unexamined.** Round 3 fixed the layout and opened only visual language — a
legitimate choice, which §8 allows — and nothing checked that declaration against the specification. It
carried a position set the grid does not contain into every treatment that followed.

**Correctness and quality were judged in the same breath.** Reviews asked whether a rule was carried.
Nobody asked whether the screen was good. *[Unverified: whether the outputs were in fact poor. No
round's HTML is archived; the judgement was made in conversation and cannot be re-inspected.]*

**The brief was checked against the specification once, and then it was not.** The round-2 brief was
checked against the accepted specification at `48fa259`; the check returned 26 findings, caught a
position vocabulary the grid forbids, and 20 were applied. The round-3 brief was never put through it,
and that is where a position set unrelated to the fixture's format entered and stayed. A check that
depends on somebody choosing to run it is not a control.

**Numbers were wrong in ways a coverage list would not catch.** Two rounds shipped with a wrong count of
players owed a fixture. A corrected count was supplied by the tooling, not by the review.

---

## 3. Roles

| Seat | Owns | Never |
|---|---|---|
| **Product Owner** | Every decision. Judges whether the screen looks right. Accepts the package | — |
| **Design coordinator** — the Product Strategist seat, run outside the tracker | The brief. **Generates the design** on a design canvas, with its generator committed as package tooling (§5.7). The render check and the NOT COVERED sweep, every round (§6.1, §6.4). The reconciliation list (§6.3). The rebuild request (§14.1). Alternatives, on demand (§8). The specification written from the frozen visual | Approves its own work. Decides anything. Checks its own computed figures — a second seat rebuilds them (§14.1) |
| **Design model** — only when the Product Owner asks for one | Structural and visual alternatives, high-fidelity screens, its own assumption report (§9) | Redefines page purpose, workflow, or a rule about what a figure means |
| **Internal Product Strategist** — the same seat, inside the tracker | Compliance. Asks for a package before any screen is implemented. **Rebuilds the figures the design computes, on the coordinator's rebuild request** (§14.1). Runs the gate. Orders scrutiny. Records the check result | Generates design. Accepts a package |
| **Product Advisor** | Implementation-readiness review on request. Reviews any amendment originating inside a design round | Redesigns |
| **Architect** | Consumes the accepted package. Owns the view model, data binding and technical specification. Gives the feasibility opinion at §9.1 | Acts as a design authority |
| **Implementor** | Builds against the accepted package | Decides anything the package left open |

### 3.1 This process amends the role contract

`10-agents_workflow.md` gives the **external** Product Strategist seat exactly one deliverable — an
amendment document in a pull request — and forbids it to write code, tests, architecture or
instructions. The internal seat already produces specification revisions on the board's approval. The
coordinator duties in §3 exceed the external seat's remit as it stood.

**That section is therefore amended alongside this file**, under *Design delivery, where a project runs
it*. It authorises the external seat to produce, for a design package only: the page brief, **the design
itself — the canvas rounds and the generator that produces them —**, the package's check scripts
(§5.7), the coverage table, the reconciliation list, the rebuild request, the page specification and the
acceptance criteria; and, when an external design model is used, the generation prompts and the
assumption audit. The generator and the scripts are package tooling: never product code, never imported,
never adopted. It does not extend to code, tests, architecture, the view model or any technical instruction,
all of which remain the Architect's under the project's change-routing decision, and the external seat
still creates nothing in the tracker.

**This process is not in force in a project until that project adopts it**, and it must not be cited as
authority before then. A brief, a package or an amendment that cites a process the project has not
adopted is citing nothing.

### 3.2 Proportionality is binding

The shared workflow governance already makes proportionality binding and routes evidence-settled
technical questions away from the Product Owner. That applies here.

**Agents check routine evidence and bring the Product Owner three things only:** exceptions, unresolved
product choices, and the visual judgement — batched, with a recommendation. Ordinary passing verdicts
are recorded as evidence and are not presented one at a time for acceptance.

The brief sets the round's scope. Alternatives are offered on demand (§8), and the design loop ends on
the Product Owner's word (§11); neither is fixed by this document.

### 3.3 A board answer is recorded inside the tracker and folded in outside it

§3 gives the brief, the generation prompts and the page specification to the **coordinator**, which
runs outside the tracker and cannot read a board answer. The **internal seat** reads the board and
owns none of those artifacts. Nothing said who carries an answer from one to the other, so the
internal seat filled the gap by editing the coordinator's artifacts itself.

That is the expensive path. The coordinator holds the package in one session; the internal seat
re-reads it from the tracker every time it folds anything in. On the S1 selection package the two
costliest runs of the whole day — **$18.71 and $12.95 of reference price** — were both the internal
seat folding board answers into the brief.

**The internal seat records the answer. The coordinator folds it in.**

- The internal seat writes the answer **on the issue**, verbatim, with the card and the timestamp,
  and says which artifacts it bears on. It edits no coordinator artifact to do this.
- The coordinator folds it into the brief, the prompts and the specification in its next session,
  reading the answer from the issue as delivered.
- **Where an answer blocks the round and the coordinator will not run before it is needed**, the
  internal seat may fold it in, and **says on the issue that it did and why**. The exception exists
  because a package must not wait on a session nobody has opened; naming it is what stops it becoming
  the rule again.

This costs one handoff per round. It is worth it when the round is expensive and not when it is
cheap, which is why the exception above is written as a judgement the internal seat makes and
records rather than as a threshold.

### 3.4 The board round is the expensive unit, and it is budgeted

A **board round** is one card to the Product Owner plus everything that follows from it: the
Advisor review that produced the questions, the coordinator's fold-in of the answers, and the
revision review of that fold-in. It is the most expensive thing this process does. On the S1
selection package, five board rounds — Q18–Q20, Q21–Q23, Q24, Q26–Q27, Q28–Q29 — cost about $90 of
reference price in one day, 63% of everything the project spent, on a single screen.

**Two board rounds is the budget for a design package.** The first settles the questions the design
space raises. The second settles what the alternatives and the Advisor's review raise against the
answers to the first.

**A third round is allowed and is not free.** The coordinator states, in one line on the issue, what
the first two rounds failed to settle and why it could not have been asked earlier. That line is the
whole cost of the exception, and it exists so that a package that genuinely needs four rounds can
have them while a package that is drifting says so in the record.

**Within a round, every open decision goes on one card.** Splitting three decisions across three
cards is three rounds wearing one round's name: each one wakes a seat, re-reads the package and
produces a fold-in. The 10-question limit is the real bound, not the tidiness of the grouping.

A question that arrives after its round has closed — because a review found it, or because an answer
created it — is held for the next round unless it blocks the work outright. Holding it is what keeps
the budget meaningful.


### 3.5 A finding about the record of the process is applied, not carded and not re-reviewed

Some findings are about the record of the process rather than the package: which head or commit
range a review covered, a commit count, a tally of corrections, a pointer to a card, issue or finding
id that has gone stale. They change no figure, rule, requirement, board answer or acceptance
criterion. **The owner applies them and lists them on the issue.** They do not go on a card, and a
commit made only of them does **not** reopen a revision review: the last review's verdict stands for
the head it named, and the list states what changed after it.

**If any line of the fix moves a figure, a rule, a requirement, a board answer or an acceptance
criterion, it is not this kind of finding**, and §3.4 applies. Anything uncertain is treated as not
this kind.

Why: on the S1 selection package on 2026-09-24, pull request #108 opened as two count corrections and
closed at seven commits and twenty-one recorded corrections. Its last five findings were all about the
review record. They cost one extra board card and one more review round, and a third round was argued
about for a commit that changed no number.

Where the project's routing decision pre-approves a class of merge — Coach Platform's DEC-002 — a pull
request made only of such fixes merges under that class; this section does not create a card where the
project's routing decision removes one.

---

## 4. Status vocabulary

| | |
|---|---|
| **DECIDED** | Approved and authoritative |
| **PROPOSED** | A candidate that has not been accepted |
| **OPEN** | A known decision still to be made |
| **UNKNOWN** | Information is not available |
| **OUT OF SCOPE** | Explicitly excluded from this page, through §13's route |

**An OPEN or UNKNOWN item that is needed to implement accepted scope blocks the gate.** An optional
proposal does not. The brief says which each item is; where it does not, the item is treated as needed
and blocks.

---

## 5. The package

### 5.1 `page-brief.md`

| Section | Contents |
|---|---|
| Identity | Page id, route, archetype where one exists |
| User and context | Who uses it and in what situation |
| Purpose | One sentence |
| Primary tasks | The dominant workflows |
| Secondary tasks | Available, must not dominate |
| Information priority | Each significant item as critical, primary, secondary or contextual |
| Data needed | Named only — not bindings, not a schema |
| Non-goals | What this page must not try to solve |
| **Design space** | FIXED · OPEN FOR DESIGN · OUT OF SCOPE, as three explicit lists |
| **Applicable accepted criteria** | Which of `design-intent.md` §3's criteria bind this page, by id, and which do not, with a reason |
| **Stack constraints** | The `design-intent.md` §6 constraint brief, as it applies here |
| **`coverage.md`** — the one requirement artifact: the coverage table and the reconciliation list in one file (§7.2, §6.3) | §7.2 |
| Round scope | What the design loop opens, and what it must not change (§3.2) |
| Open questions | Each with a status from §4 and whether it blocks |

### 5.2 `canonical.html`, `fixture.json` and `fixture-expected.md`

**The visual.** Self-contained, no external assets, one pinned viewport, one pinned fixture. Every major
region carries an id the specification refers to. Because the artifact is working HTML rather than an
image, it is the canonical visual, the annotated reference and the layout specification at once.

**It must obey the stack constraints.** the project's design-intent document states which dependencies the stack
cannot carry, and the design must obey all of them. In the first project to use this, that prohibition
spans three sections — the acceptance criteria, the visual-language section and the constraint brief —
and names a bundler, a component library, a JavaScript animation, a modal, a client-side table and a
chart library. **Read all of the sections that carry it, not one.** A design depending on a prohibited
dependency is rejected inside the design loop, not discovered at implementation.

**This is not a ban on every expensive thing.** A constraint brief that calls something *bespoke* is
stating a cost, not a prohibition. Do not widen the rejection beyond what the accepted documents name.

**The fixture is invented, always.** No real squad data leaves the Product Owner's machine
(`product-requirements.md` §4; `design-intent.md` §5). Generated code is a visual reference and is never
adopted as product code.

**The fixture ships with its expected results.** `fixture-expected.md` states, for every derived figure
the screen shows, the inputs and the result computed independently from the accepted formulas **before
generation**. It cites the formula rather than restating it. Where a formula is genuinely unresolved, it
names the blocking product decision instead of supplying an authoritative-looking number.

**Every page** covers the boundary cases its own derived figures have, plus the generic layout
stresses: a missing value, a long name, a large count, an empty region.

**A page that consumes the selection rules** must additionally cover the recorded failure cases: a
window with no captured session versus one captured with zero attendance; a reserve marker versus an
offer; thin data above the cover level; a fixture count that changes the entitlement; a player with no
assessment.

Those cases are **mandatory where the page consumes those rules and illustrative elsewhere**. No page
invents selection data, or adds screen behaviour, solely to satisfy this list. Scenarios that cannot
coexist in one static view are named as separate specimens rather than forced into one fixture.

### 5.3 `page-spec.md`

Consolidates decisions already made (§9.1), and does not discover them.

| Section | Contents |
|---|---|
| Component map | Region id → component → category (primitive · domain · page-local) → reusable yes/candidate/no |
| Interactions | Per interactive component: trigger, result, keyboard equivalent, cancel behaviour |
| States | Per component with alternates: **each applicable state inspectable through a named specimen or a reproducible interaction in the artifact**, not a list of names. A state class that does not apply is marked so, with a reason |
| Device forms | Every device form an accepted criterion requires. DA-8 requires the 360px form on every screen; it is an obligation, not an option |
| Layout rules | Max width, column behaviour, the width at which the layout changes and to what, overflow, truncation, sticky and scroll behaviour |
| Accessibility | Keyboard reach, focus order and visible focus, accessible names for icon-only controls, no meaning carried by colour alone |

### 5.4 `acceptance-criteria.md`

Structural, visual, behavioural, data, state, accessibility. **Every criterion points at a region id, a
named specimen, or a named rule.** A criterion pointing at nothing is a defect in the package.

### 5.5 `page.manifest.yaml` — the package's identity

A version string is not an identity. In the first project to use this, the requirements document
changed content while remaining v2.3, repaired across two commits. Two agents can cite the same version
and use different rules.

```yaml
package:
  id: <page-id>
  revision: <n>
  supersedes: <package revision or none>
  owningPath: <repository and path>
  step: <S0 — round N | S0 — accepted | S1 | loop — round N | S6 | S8 — freeze | S9 | S10>   # §6.6; the host automation reads it
  pullRequest: <number>        # the package's one open pull request (§6.6); a fresh session reads its comments first
sources:                       # accepted specification, by commit, not by version alone
  - {doc: product-requirements.md, version: <v>, commit: <sha>}
  - {doc: design-intent.md, version: <v>, commit: <sha>}
artifacts:
  canonicalCommit: <sha>
  viewport: <w>x<h>
  fixture: fixture.json
  expected: fixture-expected.md
acceptance:
  productOwner: <record id and date, or pending>
  gateResult: <record id, or pending>
designSystem: <version, or none>
components: [<names>]
requirements: <path to coverage.md>
```

**When a named source commit changes**, the package records the impact and rechecks only the affected
evidence. It does not silently remain DECIDED.

### 5.6 What is deliberately not in the package

**Data binding, the view model and any schema** belong to the Architect under the project's
change-routing decision.

**But the package does settle observable data semantics**, because those are product meanings and not
technical mappings: which fixture, date or selection a figure describes; its source rule; what a missing
value means; display precision where it changes interpretation; and when the figure refreshes. The
Architect maps those decisions into one technical contract and does not choose them.

### 5.7 The retained input — the generator, and its check scripts

**The generator is the retained input.** The coordinator generates the design, so what is retained is
what produces it: the page's markup source and its data, committed with the package under
`_docs/design/<page>/tools/`. It is package tooling — never product code, never imported, never linted as
source; the Architect builds from the accepted package, not from the generator. **Each round is a delta
on the generator, not a regeneration.** Each round's folder holds the rendered candidate and a
`README.md` that lists what changed, the coordinator's own assumptions, and a `brief.md` quoting the
Product Owner's notes verbatim where the round answers notes.

**The check scripts are committed with the package and run every round** — not steps remembered. Two
at least, in the same `tools/` folder:

| Script | Checks | Run |
|---|---|---|
| **Render check** | §6.1: every board rendered at desktop width and at 360px, no horizontal overflow, board heights measured against the canvas, sticky and hover behaviour present | Before every publish. A failure is fixed, not published |
| **NOT COVERED sweep** | §6.4: every row of `coverage.md` (§7.2) against the round's candidate; a requirement with no counterpart becomes a NOT COVERED row | Every round. Its output is recorded in the round's `README.md` |

A check that depends on somebody choosing to run it is not a control (§2). On the first package run this
way, the sweep was run once, before the freeze, and found two requirements eighteen rounds of
per-judgement lists had missed.

**When an external design model is used**, it has no memory and no repository access. *"Retain
everything unspecified"* is meaningless to a session that never saw the previous artifact. Every
generation pass is then driven by a single retained file containing:

| | |
|---|---|
| Applicable source excerpts | The rules this screen must satisfy, quoted, with their source and commit |
| Accepted choices so far | Decisions from earlier steps, and the design space |
| Constraints | The stack constraint brief, the no-real-data rule, the never-adopt-generated-code rule |
| The fixture | Verified invented, with its expected results |
| The prior artifact | In full, when the pass is a delta |
| The requested delta | Numbered, specific |
| Expected return | The artifacts, and the assumption report |

**The returned difference is validated.** A delta instruction is not proof that unrelated content
survived; the coordinator diffs the artifact and reports what moved that should not have.

---

## 6. The process

| | Step | Owner | Exit condition |
|---|---|---|---|
| **S0** | **The flow wireframe** — once per product or release, before its screen packages (§6.7): every screen, every moment of use as a clickable path, low fidelity | Coordinator generates; **Product Owner judges by clicking** | **The Product Owner accepts the flow** ("accept flow"), recorded as §11 records a design acceptance |
| **S1** | Brief, design space, applicable criteria, `coverage.md` built from the accepted specification, round scope | Product Owner + coordinator | Internal strategist records the page **OPEN**, having built the forward coverage independently and compared (§14.1) |
| **S2–S5, S7** | **The design loop**: generate → render check → NOT COVERED sweep → publish → the Product Owner's notes, repeated. Alternatives on demand (§8); behaviour and state decisions captured as made (§9.1); `coverage.md` updated every round (§6.3) | Coordinator generates; **Product Owner judges by eye** | **The Product Owner accepts the design for each device form**, desktop and phone named separately, and the acceptance is recorded (§11) |
| **S6** | **The loop's last sweep, not a separate pass** (§10): the sweep report at the design's acceptance is the forward and reverse result; the arithmetic is the second-seat rebuild | Coordinator; Product Owner accepts exceptions | Every applicable obligation is satisfied or routed through §13 |
| **S8** | **Provisional freeze**, with no take-in of its own (the S9 take-in carries it) | Product Owner | A named commit. No NOT COVERED row open (§6.4). Every figure the design computes rebuilt by a second seat, matching (§14.1) |
| **S9** | `page-spec.md` and `acceptance-criteria.md`, consolidating S4–S7 decisions, and the gate scripts' output (§14) | Coordinator | Both complete, and C1–C3 pass |
| **S10** | **At the S9 take-in:** the three gate scripts' output read, and G11 read (§14); scrutiny if warranted → **check result**, and **one card** | Internal strategist | Product Owner accepts the package → **DECIDED** |

**This table applies from the Intermediate phase.** In Exploratory, §6.8 replaces it.

**The loop replaces S2–S5 and S7; the stage names are kept** so that records citing them still resolve.
When an external design model is used, the loop runs the same way with the model generating, and §5.7's
retained file and §9's assumption audit apply.

**Coverage gaps surface inside the loop, not after it.** The NOT COVERED sweep runs every round, so a gap
changes the screen while it is still moving; S6 then verifies the accepted design whole, arithmetic
included. A round that changes the design after S6 re-runs S6 before the freeze.

**The freeze at S8 is provisional until the package passes.** A contradiction found at S9 or S10
reopens only the affected decisions and produces a new artifact revision — not a new round, and not a
re-run of S2.

**S10 produces a check result, not an acceptance.** The package becomes DECIDED when the Product Owner
accepts the identified package revision, and that acceptance is recorded in the manifest.

### 6.1 Render check

**Every round is rendered before it is published**: desktop width and 360px, with no horizontal
overflow, measured board heights, and sticky and hover behaviour verified. A defect found is fixed before
publishing, not reported. It is the render-check script of §5.7, run every round. The canvas type renders
only when asked, so this needs the Product Owner's standing consent, recorded once per project.

### 6.2 Canvas hygiene

One canvas per package for the candidate. Explorations — alternatives, style schemes — go on
**separate** canvases, so an accepted candidate is never overwritten. The live version is read before
every publish; a save made from inside the page is merged, never forced.

### 6.3 The reconciliation list, kept per round

Where a project runs design-first — the design the Product Owner accepts is the authority for what the
user sees and does, and the requirements align to it after the freeze (Coach Platform DEC-013) — every
gap between the design and the specification is logged in the package's `coverage.md` (§7.2), in
three kinds: **CHANGED** (the design does it differently), **ADDED** (the design does something the
specification does not) and **NOT COVERED** (a specified requirement with no counterpart in the design).

**Updated every round, not at the end.** Each row carries its kind, the round that introduced it, and the
Product Owner's answer where he gave one. The manifest records the list's state at every visual
judgement. **An ADDED or CHANGED row that introduces or changes a computed figure** carries its
computation rule, and the figure is rebuilt by a second seat before the freeze (§14.1). **A removal or a
narrowing gets its own checkbox** on the alignment card, and a change that weakens a *shows / names /
says* requirement is a narrowing. Invariants are never on the list: they bind the design.

### 6.4 NOT COVERED rows

**Found by the sweep every round** (§5.7). **Shown at every visual judgement until answered, and answered
once.** An answered row is not shown again unless the design changes it. A row the Product Owner neither
covers nor removes gets **one** design round to cover it; if it still is not covered, it goes back to him
as keep-or-remove, and that answer is final. This bounds how often a frozen design can reopen.

### 6.5 What the Product Owner is told at every round

**The loop is a conversation between the Product Owner and the coordinator, in the coordinator's chat.
He says what he wants different; the coordinator makes the next round; they repeat until he is happy.**
Nothing in it goes through the tracker or another seat. The message that publishes a round says so in
those words, because on 2026-09-26 a round-1 message that asked him to *"name the element, the defect,
and what must not change"* and then to *"hand the rebuild request to the internal Product Strategist"*
read, reasonably, as *check the design against the specification and report discrepancies to another
seat* — the opposite of the loop — and it cost him an evening to find out.

Every round's message has this shape and no other:

1. **The first line, verbatim with the round number filled in:** *"Round N is ready. Tell me what you
   want changed — anything: layout, flow, wording, what is missing, what you dislike. I make round N+1
   from your notes, and we repeat until you are happy."*
2. **The links** to the published canvas, one per device form, and which form is primary.
3. **What changed since the last round**, in a few lines. Round 1 says what the design is based on.
4. **Decide**, only if a real product choice is open — at most three, each with what he would see under
   each option and a recommendation — and the **NOT COVERED rows** to answer (§6.4). Otherwise nothing.
5. **The last line, verbatim:** *"When a form is right, say 'accept phone' or 'accept desktop'. That
   ends the loop for that form."*

**What never appears in it:**
- **Work for another seat, or anything he must carry.** The rebuild request (§14.1), take-ins and
  records reach their seats without him: committed with the round, and put on the tracker by the
  operator or the host automation. They run alongside the rounds and gate only the freeze, so they are
  not his next step and never read as one.
- **A Handoff block** (`60-workspace-document-contract.md`). The loop's next action is always his notes.
  The Handoff block belongs to the deliveries that end a stage: S1 and S9.
- **The word *defect* for his notes, or any framing of them as a check against the specification.** His
  notes may overrule the specification: the design he accepts is the authority for what the user sees
  and does, and a difference is recorded on the reconciliation list, not refused (§13).

### 6.6 One pull request for the whole loop

**The loop runs on one draft pull request per package**, opened with round 1. Every later round is a
push to it: the canonical HTML at the package root, the round's `candidates/<round>/` folder, the
reconciliation list, the expected figures and any request under `requests/`. CI renders every push.

- **It merges once, at S9**, carrying the freeze, the specification and the gate result. Only then is it
  taken in on the tracker, and only then does the Product Owner get a card — one card for the package. **No round has a merge
  card**, and no round is taken in: a card per round asked him on the tracker for a judgement the loop
  already collects in the coordinator's chat (Coach Platform, WEE-287, 2026-09-26).
- **Findings from other seats go on that pull request**, for the coordinator to take into the next
  round. The second-seat rebuild (§14.1) reports there too.
- **Every request the coordinator makes of a tracker seat is a file under the package's `requests/`**:
  a rebuild, a card for the Product Owner, a record to land. The host automation opens one issue per new
  file for the internal Product Strategist, who posts any card itself. A request addressed to the
  operator, or left outside the package, is one the Product Owner ends up carrying.
- **The loop has no tracker issue, and nothing about it is assigned to the Product Owner.** A seat
  that must wait on the loop waits on the loop's pull request reaching S9, which opens the take-in by
  itself. It does not open an issue for his notes, and it never asks him to relay its
  findings to the coordinator: the pull request carries them (Coach Platform, WEE-289, 2026-09-26).
- **A round opened as a pull request of its own** is folded into the loop's pull request by the next
  round and closed, so that exactly one design pull request per package is open during the loop.
- **The manifest's `step:`** names the loop and the round (`loop — round 3`), then `S8 — freeze`, then `S9`. The
  host automation reads it to tell a round from a delivery that ends a stage.

### 6.7 S0 — the flow wireframe

**The flow is designed before the screens.** Once per product, or per release that adds screens or a
moment of use, the coordinator runs one package whose subject is the whole app at low fidelity: every
screen, and every moment of use as a path through them. The screen packages that follow fill in a
structure that is already accepted.

**Inputs.** The requirements' account of use — on Coach Platform the season operating model and the
coach's rhythm of use (`product-requirements.md` §2.2–2.3) and each job (§5–§12); the navigation model
(`design-intent.md` §2: destinations, the screen inventory with *reached from*, *Up* and device class,
and the rules of §2.4); every existing screen, built or designed. **A screen whose package is DECIDED or
whose design is accepted is a fixed node:** the flow routes to it and does not redesign it.

**The package** is `_docs/design/app-flow/` (or `app-flow-<release>`), with the §5 structure where it
applies and these artifacts:

| Artifact | Holds |
|---|---|
| `flow-map.md` | One row per moment of use: its steps, the screen of each step, the tap count, where the task returns, the device |
| `screens.md` | The screen inventory as designed: each screen, reached from, *Up*, device class, and which package owns its detail |
| The wireframe | A clickable low-fidelity HTML prototype at the package root, generated from a committed generator, one board per screen, phone and desktop where the device class says |
| `reconciliation-list.md` | Every difference from the navigation model and the requirements, CHANGED · ADDED · NOT COVERED (§6.3) |

**Fidelity is deliberately low.** Grey boxes, real labels, invented data. **No figures, no visual
values, no component appearance**: the figures are the screen packages', the visual values are the
baseline's (§12.2), components are the extraction pass's (§12.4). A wireframe that grows detail is a
screen package started early.

**The checks, every round** — the S0 counterpart of the render check and the sweep:
- every moment of use has a path, and every path ends where the navigation model says a task returns;
- the navigation rules hold on every path, counted rather than asserted (on Coach Platform: pitchside
  in at most two taps; a capture screen never navigates away on save; *Up* is the inventory's parent;
  a task started from *This week* returns to it);
- every screen is reachable, and none is an orphan.

**The loop is §6.5's, with the first and last lines adapted:** *"Flow round N is ready. Click through
it and tell me what you want changed — a path, a screen that is missing or in the wrong place, a step
too many. I make round N+1 from your notes, and we repeat until you are happy."* and *"When the flow is
right, say 'accept flow'. That ends S0."* One pull request for the whole loop (§6.6); its manifest
`step:` reads `S0 — round N`, then `S0 — accepted`.

**What the accepted flow is.** Where design leads (Coach Platform DEC-013), the accepted flow is the
authority for navigation and the screen inventory, and `design-intent.md` §2 is aligned to it at the
alignment pass, like any accepted design. **Every later screen package's S1 starts from its screen's
wireframe** and cites the accepted flow's revision in its manifest `sources`. A screen package that
finds its screen missing from the flow, or needs a path the flow does not have, runs one flow round
first rather than deciding the path inside a screen.

---

### 6.8 The exploratory prototype

In the **Exploratory** phase the design work is **one clickable HTML prototype of the whole product**,
built by the coordinator with the Product Owner in its chat. It replaces the per-screen stages S1–S10
for as long as the phase lasts.

| | |
|---|---|
| **What** | The accepted flow (S0) grown into every known view: each screen is a page, the navigation works, invented data shows each screen's states. Screens with a finished package join as pages as designed; drafts continue as pages; screens with no package start as pages from the flow |
| **Where** | Inside the flow package, generated from a committed generator like every package, on one draft pull request; published as a canvas every round, which the Product Owner can open on a phone |
| **The design system** | One token set, the shared components and the type, in `_docs/design/system/`, built during the phase (§12). Every page uses it, not its own copy |
| **Coverage** | `gaps.md` beside the prototype: requirements no page shows yet, and what the prototype does that the requirements do not. Nothing in it is carded; it feeds the alignment pass at the phase's end |
| **Rolling alignment** | **A `gaps.md` row the Product Owner settles in the coordinator's chat is marked at once** — *decided, round n*, with his answer in his words — in a status column the coordinator keeps. At the phase's end only the rows still open go to the Product Owner, batched; the decided rows are carried into the specification as recorded answers, without a card (on Coach Platform, DEC-002 class 3) |
| **Not run** | Per-screen `coverage.md` upkeep, S8 and S9, `page-spec.md` and `acceptance-criteria.md`, second-seat rebuilds, take-ins, and product amendments. Files under `requests/` only when the Product Owner asks for one |
| **Round message** | What changed, the canvas link, at most three questions — each about what the product does, never about a pixel. Reversible choices are the coordinator's own |
| **Exit** | The Product Owner moves the project to Intermediate. Then, once: the alignment pass for the whole prototype (DEC-013 clause 5 on Coach Platform), starting from `gaps.md` and carding only its open rows; then the prototype is taken in **once, as one package**, and each page's `page-spec.md` and `acceptance-criteria.md` are written from it as the build reaches that screen, checked by the gate (§14) then. One take-in for the prototype, not one per page (REPORT-013 R-44) |

## 7. S1 — the design space and the coverage table

### 7.1 The design space

```
FIXED              what the model must not change
OPEN FOR DESIGN    what it is being asked to decide
OUT OF SCOPE       what must not appear at all
```

**The declaration itself is checked.** The internal strategist reads the design space against the
accepted specification before S2 runs, and objects where something FIXED is not actually settled, or
where something OPEN is already decided elsewhere.

Round 3's design space was never put through this check. Fixing its structure was a legitimate choice —
§8 allows it — and the defect is that the declaration itself went unexamined, which is what carried a
position set the grid does not contain into three rounds of work.

### 7.2 The requirement coverage — `coverage.md`, the one requirement artifact

**One file holds what was two** (since 2026-09-29, proposal `2026-09-29_slim-design-gate.md`): the
coverage table and the reconciliation list of §6.3. Built at S1, kept current by the sweep every round,
read by the alignment pass for its CHANGED, NOT COVERED and ADDED rows.

| Requirement | Source doc, section, version **and commit** | Where it is visible | Verdict | Product Owner's answer |
|---|---|---|---|---|
| id | folded accepted specification | region id or named specimen | **satisfied** · **CHANGED** · **NOT COVERED** · **not applicable** (reason) | card and date, where he gave one |

Plus one **ADDED** row per thing the design does that the specification does not. A row that introduces
or changes a computed figure carries its rule, and the figure is rebuilt by a second seat (§14.1).

**The independent build happens here, at the S1 take-in:** the internal strategist builds the forward
coverage from the accepted specification, not from the brief, and compares (§14.1). After S1 the sweep
keeps it current; it is not rebuilt at S10.

**Built from the accepted specification, never from a previous brief.** The defect this closes is a
brief being checked against itself.

**No source, not a requirement.** A good idea without one has three dispositions, recorded in the brief:

1. **Drop it.** The default.
2. **Amendment now**, through the chain in §13. Blocks the round when it changes structure or a rule the
   screen must show.
3. **Amendment later**, and the item goes into OUT OF SCOPE by name.

An untraceable row with no disposition is a BLOCKER at S10.

---

## 8. Alternatives

**Cheap and on demand.** The coordinator offers alternatives as boards on one exploration canvas
(§6.2) whenever a question is open — layout, control design, visual language — not as a number generated
once. A page with an open structure and no precedent may start from several directions; a page reusing
an accepted archetype may start from one, with the reuse recorded. §15 entry may begin from an existing
candidate.

**They must differ in what the brief opened.** Where structure is open, they differ structurally; a
palette or a typeface is not a direction. Where structure is deliberately fixed and visual language is
open, they differ in visual language and the brief says so.

Each alternative states what it is best at, what it gives up, what it introduces, what it assumed, and
whether the stack can build it.

---

## 9. The assumption audit — external design model only

**When the coordinator generates, there is no audit**: the assumptions are its own, and each round's
`README.md` lists them (§5.7). Gaps against the specification go to the reconciliation list (§6.3). The
rest of this section applies when an external design model is used.

Every pass returns an assumption report. Each assumption gets one disposition: **ACCEPT** (promoted into
the brief as an explicit decision), **REJECT** (corrected in the next delta, with the reason),
**MODIFY**, or **IRRELEVANT**.

An accepted assumption that states a rule about what something *means* is not an assumption. It is an
amendment, and §13 routes it.

**Corrections are delta prompts** against the retained input of §5.7, and the returned difference is
validated.

### 9.1 Decisions are captured when made, and feasibility is asked early

Interactions, alternate states and layout rules are recorded **as they are decided**, from the design loop onward.
S9 consolidates them. S9 is not where they are discovered.

Where the accepted constraints do not settle feasibility — an interaction that may be expensive, a
layout that may not survive the stack — the coordinator asks the Architect for a **bounded feasibility
opinion before the design loop ends**, not after the freeze. The opinion is advisory; the Product Owner decides.

---

## 10. S6 — requirement coverage verification

**Since 2026-09-29 S6 is the loop's last sweep, not a separate pass.** The sweep report at the design's
acceptance is the forward and reverse result below, read from `coverage.md`; the arithmetic is the
second-seat rebuild the freeze already waits on (§14.1). What follows says what that result must show.

It answers two questions and no others: **is anything missing, and are the numbers right.**

**Forward — every obligation to a place on the screen:**

| Requirement | Source and commit | Where it is visible | Verdict |
|---|---|---|---|
| id | as §7.2 | region id or named specimen | satisfied · **partial** · **not satisfied** · not applicable |

**The verdicts bind.** An applicable accepted obligation must be **satisfied**, or changed or deferred
through §13's route. *Partial* and *not satisfied* both block; acknowledging a defect never waives a
requirement. *Not applicable* requires a reason and is accepted or rejected by the Product Owner.

**Arithmetic — every derived figure against `fixture-expected.md`.** Recomputed independently, before
generation, and compared to what the artifact renders. A coverage row saying *cover status is shown*
catches neither a wrong count of players owed a fixture nor a wrong number of distinct players behind an
aggregate. This check does.

**Reverse — every region to an obligation.** Every major region traces to a requirement, or is marked a
deliberate extra with a reason. This catches something being on screen only because the data exists.

**Presented as exceptions.** The Product Owner sees failures, not-applicable claims and unresolved
choices. Passing verdicts are recorded as visible evidence and are not walked through one by one.

---

## 11. Ending the design loop — the visual decision

Structure, colour, contrast, radius, borders, spacing rhythm, type scale, alignment, density, hover and
focus, overflow and narrow-width behaviour — all are open inside the loop.

**The Product Owner judges by eye.** No checklist substitutes for it. **His word ends the loop** (*"it is
a wrap"*): there is no count budget, and the round log in the manifest shows the cost. He may instead
pause the package; either is recorded against the artifact. **He accepts each device form separately** —
a desktop acceptance does not cover the phone.

The decision may be batched with package acceptance rather than becoming another separate exchange, but
**it must exist**. S8 cannot freeze a screen whose visual decision was never taken.

**His notes are his, in his words.** He is never asked to phrase them in a form. The coordinator turns a
note into a specific change — which element, what changes, what must stay — and asks back only when two
readings would change the screen differently, stating what each would change. A note as broad as *make
it cleaner* is answered with the two or three concrete readings, not refused.

**Every round is a delta** on the generator (§5.7), not a regeneration.

**S7 ends with the values named** — colour roles, spacing steps, radius, border widths, type scale,
density — as a short table. Those values are a **proposal to the Product Owner under `design-intent.md`
§5**, not a fact established by having been used. §12 says what happens to them.

**A visual edit can break a semantic property** without adding or removing anything: hiding an input
explanation, changing how a missing value reads, weakening a guarantee group. The per-round sweep and the
reconciliation list's narrowing rule (§6.3) exist for this, and S6 re-runs the arithmetic on the accepted
design.

---

## 12. The visual language and the design system

### 12.1 What is already decided, and by whom

`design-intent.md` §5 holds the visual language and is **deliberately empty of decisions**. It records
that layout, type scale, spacing scale, colour tokens and component appearance are the Product Owner's,
to be decided **after the design prototype has been run**, and recorded in that document.

Revision 1 of this process asserted a different timing — after page 1 is *implemented* — and called it
a decision. No such decision existed in the accepted record. It came from a conversation on 2026-09-21
and is carried here as **PROPOSED**, not as authority.

### 12.2 The proposal, stated as a proposal

**Page 1's S7 value table is submitted to the Product Owner as the provisional visual baseline**, with
an explicit scope: which pages it binds, and what would reopen it. If accepted, it is recorded in
`design-intent.md` §5 through that document's own route — not here, and not in a package.

This is the part that must not wait for implementation. A second screen designed before the baseline
exists will choose different values, and that is drift with no upside.

### 12.3 Components wait, and candidacy is not promotion

**No component is promoted from page 1.** A component becomes shared on its **second** use with the
same semantics — not on its first with a similar appearance, and not because it seems likely to recur.

A concept that looks reusable is recorded as **candidate** and stays page-local until a second use
establishes shared semantics, unless the Product Owner explicitly approves an exception and records why.

**In the Exploratory phase the design system is built directly** in `_docs/design/system/`, alongside
the prototype (§6.8), rather than extracted after a first implementation. §12.3's candidacy and §12.4's
extraction apply from Intermediate, to components the build reveals.

### 12.4 Extraction

After page 1 is implemented, the internal strategist opens an extraction pass over the component map and
the value table, classifying each element as page-specific, generic component, domain component, layout
primitive, interaction pattern, design token or design decision. Implementation is what reveals which
component decisions were real; it is not what reveals which colour was right.

### 12.5 One home per kind of decision

| Kind | Home |
|---|---|
| Product rules and figures | `product-requirements.md`, via the amendment chain |
| Design acceptance criteria, visual language, stack constraints | `design-intent.md` |
| Cross-cutting decisions | `decisions.md` |
| Screen-specific design | The page package |
| Reusable components and tokens | The design system, once it exists, versioned and named in every manifest |

A package references these. It never becomes a second home for any of them.

### 12.6 What a delivery hands the build

A design is finished when the build can take it as it stands, not when it reads well. Each rule below
comes from a defect the build paid for in one week (Coach Platform, 2026-10-02 → 03), and each applies to
every page a delivery adds or changes, the exploratory prototype included.

| # | Rule | The defect it prevents |
|---|---|---|
| 1 | **Page styles ship as files.** Every page-specific rule lives in a per-page stylesheet the build can pin by blob identity, beside the design system's tokens and components; none lives only inline in a page. | The prototype held about 2,000 page-scoped rules in 14 groups and the build had only tokens and components: a faithfully built This week rendered unstyled and cost a review round (WEE-564 `F1`). |
| 2 | **The copy is final.** Every string the user reads is the text that ships; a placeholder is marked as one. The build's text comparison holds the build to it. | Five strings differed between the built page and the design, caught only by a reviewer (WEE-564 `F5`–`F8`). |
| 3 | **One invented data set.** The design reads its invented records from one data file that the app's demo loader also reads, so a built page and its design show the same content. | The app's demo set had no training sessions, so a section the design showed could not appear on the host (Coach Platform F44). |
| 4 | **A form lists its fields** against the specification's field list for that record, and draws every field it names, or says which field the specification should lose. | A form page drew neither of two fields the specification required; the coverage table had checked regions, not fields (WEE-546). |
| 5 | **Every action has an exit.** An action that can leave the page or a pending change incomplete (a chain with a gap, an empty list, a refused save) has a drawn way out. | A substitution chain with a player off and nobody on could not be applied or kept, only discarded (WEE-555). |

Rules 4 and 5 apply to pages added or changed after 2026-10-03; a frozen prototype is not reopened for
them. The page's manifest records each rule as met, with the file or the field table that shows it.

---

## 13. When a design round produces a product change

**Revision 1's test was wrong.** It said that anything changing what the user sees or does belongs to
the package. But `design-intent.md` §§2–4 governs navigation, saves, failures and device forms — all of
them things the user sees and does — and an accepted amendment has already changed a screen-to-screen
route through the product chain.

**The test:**

> **Does the choice *elaborate* accepted intent, or *change* it?**
> Elaborating unspecified presentation is the package's. Changing accepted intent — including workflow,
> acceptance criteria, scope, and any rule about what a figure means — goes through the amendment chain.

Worked examples:

| | |
|---|---|
| A tiebreak when two players compute to the same priority, where no rule exists | **Changes** — amendment |
| A count of distinct players behind an aggregate cover reading — a new derived figure | **Changes** — amendment |
| Which set of positions the cover check runs over | **Changes** — amendment |
| Adding or retargeting a route between screens | **Changes** — amendment, and one already has |
| Merging two columns that render the identical number; renaming a column; moving the sort key beside the name; enlarging the control used weekly | **Elaborates** — package |
| Making visible that a player's priority rests on attendance alone, where the rescaling rule already exists | **Elaborates** — package |

### 13.1 Three levels of authority, kept apart

A merged amendment is **not** authority. The chain is: a draft amendment, then Product Owner approval,
then the fold-in that produces an accepted specification revision. **Only the folded accepted
specification is citable by a coverage table**, and implementation waits for it.

The amendment's pull request is opened as a **draft** pull request and stays one until the board has
decided and the answers are written back into the amendment. The document's `Status:` field and the pull
request's draft state say the same thing, and the draft state is the one a tool and a person can both
read without opening the file.

### 13.2 The guard

The coordinator both runs the design round and drafts any amendment it produces.

- **The amendment stands on product reasoning alone.** *"The design needs it"* is not a reason.
- **The Product Advisor reviews any amendment originating inside a design round**, with the accepted
  sources, the original assumptions, the alternatives and the incremental scope in hand, and may reject
  the premise. Reviewing the author's stated motivation is not enough; the review examines the diff and
  the added scope.
- **The existing independent review of a load-bearing specification revision is preserved.** Approving
  an amendment does not establish that the fold-in was faithful — a previous fold-in omitted two rows
  from a figure table and left an incoherent calculation, and the revision review is what caught it.

### 13.3 What each review reads

A package grows across its rounds. The S1 selection package reached roughly three thousand lines, and
it was read in full four times, once per review, at a cost that rose with every round.

**The first review of a package and the last one before the gate read it whole.** Everything between
them reads the diff since the previous review, plus every document that diff reaches — a figure table
the diff changes is read with the text that cites it, and an amendment is read with the accepted
section it would change.

The reason for the two full reads is the failure a diff cannot show: an inconsistency between two
documents where only one of them changed. The first full read establishes that the package is
coherent; the last one establishes that it still is after everything the rounds did to it. A middle
review that suspects it has stopped being coherent says so and reads whole — **a reviewer is never
refused the full package**, and the scope here is a default, not a permission.

**A review states which of the two it did**, so a later reader knows what was looked at. A review
that read a diff and does not say so reads like a full review and is not one.

---

## 14. S10 — the gate

**Three scripts and one reading** (since 2026-09-29, proposal `2026-09-29_slim-design-gate.md`). The
scripts live once, in this repository's `tools/design_gate/`, and run at S9; the S9 take-in reads their
output and does G11. G1–G11 keep their meaning, and each is assigned to the check that carries it:

| | Check | Carried by |
|---|---|---|
| **G1** | Purpose, primary tasks and non-goals are stated | **C1 — structure** (script) |
| **G2** | The artifact is identified and recoverable: named viewport, named fixture, named commit | **C1** |
| **G3** | Every region maps to a named component with a category | **C1** |
| **G4** | Every interactive component has behaviour, including keyboard and cancel | **C1** |
| **G5** | Every applicable alternate state is inspectable through a named specimen or reproducible interaction; every inapplicable class is marked so with a reason | **C1** |
| **G6** | Layout is stated as rules, including the width at which the layout changes, and every device form an accepted criterion requires is present | **C2 — render** (the existing render check) |
| **G7** | Accessibility is demonstrated, not asserted: keyboard reach and visible focus inspected in the rendered artifact, and no meaning carried by colour alone | **C2** |
| **G8** | Every acceptance criterion points at a region, a specimen, or a rule that exists | **C1** |
| **G9** | Every applicable accepted obligation is **satisfied**, or changed or deferred through §13. Every region traces to an obligation or an accepted deliberate extra | **C3 — coverage** (script over `coverage.md`) |
| **G10** | Every coverage row cites a **folded accepted specification** at a named commit. A draft or merely-merged amendment is not authority | **C3** |
| **G11** | **The decisive check.** Do the rendered states and the fixture results satisfy the applicable accepted rules, with no unresolved contradiction and no required behaviour left for an implementer to invent? Evidence linked to the exact artifact revision | **Read by a seat** at the S9 take-in — the one check no script can do |

A script that cannot decide a row reports it as unresolved, and an unresolved row is read at G11, not
passed.

### 14.1 The check is independent

At the **S1 take-in** (moved from S10 on 2026-09-29), the internal strategist builds the forward coverage **from the accepted specification**, not from
the brief's copy of it, and compares. This catches a brief whose requirement list was stale when it was
written. The round-2 brief was checked this way once, by hand, and the check found 26 things; the
round-3 brief was not, and that is the difference this step removes.

**Independently twice, and a third time only on disagreement.** A derived figure in a fixture is
rebuilt from the accepted specification by a second seat that has not read the first seat's working.
That second rebuild earns its cost: on the S1 selection package it found that an answer about
precision moved three figures and created a tie group nobody had noticed. A **third** rebuild of
figures two independent seats already agree on confirms what is settled and finds nothing — it
happened on the same package, is recorded in the package's own words as *"three calculators written
by three seats now agree"*, and it produced no finding.

So: rebuild independently **twice**. Where the two disagree, a third rebuild settles which is right,
and the disagreement is recorded with it. Where they agree, the agreement is the evidence and the
round moves on. This does not weaken the rule above — the first rebuild still comes from the
accepted specification rather than from the brief, which is what the check is for.

**Load-bearing when the coordinator generates.** The coordinator both builds and designs, so **every
figure it computes for a design is rebuilt by a second seat before the S8 freeze**. The visual stays the
Product Owner's eye. On the first package run this way there were three such figures: a figure extended
to players the specification had not covered, an order per view, and a best position per fixture.

**The rebuild request.** The coordinator writes it as soon as a computed row lands on the reconciliation
list (§6.3): one committed prompt per batch, addressed to the second seat (the internal Product
Strategist unless the project names another). It carries the rule as the Product Owner decided it, the
views to rebuild, the instruction to rebuild **before** reading the design's figures, and where the result
goes — the package's expected-figures file, one commit, one comment on the package pull request. **It
reaches the second seat without the Product Owner:** the coordinator commits it under the package's
`requests/` with the round, and the operator — or the host automation, where it opens tracker issues from
package pull requests — puts it on the tracker; the coordinator has no tracker seat. It is never listed as
his action (§6.5). The rebuild runs
alongside the rounds, **the freeze waits on it**, and a round that changes a rebuilt figure gets a new
request. **On a mismatch** the second seat changes neither design nor specification: the coordinator
corrects the design, or takes the rule to the Product Owner.

### 14.2 Severity

| | |
|---|---|
| **BLOCKER** | An implementer would have to guess design intent, or an accepted obligation is unsatisfied |
| **MAJOR** | Important behaviour, data or state is unclear |
| **MINOR** | Limited ambiguity with low impact |

### 14.3 What passing produces

A **check result**, recorded against the package revision and the source commits it was checked against.
The Product Owner then accepts the package, and that acceptance is what makes it DECIDED.

The accepted package is linked into the Architect's implementation instruction, and into the existing
delivered-screen visual checks. **It does not create a second release gate**; the implementation review
and milestone visual checks already in governance remain the acceptance of the built screen. A prototype
gate never stands in for a delivered-screen check.

### 14.4 Scrutiny

The internal strategist orders an implementation-readiness review from the Product Advisor when the page
is large, contested, or the first of its archetype. The reviewer is told: **do not redesign**. It reports
contradictions, ambiguity, missing interactions, missing states, missing data, unclear component
boundaries, untestable criteria, and any place an implementer would have to invent behaviour.

### 14.5 How the delivered-screen checks bind to the package

No second gate is added; the checks that already accept a built screen are made to check **it against
the package** rather than against a paraphrase of it. Without this, the implementation instruction can
restate the criteria in its own words, the screenshots can show whatever data the build happened to have,
and the whole comparison rests on the Product Owner's eye in one batched pass — which is the one check
that cannot tell a figure computed wrongly from a figure computed right.

**The criteria are transcribed, not re-authored.** The Architect's implementation instruction carries
the package's `acceptance-criteria.md` as its `human-visual` criteria, quoted with the package revision
they came from. A criterion the Architect believes is wrong goes back through §13, not into a rewording.

**The arithmetic is checked by a machine.** `fixture-expected.md` holds the exact figure for every cell
of the pinned fixture, computed before generation and rebuilt independently at S10. The built screen,
loaded with the package's `fixture.json`, must show every one of those figures — each cover status and
depth, each versatility and breadth ratio, each priority and tie group. That is an **automated** test
the Implementor writes and CI runs; no human is needed to find a number that is wrong, and no human can
be relied on to find one in a dense screen. A figure that differs is a defect, not a judgement.

**The screenshots are comparable.** `human-visual` evidence for a packaged screen is taken with the
pinned fixture loaded, at the package's pinned viewport, and set beside the frozen S8 artifact at its
named commit. A screenshot of different data at a different size cannot be compared with anything.

**A difference routes by what it changes:**

| The built screen differs in | Goes to |
|---|---|
| What a figure means, or which rule computes it | §13 — it is a product change, and the package or the specification moves first |
| A figure's value, with the rule unchanged | The Architect, as a defect. The automated test above fails on it |
| Layout, spacing, emphasis, density | The Product Owner, by eye, the same owner as S7 |
| Something the package did not specify | The Product Owner — the package had a gap, and S9 should have caught it; recorded as `rework`, origin `design_drift` |

**The checker is not the builder.** Whoever judges the built screen against the package gets the package
and the built screen, not the implementer's account of what it did. The same seat that built it
confirming it matches is the check the process already has, and it is the weakest one.

---

## 15. Mid-project entry

**The internal strategist asks the Product Owner for a package for any screen named in the accepted
requirements that is not yet implemented.** The first such screen becomes page 1. Its brief is written
retrospectively from the accepted requirements and design intent, and an existing design artifact may
enter the design loop as its first round, recorded as a candidate, rather than being discarded —
which is the §15 path §8 explicitly allows.

**Screens already implemented are left alone until they are next changed — but their outstanding
obligations remain.** Recorded device-form and criterion obligations against existing screens are not
cancelled by this process and stay on the register where they already live.

---

## 16. After implementation starts

| | | |
|---|---|---|
| **Design defect** | The approved design behaves poorly or contradicts itself | Returns to the coordinator |
| **Implementation constraint** | Technical reality makes the design infeasible or disproportionately expensive | The Product Owner decides whether the design changes |
| **New product requirement** | — | The amendment chain, then a new design pass if the screen changes |
| **Implementation defect** | The implementation does not match the package | Fix the implementation, no redesign |

**A correction invalidates named things.** Any of these records which package revision, which evidence
and which acceptance it invalidates, and only the affected evidence is rechecked.

---

## 17. Failure modes this process exists to prevent

| | |
|---|---|
| **An unexamined design space** | Round 3's declaration was never checked against the specification. Fixing the structure was allowed; not checking that decision was the defect |
| **A control that depends on remembering** | The round-2 brief was checked against the specification and 26 findings came back. The round-3 brief was not, and a position set the grid does not contain went through. The render check and the NOT COVERED sweep are scripts for this reason (§5.7) |
| **A requirement lost by attrition** | A design that evolves round by round drops a requirement nobody is looking at. The first package run design-first found two only when the sweep ran before the freeze |
| **A hand-off loop** | A prompt pasted into a design tool, files dropped back, and the wrong attachment named. The coordinator generates the design itself (§3) |
| **Coverage that counts presence, not correctness** | A wrong count of players owed a fixture passes a list of cited requirements |
| **Correctness standing in for quality** | Reviews that only ask whether a rule is carried |
| **Everything in one pass** | Too many simultaneous degrees of freedom; product assumptions hide inside generated output |
| **Screenshot-only handoff** | An image cannot specify states, transitions, reflow or semantics |
| **Repeated full regeneration** | Fixing one region by replacing the whole page |
| **Silent assumptions** | Every pass reports them, or the pass is not finished |
| **A version string as an identity** | A document's content changing while its version does not |
| **Unbounded human verification** | The only human becomes the reconciliation service, and rubber-stamps |
| **Per-page design systems** | A second card, a second spacing scale, a second button hierarchy |
| **Premature universalisation** | A component library built from one page |
| **Implementation agents deciding UX** | If they are deciding, the package is underspecified |

---

**Provenance**

Reduced from two UX operating documents supplied by a Product Owner's UX advisor on 2026-09-21, to
roughly a tenth of their combined length. Reviewed independently twice on the same day: the first pass
returned *do not adopt as written* with four blockers, the second returned *adopt with named fixes* with
no blocker. Both sets of findings are folded in. The draft and both review reports are retained in the
originating project's workspace.

Its worked examples come from that project's weekly selection screen, and are examples rather than
rules.

**Amended 2026-09-25**: the coordinator generates the design, the loop replaces S2–S5 and S7, and the
render check, canvas hygiene, the per-round reconciliation list, the NOT COVERED rules and the rebuild
request are added. From the selection package's rounds 4–20 on Coach Platform, the design coordinator's
review of its DEC-013 (REPORT-008) and the process review REPORT-009 (R-4, R-5). The approved proposal is
retained as `proposals/2026-09-25_design-coordinator-generates.md`.

**End of message**
