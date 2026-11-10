---
name: domain-modeling
description: Build and sharpen the project's domain model in GLOSSARY.md and ADRs. Use when the dev defines, renames or disputes a domain term.
---

<!-- Based on mattpocock/skills: skills/engineering/domain-modeling (MIT) -->

# Domain modeling

Sharpen the project's words and record its decisions while the work happens. Reading `GLOSSARY.md` for words is not this skill. This skill is for changing the model.

## Files

- `GLOSSARY.md` at the repo root holds the domain words. Format: [references/glossary-format.md](references/glossary-format.md).
- A repo with more than one context has `GLOSSARY-MAP.md` at the root. It points to one `GLOSSARY.md` per context. Pick the context the topic belongs to. Ask if it is not clear.
- ADRs live in `docs/decision-records/`, numbered `0001-slug.md`. Format: [references/adr-format.md](references/adr-format.md). A context can have its own `docs/decision-records/` next to its glossary.

Create a file only when you have something to write in it.

## During the work

**Challenge against the glossary.** When the dev uses a word that conflicts with `GLOSSARY.md`, say so at once: "The glossary defines 'cancellation' as X, but you mean Y. Which one is it?"

**Sharpen fuzzy words.** When a word is vague or has two meanings, propose one exact term: "You say 'account'. Do you mean the Customer or the User? Those are different things."

**Test with concrete cases.** When the dev describes how two concepts relate, invent a specific case at the edge and ask what happens. Make the boundary between the concepts exact.

**Check the code.** When the dev says how something works, check whether the code agrees. Report a conflict: "The code cancels whole Orders, but you said a partial cancel is possible. Which is right?"

**Update `GLOSSARY.md` at once.** When a term is settled, write it in the glossary right then. Do not collect terms for later. The glossary holds words and definitions only. No implementation detail, no spec, no notes.

**Offer an ADR only when all 3 are true:**

1. It is hard to reverse.
2. A future reader would be surprised without the reason.
3. There was a real trade-off between real options.

If one is missing, skip the ADR.

## When the output conflicts with an ADR

If your proposal goes against an existing ADR, say so, and give the reason to reopen it: "This goes against ADR-0007 (event-sourced orders). It is worth reopening because ..." Do not override an ADR without saying so.

## Other skills

Other skills read `GLOSSARY.md` and use its words in ticket titles, test names and proposals. When a skill needs a term the glossary does not have, that is a signal for this skill: the term is new language (reconsider it) or a real gap (add it).
