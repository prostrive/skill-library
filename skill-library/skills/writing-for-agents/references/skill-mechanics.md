<!-- Based on mattpocock/skills: skills/productivity/writing-for-agents/SKILL-MECHANICS.md (MIT) -->

# Skill mechanics

What changes when the document is a skill: the frontmatter, the invocation choice and router skills.

## Frontmatter

```yaml
---
name: <same as the folder name>
description: <what it does>. Use when <one concrete trigger>.
---
```

A slash-only skill adds `disable-model-invocation: true`, and its description is a one-line summary for the dev.

## Invocation

There are two choices. Each one spends a different budget.

- **Auto-load.** The description stays in context in every session, so the agent can load the skill by itself and other skills can reach it. The dev can still type `/name`. This costs context on every turn. Write a trigger the agent can see in the work.
- **Slash-only.** `disable-model-invocation: true` hides the skill from the agent. Only a dev who types `/name` can run it, and no other skill can reach it. It costs no context, but the dev must remember that it exists.

Choose auto-load only when the agent must reach the skill without being asked, or another skill must reach it. A skill that only ever runs by hand is slash-only.

Keep these slash-only:

- skills that interview the dev
- skills that change repo config once (setup)
- skills that answer a signal only the dev can give ("I'm lost", "I'm stopping")

Reference that two slash-only skills both need cannot live in either one, because neither can load the other. Put it in a plain file that both point to.

## Splitting by invocation

Split off an auto-load skill only when it has its own trigger word that you use in real prompts, or another skill must reach it. The new description costs context in every session, so the separate reach must be worth it.

## Router skills

When there are more slash-only skills than a dev can remember, add one slash-only router skill. It names the others and says when to use each. It can only point. It cannot run them.
