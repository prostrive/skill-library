---
name: pr
description: Write a PR body that a reviewer can read fast, with a small visual summary, before-and-after evidence and the merge danger. Use when writing a PR body.
---
<!-- Based on mattpocock/skills: skills/engineering/pr (MIT), which credits Dex Horthy's show-me skill (humanlayer) for the Summary visuals -->

# PR

Use this template for the PR body:

```markdown
## Summary

<diagram, diff sketch or tree>

## Evidence

- **Before:** <screenshot, output or failing test run>
  **After:** <screenshot, output or passing test run>

## Merge danger

**Door:** <one-way or two-way>

<optional: one line>

**Blast radius:** <one word>

<optional: what can break after merge>
```

Follow the repo's PR rules in `AGENTS.md` first: title format, ticket link, branch name. Use the domain words from `GLOSSARY.md`. No preamble. Keep prose short.

## Summary

Pick the smallest view that makes the point.

- Logic or an algorithm: pseudocode.

```text
on(save)
  if content is unchanged
    return cached result
  write new content
```

- Runtime control flow: a call tree.

```text
submitForm
  createSession
    persistPrompt
  navigateToSession
```

- UI structure: a component tree with the state and module edges that matter.
- File ownership or a broad refactor: a shallow file tree with one comment per folder.
- Interaction or data flow between parts: a Mermaid sequence or flowchart.
- What changes inside a shape that already exists: a `diff` block of the tree, call tree or pseudocode.

```diff
 on(save)
-  write content
+  if content is unchanged
+    return cached result
+  write new content
```

- Show the whole block only when most of it is new or the reader needs the exact shape.

Put each visual next to the line of text it supports. Keep only the calls, files, props and states the reviewer needs. Use one or two visuals, not all of them.

## Evidence

Show that the change works, before and after.
- A screenshot is best when the change is visual and the environment allows it.
- Execution evidence is next: the test that failed and now passes, or command output.
- Say what you could not check.

## Merge danger

- **Door.** Two-way: cheap to roll back. One-way: destructive or hard to reverse, for example a data migration, a deleted column, a public API change or an email that goes out.
- **Blast radius.** What else the change can touch: other consumers, layout, mobile, jobs, other services. Run `blast-radius` when you are not sure.
