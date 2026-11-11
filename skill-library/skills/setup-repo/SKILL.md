---
name: setup-repo
description: Set up a repo for the skill-library skills. Writes AGENTS.md, the docs/agents files, GLOSSARY.md, the handoffs ignore rule and the plugin install config. Run once per repo.
disable-model-invocation: true
---

<!-- Based on mattpocock/skills: skills/engineering/setup-matt-pocock-skills (MIT) -->

# Set up a repo

Write the files the other skills read. Detect every fact you can from the repo. Ask the dev only for facts you cannot detect, in one `AskUserQuestion` round of up to 4 questions.

## 1. Read the repo

Read what exists. Assume nothing.

- `git remote -v`: the host and the repo.
- `AGENTS.md`, `CLAUDE.md`, `GLOSSARY.md`, `GLOSSARY-MAP.md`, `docs/decision-records/`, `docs/agents/`.
- `.claude/settings.json` and `.gitignore`.
- The stack: `package.json` (scripts, workspaces), lockfiles, `tsconfig.json`, lint and format config, test runner config, `README`.
- The folder layout: where the source, the tests and the shared UI live.
- 3 or 4 real source files and 1 or 2 test files, to see the naming, import and test style the code already uses.
- The last 20 commit subjects: `git log --format=%s -20`. They show the commit style.
- Branch names on the remote. They show whether branches come from the tracker.

**Done when** you can fill each section of the AGENTS.md template from the repo, or you know the section is a gap.

## 2. Ask what you could not detect

Typical gaps: the issue tracker and its team key, the domain words, rules that live only in people's heads. Ask them in one `AskUserQuestion` round of up to 4 questions, with your best guess as the first option.

Default tracker: Linear. Propose GitHub Issues only when the repo has no Linear branch names and uses GitHub Issues.

## 3. Write the files

Show the dev a short list of the files you will write or change. Then write them. Edit a file that exists in place. Keep every line the dev wrote that you did not replace.

1. **`AGENTS.md`** from [references/agents-template.md](references/agents-template.md).
   - Keep the Skills section as it is. Without it, Claude rarely loads a skill by itself.
   - Fill each section with what the repo already does. Use real paths, real script names and real examples from the code.
   - Delete a template rule the repo breaks on purpose. Do not invent a rule the code does not follow.
   - Mark each gap as `TODO(setup-repo): <what is missing>`, so the dev can find it.
2. **`CLAUDE.md`**: first line `@AGENTS.md`. Then one short section that points to `docs/agents/verify.md` for how to check a change in the running app. If `CLAUDE.md` holds conventions already, move them into `AGENTS.md` and leave the pointer.
3. **`docs/agents/tracker.md`** from [references/tracker-linear.md](references/tracker-linear.md) or [references/tracker-github.md](references/tracker-github.md). Fill in the team, the statuses and the labels. For Linear, read them with the Linear MCP if it is connected.
4. **`docs/agents/verify.md`**: a stub with the title "How to check a change in the running app" and one line: `Not set up yet. Run /verify setup.` Skip it if the file exists.
5. **`GLOSSARY.md`**: create it only if it is missing. Use the format in the `domain-modeling` skill. Add the domain words you found in the code and the answers, each with an `_Avoid_` line when the code uses two words for one thing.
6. **`.gitignore`**: add `.claude/handoffs/` if it is not there.
7. **`docs/agents/review.md`**: create it only if it is missing, from the format in the `review` skill (`references/review-md.md`). Fill "Read yourself" with the real paths of the CI config, the migrations and the auth or permission code. Add other paths only when the dev names them. Delete a line the repo does not have.
8. **`.claude/settings.json`**: merge these keys. Keep every other key.

```json
{
  "extraKnownMarketplaces": {
    "skill-library": {
      "source": { "source": "github", "repo": "prostrive/skill-library" }
    }
  },
  "enabledPlugins": {
    "skill-library@skill-library": true
  }
}
```

A dev who opens the repo then gets a prompt to install the plugin.

**Done when** each of the 8 items is written or was already correct, and `.claude/settings.json` parses as JSON.

## 4. Report

List the files you wrote and the `TODO(setup-repo)` gaps that remain. Name the next steps that apply: `/verify setup` for the app check, `/git-guardrails` for the git hook, `/setup-pre-commit` for commit checks.
