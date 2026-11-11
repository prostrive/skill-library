# The `docs/agents/deploy.md` format

A project writes this file to tell `babysit` how a merge reaches an environment and how to know it is live. Keep it short and use real names from the repo.

```markdown
# Deploy

## Environments

- `staging`: deployed from `<branch>` by the `<workflow name>` workflow, on every merge.
- `production`: deployed from `<branch>` by `<workflow name>`, started by `<who or what>`.

## How a merge reaches staging

1. <the workflow that runs after a merge, and any promote step a person or a bot starts>
2. <how long it usually takes>

## How to see that a commit is live

- <for example: `curl https://<staging host>/version` returns the commit SHA>
- <or: the deploy workflow run for that commit finished with success>

## Checks after the deploy

- <for example: `/verify` against staging, following `docs/agents/verify.md`>
- <or: a smoke test command>

## Never

- <for example: never start the production promote; a person does that>
```
