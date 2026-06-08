# `_docs/` Directory Layout

## Purpose

Define the internal layout of the `_docs/` directory at each project tier.
The tier doc (`10-project-structure-tiers.md`) governs *which* `_docs/` subdirs are required;
this document governs *what goes inside them*.

---

## Invariants (all tiers)

- `_docs/` is the per-project documentation root. Never use `docs/` (no underscore) at project level.
- `_docs/INDEX.md` is required at Tier 3 and above. At Tier 2 it is recommended once more than one spec exists.
- Spec packs live under `_docs/specs/`. Each pack is a directory named `YYYY-MM-DD_<slug>/`.
- Completed or superseded packs move to `_docs/specs/done/` rather than being deleted.
- Do not put working notes, scratch files, or agent-session output in `_docs/`. Those belong in `_todos/`.

---

## Tier 2 — Low

`_docs/` contains only specs. Each spec is a flat markdown file; no subdirectory structure required.

```
_docs/
├── INDEX.md                          # recommended once >1 spec exists
└── specs/
    └── YYYY-MM-DD-<slug>.md          # flat spec file; no subdirectory
```

**Naming:** `YYYY-MM-DD-<slug>.md` — date prefix, hyphen-separated slug.
**No role separation** is required at this tier. One file per topic is the norm.

---

## Tier 3 — Intermediate

Specs become directories (packs) to allow a spec file and implementation notes to coexist.
Architecture docs appear if the project has non-obvious structural decisions.

```
_docs/
├── INDEX.md
├── architecture/                     # optional; add when structural decisions need documenting
│   └── <topic>.md
└── specs/
    ├── YYYY-MM-DD_<slug>/
    │   ├── spec.md                   # single authoritative spec document
    │   └── impl_notes.md             # implementor working notes (non-authoritative)
    └── done/
        └── YYYY-MM-DD_<slug>/        # completed/superseded packs archived here
```

**Naming:** `YYYY-MM-DD_<slug>/` — date prefix, underscore separator, hyphen-separated slug.
**No role subdirectories** at this tier. A single `spec.md` owned by whoever wrote it is sufficient.

---

## Tier 4 — High

Full spec pack structure with role-based subdirectories per `governance/10-agents_workflow.md`.
All major subdirectories are established; the governance workflow is in force.

```
_docs/
├── INDEX.md
├── invariants.md                     # cross-project invariant catalog (INV-*)
├── architecture/                     # system context, runtime flows, state transitions
│   └── <topic>.md
├── specs/
│   ├── YYYY-MM-DD_<slug>/
│   │   ├── 10-product/               # Product Owner documents (authoritative)
│   │   │   ├── 10-product-spec.md
│   │   │   ├── 20-invariant-spec.md
│   │   │   └── 40-implementation-roadmap.md
│   │   ├── 20-architect/             # Architect documents (authoritative)
│   │   │   └── to_implementor/
│   │   │       ├── 30-architecture-spec.md
│   │   │       └── 90-acceptance-checklist.md
│   │   └── 30-implementor/           # Implementor working notes (non-authoritative)
│   │       └── to_architect/
│   │           └── impl_notes.md
│   └── done/
│       └── YYYY-MM-DD_<slug>/
├── rules/                            # agent constraints, testing standards, definition of done
│   └── agent-constraints.md
├── testing/                          # behavior contracts, coverage map
│   └── testing-strategy.md
├── governance/                       # precedence-ordered governance index
│   └── INDEX.md
└── operations/                       # failure modes, rollout policy
    └── failure-modes.md
```

**See** `governance/10-agents_workflow.md` for full detail on role ownership, document contents,
handoff format, and the workflow loop.

### Lightweight pack variant

Not every spec requires the full role subdirectory structure. A flat layout is acceptable when:
- the spec has a single author (no formal Architect/Implementor handoff)
- the scope is small enough that role separation adds no clarity
- there are no implementor back-channel notes or cross-role amendments

Flat packs place files directly in the pack directory without role subdirs:

```
_docs/specs/YYYY-MM-DD_<slug>/
├── 10-product-spec.md
├── 20-architecture.md        # optional
└── 30-implementation-plan.md # optional
```

Use the full role structure when: the spec involves phased implementation, multiple contributors,
formal Architect/Implementor handoffs, or execution warrants.

**Optional subdirectories** (add when genuinely needed):
- `_docs/archive/` — large retired content that is too large for `done/` (e.g. superseded design epochs)
- `_docs/reports/` — generated reports and SLO snapshots
- `_docs/workflow/` — process docs that don't fit governance or operations

---

## Tier 5 — Critical

Same structure as Tier 4. The following are additionally required:

- `_docs/specs/<pack>/` execution evidence artifacts per spec (what was run, from what commit, against what target, with what outcome).
- `_docs/governance/INDEX.md` must include the execution governance lane definitions.

---

## Spec pack naming convention

| Element | Format | Example |
|---|---|---|
| Date | `YYYY-MM-DD` | `2026-03-11` |
| Separator | `_` (underscore) | |
| Slug | lowercase, hyphen-separated | `custom_components` |
| Full name | `YYYY-MM-DD_<slug>` | `2026-03-11_custom_components` |

The date is the date the spec work was initiated, not completed. It is immutable once the directory is created.

---

## `_docs/INDEX.md` format

`INDEX.md` at the `_docs/` root is a navigation aid, not an authority document.
It should list available subdirectories and their purpose in a table. Example:

```markdown
# Documentation Index — <project>

| Resource | Path |
|---|---|
| Architecture | `_docs/architecture/` |
| Specs | `_docs/specs/` |
| Rules | `_docs/rules/` |
| Testing | `_docs/testing/` |
| Governance | `_docs/governance/INDEX.md` |
| Operations | `_docs/operations/` |
```
