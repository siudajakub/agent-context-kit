# Agent Context Kit

A portable, project-agnostic system that lets coding agents — Claude Code, Codex, or humans —
**carry context across sessions** and **coordinate several sessions at once** without colliding.

It is a small set of Markdown docs plus a little automation. Drop it into any repository and you
get: one canonical rules file every agent reads first, a dated status snapshot, cross-session
worklogs, hooks that surface other sessions' work automatically, and a validator that keeps the
whole thing from rotting.

It ships in two profiles:

- **standard** — durable project memory for ongoing repositories (the original kit),
- **hackathon** — a time-boxed team operating system for parallel feature lanes, worktrees,
  contract-first fan-out, a single merge train, and a rehearsed demo.

## Hackathon profile (v2)

The hackathon profile is deliberately more operational than the standard kit. It assumes several
humans and agents are shipping at once, the deadline is fixed, and integration risk matters more
than long-lived documentation.

| Need | Mechanism |
| --- | --- |
| Split work without collisions | One `hack/<owner>/<feature>` lane and sibling worktree per writer |
| Keep frontend/backend or service lanes compatible | Frozen examples and failure behavior in `docs/hackathon/contracts.md` |
| See local and remote work | `tools/hack_status.py` aggregates worktrees and fetched `hack/*` refs |
| Preserve cold-resume context | One branch-local record under `docs/lanes/` per feature |
| Keep integration runnable | Captain-owned `hack/integration` merge train; `main` stays demo-safe |
| Avoid late scope collapse | Absolute freezes, fallback/cut plan, and golden path in `HACKATHON.md` |
| Survive demo failures | Exact artifact, reset commands, deterministic fixtures, and backup in the demo runbook |

After the captain defines `AVAILABLE` rows in `TEAM_BOARD.md`, each contributor runs:

```bash
python3 tools/hack_join.py
```

The onboarding shows the project mission and unclaimed work, then asks the contributor to select
a lane. It creates `hack/<owner>/<feature>`, a sibling worktree, and a lane handoff prefilled with
the documented acceptance, claim, and dependencies. Before queueing the work for integration,
run `sh tools/hack_ready.sh`; it checks branch freshness, a clean tree, conflict markers,
documentation integrity, and optionally a command passed after `--`.

The model works on one machine without a server. For a distributed team, commit the lane record,
push a draft PR early, and run `git fetch --all --prune` before `tools/hack_status.py` so remote
claims are visible too.

---

## The problem it solves

Coding agents are stateless between sessions and blind to each other. That produces three failures:

1. **Context evaporates.** A new session (or one whose context was compacted) re-derives what the
   project is, what's already done, and what was mid-flight — slowly and often wrongly.
2. **Sessions collide.** Two agents (or an agent and you) edit the same files in parallel and race
   on the Git index, or silently undo each other's work.
3. **Docs rot.** Scattered notes drift out of date until no one trusts them, so everyone re-reads
   the code instead.

The kit fixes each one with a specific mechanism: **layered docs** for durable knowledge, **dated
snapshots** for current truth, **worklogs** for in-flight context, **hooks** for awareness, and a
**validator** for trust.

---

## How it works

### The four layers of memory

Each piece of knowledge has exactly one home, chosen by how fast it changes. Nothing has to be
reconstructed from a mix of sources.

```
                         lifespan        home                              who writes it
  ┌───────────────────┬──────────────┬─────────────────────────────────┬──────────────────┐
  │ Durable knowledge │ months       │ AGENTS.md, docs/engineering/*   │ rarely, by hand  │
  │ Current truth     │ days–weeks   │ PROJECT_STATUS.md               │ after verifying  │
  │ In-flight context │ hours–a day  │ docs/sessions/<worklog>.md      │ live, as you work│
  │ Awareness         │ per session  │ injected by hooks (no file)     │ automatic        │
  └───────────────────┴──────────────┴─────────────────────────────────┴──────────────────┘
```

- **Durable knowledge** — the rules, commands, architecture, and review gate. `AGENTS.md` is the
  one file every agent reads first; the `docs/engineering/*` files hold the detail it links to.
  Agent-agnostic on purpose, so Claude, Codex, and humans share one source of truth.
- **Current truth** — `PROJECT_STATUS.md` is a *dated, verified* snapshot of what is actually true
  in the tree right now, including what was and wasn't checked. It is not a backlog and not a wish
  list. `ROADMAP.md` (direction) and `CLEANUP_STATUS.md` (debt inventory) sit beside it.
- **In-flight context** — a worklog under `docs/sessions/` is the handoff note a session would want
  if it resumed cold: goal, the files it has claimed, decisions, current state, next step. Written
  while you work, **pruned when the work lands**. Working memory, never a backlog.
- **Awareness** — no file of its own. Hooks read the active worklogs and inject them into each new
  session, so coordination is not left to anyone remembering to look.

### The lifecycle of a session

```
  SessionStart hook ──▶ injects active worklogs ──▶ agent sees who's touching what
        │
        ▼
  read AGENTS.md ──▶ read PROJECT_STATUS.md ──▶ read task-specific docs/engineering/*
        │
        ▼
  non-trivial work?  ──▶  sh tools/session_new.sh <slug>   (claim your files)
        │
        ▼
  ...work, keeping the worklog's Current State / Next Step current...
        │
        ▼
  PreCompact hook ──▶ "flush your worklog before context is summarized"
        │
        ▼
  done ──▶ fold durable facts into PROJECT_STATUS.md ──▶ open issues for follow-ups ──▶ delete worklog
```

### The automation

Three small, dependency-light pieces make the loop run without anyone remembering to:

- **`.claude/settings.json`** wires two Claude Code hooks:
  - `SessionStart` runs `tools/session_context.sh`, which lists the active worklogs and injects
    them into the session — so every session opens already aware of parallel work.
  - `PreCompact` runs the same script with `--remind`, nudging the session to write its current
    state into its worklog **before** the context window is summarized and detail is lost.
  - The script is read-only and always exits 0, so it can never block or break a session.
- **`tools/session_new.sh <slug>`** scaffolds a dated worklog from `docs/sessions/TEMPLATE.md` with
  the date and current branch prefilled — one file per session, so parallel sessions never share a
  file.
- **`tools/check_agent_docs.py`** is the trust anchor. It verifies the required docs exist, their
  internal links resolve, `AGENTS.md` stays within its line budget, the status files carry no stray
  task checkboxes (tasks belong in the tracker), and the `SessionStart`/`PreCompact` hooks are
  actually wired. Run it in CI or a pre-commit hook and the system can't silently drift.

### Parallel sessions use separate worktrees

Two sessions in one checkout share a Git index and **will race** on `git add`/commit. For genuine
parallel work, each session gets its own **git worktree** — a sibling directory on its own branch.
Worklogs are committed, so a worktree on another machine sees the same claims. See
[`docs/sessions/README.md`](template/docs/sessions/README.md) for the full protocol.

---

## What's in the box

| File | Layer | Holds |
| --- | --- | --- |
| `AGENTS.md` | Canonical rules (read first) | Product framing, core invariants, commands, definition of done. Agent-agnostic. |
| `CLAUDE.md` | Tool entry point | Points to AGENTS.md; adds Claude- and multi-session specifics only. |
| `PROJECT_STATUS.md` | Verified snapshot | What is true in the tree *right now*, dated, with what was checked. |
| `ROADMAP.md` | Direction | Durable product direction. No task tracking. |
| `CLEANUP_STATUS.md` | Debt inventory | Factual record of legacy / known-debt surface. |
| `docs/engineering/architecture.md` | Reference | Module ownership and dependency boundaries. |
| `docs/engineering/verification.md` | Reference | Exact build/test commands and the check matrix. |
| `docs/engineering/code-review.md` | Reference | Fresh-context review rule and merge gate. |
| `docs/engineering/work-management.md` | Reference | Where actionable work is tracked vs. the status docs. |
| `docs/sessions/README.md` + `TEMPLATE.md` | **Cross-session memory** | The worklog protocol and a worklog template. |
| `tools/session_new.sh` | Automation | Scaffolds a dated worklog with branch prefilled. |
| `tools/session_context.sh` | Automation | Injects active worklogs; reminds you to flush before compaction. |
| `tools/check_agent_docs.py` | Automation | Validates docs, links, the AGENTS.md line limit, and hook wiring. |
| `.claude/settings.json` | Automation | `SessionStart` + `PreCompact` hooks that run `session_context.sh`. |

The standard profile ships under `template/` and the hackathon profile under
`template-hackathon/`; the files at the repo root (`README.md`, `install.sh`, `LICENSE`) are the
kit itself, not part of what gets installed.

---

## Install

From the target project's root:

```bash
sh /path/to/agent-context-kit/install.sh . --name "My Project"
```

For a hackathon team:

```bash
sh /path/to/agent-context-kit/install.sh . --profile hackathon --name "My Project"
```

Or point it at any directory:

```bash
sh /path/to/agent-context-kit/install.sh ~/code/my-project --name "My Project"
```

- `--name` replaces the `{{PROJECT_NAME}}` placeholder in copied files. Omit it to edit by hand.
- `--profile` selects `standard` (default) or `hackathon`.
- Files that already exist are **never overwritten**; the kit's version is written as `<file>.kit`
  next to it so you can merge (handy when the repo already has a `CLAUDE.md` or
  `.claude/settings.json`). Pass `--force` to overwrite instead.

You can also copy the selected template directory's contents into the repo by hand — the script adds
convenience (placeholder substitution, sidecars for existing files, `chmod +x`).

### After installing

1. Fill in `AGENTS.md`: **Product**, **Core Rules**, and **Commands** for this project. This is the
   one file every agent reads first — make it accurate and keep it under the line limit.
2. Replace the `<placeholders>` in `PROJECT_STATUS.md`, `ROADMAP.md`, and `docs/engineering/*`.
3. Run the validator and keep it green:

   ```bash
   python3 tools/check_agent_docs.py
   ```

4. Commit. The hooks activate on the next Claude Code session.

For the hackathon profile, fill `HACKATHON.md`, assign the integration captain, create
`hack/integration`, freeze the first cross-lane contracts, and define `AVAILABLE` work in
`TEAM_BOARD.md`. Each contributor then runs `python3 tools/hack_join.py`. The full cadence is in
`docs/hackathon/playbook.md` after installation.

---

## Daily use

- Starting non-trivial work? Scaffold a worklog and claim your files:

  ```bash
  sh tools/session_new.sh <short-topic-slug>
  ```

- Running two sessions at once? Give each its own **git worktree** (sibling directory) so they do
  not race on the Git index.
- Finishing? Fold durable facts into `PROJECT_STATUS.md`, push follow-ups to the issue tracker,
  then delete the worklog. Worklogs are working memory, not a backlog.

---

## Customizing the validator

`tools/check_agent_docs.py` keeps its tunables at the top: `REQUIRED_FILES`, `REQUIRED_TOOLS`,
`AGENTS_MAX_LINES`, and `STATUS_FILES`. Add a doc to `REQUIRED_FILES` to have its existence and
internal links checked. Wire the validator into CI or a pre-commit hook to keep the system honest.

## Notes

- The shell scripts are POSIX `sh` and rely only on `git`, `sed`, `awk`, and coreutils.
- `tools/session_context.sh` resolves the repo via `$CLAUDE_PROJECT_DIR` (set by Claude Code) and
  is read-only — it never blocks a session and always exits 0.
- Nothing here is Claude-only except `.claude/settings.json` and `CLAUDE.md`; `AGENTS.md` and the
  worklog protocol work for any agent that reads the repo.

## License

[MIT](LICENSE). Use it, fork it, adapt it.

## Author

Created and maintained by [Jakub Siuda](https://www.siuda.dev/about/), a 42 Warsaw student building AI products, developer tools and agent workflows.

[Portfolio](https://www.siuda.dev/) · [GitHub profile](https://github.com/siudajakub)
