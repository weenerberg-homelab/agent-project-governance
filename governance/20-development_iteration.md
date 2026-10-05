## Development iteration

This file defines execution-loop order only.

Role authority, ownership, escalation boundaries, and handoff schema are defined in:
- `_docs/shared/governance/10-agents_workflow.md`

### Human-in-the-loop rule
- Agents establish the intended outcome and material constraints with the User.
- Once the User requests or approves implementation, agents may implement,
  validate, and commit coherent in-scope work without repeating approval
  requests.
- Explicit approval is required for destructive/irreversible execution,
  security-sensitive actions, removing working fallback, or enabling new
  physical-control behaviour by default.

### Canonical artifacts (authoritative order)
1. `_docs/specs/.../10-product/10-product-spec.md`
2. `_docs/specs/.../10-product/20-invariant.spec.md`
3. `_docs/specs/.../20-architect/to_implementor/30-architecture-spec.md`
4. `_docs/specs/.../10-product/40-implementation-roadmap.md`

### Iteration loop
1. Define the desired behaviour and meaningful boundaries.
2. Implement the smallest coherent increment.
3. Validate in proportion to its actual consequence.
4. Review rigorously for concrete defects and hidden assumptions.
5. Correct problems or move to the next useful outcome.

Detailed mandatory/optional mappings and exact evidence contracts are useful
for high-consequence operational work. Do not require them for routine,
reversible, disabled-by-default, diagnostic, or presentation changes.

### Review rule
Architecture review must remain demanding even when implementation proceeds
quickly. Findings must identify an actual correctness, safety, data-quality,
observability, or maintainability problem and the smallest useful correction.

For gate-bearing reviews, assess the governing criteria and evidence first and
record a preliminary disposition before reading any optional Implementor
self-assessment. A self-assessment is not evidence and must not determine or
support the review outcome.

### Primary blocker rule
If a primary operational blocker exists, state it plainly. Other useful work
may still proceed when it is independent and does not obscure the blocker.

### Native-run rule for migrated paths
For actively controlling or recreate-critical migrated paths, tests alone are
not sufficient for claiming operational readiness.

At least one real governed writable-target run is required before claiming operational readiness of the migrated path.

### Prompt delta rule
Avoid repeating unchanged context. Report new behaviour, concrete findings,
validation, and the next decision only.

## Product delivery order

A product version goes from idea to release in eight steps, run inside the development phases below.
Each step names its output; nothing is written in detail before the step that settles it, and each fact
is written once, in the artifact that owns it.

| # | Phase | Step | Who | Output |
|---|---|---|---|---|
| 1 | Exploratory | **Exploration** | Product Owner with the External Product Strategist | The **product brief**: vision, philosophy, users, the version's scope and features, the rules and invariants the product must keep. It is the draft of the specification, without screen behaviour |
| 2 | Exploratory | **Feasibility of the risks** | Architect | One opinion on what could make the brief infeasible or expensive: the data model's shape, integrations, scale, commercial constraints. No architecture and no review rounds |
| 3 | Exploratory | **Prototype and design** | Design coordinator with the Product Owner | The clickable prototype and design system (`90-design-delivery.md`), and `gaps.md`: the rules the drawings raise and do not settle |
| 4 | Exploratory → Intermediate | **The full product specification** | Internal Product Strategist; one Product Advisor review; the Product Owner accepts | The brief, the prototype and the `gaps.md` answers folded into one specification: every requirement, rule, figure, invariant and acceptance criterion, with screens referred to the accepted design rather than restated. This is the boundary's alignment pass. Each page's package and criteria are completed as the build reaches it |
| 5 | Intermediate | **Architecture and the build plan** | Architect; one Architecture Advisor review; the Product Owner releases it | Architecture, data model, API and page contracts derived from the specification and the design, and the milestone set with a budget per milestone (`70-review-and-release.md`, *What a milestone budget holds*) |
| 6 | Intermediate | **Implementation** | Implementors in increments; the Architect reviews; the Operator deploys | Code behind the mechanical gates (`70-review-and-release.md`, *Reviews, rework and acceptance*) |
| 7 | Intermediate | **The Product Owner's test** | Product Owner, with the Product Assistant's acceptance evidence | A hand test at each product milestone, from a test script and the known-differences list. Findings return as amendments to step 3 (the design) or step 4 (the specification), never as another review round |
| 8 | Finalization | **Release** | All seats; the Product Owner accepts | The non-functional requirements, the strict checks, real data, and his extensive test of the major release |

The next version starts again at step 1 with its own brief, which carries forward what the released
version settled.

**Why this order** (decided 2026-10-05, `A281`, from the Coach Platform trial). There, a full
specification written before the design described screens the design then changed: every difference
cost an alignment pass, a fold-in, an independent review of each, and a card. Review rounds on a
specification the design later rewrites are paid for twice, and architecture drafted before the design is
written again after it. So the brief holds only what the design cannot settle, the full specification is
written once the prototype has converged, and the architecture is written once, from both.

A project already past step 4 finishes its current version on the order it started with; this order
applies from its next version's exploration.

## Development phases

A project runs in one of three phases. The phase sets how much rigour every seat applies. This section is
the one home of the phase rules; other documents refer to it. Adopted on 2026-09-30
(`proposals/2026-09-30_development-phases.md`, PH-Q1 to PH-Q3).

### The switch
- **One line in the project's decision record**, set only by the Product Owner: *"Phase: Exploratory,
  from <date>."* On Coach Platform it is DEC-014 in `_docs/decisions.md`.
- **Each seat is given only the current phase's column** in its instructions (the project's bundle
  builder and the coordinator template). No seat decides which phase applies.
- **A phase change** is the Product Owner's line, then a rebuild of the seat instructions.

### What each phase means

| | **Exploratory** | **Intermediate** | **Finalization** |
|---|---|---|---|
| **Goal** | See the whole product, learn what it should be | Build it, and let it converge | Release quality |
| **What is built** | **A clickable HTML prototype**: every known view, the design system, the navigation of the accepted flow, invented data. **No new screens in the app** | The app, screen by screen, from the converged prototype | The app, finished |
| **Who does the work** | The design coordinator with the Product Owner, outside the tracker. Tracker seats keep the deployed app running (defects only) | Tracker seats | Tracker seats |
| **Fidelity** | Rough is fine. It converges round by round | A built screen follows its prototype page; an image check with a tolerance | Pixel-perfect; a strict image check |
| **Requirement coverage** | One `gaps.md` for the whole prototype | Per screen, the design gate (`90-design-delivery.md` §14) | The full gate, and the second-seat rebuild of every figure |
| **Non-functional requirements** | Only what protects data and security in the deployed app | Plus phone width, keyboard reach, visible focus | All: performance, offline, full accessibility |
| **Tests** | None for the prototype. The deployed app's suite stays green | The logic that computes figures, and the criteria per state | Every criterion, and conformance |
| **Reviews** | None for the prototype. The Product Owner judges by clicking | One round normally; a record-only defect rides the next commit | Strict: a record-only defect fails the round |
| **Cards to the Product Owner** | Almost none. The coordinator asks in its chat | Money above a ceiling, data, undecided scope, against one of his answers, and the approvals the project's routing decision gives him. Each decision its own question, the recommendation first. Never a design-answered difference, a record-only correction, a small reversible choice, or a routine deploy under a standing approval (`70-review-and-release.md`, *Board cards*) | Every gate |
| **Deploy** | The prototype is published every round. The app: fixes only | Any time he says, with a demo data set | Real data, no reset |

**In every phase:** no loss of real data, no secret exposed, the deployed app's CI green, and a figure the
product computes is never shown wrong without a test saying so.

**Reversible choices in Exploratory and Intermediate are the seat's own.** A choice that a later round or
increment can undo for little cost — appearance a finished design does not settle, wording, test scope
inside an increment, order of work, names, record-keeping — the seat makes, records in one line in its
pull request, and moves on.

### Moving between phases

| Transition | When | What happens once, at the boundary |
|---|---|---|
| **Exploratory → Intermediate** | The Product Owner says so, when he has seen the system as a whole | One alignment pass for the whole prototype, carding only the `gaps.md` rows not already decided (`90-design-delivery.md` §6.8, *Rolling alignment*); one take-in for the prototype as a whole; each page's specification and criteria are written as the build reaches it; the Architect plans the build |
| **Intermediate → Finalization** | He says so, before real use | The outstanding non-functional requirements are listed and planned; the image check turns strict; the demo data reset stops |
| **Back** | He may move back a phase at any time | The phase's rules apply from then on; nothing built is undone |
