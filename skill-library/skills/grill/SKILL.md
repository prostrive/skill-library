---
name: grill
description: Interview the dev about a plan, design or decision in short rounds until every decision the work needs has a source (the dev, a cited fact, or an accepted default), and record the settled words and decisions as you go.
disable-model-invocation: true
---
<!-- Based on mattpocock/skills: skills/productivity/grilling, skills/productivity/grill-me, skills/engineering/grill-with-docs (MIT) -->

# Grill

Interview the dev until every decision the work needs is visible and settled. The dev makes the decisions. Nothing reaches a ticket or the code as a silent assumption.

## Map the decisions

Treat the plan as a tree of decisions. Each decision opens the decisions that depend on it.

Go down to the level of the acceptance criteria the tickets will carry: who can do what, what the user sees, defaults, limits, error cases, what gets logged or audited. A big choice like "admins can export reports" is not done until its details are settled too.

The **frontier** is every open decision whose prerequisites are already settled. You can ask about it now without guessing an answer you have not heard yet.

## Facts are your job

Do not ask the dev for a fact you can look up. Read the code, the tracker, `AGENTS.md`, `docs/decision-records/`, rulings and the PRD yourself. A decision that follows from a fact is not a question: record it as `[fact: <source>]`.

For a slow lookup, start a subagent with a fresh context. Ask the rest of the frontier while it runs. Only the questions that depend on its result wait.

## Ask in rounds

Follow [references/asking.md](references/asking.md). In short:

1. Take up to 4 decisions from the frontier. Pick the ones that unblock the most other decisions.
2. Ask them in one `AskUserQuestion` call. One decision per question, 2 to 4 options, each with what happens if picked.
3. Recommend an option only when a source points to it, and name the source.
4. Use the project's words from `GLOSSARY.md`. Do not use process jargon.
5. Wait for the answers. Recompute the frontier. Ask the next round.

A question that depends on another question in the same round goes to a later round.

## Defaults

When the frontier holds only small choices, take a default for each. Show them as one numbered list and ask once: accept all, or change some. Each default the dev changes becomes a question in the next round. See [references/asking.md](references/asking.md).

## Record as you go

When a decision settles a domain word or a hard-to-reverse choice, record it with the `domain-modeling` skill:

- A new or sharpened term goes into `GLOSSARY.md`.
- A decision that is hard to reverse and has a real trade-off goes into `docs/decision-records/`.

Do not write a plan doc or a spec doc. The `spec` skill turns the result into tracker tickets when the dev asks.

## Finish

The session is done when the frontier is empty and every decision has a source.

Show the decision list, grouped by source, one line each:

```
Decided by you (7)
1. Admins can export a report as CSV.
...
Facts (3)
8. The export uses the filters on screen. [fact: report list query]
...
Accepted defaults (4)
11. The file name is the report name plus the date.
...
```

Ask the dev to confirm the list. Do not act on it until they do. `spec` and `implement` use this list as it is.
