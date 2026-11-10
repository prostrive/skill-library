# The `docs/agents/review.md` format

A project writes this file to tell `review` where a person reads the code and what extra checks to run. Keep it short.

```markdown
# Review

## Read yourself

Paths where a person reads the diff, not only the evidence. One line each: a glob and the reason.

- `.github/workflows/**`: CI and deploy config
- `<migrations path>/**`: database migrations cannot be rolled back cheaply
- `<auth or permissions path>/**`: who can do what
- `<money path>/**`: code that moves or calculates money

## Extra checks

Checks the reviewers run on every PR in this repo. Delete this section if there are none.

- <for example: compare behavior with the legacy system in <path>, and report MATCHES / DIVERGENCE / GAP per behavior>

## Skip

Paths review does not comment on, for example generated code.

- `<generated path>/**`
```
