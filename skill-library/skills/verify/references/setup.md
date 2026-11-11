# /verify setup

Write `docs/agents/verify.md` and seed `features/` for a repo that has neither. You write for the next agent. It reads these files cold, in the middle of a task, and has never seen the app.

## 1. Read the repo, not the dev

Answer these from the code. Ask the dev only what you cannot observe, following the asking rules in the `grill` skill (`references/asking.md`).

- **Surface:** what does a user touch? Web UI, CLI or TUI, desktop app, API, mobile app, library. Pick the main one and note the others.
- **Run:** how does the app start locally? Use the repo's own dev command (package scripts, Makefile, README). Note ports, env vars, seed data and sign-in.
- **Drive:** how can an agent drive it? Use an existing harness first: Playwright or Cypress specs, a sign-in script, PTY helpers, curl-able endpoints. Only then pick a generic recipe: a browser for web and Electron, tmux or a PTY for CLI and TUI, plain HTTP for a service.
- **Observe:** what evidence can you capture? Screenshots, ARIA snapshots, terminal transcripts, response bodies, logs, exit codes, database rows.
- **Isolate:** can two instances run side by side (ports, data dirs, browser profiles)? Which services are shared and cannot run twice, for example an auth server or a database? Write both in verify.md.

If the checkout does not build or start, fix that first or report it exactly. A verify.md written against a broken base teaches wrong steps.

## 2. Write docs/agents/verify.md

Five sections, each with real commands from this repo. No placeholders.

- **Launch:** the exact command that starts the app, and how to tell it is ready (a log line, a URL that answers with real content). Launch reaches a usable state from an empty data dir, with migrations and seed data. Include sign-in for a test user. Never ask the dev to sign in by hand if a scripted test session is possible.
- **Doctor:** one read-only check that answers "is this instance worth driving?": process up, right build, port owned by this run, sign-in valid.
- **Drive:** the harness recipe with real selectors and commands. Prefer stable handles: ARIA names, data attributes, routes, prompt strings. No screen coordinates.
- **Evidence:** what to capture and where it goes (a gitignored folder). The proof rules: the real user path, the action and the resulting state, side effects checked, mocks only at a production boundary. When a dry-run mode is the safe path, check what it really skips by observing, not by its name.
- **Cleanup:** how to stop what the run started. Kill what you started, never by process name. Cleanup removes instances and scratch state, never the evidence.

A helper script that verify.md uses is executable, lives in the repo, and verify.md shows how to call it.

## 3. Write a driver when the app needs one

Write a driver when any of these is true: the app needs more than 3 commands to start, it has several services, it shares a service with other runs, or more than one agent may verify at the same time. Otherwise skip this step.

The driver is one script in the repo, for example `scripts/verify/<app>`, in the repo's own language. It has a fixed set of commands and `--help` lists them:

- `start`: starts this worktree's instance and waits until it is usable.
- `doctor`: read-only. Reports who owns the port (process and folder), whether that instance belongs to this worktree, the commit it runs, and the health of each shared service.
- `stop`: stops only what this worktree started, by the process ID it saved. Never by process name or port alone.
- `info`: prints the URL, ports, data folder and browser profile of this worktree's instance.
- The drive helpers the feature map needs, for example `sign-in`, `seed`, `browser <action>` or `cli -- <command>`.

Rules:

- Derive the port, data folder and browser profile from the worktree path, so each worktree gets its own instance and two runs never collide.
- Refuse to drive an instance this worktree did not start, unless the dev passes it on purpose.
- Never restart or reset a shared service. `doctor` reports a broken shared service, and the run stops there.

verify.md documents the commands, not the script's code. The feature files call the driver, not loose commands.

## 4. Seed the feature map

Create `features/README.md` and one file per user-facing feature. Start with the top 3 to 5, from routes, commands, menus or docs. Copy the shape of `feature-map-example/`:

- The README holds the baseline state, the driving rules, the proof rules, the index and the sweep order: the order in which `/verify sweep` walks the features.
- `features/journeys.md` holds the flows that cross several features, for example sign up, then create, then share. A sweep ends with it.
- Each feature file has an H1, one paragraph on what the user sees, then exactly four H2s in this order: `Sub-features`, `How to get to it (user POV)`, `Driving it with <harness>`, `Gotchas`.
- Each sub-feature has a short ID, for example `search-empty`.
- List every entry point a user has, not only the convenient one.

If the seed data lacks a precondition a drive step needs, the step fails and the reason goes in `Gotchas`. Never weaken the step to make it pass.

## 5. Prove it once

Run your own instructions end to end: Launch, Doctor, drive ONE feature, capture evidence, Cleanup. With a driver, also start a second worktree's instance next to the first and check that `doctor` tells them apart. After cleanup, check the evidence still exists. Fix what fails, and run Cleanup after every failed attempt so no processes or ports stay behind. A verify.md that was never run is a draft.

Then drive each other seeded feature once, one entry point each, so every entry point in the map has run at least once.

If you proved it in a stand-in (a container instead of a fresh machine, a local stack instead of a remote one), list every step the stand-in did that the real target will not. Those steps stay unverified.

## 6. Hand off

Report the files you wrote, the features you seeded, what you proved and what stays unverified. Mention `/verify audit` for keeping the map honest when the app changes.
