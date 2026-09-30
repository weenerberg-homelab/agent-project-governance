# Proposal — three development phases, and a clickable prototype as the exploratory phase

| | |
|---|---|
| **Status** | **PROPOSED** — for the Product Owner to read and decide (§11). Nothing is applied until he does |
| **Author** | Operator (paperclip_trial) |
| **Date** | 2026-09-30 |
| **Decided so far** | The Product Owner, 2026-09-30. **Q156 (yes):** the exploratory phase is a clickable HTML prototype; *"In the meantime I will continue with the EPS to complete all known views, develop the design system and a clickable prototype to traverse navigation and test the appflow."* **Q157 (a):** *"Wrap up M8 with what we have."* Asked for: *"a proposal for how we fit it in the documentation and how it affects all agents and phases of the project"* |

## 1. Why

The process today has one level of rigour, the finished-product level, for every piece of work. It builds
each screen in the real app as soon as its design reaches S9, with the full gate, the alignment pass and
review rounds each time.

| Evidence, Coach Platform | |
|---|---|
| M8 so far | About $356 spent by 2026-09-29 19:36 UTC. The result on screen: a navigation bar and a fixture-result skeleton that the Product Owner called *"an abomination"* |
| One screen built | Selection: $469 of design work, then $442 of build |
| Cards | Fifteen questions on one alignment card (WEE-370); a colour question that repainted a finished design (WEE-403 CA-Q1); per-pixel questions he did not want |
| Quota | Paperclip seats were about 63% of the Anthropic use after the plan change (plan meter, 2026-09-29) |
| His words | *"Agents shouldn't shit their virtual pants if I ask it to deploy a functional but half finished design. It should anticipate that the design will converge."* · *"When in 'Finalization' I am expecting pixel perfect."* |

A screen changes many times before it settles. Building each version costs hours and dollars. Drawing
each version in the prototype costs one design round.

## 2. The three phases

| | **Exploratory** | **Intermediate** | **Finalization** |
|---|---|---|---|
| **Goal** | See the whole product, learn what it should be | Build it, and let it converge | Release quality |
| **What is built** | **The clickable HTML prototype**: every known view, the design system, the navigation of the accepted app flow, invented data. **No new screens in the app** | The app, screen by screen, from the converged prototype | The app, finished |
| **Who does the work** | The design coordinator with the Product Owner, outside the tracker. Paperclip seats keep the deployed app running (defects only) | Paperclip seats | Paperclip seats |
| **Fidelity** | Rough is fine. It converges round by round | A built screen follows its prototype page; an image check with a tolerance | Pixel-perfect; a strict image check |
| **Requirement coverage** | One `gaps.md` for the whole prototype: what the requirements ask for that no screen shows yet | Per screen, the slim gate (C1–C3, G11) | Full gate, and the second-seat rebuild of every figure |
| **Non-functional requirements** | Only what protects data and security in the deployed app | Plus phone width, keyboard reach, visible focus | All: performance, offline, full accessibility |
| **Tests** | None for the prototype. The deployed app's own suite stays green | The logic that computes figures, the criteria per state | Every criterion, and conformance |
| **Reviews** | None for the prototype. The Product Owner judges by clicking | One review round normally; record-only defects ride the next commit | Strict: a record-only defect fails the round |
| **Cards to the Product Owner** | Almost none. The coordinator asks in the chat | Money above a ceiling, data, undecided scope, against one of his answers, the approvals DEC-002 routes to him. One-click cards when every question has a recommendation | Every gate |
| **Deploy** | The prototype is published on each round. The app: fixes only, demo data reset | Any time he says, demo data reset | Real data, no reset |

**In every phase:** no loss of real data, no secret exposed, the deployed app's CI green, and a figure the
product computes is never shown wrong without a test saying so.

## 3. The switch

- **One line in the project's decision record**, set only by the Product Owner:
  *"Phase: Exploratory, from 2026-09-30."* On Coach Platform: a new **DEC-014** in `_docs/decisions.md`.
- **Every seat sees only the current phase's column.** `paperclip_trial/tools/build_bundles.py` puts that
  column into each seat's instructions, and the coordinator template does the same. No agent has to work
  out which phase applies, or argue about it.
- **A phase change** is his line, then a bundle rebuild. It needs nothing else.

## 4. Moving between phases

| Transition | When | What happens once, at the boundary |
|---|---|---|
| **Exploratory → Intermediate** | He says so, when he has seen the system as a whole and wants it to converge | 1. **One alignment pass** (DEC-013 clause 5) for the whole prototype: the specification is aligned to it once, not once per screen. 2. Each screen's prototype page becomes its package at S9: `page-spec.md` and `acceptance-criteria.md`, and the slim gate. 3. The Architect plans the build milestones from the packages |
| **Intermediate → Finalization** | He says so, before V1 goes into real use | The non-functional requirements not yet built are listed and planned; the image check turns strict; the demo data reset stops (the field test, WEE-309, runs on real data) |
| **Back** | He can move back a phase at any time, for example for a large redesign | The current phase's rules apply from then on; nothing already built is undone |

## 5. The prototype

| | |
|---|---|
| **What** | The accepted app flow (S0, `_docs/design/app-flow/`), grown into every known view at design-system fidelity: each screen is a page, the navigation works, invented data shows each screen's states |
| **The design system** | One token set and the shared components, in one place: `_docs/design/system/`. It replaces the per-package token copies and the internal strategist's extraction pass (WEE-403, parked). Every prototype page uses it |
| **Where** | Committed to `coach-platform` by the coordinator from a generator, as the packages are today, and published as a canvas on every round, which works on a phone. Serving it on ha-02 as well is optional (§8, PH-Q2) |
| **The finished packages** | Selection and fixture-result join the prototype as pages. They are not rebuilt in the app during Exploratory |
| **The drafts** | This-week, create-fixture, players, season-setup, session, teams-schedule: they continue as prototype pages. Plan, settings and assessment start as pages from the app flow |
| **Gaps** | `gaps.md`: requirements no page shows yet. It feeds the alignment pass at the phase exit; nothing is carded during the phase |

## 6. What each seat does in each phase

| Seat | Exploratory | Intermediate | Finalization |
|---|---|---|---|
| **Product Owner** | Clicks through the prototype, gives notes in the coordinator chat, sets the phase | Judges each built screen by eye, answers the few cards | Accepts the release |
| **Design coordinator** (External Product Strategist) | Builds and revises the prototype and the design system; keeps `gaps.md` | Turns prototype pages into packages; revises designs on build findings | Pixel-level corrections |
| **Product Strategist** (internal) | Idle, except the requirement records the coordinator requests. No take-ins | The alignment pass at entry; take-ins at S9; the amendment chain | The same, strictly |
| **Architect** | Keeps the deployed app running; plans nothing new. Reads the prototype when asked for a feasibility opinion | Plans and reviews the build from the packages | The same, plus the non-functional requirements |
| **Implementor** | Defects in the deployed app only | Builds | Builds and fixes to the strict check |
| **Product Advisor, Architecture Advisor** | Idle | Review, one round normally | Review, strict |
| **Product Assistant** | Merges what DEC-002 routes to it | The same | The same |
| **Operator and the host watcher** | Watches the idle board without waking seats to invent work; no design take-ins opened | Take-ins, brakes and budgets as today | The same, plus the release |

## 7. What changes in the documents

**Governance (`_shared/agent-project-governance`, one pull request, the Product Owner merges):**

| File | Change |
|---|---|
| `governance/20-development_iteration.md` | A new section, *Development phases*: the table in §2, the switch in §3 and the transitions in §4. It is the one home of the phase rules |
| `governance/90-design-delivery.md` | §1 and §6: the stage table applies from Intermediate. A new §6.8, *The exploratory prototype*: S0 grows into the prototype; `gaps.md` instead of per-screen coverage; no take-ins. §12: the design system lives in `_docs/design/system/` and is built in Exploratory, not extracted after a build |
| `governance/70-review-and-release.md` | *Board cards* and *Reviews, rework and acceptance*: which cards and review rounds apply in which phase, by reference to the table |
| `governance/10-agents_workflow.md` | Each role gains its per-phase line from §6 |
| `governance/40-agent_prompts.md` | The design coordinator template reads the phase and, in Exploratory, runs the prototype; a new *Exploratory prototype session* task block |
| `skills/design-delivery`, `skills/review-and-release` | Regenerated in the same pull request |

**Coach Platform (`coach-platform`, through the usual product route):**

| File | Change |
|---|---|
| `_docs/decisions.md` | **DEC-014**: the project adopts the phases and records *Phase: Exploratory, from 2026-09-30*. DEC-013 is kept; its clause 5 alignment runs once per phase exit while in Exploratory |
| `_docs/design/system/` | New: the design system (tokens, components, type), built by the coordinator |
| `_docs/design/prototype/` or the app-flow package | The prototype's generator and pages (§8, PH-Q3) |
| `_docs/v1a-milestones.md`, `roadmap.md` | M8 closed as wrapped up; the next build milestone opens at Intermediate |

**Paperclip trial (`paperclip_trial`, a commit is a deploy):**

| File | Change |
|---|---|
| `bundles/project.md` | The per-phase rules as three blocks; the *prototype phase* rule of 2026-09-30 becomes the Exploratory block; *a built screen follows its design exactly* applies from Intermediate |
| `tools/build_bundles.py` | Reads the phase from DEC-014 and puts only that block into each seat's instructions |
| `tools/quota_watcher.py` | In Exploratory: no design take-ins, and the idle-board check does not wake seats to find work |
| `_docs/operator/PROMPT-015` | A one-paste coordinator prompt for the prototype |

## 8. Decide

- **PH-Q1 — adopt the phases, with the switch in your hands.** **Recommended: (a) yes.** What changes: §7,
  in three pull requests or commits, in the order governance, then Coach Platform, then the trial.
  The cost of (b), no: the prototype work goes on without a rule, and the seats keep applying the
  finished-product rigour to everything.
- **PH-Q2 — where you open the prototype.** **Recommended: (a) the published canvas**, which the
  coordinator already produces on every round and which works on your phone. (b) also serve it on ha-02
  next to the app: one small deploy step, and a stable address you can bookmark.
- **PH-Q3 — where the prototype lives in the repository.** **Recommended: (a) grow the app-flow package**
  into the prototype, because it already holds the clickable flow and its generator. (b) a new
  `_docs/design/prototype/` that reads the packages. It keeps them apart, and it is one more generator.

## 9. Risks

| Risk | What limits it |
|---|---|
| The prototype drifts from what can be built | The Architect gives a feasibility opinion when asked; the one alignment pass at the phase exit catches the rest, in one place |
| The alignment pass at the phase exit is large | One pass costs less than one per screen. WEE-370 alone had fifteen questions for one screen |
| The deployed app goes stale during Exploratory | It is not what you look at in Exploratory. It keeps running, with defects fixed |
| Rigour is lost for good | Finalization restores all of it, and it is written down here, not left to memory |

**End of proposal**
