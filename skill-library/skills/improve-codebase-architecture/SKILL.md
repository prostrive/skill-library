---
name: improve-codebase-architecture
description: Scan a codebase for places where shallow modules can become deep ones, show them as a visual HTML report outside the repo, then work through the one the user picks. Use when the user asks to find architecture improvements in a codebase.
---
<!-- Based on mattpocock/skills: skills/engineering/improve-codebase-architecture (MIT) -->

# Improve codebase architecture

Find architectural friction and propose **deepening opportunities**: refactors that turn shallow modules into deep ones. The aim is code that is easy to test and easy for agents to navigate.

Use the vocabulary and principles from the `codebase-design` skill: module, interface, implementation, depth, seam, adapter, leverage, locality, the deletion test, "the interface is the test surface", and "one adapter is a hypothetical seam, two make a real one". Do not drift into "component", "service", "API" or "boundary".

Use the domain words from `GLOSSARY.md`. Read the decision records in `docs/decision-records/` for the area. Do not reopen a recorded decision without a real reason.

## 1. Explore

Decide where to look before you look.
- If the user named a module, subsystem or pain point, start there.
- Otherwise read a long stretch of `git log --oneline` and find the hot spots: the files and areas that change again and again. A deeper module pays off where code changes, so weight recent change. If changes are scattered, widen the search.

Then start one subagent with a fresh context to walk that part of the codebase. Ask it to note where it feels friction:
- Where does one concept force a jump between many small modules?
- Where is a module shallow, with an interface nearly as complex as its implementation?
- Where were pure functions pulled out only for tests, while the bugs hide in how they are called?
- Where do coupled modules leak across their seams?
- Which parts are untested, or hard to test through their current interface?

Apply the deletion test to anything that looks shallow. "Deleting it would concentrate complexity" is the signal you want.

## 2. Write the HTML report

Write one self-contained HTML file to the OS temp folder, so nothing lands in the repo: `$TMPDIR` (fallback `/tmp`) `/architecture-review-<timestamp>.html`. Open it (`open` on macOS, `xdg-open` on Linux, `start` on Windows) and give the user the path.

Each candidate gets one card:
- **Files**: the modules involved.
- **Problem**: one sentence on the friction.
- **Solution**: one sentence on what changes.
- **Wins**: in terms of locality, leverage and how tests improve.
- **Before / after diagram**: side by side, drawn for this case.
- **Strength**: `Strong`, `Worth exploring` or `Speculative`.

End with a **Top recommendation**: which candidate to do first, and why.

If a candidate goes against a decision record, include it only when the friction is real enough to reopen the decision, and mark it on the card. Do not list every refactor a decision rules out.

Layout, diagram patterns and style: [references/html-report.md](references/html-report.md).

Do not propose interfaces yet. When the file is written, ask: "Which of these do you want to explore?"

## 3. Work through the chosen candidate

When the user picks one, use the `grill` skill to walk the decisions with them: constraints, dependencies, the shape of the deepened module, what sits behind the seam, which tests survive.

Keep the domain model current as decisions land, with the `domain-modeling` skill:
- A deepened module is named after a concept that is not in `GLOSSARY.md`: add the term. Create the file if it does not exist.
- A fuzzy term gets sharper: update `GLOSSARY.md` there and then.
- The user rejects the candidate for a reason a future review would need: offer to record it as a decision record so later reviews do not suggest it again. Skip reasons that are temporary or obvious.
- The user wants to compare interfaces: use the design-it-twice pattern from `codebase-design`.
