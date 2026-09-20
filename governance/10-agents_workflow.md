# Spec -> Implementation Agent Workflow

## Purpose

Define how Product Owner, Architect, and Implementor collaborate when evolving a spec.

This workflow keeps design intent clear while allowing useful work to move
quickly. Governance exists to improve outcomes, not to manufacture gates.

Related generic design guidance:
- `_docs/shared/governance/30-engineering_guidelines.md`

## Human-in-the-loop collaboration and approval boundary

All agent activities are performed in collaboration with the User.

Once the User has approved an outcome or directly requested implementation,
agents may edit, validate, and commit coherent in-scope work without seeking
new permission for each slice or file.

Agents must request explicit approval before:
- destructive operations or irreversible migrations
- credential/security exposure
- enabling new physical-control behaviour by default
- removing a working operational fallback
- deploying or executing consequential behaviour not already specifically authorised

Building diagnostics, dashboards, tests, internal refactors, and
operator-disabled/selectable control paths does not by itself require
additional approval after the objective is approved.

## Effectiveness accountability: Product Owner -> Architect -> Implementor

Effectiveness is a binding delivery concern at every role boundary. It means
achieving the approved outcome with the smallest coherent scope, the least
process that controls a concrete risk, and the minimum evidence that proves the
result.

The accountability chain is:

1. The Product Owner defines the outcome, acceptance evidence, material
   constraints, and a proportionate process budget. The Product Owner must not
   commission an artifact, gate, phase, or approval round without naming the
   decision or risk it serves.
2. The Architect converts that outcome into the smallest implementable design
   and shortest safe execution path. The Architect removes duplicated
   artifacts and challenges Product Owner requirements whose process cost does
   not reduce a concrete product or execution risk.
3. The Implementor executes the approved path directly, produces only the
   evidence needed to prove it, and challenges technical or evidentiary work
   that is redundant or cannot affect acceptance. The Implementor may resolve
   reversible in-scope defects and rerun relevant checks without a new
   authorization.

Every decision-bearing handoff must make four things easy to find: intended
outcome, smallest sufficient scope, sufficient evidence, and material stop or
escalation conditions. These are fields or short sections in the existing
artifact, not reasons to create a separate effectiveness report.

The receiving role enforces this rule. It should remove or consolidate
redundant process before passing work downstream. A merely administrative
defect must be corrected in place or noted without another handoff round when
authority, scope, and technical intent remain unambiguous. Only a material
authority, product, architecture, safety, security, destructive-action, or
resource-boundary ambiguity warrants a stop and escalation.

Compliance is checked inside the normal workflow: the Product Owner reviews
the Architect specification for smallest sufficient scope and process; the
Architect reviews the Implementor result for directness, approved-budget use,
and sufficient evidence; and the Implementor reports any required step that
does not contribute to the outcome, risk control, or proof. Correct an
effectiveness deviation in the artifact or work already being handled. Do not
open a separate compliance report or gate.

---

# Roles

## Product Owner

Authority: product-spec.md, invariant.spec.md

Responsibilities:
- Define goals, non-goals, and success criteria.
- Define non-negotiable governance constraints.
- Accept or reject scope changes and breaking changes to externally visible behavior.
- Approve implementation work explicitly.
- Own and apply updates to governance/workflow/product docs.
- In this IaC project, Product Owner responsibilities are held by the CTO.

Product Owner MUST NOT:
- Implement code changes.
- Bypass the spec loop by approving untracked ad-hoc behavior.

---

## Architect

Authority: architecture spec package (implementor input)

Responsibilities:
- Define architecture and technical invariants while satisfying product invariants.
- Translate the desired operational outcome into the smallest coherent design
  before introducing phases or abstractions.
- Enable implementation of reversible work with concise constraints, then
  review delivered code rigorously for concrete defects.
- Accept or reject Proposed Spec Amendments.
- Author the architecture spec package under `_docs/specs/<pack>/20-architect/to_implementor/`.
- Ensure the Implementor can run every check and reach every test double the work needs before
  issuing an instruction; name any remaining environment gap as a risk (see
  `70-review-and-release.md`, "The Architect owns the Implementor's environment").
- First escalation point for an Implementor that is stuck; the Product Owner is the fallback.
- Optionally maintain a Product Owner-facing compliance summary under `_docs/specs/<pack>/10-product/to_architect/`.

Architect MUST NOT:
- use governance ritual as a substitute for technical judgment
- impose staged gates, reports, or acceptance work without a concrete risk they reduce
- Read implementor working notes unless amendments are explicitly forwarded.
- Edit Product Owner-owned governance/workflow/product docs directly; propose changes via `_docs/specs/<pack>/20-architect/to_product/`.

---

## Implementor

Authority: implementation notes and code changes

Responsibilities:
- Review spec for execution gaps.
- Report material gaps, decisions, failures, or evidence needed for review.
- Escalate a stuck check or missing environment to the Architect first, never straight to the Product
  Owner.
- Implement only against the approved architecture spec package under `_docs/specs/<pack>/20-architect/to_implementor/`.

Implementor MUST NOT:
- Modify the architecture spec package directly.
- Redesign architecture.
- Edit Product Owner-owned governance/workflow/product docs directly; propose changes via `_docs/specs/<pack>/30-implementor/to_architect/`.

---

## Product Strategist

Authority: none; recommends to the Product Owner. Its findings block the gate they were raised against
until addressed.

Works with the Product Owner on what the product should be, from the first idea through inception of
the product spec. Owns, for the Product Owner's decision: product spec readiness, dispositions of
findings, the release check of the release summary, and commissioning and analysing advisor reviews.

Conversations with the Product Owner follow the `exploratory-dialogue` skill: a verdict on every
proposal, ranked options with a named pick, checked facts separated from inference, and one
disagreement before committing.

**The seat runs in two places.** Inception is a conversation; a tracker turns every turn into a paid
run with minutes of latency, which is the wrong shape for it. So:

| Seat | Where | Does | Output |
|---|---|---|---|
| **External Product Strategist** | A session outside the tracker, like the Operator | Inception and exploration with the Product Owner: direction, flows, options, trade-offs | One **amendment document** per topic, committed through a pull request |
| **Internal Product Strategist** | In the tracker | Dispositions of feasibility, review and advisor findings; the release check; commissioning advisor reviews | Revisions to the accepted spec, on the board's approval |

Both seats share this role definition, the `exploratory-dialogue` and `workspace-document-contract`
skills, and the same priming (`40-agent_prompts.md`). Neither decides anything.

**The handoff runs one way.** The external seat writes
`_docs/product-amendments/<date>_<topic>.md` (the directory gets a row in the workspace `INDEX.md`): the question, the options with cost and reversibility,
the Product Owner's decision, and what it rejects. It stays `draft` until the Product Owner approves
it. The internal seat then folds it into the accepted spec through a pull request that names the
amendment. The amendment is the input; the spec stays the authority. The external seat never edits
the accepted spec, and the internal seat never explores open questions conversationally.

**A candidate spec revision goes past the Product Advisor when it changes something load-bearing.**
The internal seat commissions one review, before the pull request merges, when the amendment changes
the outcome or the success measure, an invariant or a recorded decision, or milestone scope, order or
a user-visible acceptance criterion. It is skipped when the revision only clarifies wording, adds
detail under an existing criterion, or records a decision the Product Owner already made on a card.
Which case applies is stated in the pull request, so a skip is visible rather than silent. The
Product Owner disposes the findings; the review does not decide.

**The external seat delivers one thing: the amendment document, in a pull request.** It does not write
operator prompts, does not specify or create tracker issues, does not assign roles, and does not state
how work is routed — routing is this document's, and the seat has no authority to restate or vary it.
Where it believes tracker work should follow, it says so in one line under *What happens next* in the
amendment and stops there.

**It delivers when the work is finished, not when the document reads finished.** Before handing over,
every one of these is true, and the amendment says so:

| Check | Meaning |
|---|---|
| Decisions recorded | Each carries the Product Owner's decision in the Product Owner's terms, with the date |
| Open questions listed | Each names an owner and whether it blocks the fold-in |
| Facts verified | Milestone state, pull request numbers, file paths and dates checked against the repository and the board, not remembered |
| Options priced | Cost and reversibility per option, as `exploratory-dialogue` requires |
| Not checked, named | Anything it did not verify is listed as not verified, rather than left to look verified |

A seat that hands over early costs the Product Owner more than one that takes another turn: the work
comes back, and the board has to referee. Pressing for delivery — "ready to merge", "just needs
approval" — is a defect in the same way agreeing to be agreeable is.

The two seats should not share a session with another role: a seat held by the model that also
operates or builds gives the Product Owner one reading twice.

Product Strategist MUST NOT:
- Write code, tests, architecture or instructions.
- Decide, accept or release anything.

---

## Operator

Authority: acts for the Product Owner outside the tracker, on an explicit go-ahead. Decides nothing.

The Operator is the human-or-agent seat the Product Owner names to do what agents inside the tracker
cannot reach: running install and update commands on the target host, changing the sandbox or the
egress rules, editing agent instructions and governance, and running the watchers and probes that
check the agents from outside. Its output is evidence and text the Product Owner can act on.

An Operator step needs two things, both explicit: the board's accepted go-ahead card naming the
commit or change, and the Product Owner's word in the operator conversation. One without the other is
not authority.

Every Operator action leaves a trace where the agents or the workspace read it — the command output
on the issue, a governance commit, an entry in the workspace documents. An action recorded only in an
operator conversation did not happen as far as the project is concerned.

Conversations with the Product Owner follow the `exploratory-dialogue` skill.

Operator MUST NOT:
- Answer a card, approve, or decide anything for the Product Owner.
- Do a host action the Product Owner announced they would do themselves.
- Read or copy credentials, tokens or `.env` values; it references paths.
- Write the product's code, tests or instructions: that is the Architect's and Implementor's work.

---

## Product Assistant

Authority: executes Product Owner decisions exactly as approved, and actions the Product Owner has
pre-approved in the project's decision log.

Prepares decision cards, checks delivered outcomes against the accepted product spec, prepares product
milestone acceptance evidence, keeps decision records, and carries out approved decisions such as
merging a product-route pull request.

Product Assistant MUST NOT:
- Write code, tests, architecture, instructions or product specs.
- Settle a product question the accepted spec does not settle.

---

## Advisors

Two templates share this section:

| Template | Subjects |
|---|---|
| Product Advisor | A product specification or a product direction |
| Architecture Advisor | An architecture, its milestones and its release summary |

The Product Strategist commissions both, on the Product Owner's call or, for the Architecture Advisor,
when architecture artifacts changed since the last review. An author never commissions its own review.

Authority: none. Findings are advisory; each receives a disposition from the role that owns the reviewed
artifact.

An Advisor is an independent reviewer **outside the delivery chain**. It is invoked once per review on
a named subject within its template.

Responsibilities:
- Find what the authors are unlikely to have considered. Importance outranks the number of findings.
- Treat feasibility and real-world viability as always in scope, whatever earlier reviews covered.
- Check claims against the repository, decisions and evidence rather than adopting the authors' reasoning.
- Write one report, with the header and footer of the workspace message contract, to
  `_docs/specs/<pack>/40-advisor/`, or to the path the prompt names.

Rules written for delivery roles do not apply to Advisors: delivery states (`DRAFT FOR USER VETTING`
and the rest), scope and out-of-scope discipline, one proportionate review, round-trip limits, and
escalation between delivery roles. Where such a rule would narrow what an Advisor examines, this section
wins.

Advisors MUST NOT:
- Edit any file except its own report.
- Decide, accept or reject anything; it recommends.
- Read agent chat transcripts or working conversations it was not given.

---

# Artifact Ownership

`product-spec.md`
- Owner: Product Owner
- Status: Authoritative
- Contains: goals, non-goals, success criteria, scope

`invariant.spec.md`
- Owner: Product Owner
- Status: Authoritative
- Contains: non-negotiable constraints and governance guardrails

Architecture spec package (`_docs/specs/<pack>/20-architect/to_implementor/`)
- Owner: Architect
- Status: Authoritative
- Contains: decisions, contracts, invariants

Implementor notes
- Owner: Implementor
- Status: Working notes (non-authoritative)
- Contains: proposed spec amendments, rationale, risks, execution notes

## Typical Product Owner documents

The Product Owner typically authors or owns these documents under:
- `_docs/specs/<pack>/10-product/to_architect/`

Usually mandatory:
- `10-product-spec.md`
  - goals
  - non-goals
  - scope
  - success criteria
- `20-invariant.spec.md`
  - non-negotiable constraints
  - governance guardrails
  - risk posture
- `40-implementation-roadmap.md`
  - milestone order
  - slice order
  - acceptance milestones

Optional when relevant:
- `30-architecture-spec.md`
  - Product Owner-facing architecture compliance summary
  - not implementor-authoritative architecture
- `50-current-topology.md`
  - current-state snapshot for existing systems
- `60-dev-env.md`
  - operator/developer workflow assumptions

## Typical Architect documents

The Architect writes changes to the documents it owns itself, and specifies rather than writes changes
to code. Document work is never handed to the Implementor.

The Architect typically authors or owns these documents under:
- `_docs/specs/<pack>/20-architect/to_implementor/`

Usually mandatory:
- `30-architecture-spec.md`
  - system structure
  - boundaries
  - major decisions
- interface and contract specs
  - command/API/CLI contracts
  - lifecycle contracts
  - validation/evidence contracts
  - security/secret contracts
  - repository/layout contracts

Optional when relevant:
- slice-specific contracts
  - takeover readiness
  - bootstrap contract
  - recreate contract
- `80-operator-runbook.md`
  - operational procedure guidance
- `90-acceptance-checklist.md`
  - review-facing acceptance checklist derived from the contracts

---

# Handoffs

Inter-role handoffs should be short and useful. Include:
- `To`, `Type`, and `Scope`
- the material change, decision, or blocker
- validation/evidence relevant to a claim
- the requested next action, when any

Do not request clarification merely because administrative fields are absent
when the required technical decision is clear.

## Default efficient delivery path

Unless a concrete high-consequence risk requires more, use one pass through
the roles:

1. Product Owner states the outcome, constraints, and acceptance evidence.
2. Architect publishes one final implementor-facing specification.
3. When separate execution approval is required, Product Owner issues one
   decision that references that final specification and may also mark it
   forwarded. A separate proposal, authorization proposal, reconciliation
   artifact, and delivery artifact are not required.
4. Implementor executes the coherent scope, including reversible in-scope
   fixes and validation, and returns one decision-first completion or blocker.
5. Architect performs one proportionate technical review. Product Owner is
   involved again only for a Product Owner-owned acceptance decision or a
   material scope/risk change.

Where exact artifact identity is necessary, references are one-way: the
approval pins the final specification's identity. Do not require the
specification to contain the later approval's identity, and do not create a
circular hash or reconciliation loop.

More than one inter-role round trip before implementation requires the role
adding it to state the concrete risk, decision, or irreversible consequence it
controls. Without that justification, consolidate the step into the existing
specification or decision.

**Under `automated` orchestration this rule is weighed in tokens rather than in
User attention.** The pre-implementation restatement in the Workflow Loop meets
it: the concrete risk it controls is a divergent interpretation of an ambiguous
specification, which neither the author's own re-read nor a third-party review
detects, because both read the specification their own way.

## Delivery and persistence

The `To` field names the intended recipient. It does not prove that the User
has vetted or forwarded the artifact, and it does not grant execution
authority.

When the User mediates agent-to-agent handoffs, use an explicit delivery state:

- `DRAFT FOR USER VETTING — NOT FORWARDED`
- `FORWARDED BY USER — AWAITING RESPONSE`
- `RESPONDED TO` or `SUPERSEDED`, when applicable

Do not describe an artifact as sent, received, accepted, or operative solely
because it exists in a role-facing directory.

When the User supplies a repository path or asks that a handoff be written,
persist it at that path, verify that the file exists, and return the path to the
User. A chat response is not a persisted handoff. Fenced raw Markdown remains
the default only when the User has not requested a file artifact.

## Status and decision authority

Keep these states separate:

1. author execution status — what the author claims was completed;
2. reviewer disposition — what the reviewing role independently found; and
3. gate or milestone decision — the decision made by the role that owns the
   gate.

`COMPLETE`, `PASS`, or `ACCEPT` in an Implementor report never implies reviewer
acceptance, milestone closure, execution authorization, or a Product Owner
decision.

Unless an authoritative product document explicitly delegates it, the Product
Owner owns product, milestone, evidence-gate, and subsequent-work authorization
decisions. The Architect may issue an independent technical disposition and a
recommendation to the Product Owner. The Implementor may report results but
must not decide or recommend the overall gate disposition.

## Implementor self-assessment and reviewer independence

An Implementor recommendation is a non-binding self-assessment, never evidence.
Include it only when the governing handoff contract explicitly requests it. If
requested for individual source or implementation paths:

- label it `IMPLEMENTOR SELF-ASSESSMENT — NON-BINDING`;
- limit it to the requested path-level `ACCEPT`, `AMEND`, or `REJECT` judgment;
- put it after evidence, failures, and unresolved risks; and
- do not include an overall gate, milestone, or authorization recommendation.

The reviewer must assess requirements and evidence before reading any optional
self-assessment, record a preliminary disposition, and then compare the two.
The final review must cite independently checked criteria and evidence. It must
not cite the Implementor's recommendation as support for its disposition.

These rules apply prospectively. Do not rewrite immutable or completed reports
merely to adopt the newer reporting convention.

## High-Consequence Execution Controls

An explicit execution warrant or detailed approval record is appropriate only
for destructive, irreversible, security-sensitive, or actively actuating work
without an immediate fallback. It is not required per ordinary implementation
slice.

Once a bounded execution is authorized, ordinary implementation discoveries,
test failures, dependency corrections within an approved boundary, and
evidence-format fixes stay with the Architect and Implementor. They do not
return to the Product Owner unless they change product intent, accepted
architecture, an approved external-access/resource budget, or a
high-consequence boundary.

---

# Orchestration mode

Each project declares one orchestration mode, and several rules below depend on
it.

| Mode | Handoffs between roles | Cost of a round trip |
|---|---|---|
| `manual` | The User forwards work between roles | The User's time |
| `automated` | A control plane dispatches work between roles | Tokens |

**A rule tuned to minimise round trips under `manual` is not automatically right
under `automated`.** Under `manual` a step that returns work to the User is
expensive and is rightly removed. Under `automated` the same step costs tokens
and no human attention, so the trade reverses. State the mode before applying
any rule that limits round trips.

Projects default to `manual` unless they declare otherwise.

---

# Workflow Loop

1. Product Owner writes or updates product spec and invariants.
2. Architect writes or updates one final architecture specification for the
   coherent scope.
3. Product Owner or User approves and forwards it in one action when separate
   execution approval is required.
4. **Under `automated` orchestration only:** before implementing, the Implementor
   restates the approach, the intended insertion point, and the files it will
   touch, and returns that without code. The Architect compares it to intent. A
   divergence is corrected in the specification, not in the implementation. This
   step is omitted under `manual`, where it costs a User round trip.
5. Implementor executes, resolves reversible in-scope defects, validates, and
   returns one concise result at a decision point or material stop.
6. Architect reviews once and sends in-scope corrections directly back to the
   Implementor without involving the Product Owner.
7. Architect escalates only when the work changes goals, non-goals, success
   criteria, governance invariants, accepted architecture, or a material risk
   boundary owned by the Product Owner.

---

# Output Rules

Implementor output intended for another role MUST be raw Markdown inside fenced code blocks.

Architect output intended for another role or for file application by the owner MUST be raw Markdown inside fenced code blocks.

When the User requests persistence at a repository path, the persisted file is
the handoff artifact and the response should link to it; the fenced-code rule
does not require duplicating the full artifact in chat.

Every review or acceptance statement for a slice MUST explicitly distinguish:
- slice status
- overall milestone/refactor status

## Everything that asks for an answer carries a reference

Every item an agent puts to a human that expects a response MUST carry a **short, unique identifier**,
placed at the start of the item. This covers questions, options, proposals, requests, recommendations,
findings and actions awaiting a decision — anything the reader could answer, accept, reject or defer.

`Q1`, `Q2` for questions. `A1`, `A2` for actions awaiting a go-ahead. `F1`, `F2` for findings.
Options within one question are `(a)`, `(b)`, `(c)`. Any consistent scheme is acceptable; having none
is not.

**Identifiers are unique for the whole conversation, never reused.** Starting again at `Q1` in a later
message makes `Q1` ambiguous, and the reader's one-word answer then lands on the wrong question. If
three questions have been asked, the next is `Q4`.

**Without this the human has to quote the agent back to itself** to be understood — retyping a sentence
to identify which of four things is being answered. That cost falls on the human on every exchange,
it grows with the length of the reply, and it is entirely avoidable.

**A reply is not finished until every open item in it is referenced.** An agent that ends with an
unlabelled question has asked the reader to do its indexing.

## Every clock time carries its timezone

Every time of day an agent writes MUST name its timezone, in the same sentence or the same table
cell as the time: `14:29 UTC`, `16:39 CEST`. This binds every surface — chat, cards, comments, issue
descriptions, commit messages, documents and report files.

A bare time is read as local time by whoever reads it. When it was not local, the reader draws a
wrong conclusion about ordering, about how long something has been stalled, or about whether a
deadline has passed, and nothing on the page tells them they are wrong.

A timezone on a column header does not cover a time written in prose elsewhere. Repeat it.

Dates alone do not need a timezone. A date plus a time does. Prefer UTC for anything machine-derived
— run timestamps, log lines, API fields — and state the local zone only when the time is something
a human observed or must act at.

---

# Invariants

1. Product spec and invariants are the single source of product intent and guardrails.
2. The architecture spec package under `_docs/specs/<pack>/20-architect/to_implementor/` is the single source of implementor-facing architectural truth.
3. Implementor notes are disposable execution context.
4. No agent edits both the architecture spec package and implementor notes.
5. Public contracts remain stable unless listed under breaking changes.

---

# Escalation Rule

Implementor may escalate to Architect when:
- public API changes
- package boundaries change
- lifecycle/state invariants change
- persistence semantics change

Architect may escalate to Product Owner when:
- goals or non-goals change
- success criteria change
- governance invariants must change
- risk posture changes

---

# Review Types

For major refactors or takeovers, the following are distinct and may all be required:
- slice review
- milestone/refactor review
- code review
- operational validation

Accepted slice reviews MUST NOT be misread as accepted milestone closure.

## Code Review

Code review is a distinct governance step.
It is not the same as slice acceptance, milestone acceptance, or operational validation.

### When code review is required

Code review SHOULD be required when work:
- changes implementation logic beyond trivial edits
- changes public contracts or integration behavior
- changes safety-critical or destructive paths
- changes shared modules, framework layers, or control-plane behavior
- is part of a major refactor or takeover slice

Code review MAY be skipped for:
- pure documentation edits
- clearly trivial non-behavioral changes

### Minimum code review checks

A code review SHOULD check:
- contract alignment with the approved spec
- boundary clarity and separation of concerns
- DRY and avoidance of duplicated logic
- naming and behavior alignment
- safety and fail-closed behavior where relevant
- evidence/validation impact where relevant
- whether tests or checks are appropriate for the change scope

### Code review output

Code review output SHOULD state:
- review scope
- outcome (`accepted` | `accepted with follow-ups` | `changes required`)
- key findings
- required follow-up actions, if any

### Distinction from other reviews

- Slice review asks whether the slice goal and acceptance criteria were met.
- Code review asks whether the implementation quality and design are acceptable.
- Operational validation asks whether the system behaves correctly in execution.

Passing one does not imply passing the others.
