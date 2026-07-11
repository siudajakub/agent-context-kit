# CLAUDE.md

Claude Code entry point for this hackathon repository. The canonical rules are in
[AGENTS.md](AGENTS.md); read them first and do not duplicate them here.

## Session Startup

1. Read [AGENTS.md](AGENTS.md) and [HACKATHON.md](HACKATHON.md).
2. Run `python3 tools/hack_status.py` to see active worktrees, branches, and lane claims.
3. Read any overlapping record under [`docs/lanes/`](docs/lanes/README.md).
4. Load the relevant boundary from [contracts.md](docs/hackathon/contracts.md).

`SessionStart` and `PreCompact` hooks run `tools/hack_context.sh`. They surface active lanes and
remind the session to update its lane record before context compaction. The hooks are read-only.

## Parallel Agent Rules

- Give every concurrent writer a distinct branch, worktree, and non-overlapping file claim.
- Use read-only agents freely for review or research; only one writer owns a file at a time.
- A fresh-context agent reviews substantial lanes before they enter the merge train.
- Agents do not merge to `hack/integration` or `main`; the integration captain owns that action.

Keep `python3 tools/check_agent_docs.py` green after coordination-document changes.
