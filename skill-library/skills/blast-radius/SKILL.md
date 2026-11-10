---
name: blast-radius
description: Find what a change can break outside its diff, and prove the one fact that makes it safe by running real code. Use when the user asks what a change could break.
---
<!-- Based on backnotprop/pstack: skills/blast-radius (MIT) -->

# Blast radius

Find what a change breaks somewhere else, before it ships.

Listing the callers is not the job. You can grep those in a second. The job is the breakage grep does not show.

`how` says what the code does. `why` says why it has that shape. `blast-radius` says what it breaks elsewhere.

## Do not trust your own write-up

A write-up that sounds right reads the same whether it is true or not. So find the one or two facts the change's safety depends on, and prove them by running code.

For each fact, get it as far down this list as is cheap, and say where it stopped:

1. You said so. Worth nothing on its own.
2. You pointed at the line: a real `file:line`, or the library's own source.
3. You showed the bad case cannot happen: you walked the failure step by step and it does not reach.
4. You ran it: a script or test that calls the real code and fails loud if you are wrong.
5. You reproduced it in the running app.

Step 4 is usually one small script that imports the library the app ships and calls the exact function you worry about.

## Steps

1. Read the change: the diff, the symbols it adds, changes and deletes, and what it now does differently, including what the diff does not spell out. Read the PR and commits with `gh` and `git log`.
2. Find the one fact it is safe because of. Most risky-looking changes are safe because of a single fact, for example "this call only drops cache entries that are already dead". If that fact holds, most risks clear at once. Spend your time here.
3. Look where grep stops:
   - the source of the library you call, at its pinned version, and any local patch
   - when things run: microtasks, teardown, unmount, retries, scheduled jobs
   - what a symbol search misses: the JSON an API returns, a DB column, a wire format, another service or language that reads the same data, a feature flag, code three hops downstream
4. Rate each risk honestly: how likely, and how bad. Keep the confirmed ones. List the cleared ones separately. Cite real `file:line`. A search that finds nothing is still an answer. Never invent a caller or an API.
5. Prove the one fact. Write a script or test that runs the real code, run it, and paste what it printed.

Keep scripts out of the commit unless the user wants the test.

## Output

- **What it does.** What changed, including the part that is not obvious.
- **The fact it is safe because of.** State it, say which step of the list you reached, and show the proof. If you could not prove it, write "unproven".
- **Risks.** For each: how it breaks, `file:line`, how likely, how bad, how to check. Paste the proof for the ones that matter.
- **Cleared.** What you checked and why it is fine.
- **Before you merge.** The cheapest test or repro that catches the real bug, including the script you wrote.
