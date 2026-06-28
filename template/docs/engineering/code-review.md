# Code Review

The writer/reviewer rule and the merge gate for substantial changes.

## When A Review Is Required

Any substantial change — new behavior, cross-module edits, data/schema changes, or anything risky
— gets a review before merge. Trivial, self-contained edits may skip it.

## Writer / Reviewer Rule

- The review happens in **fresh context** — a separate session or agent that did not write the
  change — so the reviewer is not anchored to the author's assumptions.
- The reviewer checks: correctness, adherence to the AGENTS.md core rules, architecture
  boundaries, test coverage, and that verification actually ran (not just that it was claimed).

## Parallel Writers

- Parallel writers use **separate worktrees** and must not edit the same files concurrently.
- Two sessions in one checkout share a Git index and will race on `git add`/commit.

## Merge Gate

- Definition Of Done (AGENTS.md) is met.
- Required checks (verification.md) pass and are reported.
- No unrelated churn in the diff.
