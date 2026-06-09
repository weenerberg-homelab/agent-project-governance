# Project Structure Tiers

## Purpose

Define five tiers of project structure that match governance investment to project complexity and consequence.
The goal is proportionality: a single compose file should not carry the overhead of a production Python service,
and a system that can destroy infrastructure should not be governed like a stateless web service.

Each tier specifies what is **required**, what is **optional but recommended**, and what is **explicitly out of scope**.
When a project grows or its consequence profile changes, promote it to the next tier — do not add structure pre-emptively.

---

## Two axes, one ladder

Project structure is shaped by two independent properties:

- **Complexity** — size of the codebase, number of agents, architectural depth, rate of change.
- **Criticality** — consequence of a mistake: data loss, infrastructure damage, credential exposure, hard-to-reverse mutations.

A project can be complex without being critical (HomeAssistant: complex codebase, recoverable failures) and critical without being especially complex (a deployment script that deletes the wrong server). Tiers 1–4 are primarily driven by complexity. Tier 5 is triggered by criticality — it adds execution governance on top of whatever code governance is already in place.

---

## Tiers at a glance

| Tier | Label | Typical contents |
|---|---|---|
| 1 | Trivial | Config files, one-off scripts, no application code |
| 2 | Low | Small services or scripts, limited logic, operational focus |
| 3 | Intermediate | Real application code, tests, CI, shallow governance |
| 4 | High | Large codebase, formal spec system, comprehensive CI, full governance |
| 5 | Critical | High-consequence mutations, execution governance, formal audit trail |

---

## Universal requirements

These apply at every tier, regardless of complexity or criticality:

- All projects must be under version control.
- All projects must have an `AGENTS.md` (see tier-specific content requirements below).

---

## Cross-tier conventions

These conventions apply wherever the relevant structure exists, regardless of tier.

### Python tooling configuration

`pyproject.toml` is the sole configuration file for all Python tooling. No separate `pytest.ini`, `.coveragerc`, `setup.cfg`, or per-tool dotfiles. All sections — `[tool.ruff]`, `[tool.mypy]`, `[tool.pytest.ini_options]`, `[tool.coverage.*]`, `[tool.bandit]` etc. — live in `pyproject.toml`.

### Testing output paths

All generated test and quality output goes under `testing/reports/` (always gitignored). Standard paths:

| Artifact | Path |
|---|---|
| Coverage data file | `testing/reports/coverage/.coverage` |
| Coverage HTML | `testing/reports/coverage/htmlcov/` |
| Coverage XML | `testing/reports/coverage/coverage.xml` |
| Lint / static analysis | `testing/reports/<tool>/` |
| CI quality snapshots | `testing/reports/<stamp>/` |

### `testing/` internal structure

`testing/` is the unified testing area. It contains test code, infrastructure scripts, and generated output. Internal layout:

```
testing/
├── conftest.py
├── <domain>/               # one sub-folder per domain; mirrors src/ structure
│   └── test_*.py
├── smoke/                  # cross-domain wiring checks (exception to domain rule)
├── tools/                  # quality scripts used by CI and local runs
└── reports/                # gitignored; all generated output
```

Test types (unit, integration, slow, performance) are distinguished by **pytest markers**, not by directory structure. This keeps all tests for a domain co-located while still allowing `pytest -m "not slow"` or `pytest -m smoke`.

At Tier 3 with few test files a flat layout inside `testing/` is acceptable. Domain sub-folders are required at Tier 4.

### `_todos/` is gitignored

`_todos/` contains local working material — agent reminders, analysis notes, deferred tasks. It is always gitignored; its contents are not committed to version control.

---

## Tier 1 — Trivial

**Characteristics:** No application code or a single script. Changes are infrequent and low-risk. A new agent or developer arriving here should be oriented in one paragraph.

### Required
- `AGENTS.md` — one paragraph: what this is, what it does, key files.
- `.gitignore` — at minimum: secrets (`.env`), OS noise (`.DS_Store`).

### Required if secrets are present
- `.env.example` — template for required environment variables; `.env` gitignored.

### Explicitly out of scope
Tests, CI workflows, linting config, tooling config, docs directories.

### Promotion signal
Promote to Tier 2 when: the project gains more than one meaningful script or service, or when another project depends on it.

---

## Tier 2 — Low

**Characteristics:** Operational configuration, compose stacks, shell scripts, or small Python utilities. Logic is present but contained. Changes happen occasionally. Errors are recoverable.

### Required
- Everything from Tier 1.
- `AGENTS.md` — layout table (path → what it is) and common operations. Still inline, not a pointer index.
- `_docs/specs/` or `_docs/` — record non-obvious decisions and operational specs. Even one spec document beats zero when the project has external dependencies or a defined contract. See `20-docs-layout.md` for the expected internal layout at each tier.
- `_todos/` — deferred tasks, agent reminders, and working notes that are not authoritative documentation. Always gitignored (see cross-tier conventions). Typical subdirs: `analysis/` (investigation notes), `reports/` (generated snapshots). Files are named `ID_Description.md`.

### Required if Python code is present
- `pyproject.toml` — sole configuration file for all Python tooling (see cross-tier conventions). At this tier: `[tool.ruff]` at minimum.
- `.gitignore` entries for Python caches: `__pycache__/`, `.mypy_cache/`, `.ruff_cache/`, `.benchmarks/`.

### Optional
- `requirements-static.txt` — if static analysis is useful locally.
- `.vscode/extensions.json` — if the repo is opened in VS Code regularly.
- `testing/` — add when a custom runner script or shared tooling exists. Contains `run_tests` (runner), `tools/` (helper scripts), `reports/` (generated output, gitignored).

### Explicitly out of scope
Formal testing strategy, CI workflows, pyrightconfig, METRICS.md, governance index.

### Promotion signal
Promote to Tier 3 when: the project has a non-trivial test suite, external consumers, or logic that requires correctness guarantees under change.

---

## Tier 3 — Intermediate

**Characteristics:** A real application or service with meaningful domain logic. Tests exist and are maintained. CI provides basic quality gates. The codebase is stable enough that agents can work on it safely without deep governance, but discipline in tooling and test coverage is needed.

### Required
- Everything from Tier 2.
- `AGENTS.md` — front door with "Where to look" section pointing to key docs. Inline rules kept to essential constraints; detailed rules live in docs files.
- `pyproject.toml` — consolidated tool config: `[tool.ruff]`, `[tool.mypy]`, `[tool.pytest.ini_options]` with `--strict-config --strict-markers` and explicit marker taxonomy, `[tool.coverage.*]` with standard output paths (see cross-tier conventions).
- `requirements-dev.txt` — test and dev dependencies (pytest, coverage).
- `requirements-static.txt` — static analysis tools (ruff, mypy, bandit).
- CI workflow — at minimum: lint gate + test gate on push/PR.
- `.vscode/` — `extensions.json` and `settings.json` committed.
- `testing/` — unified testing area (see cross-tier conventions). At this tier a flat layout is acceptable; domain sub-folders recommended once test count grows beyond ~20 files.

### Required if type checking is active
- `pyrightconfig.json` — LSP type coverage, scoped to source tree.

### Optional
- `METRICS.md` — document quality dimensions and how to run them.
- `launch.json` — VS Code debug configurations.
- Architecture docs under `_docs/architecture/`.

### Explicitly out of scope
Formal spec system with Architect/Implementor roles, arch-guards, supply-chain scanning, governance index. These belong in Tier 4.

### Promotion signal
Promote to Tier 4 when: the codebase has multiple agents working on it, architectural invariants need formal protection, or changes require phased rollout with explicit acceptance criteria.

---

## Tier 4 — High

**Characteristics:** A production system with significant domain logic, formal governance, and a need for change safety under multiple concurrent agents or workstreams. The cost of an undetected regression or architectural drift is high. Failures are recoverable but expensive.

### Required
- Everything from Tier 3.
- `AGENTS.md` — pure front-door pointer index. No inline rules. Every rule has a home in a docs file; AGENTS.md only lists where to look.
- `_docs/rules/` or equivalent — collected agent constraints (testing standards, definition of done, CI guardrails, operational constraints). This requirement is satisfied if a workspace-level `_shared/agent-rules/` directory covers the project's constraints and `AGENTS.md` points to it explicitly.
- `_docs/specs/` — formal spec system with Architect/Implementor authority model.
- `_docs/invariants.md` — explicit system invariants (`INV-*` catalog).
- `_docs/testing/testing-strategy.md` — behavior contracts that must remain stable under refactor.
- `_docs/governance/INDEX.md` — precedence-ordered index of all authoritative documents.
- `METRICS.md` — full quality dimensions documentation.
- CI — comprehensive pipeline: lint, type check, security scan, arch guards, supply chain, build metadata verification, workspace integration smoke.
- `requirements-static.txt` — separate from `requirements-dev.txt`; includes bandit, pip-audit, pyright, vulture.

### Required (in addition to Tier 3)
- `testing/` — domain sub-folders required at this tier (see cross-tier conventions). Flat layout is not acceptable for a Tier 4 codebase.

### Recommended
- `pyrightconfig.json` with strict paths matching mypy per-module strict overrides.
- Architecture docs (`_docs/architecture/`) covering system context, runtime flows, state transitions.
- Operations docs (`_docs/operations/`) covering failure modes and rollout policy.

### Notes on the pointer-index AGENTS.md
The front-door pattern matters most at this tier because multiple agents arrive with different context and different tasks. A wall of rules slows orientation and creates maintenance drift. A pointer index stays stable even as individual rule files evolve.

### Promotion signal
Promote to Tier 5 when: the project manages infrastructure, credentials, or persistent data where mistakes are hard or impossible to reverse, and where running the code is as consequential as writing it.

---

## Tier 5 — Critical

**Characteristics:** A system where execution has real-world consequences that are hard to reverse — infrastructure destruction, credential exposure, data loss, or security boundary violations. Governance covers not just *what is written* but *what is run* and *when*. The authority model expands beyond Architect/Implementor to include a Product Owner and optional Reviewer.

The key distinction from Tier 4: **Tier 4 governs commits. Tier 5 governs commits and deployments.**

### Required — everything from Tier 4, plus:

**Authority model**
- Formal multi-role governance: Product Owner (defines intent and guardrails), Architect (technical contracts), Implementor (code and notes), Reviewer (safety check on high-risk actions).
- Explicit doc ownership rules: each document type has a single owner; other roles submit proposals via routing channels rather than editing directly.

**Governance lanes**
- At least two ceremony levels: a lightweight lane for routine execution already covered by current specs, and a formal lane for changes to public contracts, security model, destructive semantics, or milestone decisions.
- The lightweight lane reduces paperwork; it does not remove the approval requirement.

**Pre-execution gate**
- Before any mutable or destructive action: the execution surface must be committed to git, and the exact commit SHA must be known and recorded.
- Push to remote required by default for high-risk actions (infrastructure mutations, first takeover of a host, destructive modes).
- Local-only exceptions permitted but must be explicitly recorded with justification and post-action obligation to push.

**Execution evidence**
- Formal evidence artifacts per action, per spec, per target — not just CI logs. Evidence records what was run, from what commit, against what target, with what outcome.

**Secret management**
- Secrets encrypted in-repo (e.g. SOPS) rather than gitignored plaintext. Encryption is the audit trail.

**Safety invariants**
- Explicit IaC/operational invariants documented and enforced: no overwrite of host-local secrets, no destructive defaults, idempotency requirements, image pinning policy.

### Recommended
- Import-linter or equivalent for enforcing architecture contracts as a hard CI gate.
- Semgrep or equivalent for security-pattern scanning.
- Quality snapshot system for tracking quality state over time.
- Upstream lock files for tracking deployed stack versions.
- Rehearsal targets (non-production hosts) for validating high-risk playbooks before executing on protected hosts.

### Notes on AGENTS.md style at Tier 5
At this tier, AGENTS.md may legitimately be a wall of text rather than a pointer index. The governance rules — command safety classification, pre-execution requirements, role routing — are things an agent needs immediately upon arrival, not after following pointers. If the governance is concise enough to be read in full, inline is better than indirected. If it grows large, extract sections to docs and convert to a pointer index as in Tier 4.

---

## Workspace-level orientation

Each workspace root (a directory containing multiple projects) should have its own `AGENTS.md` that provides:
- What the workspace contains and how the projects relate.
- Which project handles what.
- Common operational commands (compose targets, env setup).
- No project-specific rules — those belong in each project's own AGENTS.md.

This is distinct from both the server-level `.codex/AGENTS.md` (global rules applying everywhere) and the project-level AGENTS.md.

The full hierarchy:

```
.codex/AGENTS.md                        Server-wide rules (all workspaces)
<workspace>/AGENTS.md                   Workspace orientation (layout, relations, ops)
<workspace>/_docs/governance/           Workspace-specific governance docs (see below)
<workspace>/<project>/AGENTS.md         Project front door (Tier 2–5 pointer index or inline)
<project>/_docs/rules/                  Detailed project rules (Tier 3–5)
_shared/agent-rules/                    Cross-workspace shared rules (referenced by pointer)
```

### Workspace project inventory

Tier assignments for the projects in a workspace are workspace-specific and do not belong in this shared document. Each workspace that adopts this framework must maintain its own inventory at:

```
<workspace>/_docs/governance/project-inventory.md
```

That file must contain:

1. **Repository map** — a tree diagram showing all projects in the workspace, their nesting depth, and which are independent git repos vs. inline content.
2. **Remote URL table** — one row per independent git repo: local path and remote URL.
3. **Tier assignments table** — columns: project path, tier, one-line rationale.
4. **Rationale notes** — prose explanation for any non-obvious tier choice.

It references this document for tier definitions. This separation keeps the shared framework reusable across workspaces without embedding workspace-specific content here.
