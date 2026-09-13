## Governance discovery

Purpose: establish the minimum governance needed to ship safely and avoid process drift.

### Outputs
- a written product spec
- a written invariant spec
- a written architecture spec
- a written implementation roadmap
- a written current-state/topology summary
- a written operator/dev-environment summary

### Governance decisions to make early
- collaboration model and approval rule
- change-control path
- gate-decision authority and the separation of author status, reviewer
  disposition, and gate decision
- whether path-level self-assessments are needed and how reviewer independence
  is protected
- handoff persistence and delivery-state semantics when the User vets and
  forwards agent artifacts
- secret-handling ownership
- environment classes and approval thresholds
- release semantics

### Discovery checklist
- target environments
- operator environments
- identity and access model
- failure modes
- definition of successful reproduction or delivery

### Risk register
Record accepted risks explicitly, even if no mitigation is planned yet.
