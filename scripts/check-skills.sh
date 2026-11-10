#!/usr/bin/env bash
# Checks every skill against the rules in CLAUDE.md. Exit 1 on any failure.
set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS_DIR="$ROOT/skill-library/skills"
MAX_BODY_LINES=120
BANNED_DESCRIPTION_PATTERN='MUST|[Aa]lways|[Ee]ven if|1%|[Nn]ot optional|[Nn]ot negotiable'
failures=0

fail() {
  echo "FAIL $1: $2"
  failures=$((failures + 1))
}

frontmatter_value() {
  awk -v key="$2" '
    NR == 1 && $0 == "---" { inside = 1; next }
    inside && $0 == "---" { exit }
    inside && index($0, key ":") == 1 { sub("^" key ":[ ]*", ""); print; exit }
  ' "$1"
}

for skill_file in "$SKILLS_DIR"/*/SKILL.md; do
  skill_dir="$(basename "$(dirname "$skill_file")")"
  name="$(frontmatter_value "$skill_file" name)"
  description="$(frontmatter_value "$skill_file" description)"
  is_slash_only="$(frontmatter_value "$skill_file" disable-model-invocation)"

  [ "$(head -n 1 "$skill_file")" = "---" ] || fail "$skill_dir" "file does not start with frontmatter"
  [ "$name" = "$skill_dir" ] || fail "$skill_dir" "name '$name' does not match the folder"
  [ -n "$description" ] || fail "$skill_dir" "description is empty"

  if echo "$description" | grep -Eq "$BANNED_DESCRIPTION_PATTERN"; then
    fail "$skill_dir" "description uses a banned word (MUST, always, even if, 1%, not optional, not negotiable)"
  fi

  if [ "$is_slash_only" != "true" ] && ! echo "$description" | grep -q "Use when"; then
    fail "$skill_dir" "auto-load skill has no 'Use when' trigger in its description"
  fi

  body_start="$(awk 'NR > 1 && $0 == "---" { print NR; exit }' "$skill_file")"
  total_lines="$(wc -l < "$skill_file" | tr -d ' ')"
  body_lines=$((total_lines - body_start))
  [ "$body_lines" -le "$MAX_BODY_LINES" ] || fail "$skill_dir" "body has $body_lines lines, max is $MAX_BODY_LINES"

  first_body_line="$(sed -n "$((body_start + 1)),\$p" "$skill_file" | grep -v '^[[:space:]]*$' | head -n 1)"
  echo "$first_body_line" | grep -q '^<!--' || fail "$skill_dir" "first body line is not a source comment"
done

if grep -rnE '/Users/|/home/[a-z]' "$ROOT/skill-library" > /dev/null; then
  grep -rnE '/Users/|/home/[a-z]' "$ROOT/skill-library" | sed 's/^/FAIL absolute path: /'
  failures=$((failures + 1))
fi

skill_count="$(ls -d "$SKILLS_DIR"/*/ 2> /dev/null | wc -l | tr -d ' ')"
if [ "$failures" -gt 0 ]; then
  echo "$failures problem(s) in $skill_count skills"
  exit 1
fi
echo "OK: $skill_count skills pass"
