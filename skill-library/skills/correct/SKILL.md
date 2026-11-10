---
name: correct
description: Find the mistakes agents keep repeating in this repo and make each one impossible with architecture, types, a lint or a test before falling back to docs. Use when the user says the agent keeps repeating a mistake in this repo.
---
<!-- Based on backnotprop/pstack: skills/correct and skills/principle-encode-lessons-in-structure (MIT) -->

# Correct

The user keeps correcting agents in this repo for the same mistakes. Change the repo so the next agent cannot make them.

Assume every contributor is an agent that sees only the files it opened, copies the nearest example and takes the shortest path that compiles. Shape the repo so a change that looks right from one file is right for the whole repo.

A rule written a second time is a sign the fix belongs in structure. More text is the symptom, not the fix.

## 1. Find the mistake classes

Read recent commits, reverts, review comments, `AGENTS.md`, `CLAUDE.md`, and comments that explain workarounds. Include the mistake the user just named. Group the mistakes into classes. A class counts once it has happened twice.

## 2. Fix each class at the highest level that works

1. **Architecture removes it.** Give each piece of state one owner and each task one supported way. Hide internals so the wrong import fails. Replace hand-synced lists with one source of truth. Delete old paths and dead code that an agent would copy.
2. **Types forbid it.** Make the bad state impossible to write.
3. **A lint or CI check catches it.** The error message names the file, type or function to use instead. If the bad pattern is already common, fail only when a change adds more of it.
4. **A test catches it.** Fix or delete any test that still passes when its behavior breaks, or that fails when only internals change.
5. **Docs, last.** Only for judgment calls. Nothing fails when an agent skips a doc. When a rule must stay in text, put it where agents read it and add one example of the failure.

## 3. Fix and prove

- Fix the most frequent classes now, one commit each.
- Prove each new check fails on a real past mistake. Show the command and its output.
- Run the same command locally and in CI.
- An exception goes on the offending line, with a reason and an expiry date, and a person approves it.

## 4. Keep the rule table

Keep a table in `AGENTS.md` that pairs each rule with what enforces it (`architecture`, `type`, `lint: <name>`, `test: <path>`, or `doc only`).

When the user corrects you again:
- Fix the mistake and add the rule to the table.
- If the rule was already there and nothing enforced it, it is a repeat. Move it up a level in the same change.
- Drop a rule once its mistake can no longer happen.

## Output

Each class with its evidence, the level you picked, and why a higher level did not work.
