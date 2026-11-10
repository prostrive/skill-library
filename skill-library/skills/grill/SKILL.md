---
name: grill
description: Interview the dev about a plan, design or decision in short rounds until every open decision is settled, and record the settled words and decisions as you go.
disable-model-invocation: true
---
<!-- Based on mattpocock/skills: skills/productivity/grilling, skills/productivity/grill-me, skills/engineering/grill-with-docs (MIT) -->

# Grill

Interview the dev until you both share one understanding of the plan. Nothing stays silently assumed.

## Map the decisions

Treat the plan as a tree of decisions. Each decision opens the decisions that depend on it.

The **frontier** is every open decision whose prerequisites are already settled. You can ask about it now without guessing an answer you have not heard yet.

## Ask in rounds

1. Pick at most 3 questions from the frontier. Take the ones that unblock the most other decisions.
2. Number each question. Give your recommended answer under it.
3. Word each question so that "yes" accepts your recommendation.
4. Use the project's words from `GLOSSARY.md` when it exists. Do not use process jargon.
5. Wait for the answers. Then recompute the frontier and ask the next round.

A question that depends on another question in the same round goes to a later round.

Format:

```
**Q1. <short title>.** <question, with the options if there are options>

Recommended: <your answer>
```

## Facts are your job

Do not ask the dev for a fact you can look up. Read the code, the tracker, `AGENTS.md` and `docs/decision-records/` yourself.

For a slow lookup, start a subagent with a fresh context. Ask the rest of the frontier while it runs. Only the questions that depend on its result wait.

Decisions belong to the dev. Put each one to them and wait.

## Record as you go

When a decision settles a domain word or a hard-to-reverse choice, record it with the `domain-modeling` skill:

- A new or sharpened term goes into `GLOSSARY.md`.
- A decision that is hard to reverse and has a real trade-off goes into `docs/decision-records/`.

Do not write a plan doc or a spec doc. The `spec` skill turns the result into tracker tickets when the dev asks.

## Finish

The session is done when the frontier is empty. Give a short list of the settled decisions. Ask the dev to confirm it. Do not act on the decisions until the dev confirms.
