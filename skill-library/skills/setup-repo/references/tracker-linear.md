# docs/agents/tracker.md template: Linear

Copy the block below into `docs/agents/tracker.md`. Fill in the values from the Linear MCP or from the dev.

```markdown
# Issue tracker: Linear

Tickets for this repo live in Linear, team `<TEAM KEY>` (<team name>). Use the Linear MCP for every read and write.

## Statuses

| Role | Status in this team |
|---|---|
| New, not looked at | `<Triage>` |
| Waiting on the reporter | `<Needs Info>` |
| Ready to build | `<Todo>` |
| In progress | `<In Progress>` |
| In review | `<In Review>` |
| Done | `<Done>` |
| Will not do | `<Canceled>` |

## Labels

<The labels this team uses, one per line, with what each means. Use these labels. Do not create new ones.>

## Rules

- Search for an existing ticket on the same thing before you create one.
- The ticket is the spec. Acceptance criteria go in the ticket, not in a doc in the repo.
- Branch names come from Linear, for example `feature/<team-key>-123`.
- Read the comments too. `get_issue` does not return them.

## When a skill says "publish to the tracker"

Create a Linear issue in team `<TEAM KEY>`.

## When a skill says "fetch the ticket"

Get the issue and list its comments.
```
