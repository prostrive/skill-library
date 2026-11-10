---
name: spec
description: Turn what was discussed into a spec and a set of thin end-to-end tickets with blocking links, published to the tracker. Use when the user asks to turn the conversation or a plan into a spec or tickets.
---
<!-- Based on mattpocock/skills: skills/engineering/to-spec, skills/engineering/to-tickets (MIT) -->

# Spec

Turn the conversation, a plan or a ticket into a spec and tickets in the tracker. Do not interview the dev. Work from what was already said. The tracker is the only place the spec lives. Do not commit a spec or plan file.

## Tracker

Read `docs/agents/tracker.md` for the tracker, the team, the statuses and the labels. When the file is missing, use the Linear MCP and the team's existing statuses and labels.

## 1. Gather

- Use the conversation. If the dev passes a ticket ID or URL, read its full body and comments.
- Read the code in the area. Use the words from `GLOSSARY.md`. Follow the decisions in `docs/decision-records/`.
- Search the tracker for tickets that already cover the same capability. One capability gets one ticket. Update or link an existing ticket instead of making a second one.

## 2. Name the test seams

A seam is the public interface where a test watches the behavior. Prefer seams that already exist. Prefer the highest seam that still catches the bug class. Fewer seams is better.

## 3. Draft the tickets

Cut the work into thin end-to-end slices:

- Each slice goes through every layer it needs (data, API, UI, tests) and can be shown or checked on its own.
- Each slice fits in one fresh agent session.
- Any clean-up that makes the change easier comes first, as its own ticket.
- Each ticket lists the tickets that block it. A ticket with no blockers can start now.

**A wide mechanical change** (rename a column, retype a shared symbol) cannot be one green slice. Sequence it as expand, migrate, contract: add the new form next to the old one, move callers in batches (one ticket per batch), then delete the old form in a ticket blocked by every batch.

## 4. Show the breakdown once

Show a numbered list. Per ticket: title, blocked by, what it delivers. Ask at most these 3 questions:

1. Is the size of the tickets right?
2. Are the blocking links right?
3. Should a ticket be merged or split?

Change the list until the dev agrees.

## 5. Publish

1. Create the spec as the parent ticket (template below). If the source was an existing ticket, use that ticket as the parent and do not change its body.
2. Create the child tickets in order, blockers first, so each ticket can link to real IDs.
3. Use the tracker's own "blocked by" link where it has one.
4. Set the status the team uses for "ready".

Do not put file paths or code in tickets. They go stale. A short snippet from a prototype that pins a decision (a state machine, a schema, a type) is fine.

End with the list of ticket IDs and links.

## Spec template (parent ticket)

```markdown
## Problem
What the user faces, in their words.

## Solution
What changes for the user.

## User stories
1. As a <role>, I want <feature>, so that <benefit>.

## Decisions
Modules, interfaces, schema and API changes, and choices the dev made. No file paths.

## Testing
The seams under test, and similar tests that already exist.

## Out of scope
What this does not change.
```

## Child ticket template

```markdown
## What to build
The end-to-end behavior this ticket makes work, from the user's side.

## Acceptance criteria
- [ ] criterion 1
- [ ] criterion 2

## Blocked by
- <ticket ID>, or "None". Leave this out when the tracker link is set.
```
