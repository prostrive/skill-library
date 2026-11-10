---
name: implement
description: Build a ticket or a spec in code, test-first where a cheap test target exists, then verify it in the real app and review it. Use when the user asks to build a ticket or spec.
---
<!-- Based on mattpocock/skills: skills/engineering/implement, skills/engineering/implement-spec, skills/engineering/tdd; backnotprop/pstack: skills/tdd (MIT) -->

# Implement

Build the work in a ticket or spec. Do not write a plan doc. The ticket is the spec.

## Start

1. Fetch the ticket from the tracker (`docs/agents/tracker.md`, or the Linear MCP when the file is missing). Say its title before you start. If the reference is ambiguous, ask.
2. Read `AGENTS.md`, `GLOSSARY.md` and the decision records in the area you touch.
3. Find the nearest similar code in the repo and copy its patterns.

## One ticket: the test loop

Work one acceptance criterion at a time:

1. **Test first.** Write one test for the criterion on the real function, at a public seam. Use the project's words in the test name.
2. **Watch it fail.** Run it. It must fail for the reason the criterion names. If it passes or fails for another reason, fix the test first.
3. **Make it pass.** Write the smallest change that passes. Do not add code for later criteria.
4. **Repeat** for the next criterion.

Every test must be able to fail. Ask of each test: would it still pass if the behavior were broken? A test that starts in the state it asserts, recomputes the expected value the way the code does, or asserts an absence without proof that the event ran, cannot fail. See [references/tests.md](references/tests.md).

When no cheap test target exists (it needs a large harness, brittle mocks or production-only state), do not force a test. Use the closest real check: a script, a curl, a browser run. Say which one you used.

Run the type checker and the single test file often. Run the full test suite once at the end.

## Several tickets

When the dev gives a spec with several tickets:

1. Read the tickets and their blocking links. The **frontier** is every ticket whose blockers are done.
2. Create one integration branch.
3. For each frontier ticket, start a fresh implementer subagent with a fresh context. Each one works in its own git worktree on its own branch, with its own browser profile. Give it pointers (ticket ID, branch), not copies of the text.
4. When an implementer finishes, merge its branch into the integration branch. Then start subagents for the tickets that the merge unblocked.
5. Remove the worktrees when all tickets are merged.

Keep exploration notes outside the repo.

## Before you say done

1. For a change a user can see, run the `verify` skill and drive the change in the real app.
2. Run the `review` skill on the change. Fix what it finds.
3. Commit on the current branch, following the git rules in `AGENTS.md`.
4. Move the ticket in the tracker the way the team closes work.

## Report

- The tests you added, the failure each one showed before the fix, and the passing run after.
- What you checked in the real app, and what you could not check.
- Anything you left out, and why.
