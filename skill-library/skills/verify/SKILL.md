---
name: verify
description: Drive the real app the way a user does to prove a change works, using the project's docs/agents/verify.md and its feature map in features/. Use when you are about to say an app change is done.
---

<!-- Based on backnotprop/pstack: skills/create-verification-skill, skills/maintain-verification-skill, skills/principle-prove-it-works (MIT) -->

# Verify

A change is done when you watched the real app do the right thing. A green test you did not watch run, a build that compiles, or a subagent's report is not proof.

The project holds two things:

- `docs/agents/verify.md`: how to start the app and drive it. It has five sections: Launch, Doctor, Drive, Evidence, Cleanup.
- `features/`: the feature map. `features/README.md` is the index, plus the baseline state and the driving rules. Each other file is one feature with four sections: `Sub-features`, `How to get to it (user POV)`, `Driving it with <harness>`, `Gotchas`. See `references/feature-map-example/`.

## Modes

- `/verify` (default, and when this skill loads by itself): prove the current change.
- `/verify setup`: write `docs/agents/verify.md`, a driver script when the app needs one, and seed `features/` for a repo that has none of them. Follow `references/setup.md`.
- `/verify sweep`: check the whole app, not one change. Walk the sweep order in `features/README.md`, drive each feature's entry points, and end with `features/journeys.md`. Report one line per feature: passed, failed with evidence, or not reachable with the reason.
- `/verify audit`: check that verify.md and the feature map still match the app. Follow `references/audit.md`.

If `docs/agents/verify.md` is missing in default mode, say so. Then verify as well as the repo allows (its dev command, its existing e2e harness, curl for an API), and offer `/verify setup`. Do not invent a harness.

## Default mode

1. **Scope.** List the user-facing behavior the change touches. Find the matching files in `features/`. A change to a feature that has no file is a gap: say so, and verify it from the code anyway.
2. **Launch.** Follow Launch in verify.md. When verify.md names a driver, use its `start` and `doctor` commands. Ready means usable, not only that a process answers. Never drive an instance you did not start, unless verify.md says the dev already runs a shared one.
3. **Doctor.** Run the Doctor check before the first drive and again after any drive that fails or surprises you.
4. **Drive.** Follow the feature file's drive steps for every entry point the change can affect. For each one, drive every state the change can touch: success, cancel, error, empty, and persistence (reload or read the value back a second way). Use the real user path: no internal setters, no test-only endpoints, no mocks except where production already has a boundary.
5. **Evidence.** Capture the action and the resulting state, not only the final screen. Check side effects too: rows written, files created, messages sent. Store the evidence where verify.md says.
6. **Cleanup.** Stop what you started. Never kill a process by name. Evidence survives cleanup. Check it is still there.
7. **Report.** Two lists: what you checked, with the entry point and the evidence path for each, and what you could not check, with the reason. Say "done" only when the first list covers the change.

## Fail conditions

The run fails, and you report it as failed, when:

- You weakened a drive step or an expected result to make it pass. A missing precondition is a failure, and its reason goes in the feature's `Gotchas`.
- You proved fewer entry points than the feature file lists for the behavior you changed.
- You report a skipped entry point as verified through a different path.
- The only proof is a test run, a log line or an agent's word that you did not check against the real app.

When a check fails, suspect how you observed it before you suspect the app. Then rerun once. If it still fails, report the failure with the steps and the evidence. Do not change product code in the same breath to make the check pass.

## Update the map

When a change adds or moves a user-facing entry point, update its feature file in the same PR. Keep implementation details out of the map: user paths, stable handles (ARIA names, routes, CLI flags), required state, and observable proof only.

## Parallel runs

Two runs never share an instance, a data directory or a browser profile. If verify.md says the app cannot run twice side by side, run the verifications one after another.
