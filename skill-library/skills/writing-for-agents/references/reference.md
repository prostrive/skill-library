<!-- Based on mattpocock/skills: skills/productivity/writing-for-agents (MIT) -->

# Writing for agents: reference

The levers behind the checklist in `SKILL.md`.

## Context pointers

A context pointer is a line in the agent's context that names material outside it and says when to reach it. A skill description is one. A line in `AGENTS.md` that names a doc is another. The wording of the pointer, not the material behind it, decides when and how reliably the agent reaches the material. If the agent misses material it needs, sharpen the pointer first. Move the material inline only if that fails.

A pointer does two jobs: it says what the material is, and it lists the cases that should trigger it. Every word of an always-loaded pointer costs on every turn, so prune it harder than the body.

- Put the leading word first. That is where the trigger works.
- One trigger per real case. Collapse synonyms.
- Cut what the body already says.

## The two loads

- **Context load** is the cost on the agent: material that sits in context every turn, such as an `AGENTS.md` line or a skill description.
- **Cognitive load** is the cost on the dev: knowing which documents exist and when to use each. It is the price of human control. Spend it where human judgment matters.

Material behind a pointer costs only the pointer line. Material with no pointer costs only cognitive load.

## Information hierarchy

A document holds **steps** (ordered actions) and **reference** (rules and facts read on demand). Place each piece on a ladder by how soon the agent needs it:

1. In-file steps: what the agent does, in order.
2. In-file reference: read on demand. A flat list of rules is fine.
3. Disclosed reference: a separate file behind a pointer, loaded only when the pointer fires.

Push too little down and the top bloats. Push too much down and the agent misses what it needs. The test: inline what every run needs, disclose what only some runs reach.

Keep a concept's definition, rules and caveats under one heading. Scattered parts of one meaning read as separate things.

**Sprawl** is a document that is too long even when every line is true. Attention thins. The cure is to disclose reference and to split by branch or by sequence.

## Steps and done-when lines

Every step ends on a done-when line. Two properties matter:

- **Clarity.** The agent can tell done from not done. A vague line ("understanding reached") invites the agent to stop early, because the next steps pull its attention. Sharpen the line first. If it stays fuzzy and you see the agent rush, hide the later steps behind a real context boundary: a handoff or a subagent.
- **Demand.** How much the line requires. "Every changed model has a test" forces thorough work. "Write tests" does not. Demand also binds flat reference: "every rule applied".

The strongest done-when lines are checkable and exhaustive.

## When to split

A split spends one of the two loads, so split only when it pays:

- **By sequence.** Split a run of steps when the later steps tempt the agent to rush the current one. Merging sequences does the reverse.
- **By invocation.** See `skill-mechanics.md`.

## Leading words

A leading word is a short concept the model already knows ("lesson", "tracer bullet", "fog of war"). Repeated as a token, it anchors a whole behaviour in few words. In the body it makes the agent repeat the same behaviour at each site. In a pointer, when the same word lives in your prompts and your code, it makes the agent reach the material more reliably. A coined word has no prior meaning, so it costs definition tokens. Prefer an existing word.

Look for passages to collapse:

- "fast, deterministic, low-overhead" becomes "tight" (a tight loop).
- "a loop you believe in" becomes "red": the loop goes red on the bug, or it does not.

**Negation** works against you. A ban puts the banned behaviour in context and makes it more likely. State the target behaviour ("write one-line comments"). Use a ban only for a hard guardrail you cannot phrase as a positive, and pair it with the positive.

## Pruning

- **One source of truth.** Each meaning lives in one place, so a change is a one-place edit. Duplication costs tokens and makes a rule look more important than it is.
- **The environment is a source of truth.** `package.json` scripts, config files, the folder layout and `--help` output already hold many facts. A document that repeats them is a cache that goes stale. Write down only what the agent cannot find by looking.
- **Relevance.** Each line must still affect what the document does. Lines go stale when the code changes. Without pruning, documents collect stale layers, because adding feels safe and deleting feels risky.
- **No-ops.** A sentence that the model already obeys by default does nothing. The test is whether it changes behaviour compared with the default. Settle a disagreement by running the document. Delete the whole sentence. A leading word that is too weak to beat the default ("be thorough") is also a no-op. Use a stronger word ("relentless").
