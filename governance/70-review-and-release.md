# Review and release procedures

> Landed 2026-09-15 from the Sessionboard bootstrap flow product specification
> (`agent_chat_tracker/_docs/specs/2026-09-13_bootstrap_flow/10-product/10-product-spec.md` @ `9ecef73`),
> checkpoints 1, 3, 4 and 7, so they can be used outside Sessionboard. Identifiers in parentheses (M5, N3, R-M7, …)
> refer to Sessionboard review findings and are kept for provenance. Mechanisms specific to the Sessionboard
> supervisor (check runner, board, orchestrator) are the project's to map onto its own tooling.

## Dispositions of findings

### Architect feasibility feedback

**The Architect raises findings. It never edits the product spec.**

Every finding receives a disposition on the record from the Product Owner and Assistant before the
spec returns to the Architect:

| Disposition | Effect |
|---|---|
| Accepted | The spec changes |
| Rejected, with reason | The spec stands; the reason is recorded |
| Deferred | Becomes an open question with an owner |

The product spec keeps one owner, and every change to product intent traces to a decision.

**An accepted finding enters the spec as intent plus a verification, never as a mechanism.** The
mechanism belongs to the Architect. Decided 2026-09-14, after two round 2 recurrences (M7, M4) were
caused by a mechanism and a counting unit written into dispositions, not by unclear intent.

## Advisor review

### What the Advisor receives

| Receives | Why |
|---|---|
| The instruction that this is a **product review**, with the stance below and no focus areas | Any focus area narrows attention toward anticipated problems |
| The product spec as it now stands | The subject |
| The feasibility findings with their dispositions | So it can challenge a rejection rather than re-find the issue |
| Read access to decisions, invariants and the deployed store | Independence comes from checking claims |
| **Not** the Product Owner–Assistant conversation | A reviewer who reads the reasoning tends to adopt it. Verified: an Advisor attempt to read a provider transcript fails. Mechanism belongs to the Architecture pass (M7, R-M7) |

### One unsteered review

**The priority is black swans**: problems nobody anticipated. Any steering, including a checklist of
review questions, points attention at anticipated categories and works against that. Inconsistencies
and missing or excess detail are expected to surface anyway, as the easier findings.

No steered follow-up by default. Steered questions also imply a commitment to act on the answers,
where unsteered advice carries only the mandatory disposition.

**Stance, not categories.** Decided 2026-09-14. A bare "review the spec" anchors the reviewer to the
document's own framing. The prompt therefore sets the objective and stance, never where to look:

| In the prompt | Not in the prompt |
|---|---|
| Competent reviewers have already covered ordinary omissions and inconsistencies | Any list of categories to look for |
| Optimise for importance, not for the number of findings | Review questions or checklists |
| Attack from outside the specification's framing | Focus areas |
| Prospective postmortem: *what would have to happen six months after launch for the team to say "we completely failed to anticipate that"?* | |

### Report format — how to report, not where to look

**Accepted 2026-09-13 as the starting format.** Every report and prompt also carries the header and
footer from `workspace-document-contract.md` §2a.

| Tier | Meaning |
|---|---|
| **Premise** | Could invalidate the outcome, a constraint, or the approach |
| **Material** | Needs a spec change before the Architecture pass |

**The Advisor reports no Minor findings** (decided 2026-09-14). The Architect and Assistant cover them,
and Advisor tokens are the most expensive in the flow.

Premise findings are listed first. Each finding carries:

| Field | Content |
|---|---|
| Section | The spec section it concerns |
| Assumption | What the specification assumes |
| Counter-scenario | The situation in which the assumption fails |
| Why it matters | The consequence |
| Evidence or `scenario` | Evidence where it exists; otherwise labelled `scenario`, so speculation never reads as fact |
| Suggestion | Change the spec now, or record the risk. A suggestion only; the disposition stays with the Product Owner |

The report ends with the answer to the prospective postmortem question.

Every finding receives a disposition from the Product Owner and Assistant, as in checkpoint 1.

Guardrails: one invocation at this checkpoint, never inside a loop, and a per-invocation budget.

## Release

### Who decides each finding

| Finding | Decided by |
|---|---|
| Material or Minor, technical only | Architect |
| Premise, or any finding that changes outcome, non-goals, budget or acceptance | Product Owner, with the Assistant |

Dispositions as in checkpoint 1: accepted, rejected with reason, deferred.

### Release summary — what the Product Owner approves

The Product Owner approves a one-page release summary, not the architecture artifacts. The Assistant
checks it before it reaches the Product Owner.

| Section | Assistant check |
|---|---|
| Coverage map: each product acceptance criterion → the technical milestone that delivers it | No criterion without a milestone; no milestone that serves no criterion |
| Effort and token estimate compared with the spec's budget constraint | Within budget, or the gap is stated |
| First technical milestone: what becomes visible to the Product Owner when it closes | Checkable by the Product Owner, not only by tests |
| Deferred open questions, each with an owner | None without an owner |
| Premise findings with their dispositions | All dispositioned |

| Product Owner option | Effect |
|---|---|
| Release | First technical milestone starts |
| Send back, with reason | Architect revises; reason recorded. After two send-backs: working session, Product Owner and Assistant, as in checkpoint 2 (M5) |
| Re-scope | Returns to checkpoint 1 as an amendment |

Under `manual` orchestration the release summary is the same artifact, presented in the same conversation.

## Reviews, rework and acceptance

### Instruction review requires independent check evidence

The Implementor's final report cites the delivered commit. Before the Architect reviews, the
orchestrator runs every `Acceptance checks` command on that commit as a non-agent step, inside the
preventive boundary, since the commands are document content (P2). Test runs
observed in the transcript do not count: they may predate the final state and come from the session
under review.

### Review findings

A Review with `Verdict: reject` or `accept-with-conditions` carries one row per finding:

```
| # | Check or criterion | Evidence | Required change | Origin |
|---|---|---|---|---|
| R1 | AC-2 `pytest tests/test_queue.py` | exit 1, test_rank_blocked, commit a1b2c3 | Rank blocked-on-PO first | implementation |
| R2 | AC-4 human-visual | screenshot 3, badge overlaps title | Badge wraps below title | instruction |
```

| Field | Rule |
|---|---|
| Check or criterion | A declared acceptance check. Keeps findings in scope |
| Evidence | Independent check output or `file:line`. Nothing unverifiable |
| Required change | The outcome, not the implementation |
| `Origin` | `implementation` or `instruction`. Answers which role's defect caused the cycle |

| Origins | Instruction |
|---|---|
| All `implementation` | Unchanged |
| Any `instruction` | New version with a revision block: version, change, finding answered |
| Revision changes `Allowed paths` or `Acceptance checks` | Implementor acknowledges the delta before rework |

### Rework report

A Report with `Responds to: <review id>`, one row per finding:

```
| # | Action | Commit | Check result |
|---|---|---|---|
| R1 | fixed | d4e5f6 | exit 0 |
| R2 | disputed: overlap only below 360px, instruction sets 400px minimum | — | screenshot 3b |
```

| Action | Meaning |
|---|---|
| `fixed` | Commit cited; confirmed by the independent check run |
| `disputed` | Evidence required; the Architect records a disposition |
| `not reproducible` | Steps tried, cited |

A finding without a row fails the mechanical check, as a missing acknowledgement section does.

Each `reject` is one cycle against `Max cycles`. Rework resumes the same session.

On `accept`, delivered work is integrated into the project's main branch by a non-agent step. A conflict
pauses to the Architect. Checks needing Docker run after integration (N1, N2).

### `human-visual` checks — batched per technical milestone

The Implementor attaches screenshots or a recording per check. The Product Owner reviews all
`human-visual` checks of a technical milestone in one pass. Accepted risk: a late visual defect can
cost rework across several instructions.

### Technical milestone acceptance

| Step | Who |
|---|---|
| Every instruction accepted; independent check run on the milestone's final commit | Orchestrator |
| Coverage: the milestone delivers the product criteria the release summary mapped to it | Assistant |
| Advisor review, only if architecture artifacts changed after the last Advisor architecture review (checkpoint 4 trigger rule). Planned changes already reviewed are not reviewed again | Advisor, once, budgeted |
| Accept, accept-with-conditions, or reject | Architect |

Each condition becomes a work item assigned to the next milestone. After two `reject` verdicts on a
technical milestone, it escalates to the Product Owner (M5).

### Product milestone acceptance

The Assistant prepares one row per checkpoint 1 acceptance criterion: evidence, location, holds or not.
The Product Owner accepts, accepts with conditions (each a work item), or rejects with reason. No cycle
limit: the Product Owner drives this loop (M5).

**Evidence from use.** Product milestone acceptance includes human testing in the real setting; for
`football` V1a, a field session at the pitch. When use shows the outcome is not met although every
declared check passes, the result is a **product finding** to the Product Owner, never an implementation
defect or scope growth. In M6 it returns to the product spec manually (RPT-BF-ADV-001 P2).
