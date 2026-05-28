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

## Tier 1 — Trivial

**Characteristics:** No application code or a single script. Changes are infrequent and low-risk. A new agent or developer arriving here should be oriented in one paragraph.

### Required
- `AGENTS.md` — one paragraph: what this is, what it does, key files.
- `.gitignore` — at minimum: secrets (`.env`), OS noise (`.DS_Store`).
- Version control (`git init`).

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
- `docs/specs/` or `docs/` — record non-obvious decisions and operational specs. Even one spec document beats zero when the project has external dependencies or a defined contract.

### Required if Python code is present
- `pyproject.toml` with `[tool.ruff]` for linting (or standalone `ruff.toml`).
- `.gitignore` entries for Python caches: `__pycache__/`, `.mypy_cache/`, `.ruff_cache/`, `.benchmarks/`.

### Optional
- `requirements-static.txt` — if static analysis is useful locally.
- `.vscode/extensions.json` — if the repo is opened in VS Code regularly.

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
- `pyproject.toml` — consolidated tool config: `[tool.ruff]`, `[tool.mypy]`.
- `pytest.ini` — with `--strict-config --strict-markers` and explicit marker taxonomy.
- `requirements-dev.txt` — test and dev dependencies (pytest, coverage).
- `requirements-static.txt` — static analysis tools (ruff, mypy, bandit).
- CI workflow — at minimum: lint gate + test gate on push/PR.
- `.vscode/` — `extensions.json` and `settings.json` committed.

### Required if type checking is active
- `pyrightconfig.json` — LSP type coverage, scoped to source tree.

### Optional
- `METRICS.md` — document quality dimensions and how to run them.
- `launch.json` — VS Code debug configurations.
- Architecture docs under `docs/architecture/`.

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
- `docs/rules/` or equivalent — collected agent constraints (testing standards, definition of done, CI guardrails, operational constraints).
- `docs/specs/` — formal spec system with Architect/Implementor authority model.
- `docs/specs/invariants.md` — explicit system invariants (`INV-*` catalog).
- `docs/testing/testing-strategy.md` — behavior contracts that must remain stable under refactor.
- `docs/governance/INDEX.md` — precedence-ordered index of all authoritative documents.
- `METRICS.md` — full quality dimensions documentation.
- CI — comprehensive pipeline: lint, type check, security scan, arch guards, supply chain, build metadata verification, workspace integration smoke.
- `requirements-static.txt` — separate from `requirements-dev.txt`; includes bandit, pip-audit, pyright, vulture.

### Recommended
- `pyrightconfig.json` with strict paths matching mypy per-module strict overrides.
- `.coveragerc` — explicit coverage configuration.
- Architecture docs (`docs/architecture/`) covering system context, runtime flows, state transitions.
- Operations docs (`docs/operations/`) covering failure modes and rollout policy.

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
.codex/AGENTS.md                   Server-wide rules (all workspaces)
<workspace>/AGENTS.md              Workspace orientation (layout, relations, ops)
<workspace>/<project>/AGENTS.md    Project front door (Tier 2–5 pointer index or inline)
<project>/docs/rules/              Detailed project rules (Tier 3–5)
_docs/shared/agent-rules/          Cross-workspace shared rules (referenced by pointer)
```

---

## Projects in this ecosystem — tier assignments

| Project | Tier | Rationale |
|---|---|---|
| `scripts/` (docker root) | 1 | Single diagnostic shell script |
| `vantage_monitor/` | 1 | Two compose services, one config file, no code |
| `photos/shared/immich_common` | 1 → 2 | One Python file today; shared dependency — promote when it grows |
| `backups/` | 2 | Compose + shell scripts + small Python exporter; no tests |
| `homeautomation/` (workspace) | 2 | Workspace-level AGENTS.md and compose orchestration only |
| `photos/` (umbrella) | 2 | Orchestration layer; Makefile targets; no application code |
| `photos/immich-smart-albums` | 3 | Real Python service with tests and CI; governance depth still shallow |
| `photos/media_ingest` | 4 | Spec system, arch guards, supply-chain, comprehensive CI, full governance |
| `homeautomation/homeassistant` | 4 | Most mature; shared agent-rules; full quality pipeline |
| `stugan-iac` | 5 | IaC mutations affect real infrastructure; credential management; multi-role governance; execution evidence |

### Why `photos/media_ingest` is Tier 4, not Tier 5
The photos library is sensitive but recoverable. A bad deployment does not destroy infrastructure or expose credentials. Failures are expensive and painful but reversible. Execution governance is not warranted.

### Why `homeautomation/homeassistant` is Tier 4, not Tier 5
HomeAssistant controls physical devices and takes a long time to rebuild, but failures don't cause irreversible harm. The codebase is the most complex in the ecosystem, but complexity alone does not warrant Tier 5.

### Why `backups/` is Tier 2, not Tier 1
It has operational scripts with non-trivial behaviour (Kopia bootstrap phases, Prometheus exporter), a spec in `docs/specs/`, and a dependency on an external backup system where errors are hard to reverse. The spec and AGENTS.md are appropriate overhead.

### Why `immich-smart-albums` is Tier 3, not Tier 4
Real tests and CI, but no formal spec system, invariant catalog, arch guards, or governance index. The domain logic is contained enough that informal governance is adequate for now. Promote to Tier 4 if a phased architectural refactor becomes necessary.
