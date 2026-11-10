---
name: no-comments
description: Clean up code comments in a diff or files to the house rule (why, never what, two lines max) and turn comments that guard a workaround into code, types or tests. Use when the user asks to clean up or review code comments.
---
<!-- Based on backnotprop/pstack: skills/no-comments and its comment-sicko reference (MIT) -->

# No comments

Remove comments that do not earn their place. Act on the code problems they hide.

## The house rule

- A comment explains why, never what.
- Two lines max.
- A longer reason goes in `docs/decision-records/`, and the code cites it in one line.
- `AGENTS.md` may add rules. They win.

## Scope

The files or diff the user names. Otherwise the current diff against the base branch, with the working tree.

## What stays

- License or legal headers.
- Behavior forced by something we cannot change: a dependency, platform, vendor or protocol. Keep it short.
- Doc comments that define a public API contract.
- Links to an issue or RFC that explains a constraint code cannot express.
- Formatter directives such as `prettier-ignore`.
- A lint suppression only when its rule is wrong for this line or is style only.

When you are not sure a comment fits this list, it goes.

## What goes

- Narration of what the next line does.
- Banners and section dividers.
- Commented-out code.
- History: "changed from X", "was Y before", "added for ticket Z".
- Long justifications. If code needs a paragraph to defend it, the code is the problem.

## Steps

1. Read each comment with the code around it.
2. A comment that explains a surprise in our own code: delete it and flag the symbol. The fix is a rename, an extracted function, a type or a different shape that makes the behavior obvious.
3. A comment that claims a rule of something outside our code: check that thing's docs or source. Proven true: keep it. Proven false or not ours: delete it. Cannot check: keep it and list it under "Check".
4. `IMPORTANT`, `do not remove`, `too risky`, `fine for now`: read the code around it, and use `how` or `why` on the symbol when the claim is not obvious. Then apply steps 2 and 3.
5. Lint and type suppressions (`eslint-disable`, `@ts-ignore`, `@ts-expect-error`, and the like): look the rule up. If it protects correctness or safety, remove the suppression and fix the code.
6. A comment that guards a real constraint ("do not change this wording", "talk to X first"): offer the cheapest check that enforces it, such as a type, a runtime assert, a test or a lint. Ask once. If the user agrees, add the check and delete the comment. If not, delete it and list the constraint as open.
7. Fix trivial flagged code directly: delete a dead path, drop an unused parameter, call the real API. Larger fixes stay in scope or go to the open list. Never add a guard for a symptom.

Do not change application behavior while you delete comments.

## Output

Files touched, number of comments deleted, the code fixes you made, comments kept under "Check" with the rule each one claims, constraints you encoded, and open work.
