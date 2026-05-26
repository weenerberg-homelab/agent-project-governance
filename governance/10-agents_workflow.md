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
- Implement only against the approved architecture spec package under `_docs/specs/<pack>/20-architect/to_implementor/`.

Implementor MUST NOT:
- Modify the architecture spec package directly.
- Redesign architecture.
- Edit Product Owner-owned governance/workflow/product docs directly; propose changes via `_docs/specs/<pack>/30-implementor/to_architect/`.

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

## High-Consequence Execution Controls

An explicit execution warrant or detailed approval record is appropriate only
for destructive, irreversible, security-sensitive, or actively actuating work
without an immediate fallback. It is not required per ordinary implementation
slice.

---

# Workflow Loop

1. Product Owner writes or updates product spec and invariants.
2. Architect writes or updates the architecture spec package.
3. Implementor reviews for execution gaps and writes structured feedback.
4. Human forwards only the relevant amendment content between roles.
5. Architect updates the architecture spec package if required.
6. Implementor reconciles notes and continues execution.
7. If an amendment changes goals, non-goals, success criteria, or governance invariants, Architect escalates to Product Owner.

---

# Output Rules

Implementor output intended for another role MUST be raw Markdown inside fenced code blocks.

Architect output intended for another role or for file application by the owner MUST be raw Markdown inside fenced code blocks.

Every review or acceptance statement for a slice MUST explicitly distinguish:
- slice status
- overall milestone/refactor status

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
