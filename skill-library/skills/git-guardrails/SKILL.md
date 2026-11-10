---
name: git-guardrails
description: Add a Claude Code hook that blocks git commands that lose work or write to a protected branch, such as force push, a push to main or develop, reset --hard and branch -D.
disable-model-invocation: true
---

<!-- Based on mattpocock/skills: skills/misc/git-guardrails-claude-code (MIT) -->

# Git guardrails

Install a PreToolUse hook. It stops the agent before it runs a dangerous git command. The dev can still run the command by hand.

## What the hook blocks

The script is [scripts/block-dangerous-git.sh](scripts/block-dangerous-git.sh). It blocks:

- a force push (`--force`, `-f`, `--force-with-lease`)
- a push to a protected branch: `main`, `master` or `develop`
- `git reset --hard`
- `git clean -f` and its variants
- `git branch -D`
- `git checkout .` and `git restore .`
- `git stash drop` and `git stash clear`

A normal push of a feature branch passes.

## Steps

1. **Pick the scope.** Default: this repo only, so the whole team gets the hook. Install it for all repos (`~/.claude/`) only when the dev asks for that.
2. **Check `jq`.** The script needs it. Run `command -v jq`. If it is missing, tell the dev how to install it (`brew install jq` on macOS) and stop.
3. **Copy the script.**
   - Repo: `.claude/hooks/block-dangerous-git.sh`
   - All repos: `~/.claude/hooks/block-dangerous-git.sh`

   Run `chmod +x` on it.
4. **Set the protected branches.** Read the default branch with `git symbolic-ref refs/remotes/origin/HEAD` and the long-lived branches on the remote. Put them in `PROTECTED_BRANCHES` in the copied script.
5. **Add the hook to the settings file.** Repo: `.claude/settings.json`. All repos: `~/.claude/settings.json`. Merge it into the `hooks.PreToolUse` array. Keep every other key.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/block-dangerous-git.sh"
          }
        ]
      }
    ]
  }
}
```

For all repos, the command is `~/.claude/hooks/block-dangerous-git.sh`.

6. **Test it.** Each of these must exit 2 and print `BLOCKED`:

```bash
echo '{"tool_input":{"command":"git push --force origin feature/x"}}' | <script>; echo "exit $?"
echo '{"tool_input":{"command":"git push origin main"}}' | <script>; echo "exit $?"
```

This one must exit 0:

```bash
echo '{"tool_input":{"command":"git push -u origin feature/x"}}' | <script>; echo "exit $?"
```

**Done when** all 3 tests give the expected exit code and the settings file parses as JSON.

Report the scope, the protected branches and the test results. The dev can add or remove patterns in the copied script.
