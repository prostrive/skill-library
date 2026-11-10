# AGENTS.md template

Copy the block below into the repo's `AGENTS.md`. Replace every `<...>` with what the repo does. Delete an example rule that does not fit the repo. Mark a gap as `TODO(setup-repo): <what is missing>`.

Keep it short. Each line states a rule a person or an agent can follow. A rule that a linter or a config file already enforces does not go here.

```markdown
# <Project name> conventions

Read this before you write code here. It applies to people and to coding agents. Words come from [GLOSSARY.md](GLOSSARY.md).

## Skills

This repo uses the skill-library plugin. Load the matching skill before you start:

- A bug, error, failing test or slowdown: `diagnose`.
- How code works, or where new code belongs: `how`. Why code or a decision is the way it is: `why`.
- Building a ticket or spec: `implement`. Turning a plan into tickets: `spec`.
- Before you say an app change is done: `verify`.
- Reviewing a PR or diff: `review`. Writing a PR body: `pr`.
- A question about a topic that has an expert in `.claude/agents/`: `ask`.

## Words

- Code uses the glossary words: `<term>`, `<term>`. Not `<avoided synonym>`.
- Table, function and component names follow `GLOSSARY.md`.
- A new term goes into the glossary before it goes into the code.

## Folders

- <Where the backend code lives, one domain per file or folder, and where shared logic goes.>
- <Where the frontend code lives, and where shared UI lives. Use an existing component before you write a new one.>
- <Where tests live: next to the code, or in a test folder.>

## Files and imports

- <File naming: kebab-case, camelCase or PascalCase, and the exceptions.>
- <Import style: the path alias to use, and when a relative import is allowed.>

## Tests

- Each acceptance-criteria line on a ticket gets one test on the real function.
- A test must be able to fail. A test that starts from the state it asserts, or asserts an absence without proving the event happened, proves nothing.
- <The test runner and the command: `<package manager> test`.>
- A ticket is not done without its tests. For a change a user can see, also check it in the running app. See `docs/agents/verify.md`.

## Code

- <Language rules the repo follows: strict mode, no `any`, `const` over `let`, `async`/`await`, early returns.>
- <Error handling: how errors are thrown or returned, and the error shape.>
- <Naming: camelCase, PascalCase, `UPPER_SNAKE_CASE` constants, booleans start with `is`, `has` or `should`.>

## Comments

- Explain why, never what.
- Two lines max. A longer reason goes in `docs/decision-records/`, cited in one line.

## Writing

This applies to chat replies, PR bodies, ticket text, commit bodies and docs.

- Say the thing first. Give the reason after, only if it is not obvious.
- Use the short, everyday word and the real name of the file, flag or command.
- Active voice. One thought per sentence. Short sentences.
- Cut every sentence that carries no information. No closing line that repeats what you said.
- No headers in chat replies. No em dashes. No marketing words.
- Use the words of the glossary, not new jargon.
- When you tidy text the dev wrote, keep their tone and meaning. Fix only grammar and punctuation.

## Git

- One ticket per PR. The PR links the ticket.
- Branch names: <the name the tracker gives, for example `feature/abc-123`>.
- Conventional commits: `feat:`, `fix:`, `chore:`, `refactor:`, `docs:`.
- Never commit `.env` files, secrets or credentials.

## Gotchas

- <Things that look wrong but are on purpose. Agents must not "fix" them.>
```
