# docs/agents/tracker.md template: GitHub Issues

Copy the block below into `docs/agents/tracker.md`.

```markdown
# Issue tracker: GitHub Issues

Tickets for this repo live in GitHub Issues. Use the `gh` CLI. `gh` reads the repo from `git remote -v`.

## Commands

- Create: `gh issue create --title "..." --body "..."`. Use a heredoc for a long body.
- Read: `gh issue view <number> --json number,title,body,labels,comments`.
- List: `gh issue list --state open --json number,title,labels` with `--label` filters.
- Comment: `gh issue comment <number> --body "..."`.
- Labels: `gh issue edit <number> --add-label "..."` and `--remove-label "..."`.
- Close: comment first, then `gh issue close <number>`. `gh issue close --comment` drops the comment on an issue that is already closed.
- Sub-issue: `gh issue create --parent <number> ...` (gh 2.94 or later). Without it, put `Part of #<number>` at the top of the body.
- Blocked by: `gh issue edit <child> --add-blocked-by <blocker>` (gh 2.94 or later). Without it, put `Blocked by: #<n>` at the top of the body.

Before the first `gh issue create` in a session, check the target with `gh repo view --json nameWithOwner`. In a fork, `gh` can point at the upstream repo.

## Labels

| Role | Label |
|---|---|
| New, not looked at | `needs-triage` |
| Waiting on the reporter | `needs-info` |
| Ready for an agent | `ready-for-agent` |
| Needs a person | `ready-for-human` |
| Will not do | `wontfix` |

## Rules

- Search for an existing issue on the same thing before you create one.
- The issue is the spec. Acceptance criteria go in the issue, not in a doc in the repo.

## When a skill says "publish to the tracker"

Create a GitHub issue.

## When a skill says "fetch the ticket"

`gh issue view <number> --json number,title,body,labels,comments`.
```
