---
name: research
description: Research a question against primary sources and give a cited answer that lists the options rejected and how many sources were read. Use when the user asks to research a topic, an API, a library or a set of options.
---

<!-- Based on mattpocock/skills: skills/engineering/research; backnotprop/pstack: skills/principle-explain-the-number (MIT) -->

# Research

Start a research subagent with a fresh context. Run it in the background when there is other work to do, so the session keeps going while it reads. Give it the question, what the user already ruled out, and the rules below.

## Rules for the researcher

1. **Primary sources first.** Official docs, source code, specs, changelogs, first-party APIs, pricing pages. A blog post or a forum answer only leads you to the primary source. It does not replace it. Follow each claim back to the source that owns it.
2. **Check what is current.** Note the version and the date of each source. Prefer the latest stable docs. Say when a source is older than the thing it describes.
3. **Cite every claim.** Each claim gets a link or a `path:line`. A claim you cannot cite is marked as unconfirmed, or it is left out.
4. **Cover the options.** For a choice between options, look at each serious option, not only the first one that fits. Do not repeat an option the user already rejected.
5. **Numbers need context.** For a measured number (a benchmark, a latency, a limit, a price), say where it comes from, under which conditions, and what else it could be measuring. Do not compare numbers from different setups as if they were the same.
6. **Do not stop early.** Read until the answer holds, not until the first plausible answer. If the sources disagree, say so and show both.

## The answer

Short and in this order:

1. **Answer:** the direct answer or recommendation in 1 to 3 sentences.
2. **Evidence:** the facts that carry it, each with its source.
3. **Rejected:** each option or explanation you looked at and dropped, with the reason in one line.
4. **Open:** what you could not confirm, and who or what could settle it.
5. **Coverage:** the number of sources read, and which kinds (docs, source code, issues, changelogs).

## Keep or not

Answer in the chat by default. Write the findings to a Markdown file only when the user asks to keep them. Then save it where the repo already keeps such notes. If there is no such place, use `docs/research/<topic>.md` and say where it went. Keep the same five sections and the source links.
