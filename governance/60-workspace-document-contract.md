# Workspace document contract

> Landed 2026-09-15 from `agent_chat_tracker/_docs/product/workspace-document-contract.md` @ `9ecef73`,
> as that document itself requested ("draft for the Architect to land in `_shared/agent-project-governance/`").
> This copy is authoritative from now on; the Sessionboard copy is historical.

**Owner:** Sessionboard, on behalf of the Product Owner · **Status:** draft for the Architect to land in `_shared/agent-project-governance/`
**Date:** 2026-09-13 · **Decided by:** Product Owner, 2026-09-12 and 2026-09-13 · **Contract version:** 1

Sessionboard specifies this contract and updates it. Every project complies on its own schedule.
Sessionboard's software verifies compliance and reports it. **Compliance never gates delivery.**

---

## 1. Why these fields exist

A field earns its place in a header by naming a query that needs it. Everything else stays prose.
Unfilled headers are worse than absent ones, because they parse.

| Query | Fields it needs |
|---|---|
| Does this project have executable work? | work item `Status` |
| Which item should the PO look at first? | work item `Kind`, `Value`, `Milestone`, `Effort`, `Due` |
| What may this item spend? | work item `Effort`, or `Budget` when overridden |
| Can this item close without a human looking at it? | work item `Verification` |
| Is this item in the milestone we are delivering? | work item `Milestone`, project `Current milestone` |
| What depends on this item? | computed from other items' `Blocked on` |
| How long has this been waiting? | work item `Raised` |
| Is this project stopped because of the PO? | work item `Blocked on` |
| Which project blocks which? | `Blocked on: external · <project>` |
| What is the correction-cycle rate? | review `Verdict` |
| Which role's defect caused a cycle? | review `Verdict`, finding `Origin`, `Responds to` |
| What is the open work package? | instruction `Id`, `Status`, `Gate` |
| Has this work left its agreed scope? | instruction `Allowed paths` |
| Which model runs this instruction? | instruction `Difficulty`, project default provider |
| When must this stop by itself? | instruction `Max cycles`, `Max failures same check`, `Wall clock` |
| How far along is this instruction? | instruction `Acceptance checks` |
| Was this chat primed for the role it claims? | role prompt in `40-agent_prompts.md`, matched against the transcript |

---

## 2. Document classes and required fields

Six document classes, plus the message classes in §2a. Fields go in a header block before any prose. **Several fields may share a line,
separated by `·`**, which is the convention already in use:

```
**Id:** ACT-021 · **Kind:** feature · **Status:** ready · **Owner:** Implementor
```

A reader must accept both one-per-line and `·`-separated forms. Requiring one-per-line would force a
rewrite of every existing header for no gain.

| Class | Required fields |
|---|---|
| Work item | `Id`, `Title`, `Kind`, `Status`, `Owner`, `Raised`, `Blocked on` (when `Status: blocked`), `Instruction`, `Milestone`, `Value`, `Effort`, `Verification`, `Due` (optional), `Budget` (optional) |
| Instruction | `Id`, `Type`, `Status`, `Gate`, `Responds to`, plus the execution envelope in §3.6 |
| Report | `Id`, `Type`, `Responds to` |
| Review | `Id`, `Type`, `Responds to`, `Verdict`, findings table when `Verdict` is not `accept` (checkpoint 7 of the bootstrap flow) |
| Decision | `Id`, `Date`, `Status`, `Supersedes` (when it does) |
| Milestone | `Id`, `Title`, `Type`, `Parent` (technical only), `Status`, `Accepted by`, `Accepted on` |

Work items live in `_todos/`, closed ones in `_todos/_done/`. Specification documents live in
`_docs/specs/<date>_<slug>/` under `10-product/`, `20-architect/`, `30-implementor/` or `40-advisor/`. Product
documentation that belongs to no single slice lives in `_docs/product/`.

**Contract version.** Each project declares which version of this contract it complies with. Projects
migrate at different times, so without it a new field is reported as a violation everywhere at once
the day the contract changes. One line per project.

**Project identity.** `Blocked on: external` names another project, so the workspace needs one
canonical project identifier. Three namespaces exist today: the directory name under the workspace
root, the GitHub repository name, and Sessionboard's own project id. **The directory name is
canonical**, because it is the only one visible from a mounted filesystem and the only one that does
not require a lookup. `_docs/governance/project-inventory.md` already maps it to the other two.

### 2a. Messages

Three message classes, decided 2026-09-13. Every message between roles is a document under this
contract, so messages use the same header schema, never a separate one.

| Class | From → to | Header | Closing block |
|---|---|---|---|
| **Prompt** | Control plane or role → agent session | Yes | Footer |
| **Report** | Agent → role, persisted as a document | Yes | Footer |
| **Handoff summary** | Agent → human, in chat | No | Handoff block |

#### Header — prompts and reports

| Field | Prompt | Report |
|---|---|---|
| `Id`, `Type` | yes | yes |
| `Project`: the project directory name (see Project identity) | yes | yes |
| `From role`, `To role` | yes | yes |
| `To agent`: the receiving agent's name, `<Project> - <Template>` where agents are named; omitted when the recipient is a human | yes | yes |
| `Responds to` | yes | yes |
| `Work item`, `Milestone` | yes | yes |
| `Session type`: specify · implement · acknowledge · rework · review-gating · review-advisory · document | yes | — |
| `Expected output type` | yes | — |
| `Contract version`, `Orchestration mode` | yes | yes |

**A receiver checks `Project` and `To role` or `To agent` before acting.** On a mismatch it does nothing
and replies with one line naming the mismatch. A pasted message without `Project` is treated as before.

`Session type` on a prompt is what makes the activity cost category known at spawn, as
`activity-cost-accounting.md` requires. Values map one-to-one to its categories; `acknowledge` counts as
`implementation`. Because rework resumes the implementing session, the category is set per prompt, not
per session.

#### Footer — prompts and reports

| Field | Why only the message can carry it |
|---|---|
| `Inputs relied on`, each with its commit or version | Provenance: whether the work rests on a stale input |
| `End of message` marker | Detects truncation. An output cut off at a token limit otherwise looks complete |

**The footer carries no self-reported metrics.** Cost, tokens, model, effort and session id are
measured by Sessionboard from the transcript. A self-reported copy would be a second, untrusted source
for the same fact.

#### Handoff block — agent to human

Every agent-to-human message that produces an artifact or requests an action ends with a block in
rendered markdown, **never inside a code fence**, because a fence makes the paths unclickable:

```markdown
**Handoff**

| # | Artifact | To |
|---|---|---|
| 1 | [<file name>](<repo-relative path>) | <recipient role> |

| | Owner | Action | Work item | Order |
|---|---|---|---|---|
| A | <owner> | <action> | <work item id> | blocks X · after X · independent |

**Parallel now:** <action letters> · **Waiting on:** <action letters, or none>
```

Every file mentioned anywhere in the message, not only in the block, is a link.

| Rule | Why |
|---|---|
| Always last, always present. `Actions: none` when nothing is requested | An absent block means a malformed message, not an idle one |
| One owner per action | The human is not left to infer who acts |
| Every dependency explicit | Answers what can run in parallel without reconstruction |
| Repo-relative, clickable paths | "Where is the report" is one click |
| Each action cites its work-item id | The block is a view. The durable fact is the work item's `Blocked on` |

**Mode-conditional.** Under `manual` the block lists every forward, because the human routes. Under
`automated` it lists only actions the human must take, because the control plane dispatches.

To land in `_shared/agent-project-governance` under Output Rules, with the rest of this contract.

---

## 3. Vocabularies

### 3.1 Work item `Status` — seven values

| Value | Meaning | Who owes the next move |
|---|---|---|
| `open` | Raised, not yet specified | Architect |
| `ready` | Specified and executable | Implementor |
| `in-progress` | Owner is executing | Owner |
| `in-review` | Delivered, under review | Architect for instructions and technical milestones; Product Owner for product milestones |
| `blocked` | Cannot proceed | See `Blocked on` |
| `done` | Accepted and closed | Nobody |
| `dropped` | Closed without delivery | Nobody |

`open` and `ready` are not merged. The boundary between them is which role is the bottleneck, which
is the question the attention queue exists to answer.

`done` and `dropped` are not merged. Throughput must not count abandoned work as delivered.

### 3.2 Review `Verdict` — three values

`accept` · `accept-with-conditions` · `reject`

### 3.3 `Blocked on` — reason and target

Shape: `Blocked on: <reason> · <target>`

| Reason | Target | Query it serves |
|---|---|---|
| `decision` | the role that owes the answer | Stopped because of the PO |
| `dependency` | a work-item id in this project | Within-project ordering and starvation |
| `external` | **another project** | Cross-project dependency edges |
| `resource` | quota, budget or infrastructure | Ties to the quota and budget work |

`external` naming the target project produces a dependency graph across the portfolio from documents
that are already written. It records the dependency that actually bit, which is better evidence than
a static analysis listing every dependency that theoretically exists.

There is deliberately no `review` reason. `in-review` is already a status, and one fact has one home.

### 3.3a Milestones — two types, one hierarchy

| Type | Declared and specified by | Reviewed and accepted by |
|---|---|---|
| `product` | Product Owner | **Product Owner** |
| `technical` | Architect | **Architect**, once functional implementation is complete and non-functional checks pass |

A technical milestone carries `Parent`, naming the product milestone it delivers part of. A product
milestone has no parent.

This is already the shape of Sessionboard's own history: M3 is a product milestone and M3.1 through
M3.13 are technical milestones under it.

**Each project declares two current milestones**, not one: the current product milestone and the
current technical milestone within it. They live in the project's `AGENTS.md`, which every agent
already reads and which already carries milestone state in prose.

> **Open governance change.** `AGENTS.md` gate 2 currently reads *"Architect verifies … PO accepts"*
> for every milestone. Architect acceptance of technical milestones is a delegation of that gate and
> needs a `DEC-*` entry before this table is authoritative. `10-agents_workflow.md` needs the same
> strengthening.

### 3.4 Declared fields on the work item

| Field | Values | Owner | Why declared |
|---|---|---|---|
| `Kind` | `feature` · `defect` · `chore` | Raiser | Only `defect` changes rank. A severe bug is `defect` plus `Value: high` |
| `Value` | `high` · `medium` · `low` | Product Owner | Business value is stable over an item's life |
| `Milestone` | a milestone id, or empty | Product Owner | Empty means unscheduled |
| `Effort` | `high` · `medium` · `low` | Architect | Derives the token budget, and is the denominator for progress-per-compute |
| `Verification` | `automated` · `human-visual` | Architect proposes, PO confirms | Some work cannot be accepted without a human looking at it |
| `Due` | a date | Product Owner | Optional. Dates resolve rather than going stale |
| `Budget` | a token count | Product Owner | Optional. Overrides the budget derived from `Effort` |
| `Raised` | a date | Raiser | Age is the ranking fallback. File mtime is unusable, since a formatting edit changes it |

**Budget is derived from `Effort`, not declared per item.** The derivation uses the median token
cost of completed items in the same effort class in this workspace, so it is grounded in local data
and tightens as data accumulates. `Budget` overrides it for an item known to be unusual.

**`Verification: human-visual` marks work that cannot be auto-accepted.** User-interface work is the
common case: the agent has no feedback loop for a visual result, so acceptance needs an eye. The
board routes these to the Product Owner for visual sign-off rather than inferring the need from a
title, batched once per technical milestone (bootstrap flow checkpoint 7).

**There is one magnitude scale, not two.** Severity is not a separate field. A severe defect is
`Kind: defect` with `Value: high`. Two scales meaning "how much this matters" would disagree, and
reconciling them would fall to a human.

**Current milestone is declared once per project**, not per item. The item says which milestone it
belongs to; the project says which milestone is current. Deriving "current" from the newest spec
pack would mis-rank every item the moment a pack is opened early.

**The Product Owner owns the scores. The assistant ensures they get set and proposes values.**
`Value`, `Milestone` and `Due` are Product Owner decisions; chasing unscored items and drafting a
proposed score is the assistant's work. Score coverage and staleness therefore report to the
assistant, not to the Product Owner, who sees the ranked queue.

**Urgency is deliberately not a field.** It decays faster than anything else here, and it decomposes
into two things that do not: a `Due` date, and the number of items blocked on this one, which is
computed from other items' `Blocked on: dependency` entries.

**Dependents are computed, never declared.** A declared count goes stale the moment another item
changes. The edges already exist in §3.3.

Three values per scale, not ten. Small vocabularies are the convention throughout this workspace:
three verdicts, four confidences, five phases. A ten-point scale invites false precision and drifts.

### 3.5 Ranking rules

**Rank lexicographically, never by weighted score.** The board must state in one line why an item
sits where it does. A composite number cannot be checked by the reader, and a rank that cannot be
explained will not be trusted.

Order, highest first:

1. `Status: blocked` with `Blocked on: decision` naming the Product Owner
2. `Kind: defect` with `Value: high`
3. In the current **technical** milestone
4. In the current **product** milestone, other technical milestones under it
5. `Value`
6. `Due` proximity
7. `Effort`, cheapest first
8. Dependent count
9. Age

Milestone membership outranks `Value` deliberately. A high-value feature outside the current
milestone is scope creep, and milestone discipline exists to stop it. A severe defect is the only
thing that jumps the milestone boundary, which is why `Kind` exists.

`Effort` breaks ties cheapest first. This raises throughput on equal-value work. It also biases
against hard items, which is how backlogs accumulate expensive work nobody starts, so it sits below
`Due` rather than above it.

Age is the fallback, not a priority signal. An old item is not an important one.

**A partially scored queue ranks by age and says so.** Interleaving scored and unscored items
produces an incoherent order. If coverage is incomplete, the queue states "ranked by age, N of M
unscored" rather than mixing the two silently.

**Priority carries its own age.** An item scored long ago that has not moved states when it was
scored. Same rule as data freshness elsewhere: a value is rendered with the age of the judgement
behind it.

### 3.6 Execution envelope — on the instruction, not the work item

The work item is what the Product Owner tracks. The instruction is the Architect's contract with the
Implementor, so the envelope belongs there.

| Field | Produces |
|---|---|
| `Allowed paths` | Scope-growth detection, by comparing tool-call paths against the declaration |
| `Architectural change` | `yes` or `no`. Makes gate 3 checkable rather than a norm |
| `Difficulty` | `low` · `medium` · `high`, set by the Architect. Selects the Implementor model through the mapping table in `_shared` governance. Independent of `Effort`, which is size |
| `Max cycles` | An exact stop. One cycle is one `reject` verdict on the instruction, countable from documents |
| `Max failures same check` | An exact stop on the repeated-failure loop |
| `Wall clock` | An exact stop |
| `Acceptance checks` | Each check with an id and the command that verifies it, or `human-visual`. The Implementor runs checks by id through a check runner that records id and exit code, so progress is exact by construction. Runner output is a progress signal, never acceptance evidence |
| `Budget extension` | Optional. Set once by the Architect, at most 50% of the derived or overridden budget, with reason. Anything larger is a Product Owner `Budget` change on the work item |

Token budget is not repeated here. It comes from the work item's `Effort` or its `Budget` override,
plus any `Budget extension`.

**A declared threshold converts an inferential signal into an exact one.** "Three failures on the
same check" is arithmetic once the instruction says three. This is what allows an automatic stop on
conditions other than budget exhaustion, and it is why the thresholds are declared rather than
inferred.

There is deliberately no `escalation_on` list. Once every condition carries a threshold, what
escalates is derivable from which thresholds exist.

`Allowed paths` is the existing out-of-scope section made checkable. `AGENTS.md` already calls that
the most valuable line in any instruction; this gives it a form a test can read.

### 3.7 Role priming is observable

Role prompts are known artifacts in `_shared/agent-project-governance/governance/40-agent_prompts.md`.
A chat that claims a role can therefore be checked against the prompt that role requires.

A chat carrying a role it was never primed for is mislabelled, and nothing detects that today. This
is a compliance check on the transcript. It needs no orchestration and no agent cooperation.

---

## 4. Rules for the reader

**Degrade per field, never per project.** An unrecognised value yields `unknown` plus a drift
warning, never a nearby value. This is ARCH-INV-007's existing discipline. A project with prose
statuses still appears, still counts its items, and the drift warning names the files that remain
unmigrated.

**An unreportable project surfaces as unreportable.** A project whose work items do not parse gets
its own queue entry stating that it cannot report whether it needs attention. It is neither idle nor
healthy, and rendering it as either would be a judgement presented as a measurement.

**No cross-project aggregate renders without its compliance coverage.** Partial migration biases
every portfolio number. This is ARCH-INV-008's rule applied to a second axis, and the precedent is
`ScanBatch` completeness, which exists so a partial fleet result is detectable rather than
indistinguishable from a quiet one.

---

## 5. Compliance is report-only

A format violation never blocks a milestone, a delivery or a gate. It is reported, it appears in the
same queue so it does not rot, and the project owner decides when to fix it.

The reason is the governance framework's own rule: do not commission a gate without naming the risk
it controls. A missing header field controls no product risk. The moment one can block a milestone,
the field gets filled with whatever parses, and the data becomes worse than absent.

---

## 6. Migration

No deadline is set here. The board reports coverage per project, and coverage is the migration
tracker. `agent_chat_tracker` work items already carry `Status`, `Owner`, `Instruction` and `Gate`
in the required shape; the Home Assistant repository carries the same facts as prose and is the
larger migration.
