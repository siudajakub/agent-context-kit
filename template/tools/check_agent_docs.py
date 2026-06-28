#!/usr/bin/env python3
"""Validate the agent context/memory docs and their automation wiring.

Run from the repository root: `python3 tools/check_agent_docs.py`.
Keep this green after documentation changes. It checks that the required docs exist, that their
internal markdown links resolve, that AGENTS.md stays within its line budget, that the status
files carry no task checkboxes (those belong in the issue tracker), that the session scripts
exist, and that the SessionStart/PreCompact hooks run tools/session_context.sh.

Adapt the tunables below (REQUIRED_FILES, AGENTS_MAX_LINES, STATUS_FILES) to your project.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

# Docs that must exist and whose internal links must resolve.
REQUIRED_FILES = (
    "AGENTS.md",
    "CLAUDE.md",
    "PROJECT_STATUS.md",
    "ROADMAP.md",
    "CLEANUP_STATUS.md",
    "docs/engineering/architecture.md",
    "docs/engineering/verification.md",
    "docs/engineering/code-review.md",
    "docs/engineering/work-management.md",
    "docs/sessions/README.md",
    "docs/sessions/TEMPLATE.md",
)

# Automation that backs the cross-session memory.
REQUIRED_TOOLS = (
    "tools/session_context.sh",
    "tools/session_new.sh",
)
SETTINGS_FILE = ".claude/settings.json"
REQUIRED_HOOK_EVENTS = ("SessionStart", "PreCompact")

# Files that record state and must not grow a task list (the tracker owns tasks).
STATUS_FILES = ("PROJECT_STATUS.md", "ROADMAP.md", "CLEANUP_STATUS.md")

# AGENTS.md is the always-loaded canonical file; keep it short. Detail goes in docs/engineering/.
AGENTS_MAX_LINES = 140

LINK_PATTERN = re.compile(r"(?<!!)\[[^]]+\]\(([^)]+)\)")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate_markdown_links(path: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for target in LINK_PATTERN.findall(text):
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        clean_target = target.split("#", 1)[0]
        if not clean_target:
            continue
        resolved = (path.parent / clean_target).resolve()
        if not resolved.exists():
            fail(errors, f"{path.relative_to(ROOT)}: broken local link: {target}")


def validate_session_hooks(errors: list[str]) -> None:
    settings_path = ROOT / SETTINGS_FILE
    if not settings_path.is_file():
        fail(errors, f"missing {SETTINGS_FILE}: the SessionStart/PreCompact hooks live here")
        return
    try:
        settings = json.loads(settings_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(errors, f"{SETTINGS_FILE}: invalid JSON ({exc})")
        return
    hooks = settings.get("hooks", {})
    for event in REQUIRED_HOOK_EVENTS:
        groups = hooks.get(event)
        if not groups:
            fail(errors, f"{SETTINGS_FILE}: missing {event} hook")
            continue
        commands = [
            entry.get("command", "")
            for group in groups
            for entry in group.get("hooks", [])
        ]
        if not any("session_context.sh" in command for command in commands):
            fail(errors, f"{SETTINGS_FILE}: {event} hook must run tools/session_context.sh")


def main() -> int:
    errors: list[str] = []
    for relative in REQUIRED_FILES:
        path = ROOT / relative
        if not path.is_file():
            fail(errors, f"missing required document: {relative}")
            continue
        validate_markdown_links(path, errors)

    for relative in REQUIRED_TOOLS:
        if not (ROOT / relative).is_file():
            fail(errors, f"missing required tool: {relative}")

    validate_session_hooks(errors)

    agents = ROOT / "AGENTS.md"
    if agents.is_file() and len(agents.read_text(encoding="utf-8").splitlines()) > AGENTS_MAX_LINES:
        fail(errors, f"AGENTS.md exceeds the {AGENTS_MAX_LINES}-line project limit")

    for relative in STATUS_FILES:
        path = ROOT / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if re.search(r"^- \[[ xX]\]", text, re.MULTILINE):
            fail(errors, f"{relative}: task checkbox found; track tasks in the issue tracker")

    if errors:
        print("Agent documentation validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Agent documentation validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
