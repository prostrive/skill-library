---
name: why
description: Find out why code or a design decision is the way it is, from git history, PRs, tickets, docs and chat, and give a cited answer that separates what is known from what is inferred. Use when the user asks why code, a value or a decision is the way it is.
---

<!-- Based on backnotprop/pstack: skills/why (MIT) -->

# Why

Find the forces that shaped a piece of code: the decision, the tradeoff, the incident, the customer request. For how the code works, use the `how` skill.

Work like a careful investigator. Say what you know, what you infer, and what you could not find. An honest "we don't know" beats a confident guess. Read `references/epistemics.md`. The synthesizer follows it.

## 1. Target and question

The target is a piece of code, a pattern, a value or a named decision. The question is a rationale, a tradeoff, a motivating edge case, an outside constraint, dead code or a history sweep. If the target is vague, guess from the conversation (open files, recent edits, what was just discussed), state your reading in one line, and go on.

## 2. Code anchor

Build the seed context yourself before you start any subagent:

- File paths with line ranges, and the key symbols.
- `git blame -L <start>,<end> <file>` for the last-touch commits.
- `git log --follow --oneline -20 -- <file>` for recent history with PR numbers.
- `git log -1 --format=%B <commit>` to find PR numbers and ticket IDs.
- `gh pr view <number> --json title,body,author,createdAt,mergedAt,labels,closingIssuesReferences,comments,reviews` for each commit that matters.

Every investigator and the synthesizer get this anchor.

## 3. Investigators

List the MCP servers connected to this session. In Claude Code their tools are named `mcp__<server>__<tool>`. Map each one to one evidence category:

1. Source control history (git and `gh`, always available)
2. Issue or ticket tracker (Linear, Jira, GitHub Issues)
3. Long-form documents (Notion, Confluence, Google Docs)
4. Team chat (Slack, Teams, Discord)
5. Infrastructure observability (Datadog, Grafana, New Relic)
6. Error tracking (Sentry, Rollbar, Bugsnag)
7. Product analytics warehouse (Databricks, Snowflake, BigQuery)

If `docs/decision-records/` exists, it belongs to source control. Read it first.

Start one investigator subagent per category that has a matching MCP, all in one message, each with a fresh context and exactly one source. Investigators read only. They never write files or change anything outside.

Each investigator prompt is `references/investigator-prompt.md` filled in, plus:

- the playbook for its category from `references/sources/` (index: `references/source-playbook.md`). Adapt it to the actual MCP.
- `references/sources/incident-postmortem.md` if the target looks defensive: null checks, retries, timeouts, rate limits, feature flags, guards.
- the code anchor and the user's question.

Skip a category only with a written reason that goes into Sources Consulted:

- No MCP for it in this session. Name it as a gap: "Team chat not searched. No chat MCP is connected."
- It is provably irrelevant, for example error tracking for a build-time script.

If the PR description already answers the question fully, you may answer without investigators. Say that you did, and why the other searches would add nothing.

## 4. Synthesize

Start one synthesizer subagent with a fresh context. Give it the investigator findings (including empty results and skipped categories with reasons), the code anchor, the user's question, `references/epistemics.md` and `references/synthesizer-prompt.md`.

## 5. Present

Give the synthesizer's answer. You may fix wording or add context from the conversation. Do not change the confidence language.

The structure comes from `references/synthesizer-prompt.md`: The Question, The Code in Question, What We Found, What We Can Reasonably Infer, Competing Hypotheses, What We Don't Know, Sources Consulted, Confidence Summary. Keep Sources Consulted as one line per category, including empty and skipped ones.

If the question comes before a change to this code, end with a short Preserve / Change / Avoid / Risk list for that change.

## Traps

- **Recency bias.** The latest commit is often not the reason. The current shape builds on older decisions. Trace back.
- **Confirming the user's guess.** "I assume it's for performance?" is one hypothesis to test, not the answer.
- **Code as its own evidence.** What code does is mechanics. Intent needs an author's words.
