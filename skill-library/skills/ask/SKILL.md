---
name: ask
description: List, ask and create topic experts. Each expert is a subagent with a short brief in the repo that it rewrites after each answer. Use when the user asks a question about a topic that has an expert in .claude/agents/.
argument-hint: "[<topic> <question> | new <topic>]"
---

<!-- Based on backnotprop/pstack: skills/recall and mattpocock/skills: skills/engineering/domain-modeling (MIT) -->

# Ask

A topic expert keeps the context of one topic between sessions, for example one module or one integration. The context lives in a short brief file, not in a long chat. Each question costs one read of the brief.

An expert is two files:

- `.claude/agents/<topic>.md`: the subagent. Its instructions point at the brief.
- `docs/topics/<topic>.md`: the brief. Facts, decisions with dates, and open questions.

The registry is the set of `.claude/agents/*.md` files that have a matching `docs/topics/<topic>.md`.

## `/ask`: list the experts

List each expert: its topic, the description line from its agent file, and the date the brief last changed (`git log -1 --format=%cs -- docs/topics/<topic>.md`). If there are none, say so and show how to create one.

## `/ask <topic> <question>`: ask an expert

1. Check that both files exist. If not, list the experts that do exist and stop.
2. Start the expert as a subagent with its agent type `<topic>` and a fresh context. Pass the question word for word.
3. The expert follows its own instructions: it reads the brief, checks recent commits and tickets on the topic, answers, and rewrites the brief.
4. Give the dev the expert's answer. Add one line if the brief changed.

Send a follow-up question on the same topic in this session to the same subagent, so it keeps its context. A question on another topic goes to that topic's expert.

When the dev asks a question in plain words and an expert's topic clearly matches it, ask that expert. Say which expert answered.

## `/ask new <topic>`: create an expert

1. Use a short kebab-case topic name.
2. Ask the dev, in one `AskUserQuestion` round, only what the code, the tracker and the docs cannot answer:
   - What does this topic cover, and what is out of it?
   - Where does its truth live: code folders, tracker project or label, docs?
   - What has already been decided?
3. Write `.claude/agents/<topic>.md` from `references/expert-template.md`.
4. Write `docs/topics/<topic>.md` with the brief sections from the template, filled with the answers. Leave a section empty rather than guess.
5. Tell the dev the expert exists and how to ask it.

Both files belong in git, so the whole team shares the expert.

## The brief stays short

The expert rewrites the brief after each answer. It does not only append. It removes facts that are no longer true, merges duplicates and moves answered questions to the decisions. A brief past about 80 lines needs cutting before it grows further.
