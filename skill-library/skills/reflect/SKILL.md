---
name: reflect
description: Review this session for what went wrong, and turn each real lesson into a concrete edit to a skill, AGENTS.md or a check, applied only after the dev accepts it.
disable-model-invocation: true
---

<!-- Based on backnotprop/pstack: skills/reflect and mattpocock/skills: skills/engineering/retro (MIT) -->

# Reflect

Find the lessons in this session that will still hold in 6 months, and put each one where the next agent will meet it. Skip a session that was trivial or went to plan. A one-off is not a lesson.

## 1. Find the transcript

Claude Code keeps it at `~/.claude/projects/<slug>/<session-id>.jsonl`. The slug is the workspace path with every character that is not a letter or digit turned into `-`. Take the newest files first and confirm the right one: its first user message matches this session's opening prompt.

Read only this workspace's folder. Other projects' transcripts are private.

If you cannot find the file, write a short digest of the session and pass that instead.

## 2. Run three reviewers in parallel

Start three subagents in one message, each with a fresh context. Give each one `references/reviewer.md` with its lens filled in and the transcript path or digest:

| Lens | Looks for |
|---|---|
| Judgment | Mistakes and corrections, dev preferences, codebase knowledge, decisions and their reasons, friction in skills or delegation |
| Tooling | Commands, flags, paths and test or CI details the agent had to discover. Every time the dev handed over context the agent could have fetched itself |
| Divergent | What the other two will miss: decisions that worked for the wrong reason, skipped or self-reported checks, missed second-order effects, skills that should have run but did not |

## 3. Synthesize

Start one more subagent with `references/synthesizer.md` and the three reviewer outputs. It returns three lists: Accepted, Rejected and Backlog.

## 4. Prefer a check over prose

Before you show the list, move each Accepted item that a lint rule, type, test, hook or script could enforce to Backlog, with the check named. Text in a skill is for what no check can catch. The `correct` skill builds such checks.

## 5. Show and apply

Show the full Accepted, Rejected and Backlog lists. Wait for the dev to pick which Accepted rows to apply. Do not apply anything before that.

Apply each accepted row by where it goes:

- **A project skill, `AGENTS.md` or `GLOSSARY.md` in this repo:** edit the file directly.
- **A base skill from the skill-library plugin:** do not edit the installed copy in the plugin cache. Write the change as a branch and PR on the skill-library repo, with the session evidence in the PR body. Give the dev the PR link.
- **A skill description that did not trigger when it should have:** rewrite the description's `Use when` trigger. Same routing as above.
- **A new skill:** draft it with the `writing-for-agents` skill, in the project's `.claude/skills/` first. It moves to the base only when a second project needs it.

Put each Backlog item in the tracker as a ticket only when the dev agrees.

## 6. Report

A short list, no preamble:

- Applied: path, and what changed in one line.
- PRs opened: link, and what changed in one line.
- Backlog: each item and its proposed check.
- Dropped: each rejected finding and the reason.
