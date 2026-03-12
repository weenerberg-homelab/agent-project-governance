# Upstream Promotion Workflow Pattern

## Purpose

Define a pragmatic but governed workflow for promoting a service-config change from a workspace repo into `iac` and then into live deployment.

This pattern supports an operating model where:
- live-first service development may occur outside governed IaC mode
- governed state is restored by promoting an immutable upstream ref into `iac`
- `iac` remains the deployment control plane

## When this pattern applies

Use this pattern when:
- service or stack configuration is authored in a repo outside the main `iac` repo
- operators want fast live-first iteration during development
- the project still requires a governed deploy path and a clear declared source of truth

Do not use this pattern to justify permanent unmanaged drift.

## P1 — Two-mode operating model

There are two distinct modes:

### Live development mode
- work occurs in the service or stack workspace repo, for example:
  - `~/infra/<repo>/`
- changes may be tested directly against the live host
- during this period, `iac` is temporarily not the live source of truth

### Governed promotion mode
- an immutable upstream ref is selected
- the `iac` pin is updated to that ref
- governed deploy runs from `iac`
- after successful deploy, `iac` becomes the live declared source of truth again

## P2 — Source-of-truth boundaries

For a stack using upstream promotion:

- the upstream service repo owns:
  - authoring of service or stack config
  - commits, tags, releases

- `iac` owns:
  - the pinned deployed ref
  - the governed deploy path
  - the declared live state after promotion succeeds

The service repo is not the deployment control plane.
`iac` remains the deployment control plane.

## P3 — Immutable promotion requirement

Governed promotion MUST use an immutable upstream ref:
- tag
- commit SHA
- equivalent immutable identifier

Branch heads or floating refs MUST NOT be used as the governed deployed ref.

## P4 — Promotion front door

A common promotion command MAY exist, for example:
- `make <project> promote`
- a shared promotion wrapper
- a governed release helper

This front door is allowed to orchestrate:
1. service-repo checks or tests
2. immutable tag/ref selection or creation
3. `iac` pin update
4. governed deploy from `iac`

This command is a front door only.
It does not replace `iac` as the deployment control plane.

## P4a — Manual promotion is allowed

A shared promotion front door is optional.

Until a shared front door exists, operators MAY execute the promotion workflow manually, provided the same governed order is preserved:

1. run upstream checks or tests as needed
2. create or select an immutable upstream ref
3. move to the `iac` control plane repo
4. reconcile the selected immutable ref into `iac`
5. review and commit the explicit `iac` pin/materialization change
6. run governed validation from `iac`
7. run governed deploy from `iac`

Example manual shape:
- create or select a tag or commit SHA in the upstream repo
- run `ops reconcile-upstream <site> <host> <ref> [upstream-repo-url]` in `iac`
- review the materialized diff and updated lock/pin record
- run `ops validate <site> <host>`
- run `ops deploy <site> <host>`

This manual path is a valid governed promotion flow.

It does not weaken the core rules:
- immutable refs only
- explicit `iac` pin update
- fail-closed ordering
- governed deploy occurs through `iac`

## P5 — Fail-closed ordering

Promotion MUST fail closed.

Minimum required order:
1. run checks or tests
2. create or select immutable ref
3. update `iac` pin
4. run governed deploy from `iac`

If any step fails:
- stop immediately
- do not continue to later steps
- do not treat the release as governed or promoted

## P6 — No direct deploy from service repo in governed mode

The promotion workflow MUST NOT treat direct deploy from the service repo as the governed deployment step.

The service repo may be used for live-first development outside governed IaC mode.
But governed promotion deploy MUST occur through `iac`.

## P7 — Required promotion record

A promotion run MUST make reviewable at minimum:
- upstream repo identifier
- promoted immutable ref
- updated `iac` pin target
- governed deploy result

## P8 — Drift model

Before governed promotion completes:
- live may be ahead of `iac`

After governed promotion completes successfully:
- `iac` is authoritative again for the deployed stack state

This drift model must remain explicit and must not be hidden.

## P9 — Minimal coupling rule

Service repos SHOULD NOT need to know the internal `iac` file layout beyond what is required by the promotion interface.

Preferred shape:
- a shared promotion tool or wrapper updates the pin and triggers deploy
- not per-service custom logic that edits `iac` internals directly

## P10 — Acceptance

A promotion workflow is acceptable when:
- immutable refs are used
- `iac` pin update is explicit
- governed deploy runs through `iac`
- failure is fail-closed
- declared state returns to `iac` after successful promotion

## Related integration points

Project-specific docs may reference this pattern from:
- architecture overview/spec
- operator interface spec
- runbook
- acceptance checklist

Those project-specific docs may add concrete commands, paths, and evidence expectations, but they should not weaken this pattern.
