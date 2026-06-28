#!/bin/sh
# Install the agent-context kit into a target project.
#
# Usage:
#   sh install.sh [target-dir] [--name "Project Name"] [--force]
#
#   target-dir    Where to install (default: current directory).
#   --name NAME   Replace the {{PROJECT_NAME}} placeholder in copied files.
#   --force       Overwrite files that already exist (default: skip and report them).
#
# The kit is copied file-by-file. Existing files are left untouched unless --force is given, so it
# is safe to run inside a project that already has a CLAUDE.md or .claude/settings.json — those are
# reported and skipped, and the kit's versions are written next to them as *.kit so you can merge.

set -eu

KIT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
SRC="$KIT_DIR/template"

target="."
name=""
force=0

while [ $# -gt 0 ]; do
  case "$1" in
    --name) name="${2:-}"; shift 2 ;;
    --name=*) name="${1#--name=}"; shift ;;
    --force) force=1; shift ;;
    -h|--help) sed -n '2,12p' "$0"; exit 0 ;;
    -*) echo "unknown option: $1" >&2; exit 2 ;;
    *) target="$1"; shift ;;
  esac
done

if [ ! -d "$SRC" ]; then
  echo "missing template directory: $SRC" >&2
  exit 1
fi
mkdir -p "$target"
target=$(CDPATH= cd -- "$target" && pwd)

if [ "$target" = "$KIT_DIR" ]; then
  echo "refusing to install the kit into itself" >&2
  exit 1
fi

copied=0
skipped=0
sidecar=0

# Substitute {{PROJECT_NAME}} in a file when --name was given.
apply_name() {
  [ -n "$name" ] || return 0
  esc=$(printf '%s' "$name" | sed -e 's/[&|\\]/\\&/g')
  sed "s|{{PROJECT_NAME}}|$esc|g" "$1" > "$1.tmp" && mv "$1.tmp" "$1"
}

# Copy every file under template/, preserving structure, including dotfiles like .claude/.
find "$SRC" -type f | while IFS= read -r file; do
  rel=${file#"$SRC/"}
  dest="$target/$rel"
  mkdir -p "$(dirname -- "$dest")"

  if [ -e "$dest" ] && [ "$force" -eq 0 ]; then
    cp "$file" "$dest.kit"
    apply_name "$dest.kit"
    echo "  exists, wrote sidecar: $rel.kit  (merge into your $rel)"
    sidecar=$((sidecar + 1))
    continue
  fi

  cp "$file" "$dest"
  apply_name "$dest"
  case "$rel" in
    tools/*.sh|tools/*.py) chmod +x "$dest" ;;
  esac
  echo "  installed: $rel"
  copied=$((copied + 1))
done

# The subshell above runs in a pipe, so re-derive the counts for the summary.
copied=$(find "$SRC" -type f | while IFS= read -r f; do
  rel=${f#"$SRC/"}; [ -e "$target/$rel" ] && [ ! -e "$target/$rel.kit" ] && echo x; done | wc -l | tr -d ' ')
sidecar=$(find "$SRC" -type f | while IFS= read -r f; do
  rel=${f#"$SRC/"}; [ -e "$target/$rel.kit" ] && echo x; done | wc -l | tr -d ' ')

echo ""
echo "Done. Installed into: $target"
echo "  files written:  $copied"
[ "$sidecar" -gt 0 ] && echo "  sidecars (.kit): $sidecar  — files that already existed; merge by hand"
echo ""
echo "Next steps:"
echo "  1. Edit AGENTS.md: Product, Core Rules, and Commands for this project."
echo "  2. Fill PROJECT_STATUS.md / ROADMAP.md and the docs/engineering/* placeholders."
echo "  3. Run the validator:  python3 tools/check_agent_docs.py"
echo "  4. Commit. The SessionStart/PreCompact hooks activate on the next Claude Code session."
