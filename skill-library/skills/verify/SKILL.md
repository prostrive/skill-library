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

If `docs/agents/verify.md` is missing in default mode, say so, and check if another branch has it (for example the default branch). Then verify only with what cannot touch the dev's own stack: tests, type checks, a harness that starts its own isolated copy, or requests to an instance the dev names. Never start, reset or seed a stack with the repo's normal dev commands: they often share fixed ports, data and container names with the dev's running stack. Offer `/verify setup`. Do not invent a harness.

## Default mode

1. **Scope.** List the user-facing behavior the change touches. Find the matching files in `features/`. A change to a feature that has no file is a gap: say so, and verify it from the code anyway.
2. **Launch.** Follow Launch in verify.md. When verify.md names a driver, use its `start` and `doctor` commands. Ready means usable, not only that a process answers. Never drive an instance you did not start, unless verify.md says the dev already runs a shared one.
3. **Doctor.** Run the Doctor check before the first drive and again after any drive that fails or surprises you.
4. **Drive.** Follow the feature file's drive steps for every entry point the change can affect. For each one, drive every state the change can touch: success, cancel, error, empty, and persistence (reload or read the value back a second way). Drive a state that shows only once, such as an empty list, first, or `reset` before it. An entry point counts as driven when you reached it the way a user does, checked that the final URL or screen is the one you meant (a redirect can land you elsewhere), and ran its main action. Opening a page alone is not enough. Use the real user path: no internal setters, no test-only endpoints, no mocks except where production already has a boundary. A precondition that only another role can create, such as an admin setting, goes through that role's real path (its UI or API), never through a direct database write.
5. **Evidence.** Capture the action and the resulting state, not only the final screen. Check side effects too: rows written, files created, messages sent. Store the evidence where verify.md says.
6. **Cleanup.** Cleanup is part of the run, never a task for the dev. Before Launch, write down in the evidence folder everything you start: container project names, networks, volumes, process IDs, worktrees. At the end, and also when a step fails or you stop early, remove every item on that list, then check that none is left. Something the run created by mistake, even inside another project, is on the list too: check its creation time, then remove it. When a cleanup command needs the dev's permission, ask for it in the run. Never kill a process by name. Evidence survives cleanup. Check it is still there.
7. **Report.** Use the report format below. Say "works" only when the checked list covers the change.

## Report format

Write for the dev, not for the next agent. Plain words, no emoji. In this order, and leave out a section that is empty:

```
**<Works | Works, with gaps | Broken>.** <One sentence: what the change does now, as a user sees it.>

**Checked** (evidence in <path>)
- <behavior, in user words>: ok | broken

**Not checked:** <what, and why, one line each>

**Product issues:** <what a user sees, and whether it is older than this change>

**Cleaned up:** <what you stopped. Name only what you could not clean, or any harm to something you did not start>
```

Keep these out of the report:

- Your own failed attempts, for example a request you built wrong. Retry them. They are not results.
- Setup trouble, for example a missing env var or config value. Fix it in `docs/agents/verify.md` or the feature's `Gotchas`, and add one line: "Updated Gotchas in <file>".
- Cleanup steps for the dev. A report that asks the dev to clean up is a failed cleanup: go back and finish it.
- Internal IDs and raw payloads. Put them in the evidence folder.

## Fail conditions

The run fails, and you report it as failed, when:

- You weakened a drive step or an expected result to make it pass. A missing precondition is a failure, and its reason goes in the feature's `Gotchas`. Changing an expectation is a correction, not a weakening, only when the feature file was wrong about the product and you record the proof (code, ticket or decision) in `Gotchas`.
- You proved fewer entry points than the feature file lists for the behavior you changed.
- You report a skipped entry point as verified through a different path.
- The only proof is a test run, a log line or an agent's word that you did not check against the real app.

When a check fails, suspect how you observed it before you suspect the app. Then rerun once. If it still fails, report the failure with the steps and the evidence. Do not change product code in the same breath to make the check pass.

## Update the map

When a change adds or moves a user-facing entry point, update its feature file in the same PR. Keep implementation details out of the map: user paths, stable handles (ARIA names, routes, CLI flags), required state, and observable proof only.

## Parallel runs

Two runs never share an instance, a data directory or a browser profile. Every container command sets its own project name, derived from the worktree path. Never rely on the folder name: a worktree folder can have the same name as the main checkout. If verify.md says the app cannot run twice side by side, run the verifications one after another.
