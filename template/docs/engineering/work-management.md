# Work Management

Where actionable work is tracked, and how it relates to the status docs. The split keeps each
file single-purpose so nothing has to be reconstructed from a mix of sources.

## Ownership

- **Actionable work** (tasks, priority, assignees) → the issue tracker / project board.
- **Verified state** → `PROJECT_STATUS.md`.
- **Direction** → `ROADMAP.md`.
- **Legacy / debt inventory** → `CLEANUP_STATUS.md`.
- **In-flight, not-yet-durable context** → a worklog under `docs/sessions/`.

## Tracker

- <url to the issue tracker / board>

## Conventions

- Status, roadmap, and cleanup files contain **no task checkboxes** — link the tracking issue
  instead (the docs validator enforces this).
- One issue per discrete piece of work; reference it from worklogs and commit messages.
