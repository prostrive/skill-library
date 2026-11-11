# skill-library

The base skills for Prostrive projects, as one Claude Code plugin. It replaces `superpowers-lite`.

Most skills are reworked from [mattpocock/skills](https://github.com/mattpocock/skills) and [backnotprop/pstack](https://github.com/backnotprop/pstack). See `THIRD_PARTY_NOTICES.md`.

What it does not do: no startup hook, no lane question, no forced plan or spec docs. Nothing loads before your first message except the one-line skill descriptions.

## Install in a project

Commit this to the project's `.claude/settings.json`. Each dev then gets an install prompt when they open the repo.

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

Or install it by hand in Claude Code:

```
/plugin marketplace add prostrive/skill-library
/plugin install skill-library@skill-library
```

Then run `/setup-repo` once in the project.

## Skills

Slash-only skills run only when you type `/name`. Auto skills also load by themselves when the work matches their trigger.

| Skill | Mode | What it does |
|---|---|---|
| `grill` | slash-only | Asks you questions about a plan until every decision is made |
| `triage` | slash-only | Moves tickets through triage and asks about unclear ones before it writes a brief |
| `setup-repo` | slash-only | Writes `AGENTS.md`, the glossary and the `docs/agents/` files for a repo |
| `git-guardrails` | slash-only | Adds a hook that blocks push, `reset --hard`, `clean` and `branch -D` |
| `setup-pre-commit` | slash-only | Sets up pre-commit hooks for format, types and tests |
| `catch-up` | slash-only | Tells you what is next and what waits on you, in plain words |
| `wait-what` | slash-only | Says the last message again, with more context and plainer words |
| `handoff` | slash-only | Writes a handoff note so a new session can continue the work |
| `reflect` | slash-only | Reviews the session and turns each lesson into an edit of a skill |
| `babysit` | slash-only | Drives PRs to merge-ready (conflicts, review comments, CI); with `land`, merges them one at a time and follows the deploy |
| `verify` | auto | Drives the real app to prove a change works before it is called done |
| `diagnose` | auto | Finds the root cause of a bug, error or failing test |
| `implement` | auto | Builds a ticket test-first |
| `spec` | auto | Turns the conversation into a spec and tickets in the tracker |
| `review` | auto | Reviews a PR or branch for standards, spec and real bugs |
| `pr` | auto | Writes the PR body |
| `research` | auto | Researches a question from primary sources and saves the result |
| `blast-radius` | auto | Finds what a change can break outside the diff |
| `correct` | auto | Turns a mistake agents repeat into a type, lint or test that blocks it |
| `why` | auto | Explains why code is the way it is, from history and tickets |
| `how` | auto | Explains how code works and where new code goes |
| `domain-modeling` | auto | Keeps the glossary and decision records up to date |
| `writing-for-agents` | auto | Rules for writing skills, `AGENTS.md` and `CLAUDE.md` |
| `codebase-design` | auto | Shared words for module design: depth, seams, interfaces |
| `improve-codebase-architecture` | auto | Finds modules that can get a simpler interface |
| `statechart` | auto | Checks a state flow with a TLA+ model and draws it |
| `no-comments` | auto | Removes comments that only say what the code does |
| `wizard` | auto | Writes a step-by-step script for steps only a person can do |
| `ask` | auto | Lists, asks and creates topic experts for the repo |

## Extend it in a project

A project adds files that the base skills read: `AGENTS.md`, `GLOSSARY.md`, `docs/agents/*.md`, `features/` and topic experts. The table in `CLAUDE.md` lists each file and the skills that read it. A project can also add its own skills in `.claude/skills/`. It never edits a base skill.

## Contribute

1. Read the rules in `CLAUDE.md`.
2. Make the change on a branch.
3. Bump `version` in `skill-library/.claude-plugin/plugin.json`.
4. Run `bash scripts/check-skills.sh`.
5. Open a PR. The maintainer reviews every PR.

## Pilot data

`python3 -I scripts/mine-transcripts.py --days 14` counts how often each skill loaded, how often devs typed it, and the interrupts and corrections that came right after. It prints counts only, never message text.
