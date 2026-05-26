# Engineering Guidelines

These are generic engineering and design expectations for governed work.

They are intentionally technology-agnostic.
Project-specific constraints and tool behavior belong in project overlays and spec packs.

## Core principles

### 0. Proportionality and useful progress
Spend process and design effort in proportion to real consequence.

Prefer:
- the smallest technically coherent step that produces useful behaviour or evidence
- reversible, operator-selectable deployment while a feature is being proven
- strict review of delivered code without delaying harmless implementation

Avoid:
- treating private/local reversible work as formal production certification
- introducing gates, reports, or abstractions without a concrete defect or risk they address
- confusing caution with technical quality

### 1. Separation of concerns
Design components so each has a clear responsibility and a narrow reason to change.

Prefer:
- distinct boundaries between workflow, policy, integration, state handling, and presentation
- interfaces that make responsibility explicit
- small composable units over large mixed-purpose units

Avoid:
- single modules that accumulate unrelated responsibilities
- hidden coupling between unrelated layers
- pushing policy decisions into convenience wrappers or ad hoc scripts

### 2. DRY
Keep one authoritative definition of a rule, contract, or behavior.

Prefer:
- one canonical place for each invariant, contract, or mapping
- derived summaries and checklists only when they clearly point back to the authority source
- shared helpers only when they preserve clarity

Avoid:
- duplicated contract definitions across multiple active docs
- repeated logic that drifts over time
- “copy and tweak” patterns that silently create forks of truth

### 3. Clean solutions before incidental complexity
Default to the simplest sound design that solves the real problem.

Prefer:
- solutions that improve clarity, maintainability, and correctness without
  preventing useful progress
- root-cause fixes over surface patches
- explicit tradeoff decisions when choosing a short-term workaround

Allow quick fixes only when:
- they are explicitly temporary
- their risk and scope are understood
- they do not become de facto architecture by inertia

### 4. Stable contracts, flexible internals
Keep externally relied-on contracts stable unless a deliberate change is approved.

Prefer:
- preserving public interfaces while improving internal structure
- explicit migration plans when contracts must change
- compatibility layers only as a temporary bridge

### 5. Fail closed where consequence requires it
When destructive targeting, security, irreversible state, or physical-control
execution is ambiguous, stop and require clarification. For reversible local
implementation uncertainty, make reasonable explicit assumptions, implement,
and surface them for review.

Prefer:
- explicit validation before execution
- explicit approval semantics for risky actions
- evidence that shows what actually happened

### 6. Evidence over narrative
Operational and acceptance claims should be backed by concrete evidence, not interpretation alone.

Prefer:
- machine-readable evidence where practical
- explicit pass/fail criteria
- review notes that point to evidence rather than re-explain it

Evidence requirements must be proportional. Focused tests and observable
runtime comparison are enough for reversible work; do not demand ceremonial
artifacts without a concrete purpose.

### 7. Minimize hidden knowledge
Normal operation should not depend on undocumented operator memory or implicit local context.

Prefer:
- explicit runbooks, contracts, and evidence fields
- predictable paths and conventions
- documented assumptions and exceptions

### 8. Status is not quality
Deployment status and measured technical quality are different concepts.

Prefer:
- publish shadow/active/disabled status separately from model confidence or quality
- judge a model or implementation by evidence, not by whether it has been enabled

Avoid:
- lowering a quality score because a feature is still operator-disabled
- using administrative state as a substitute for technical assessment

## Application rule

If a project-specific document appears to conflict with these guidelines:
- first check whether the project-specific rule is a necessary specialization
- if not, prefer the simpler and more defensible design aligned with these guidelines

These guidelines guide design judgment.
They do not override approved product constraints or project-specific safety invariants.
