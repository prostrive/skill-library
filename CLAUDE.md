# skill-library

A Claude Code plugin marketplace with one plugin, `skill-library`: the base skills for Prostrive projects. Projects add their own skills on top. They never edit a base skill.

## Layout

- `.claude-plugin/marketplace.json`: the marketplace manifest.
- `skill-library/.claude-plugin/plugin.json`: the plugin manifest. Bump `version` (0.x) in every PR that changes a skill.
- `skill-library/skills/<name>/SKILL.md`: one folder per skill. Long detail goes in `skill-library/skills/<name>/references/*.md`.
- `skill-library/agents/*.md`: subagents that skills start.
- `scripts/check-skills.sh`: the CI check. Run it before you open a PR.
- `scripts/mine-transcripts.py`: reads a dev's local Claude Code transcripts and counts skill use and friction. Used to decide the pilot questions.

## How to write a skill

These rules apply to every file under `skill-library/`. `scripts/check-skills.sh` enforces the ones a script can check.

**Frontmatter.**
- `name` matches the folder name.
- `description` is one or two sentences.
- A skill that only runs when a dev types `/name` has `disable-model-invocation: true`. Its description says what it does.
- A skill that Claude may load by itself has no such line. Its description says what it does, then `Use when <one concrete trigger>.` One trigger, described as something Claude can see in the work.
- Never write `MUST`, `always`, `even if`, `1%`, `not optional` or `not negotiable` in a description. That pattern made the old plugin fire on everything.

**Body.**
- Under 120 lines. Move detail to `references/`.
- Plain English. Active voice. Short sentences. One instruction per sentence. No marketing words.
- Say what to do, not why the skill exists.
- No ceremony: no lane questions, no sign-off quizzes, no committed plan or spec docs. The tracker ticket is the spec.
- A skill that asks the dev questions follows `skill-library/skills/grill/references/asking.md`: the `AskUserQuestion` dialog, up to 4 questions per round, one decision per question, and only questions the code, the tracker or the docs cannot answer.
- Start subagents with a fresh context, not a fork. Parallel subagents each get their own git worktree and their own browser profile.

**Generic only.** This repo is public.
- No client names, project names, people, ticket IDs, URLs of private systems or absolute paths.
- Project facts come from files in the project repo. A skill names the file it reads and works when the file is missing.

**Credit.** Most skills are reworked from MIT-licensed sources. The first line after the frontmatter is an HTML comment that names the source, for example `<!-- Based on mattpocock/skills: skills/engineering/tdd (MIT) -->`. `THIRD_PARTY_NOTICES.md` holds the licenses.

## Project files the skills read

A project extends the base with these files. Every one is optional.

| File | Read by | Holds |
|---|---|---|
| `AGENTS.md` | all | The repo conventions, written by `setup-repo` |
| `GLOSSARY.md` | all | Domain words and the words to avoid |
| `docs/decision-records/` | `domain-modeling`, `why`, `review` | ADRs |
| `docs/agents/tracker.md` | `spec`, `triage`, `implement`, `review` | Issue tracker, team, statuses, labels |
| `docs/agents/verify.md` | `verify` | How to start the app and sign in |
| `features/` | `verify` | The feature map: one file per feature |
| `docs/agents/review.md` | `review`, `pr` | Paths a person reads themselves, extra review checks, paths to skip |
| `.claude/agents/<topic>.md` + `docs/topics/<topic>.md` | `ask` | Topic experts and their briefs |
| `.claude/handoffs/` (gitignored) | `handoff`, `catch-up` | Handoff notes between sessions |

## Releases

Changes go through a PR. The maintainer reviews every PR. A project skill moves into the base only when 2 or more projects need it.
