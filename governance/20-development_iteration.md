## Development iteration

This file defines execution-loop order only.

Role authority, ownership, escalation boundaries, and handoff schema are defined in:
- `_docs/shared/governance/10-agents_workflow.md`

### Human-in-the-loop rule
- Agents propose plans and patches in chat.
- No implementation, file edits, or deploys occur unless the User explicitly approves.

### Canonical artifacts (authoritative order)
1. `_docs/specs/.../10-product/10-product-spec.md`
2. `_docs/specs/.../10-product/20-invariant.spec.md`
3. `_docs/specs/.../20-architect/to_implementor/30-architecture-spec.md`
4. `_docs/specs/.../10-product/40-implementation-roadmap.md`

### Iteration loop (each slice)
1. Pick a slice with explicit acceptance criteria.
2. Agree the proposal in chat and get approval.
3. Update spec if needed.
4. Implement.
5. Review.
6. Validate.
7. Record the next slice.

### Mandatory vs Optional mapping
For each slice, acceptance criteria MUST be split into:
- `mandatory` (blocking)
- `optional` (non-blocking)

Each mandatory criterion MUST map to:
- exact command
- exact evidence artifact path
- exact field/value checks

### Review status rule
Every architect/reviewer acceptance statement for a refactor or migration slice SHOULD explicitly state:
- slice status
- overall milestone/refactor status

### Primary blocker rule
If a primary operational blocker exists, secondary cleanup/performance/documentation slices MUST NOT be treated as meaningful closure progress for that milestone until the blocker is resolved.

### Native-run rule for migrated paths
For migrated governed execution paths, tests alone are not sufficient for operational acceptance when the path is safety-critical or recreate-critical.

At least one real governed writable-target run is required before claiming operational readiness of the migrated path.

### Prompt delta rule
Each follow-up handoff SHOULD start with:
- `What changed since last review`

Avoid repeating unchanged context unless required for safety or approval.
