---
name: diagnose
description: Find the root cause of a bug or a slowdown with a feedback loop that goes red on the bug before any fix, then fix it where it starts. Use when something is broken, throws, fails or is slow.
---
<!-- Based on mattpocock/skills: skills/engineering/diagnosing-bugs; backnotprop/pstack: skills/principle-fix-root-causes, skills/principle-attack-the-premise (MIT) -->

# Diagnose

Read `GLOSSARY.md` and the decision records in the area first, so you know what the modules mean.

Replace every secret in commands and output with `<REDACTED>`. Keep credentials in environment variables, not in what you show.

## 1. Build a feedback loop

This is the main step. With a pass/fail signal that goes red on this bug, you will find the cause. Without one, reading code will not save you.

Try these, in this order:

1. A failing test at the seam that reaches the bug.
2. A curl or HTTP script against the running app.
3. A CLI run with a fixed input, diffed against a known-good output.
4. A headless browser script that drives the UI and checks the DOM, console or network.
5. A replay of a captured request, payload or event log.
6. A small harness that runs only the broken code path.
7. A loop over many random inputs, for "sometimes wrong".
8. `git bisect run` between a good and a bad commit.
9. The same input through the old and the new version, with a diff.
10. Last: a script that walks a person through the steps. Start from [scripts/hitl-loop.template.sh](scripts/hitl-loop.template.sh).

Then make the loop faster, sharper (assert the exact symptom) and deterministic (pin time, seed random, isolate files and network).

For a flaky bug, raise the failure rate: run the trigger 100 times, in parallel, under load.

You are done with this step when you can name one command that you already ran, with its output, and that:

- drives the real code path and asserts the user's exact symptom,
- gives the same result every run,
- runs in seconds,
- runs without a person, except through the script in step 10.

Do not form a theory before this command exists. If you cannot build a loop, stop. Say what you tried. Ask the dev for access to an environment that shows the bug, a captured artifact (HAR, logs, recording), or approval for temporary logging in production.

## 2. Reproduce and shrink

Run the loop and watch it go red. Check that it is the failure the user described, not a different one nearby.

Then shrink it. Remove inputs, callers, config and steps one at a time. Rerun after each cut. Stop when every part left is needed for the failure.

## 3. Hypotheses

Write 3 to 5 hypotheses, ranked. Each one states a prediction: "If X is the cause, then changing Y makes the bug go away."

Show the list to the dev. They may know that one is already ruled out. Do not wait for an answer if they are away.

## 4. Probe

Each probe tests one prediction. Change one thing at a time.

- Prefer a debugger or REPL over logs.
- Put logs only at the boundaries that separate two hypotheses. Tag each one with a unique prefix, like `[DEBUG-a4f2]`, so you can remove them with one grep.
- For a slowdown, measure first: a timing harness, a profiler or a query plan. Then bisect.

## 5. Find the root cause

The symptom is where a wrong state became visible. The root cause is the first place the code made a wrong decision.

- Ask "why" at each step until the answer is a wrong decision in the code, not a result of an earlier one.
- Ask whether the state that broke the code is a valid state. If it is valid, the code that broke on it is the cause. If it should never exist, find what created it. A guard, retry, swallowed error or clamp at the symptom only hides the bug.
- A failure that only appears after a restart points to saved state first: config, caches, lock files.
- Look for the same fault in other places and fix all of them.

When two fixes that share one assumption both failed, stop fixing. Write the assumption down in one sentence. Test it directly before the next fix.

## 6. Fix and lock it

1. If a seam exists that reproduces the real bug pattern, turn the shrunk repro into a failing test there. Watch it fail.
2. Apply the fix at the root cause.
3. Watch the test pass. Rerun the original loop from step 1.

If no such seam exists, say so. That is a finding about the design.

## 7. Clean up

- The original loop no longer shows the bug.
- The regression test passes, or you said why there is none.
- No `[DEBUG-` logs remain.
- Throwaway harnesses are deleted.
- The commit or PR message names the cause that turned out to be true.

If the cause took a long dig to find, propose the cheap signal (a log line, a metric, an assertion) that would have shown it at once.
