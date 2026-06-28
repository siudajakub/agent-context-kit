# {{PROJECT_NAME}} Agent Guide

Canonical, agent-agnostic rules for this repository. Every agent — Claude, Codex, or human —
reads this first. Tool-specific entry points (e.g. [CLAUDE.md](CLAUDE.md)) add only their own
specifics and must not duplicate this file. When a rule changes, edit this file.

## Product

<One paragraph: what this project is, who it is for, and the design bias that should guide every
change — e.g. "prefer small, targeted changes that preserve the existing architecture over broad
rewrites.">

## Read First

- [Architecture](docs/engineering/architecture.md) for module ownership and dependency boundaries.
- [Verification](docs/engineering/verification.md) before selecting checks or claiming completion.
- [Code review](docs/engineering/code-review.md) before merging a substantial change.
- [Work management](docs/engineering/work-management.md) before adding or changing task tracking.
- [Project status](PROJECT_STATUS.md) for the latest verified snapshot.
- [Roadmap](ROADMAP.md) for product direction. The issue tracker owns actionable work.
- [Sessions protocol](docs/sessions/README.md) before running alongside other sessions or worktrees.

## Context Loading

Always read this file first. Then list `docs/sessions/` and read any worklog whose claim
overlaps your task, so you do not collide with a parallel session.

Before implementation, read the linked project docs that match the task:

- Architecture or module-boundary changes: `docs/engineering/architecture.md`.
- Build, test, CI, release, or verification changes: `docs/engineering/verification.md`.
- Backlog, board, roadmap, or status changes: `docs/engineering/work-management.md`.
- Large changes before merge: `docs/engineering/code-review.md`.

For broad, unclear, or cross-cutting tasks, read every file in `docs/engineering/` before editing.

## Core Rules

<Project-specific invariants. Replace these examples with yours — these are the rules an agent
must never break.>

- Preserve module boundaries; keep data and service logic out of the presentation layer.
- Reuse existing modules, repositories, and shared utilities instead of adding parallel ones.
- Do not introduce a second source of truth for state that already has one.
- Do not hardcode user-facing strings or styling that belong in the shared layer.
- Work with existing uncommitted changes; never revert unrelated user work.

## Commands

<The exact build/test/lint commands for this project. Agents use these verbatim — do not invent
new ones. Replace the placeholders.>

```bash
<install>     # e.g. npm install
<build>       # e.g. npm run build
<test>        # e.g. npm test
python3 tools/check_agent_docs.py
```

## Definition Of Done

- The requested behavior works across every affected entry point.
- Relevant tests are added or updated and fresh checks pass.
- User-visible behavior, architecture, and project status docs are updated when affected.
- The final diff contains no unrelated churn, debug artifacts, or stale generated files.
- Substantial changes receive a fresh-context review following `docs/engineering/code-review.md`.

## Parallel Sessions

- One worktree per concurrent writer; never edit the same files from two sessions at once.
- Keep a worklog under `docs/sessions/` for work that spans sittings or runs in parallel; scan
  that directory for overlapping claims before starting.
- Fold durable facts into `PROJECT_STATUS.md` and follow-ups into the issue tracker, then prune
  the worklog. See [docs/sessions/README.md](docs/sessions/README.md).

## Working Mode

- During planning, clarify intent and major tradeoffs.
- During execution, deliver the complete change, including adjacent integration and verification.
- Pause only for destructive work or decisions with materially different consequences.
