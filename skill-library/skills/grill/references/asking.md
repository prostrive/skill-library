# How to ask the dev

These rules apply to every skill that puts a decision to the dev: `grill`, `spec`, `implement`, `triage`.

## Use the question dialog

Ask with the `AskUserQuestion` tool when it is available. It shows clickable options, and the dev answers a whole round in one go.

- **Up to 4 questions per round.** Send them in one call. Never send one question when more are ready.
- **One decision per question.** If "yes" would accept two things, it is two questions. "Admins can export, and the export uses the screen filters" is two decisions.
- **2 to 4 options per question.** Each option has a short label and a one-line description of what happens if the dev picks it. The dialog adds "Other" by itself.
- **Recommend only with a reason.** Put the recommended option first and add "(Recommended)" to its label only when the code, a ruling, a legacy system or the PRD points to it. Name that source in the option's description. With no evidence, give no recommendation.
- **Multi-select** when the choices combine, for example which fields a row shows.
- **Header:** a chip of at most 12 characters, for example "Scope" or "Export".
- **Context:** at most 2 short lines in the chat above the dialog. Facts the dev needs to decide go in the question or the option descriptions, not in paragraphs.

When the dialog is not available, use the same structure as a numbered list, with lettered options the dev can answer as "1a, 2c, 3b".

## Defaults

Some choices are too small for a question, for example the wording of an error or the order of columns. Take a default for each, then show all of them at once:

1. A numbered list, one line each: the choice and the default you took.
2. One dialog question: "Accept all defaults" or "I change some". If the dev changes some, each one they name becomes a question in the next round.

Never leave a default out of the list because it seems obvious.

## Sources

Every decision that ends up in a ticket or in code has one source:

- `[dev]`: the dev decided it.
- `[fact: <source>]`: it follows from the code, a ruling, a legacy system, the PRD or the ticket. Name the source.
- `[default]`: you chose it and the dev accepted it in the defaults list.

A choice with none of these is still open. Ask it.
