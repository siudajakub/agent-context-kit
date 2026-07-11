#!/bin/sh
# Read-only SessionStart/PreCompact hook. Always exits successfully.

remind=0
[ "${1:-}" = "--remind" ] && remind=1
root=${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || echo .)}

echo "Hackathon context: active feature lanes and claims"
python3 "$root/tools/hack_status.py" 2>&1 || echo "Could not aggregate lane status; inspect docs/lanes and TEAM_BOARD.md manually."

if [ "$remind" -eq 1 ]; then
  echo ""
  echo "Context compaction is imminent. Update your lane's Current State, Next Step, Verification,"
  echo "and any contract change before continuing."
fi

exit 0
