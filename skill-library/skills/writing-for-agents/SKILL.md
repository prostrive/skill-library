---
name: writing-for-agents
description: How to write a document an agent reads, such as a skill, AGENTS.md or CLAUDE.md. Use when creating or editing a skill, AGENTS.md or CLAUDE.md.
---

<!-- Based on mattpocock/skills: skills/productivity/writing-for-agents (MIT) -->

# Writing for agents

A document for an agent works when the agent takes the same path through it every run. The words decide that path. This file is the checklist. [references/reference.md](references/reference.md) explains each lever. [references/skill-mechanics.md](references/skill-mechanics.md) covers skill frontmatter and invocation.

## Before you write

1. **Check the environment first.** A fact the agent can read from `package.json`, a config file, `--help` or the folder layout does not go in the document. Write down only what the agent cannot find by looking: the unwritten rule, the reason behind a choice, the gotcha.
2. **Pick the home.** A rule for every task in the repo goes in `AGENTS.md`. A procedure that runs only sometimes is a skill. Detail that only some runs need goes in a `references/` file behind a pointer.
3. **For a skill, pick the invocation.** Slash-only (`disable-model-invocation: true`) costs no context but the dev must remember it. Auto-load costs its description in every session. Choose auto-load only when the agent must reach the skill without being asked. See [references/skill-mechanics.md](references/skill-mechanics.md).

## The description (the pointer)

The description of an auto-load skill sits in context every turn. It decides when the agent loads the skill.

- First, say what the skill does, in one sentence. Then `Use when <one concrete trigger>.` The trigger is something the agent can see in the work: a failing test, a "done" claim, an edit to a file.
- One trigger per real branch. Synonyms for one case are one trigger.
- Never write `MUST`, `always`, `even if`, `1%`, `not optional` or `not negotiable`. Pressure words make a skill fire on everything.
- A slash-only skill has a one-line description for the dev. No trigger list.

## The body

- **Steps in order.** Number the steps the agent performs.
- **Each step ends on a done-when line.** The agent can check it, and it covers all the work: "every changed model has a test" beats "write tests".
- **Disclose what only some runs need.** Inline what every run needs. Move the rest to `references/` behind a link that says when to read it.
- **Keep one meaning in one place.** Do not repeat a rule in two files. Point to it.
- **Say the positive.** State the behaviour you want. A ban puts the banned behaviour in context. Use a ban only for a hard guardrail, and pair it with the positive.
- **Use leading words.** One existing word ("tracer bullet", "red", "tight loop") carries a whole behaviour in fewer tokens than a sentence. Reuse it at each site.
- **Delete no-ops.** A sentence that the model already follows by default changes nothing. Delete the whole sentence.
- **Stay under about 120 lines.** A long document thins the agent's attention, even when every line is true.

## Style

Plain English. Active voice. One instruction per sentence. Short words. The real names of files, commands and flags. No marketing words. Do not explain why the document exists. Say what to do.

Questions to the dev: at most 3 at a time, and only what the code, the tracker or the docs cannot answer.

## After you write

1. Read each sentence and ask: does it change what the agent does? If not, delete it.
2. Check each done-when line: can the agent tell done from not done?
3. In the skill-library repo, run `bash scripts/check-skills.sh`.
4. If you can, run the skill once on a real task and watch where the agent takes a different path than you meant. Fix the wording there.

**Done when** every sentence changes behaviour, every step has a done-when line, and the description has one trigger with no pressure words.
