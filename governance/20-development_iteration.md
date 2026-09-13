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
