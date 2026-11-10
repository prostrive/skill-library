---
name: how
description: Explain how a part of the codebase works, or where new code belongs, at the level a senior engineer needs to start working in it. Use when the user asks how code works, asks for a walkthrough before a change, or asks which module or layer should own something.
---

<!-- Based on backnotprop/pstack: skills/how (MIT) -->

# How

Answer "how does X work?" and "where should this live?" from the code. Give a working mental model, not annotated source. For why the code is shaped this way, use the `why` skill.

If the question is vague, state how you read it in one line and go on. The user can redirect.

## 1. Size it

- **Simple:** one module, one utility, or one function. Start no explorers. Start one explainer subagent that explores and explains in one pass, built from `references/explainer-prompt.md` without the explorer-findings section. Go to step 4.
- **Complex:** a subsystem across files or services, a cross-cutting feature, or a full overview. Go to step 2.

When in doubt, take the simple path.

## 2. Explore (complex only)

Split the question into 2 to 4 angles, each a separate slice of the subsystem. Start one read-only explorer subagent per angle, all in one message, each with a fresh context and `references/explorer-prompt.md` filled in.

## 3. Synthesize (complex only)

When all explorers are back, start one explainer subagent with `references/explainer-prompt.md` and every explorer's findings filled in.

## 4. Present

Give the explainer's answer. Fix wording or add context from the conversation, but do not rewrite it.

Use the sections from `references/explainer-prompt.md` and drop the ones that do not apply: Overview, Key Concepts, How It Works, Where Things Live, Gotchas.

For a placement question, end with one recommendation: the file or module, and the one or two facts from the code that decide it.

Use the words from `GLOSSARY.md` if the repo has one.
