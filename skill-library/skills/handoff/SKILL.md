---
name: handoff
description: Write a short handoff note in the repo so a fresh session can continue this work, with the state checked live.
argument-hint: "What will the next session work on?"
disable-model-invocation: true
---

<!-- Based on mattpocock/skills: skills/productivity/handoff and backnotprop/pstack: skills/recall (MIT) -->

# Handoff

Write a note that lets a new agent continue this work after reading it once.

## Where

Write to `.claude/handoffs/<YYYY-MM-DD>-<slug>.md` in the repo root. The slug is 2 to 4 words that name the work. Do not write to `/tmp` or another temp folder.

`.claude/handoffs/` holds working notes, not project docs. If the repo's `.gitignore` does not list `.claude/handoffs/`, add that line.

If the dev passed an argument, it says what the next session will work on. Shape the note around that.

## Check the state live

Do not write the state from memory. Check it now:

1. `git branch --show-current` and `git status --short`.
2. Commits on this branch that are not on the base branch: `git log --oneline <base>..HEAD`.
3. Open PRs for this branch and their checks: `gh pr list --head <branch>` and `gh pr checks <number>`.
4. The tracker tickets this work touched, with their current status. `docs/agents/tracker.md` names the tracker if the repo has one.

If a check fails or a tool is missing, write "not checked" for that line. Do not guess.

## What goes in the note

Use these sections. Leave out a section that has nothing in it.

- **Goal:** one or two sentences. What the work is for.
- **State:** branch, uncommitted changes, PRs with their check status, tickets with their status. Each line says where the fact came from.
- **Decisions:** what was decided in this session and why, one line each. Only decisions a new agent could otherwise get wrong.
- **Next steps:** numbered, in the order to do them. The first step is concrete enough to start on.
- **Open questions:** what waits on the dev or on someone else, and who.
- **Suggested skills:** the skills the next agent will likely need, for example `/implement` or `/verify`.

## Rules

- Link to what already exists. Name a ticket, PR, commit, ADR or file by its ID, URL or path. Do not copy its content into the note.
- Remove secrets: API keys, passwords, tokens, personal data.
- Keep it short. If a section grows past 10 lines, cut detail, not items.

Reply with the path of the note and nothing else.
