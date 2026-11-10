#!/usr/bin/env bash
# Claude Code PreToolUse hook. Blocks git commands that lose work or write to a protected branch.
# Exit 2 tells Claude Code to block the command and show stderr to the agent.

INPUT=$(cat)
COMMAND=$(printf '%s' "$INPUT" | jq -r '.tool_input.command // empty')
[ -z "$COMMAND" ] && exit 0

PROTECTED_BRANCHES="main|master|develop"

DANGEROUS_PATTERNS=(
  "git push.*(--force|-f( |$)|--force-with-lease)"
  "git push.*( |:)($PROTECTED_BRANCHES)( |$)"
  "git reset --hard"
  "git clean -[a-z]*f"
  "git branch -D"
  "git checkout (--)? *\.( |$)"
  "git restore (--staged )?\.( |$)"
  "git stash (drop|clear)"
)

for pattern in "${DANGEROUS_PATTERNS[@]}"; do
  if printf '%s' "$COMMAND" | grep -qE "$pattern"; then
    echo "BLOCKED: '$COMMAND' matches '$pattern'. The dev blocked this command. Ask the dev to run it." >&2
    exit 2
  fi
done

exit 0
