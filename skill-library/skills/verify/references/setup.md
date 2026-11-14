# /verify setup

Write `docs/agents/verify.md` and seed `features/` for a repo that has neither. You write for the next agent. It reads these files cold, in the middle of a task, and has never seen the app.

## 1. Read the repo, not the dev

Answer these from the code. Ask the dev only what you cannot observe, following the asking rules in the `grill` skill (`references/asking.md`).

- **Surface:** what does a user touch? Web UI, CLI or TUI, desktop app, API, mobile app, library. Pick the main one and note the others.
- **Run:** how does the app start locally? Use the repo's own commands (package scripts, Makefile, README). When the dev stack uses fixed ports that other runs share and the repo also has a test or e2e stack that starts its own copy, prefer the test stack. Note ports, env vars, seed data and sign-in.
- **Drive:** how can an agent drive it? Use an existing harness first: a sign-in script, PTY helpers, curl-able endpoints. For a web UI or Electron, use Playwright CLI (`playwright-cli`, npm package `@playwright/cli`). For CLI and TUI, use tmux or a PTY. For a service, use plain HTTP.
- **Observe:** what evidence can you capture? Screenshots, ARIA snapshots, traces, console and network errors, terminal transcripts, response bodies, logs, exit codes, database rows.
- **Isolate:** can two instances run side by side (ports, data dirs, browser sessions)? Which services are shared and cannot run twice, for example an auth server or a database? Write both in verify.md.
- **Live keys:** which env vars connect the app to real outside services: payments, email, SMS, webhooks, AI APIs, invoicing? List them. Section 3 blanks them.
- **Remote environments:** does the project have a staging or preview environment? Find its URLs in the deploy config, env templates or docs. Ask the dev what an agent may write there.

If the checkout does not build or start, fix that first or report it exactly. A verify.md written against a broken base teaches wrong steps.

## 2. Write docs/agents/verify.md

Five sections, each with real commands from this repo. No placeholders.

- **Launch:** the exact command that starts the app, and how to tell it is ready (a log line, a URL that answers with real content). Launch reaches a usable state from an empty data dir, with migrations and seed data. Include sign-in for each test role (see Sign-in below). List the test accounts. Add a Staging part when the project has one (see Staging below).
- **Doctor:** one read-only check that answers "is this instance worth driving?": process up, right build, port owned by this run, sign-in valid.
- **Drive:** the harness recipe with real selectors and commands. Prefer stable handles: ARIA names, data attributes, routes, prompt strings. No screen coordinates. For a web UI, check console errors and failed network requests after each flow.
- **Evidence:** what to capture and where it goes (a gitignored folder). The proof rules: the real user path, the action and the resulting state, side effects checked, mocks only at a production boundary. When a dry-run mode is the safe path, check what it really skips by observing, not by its name.
- **Cleanup:** how to stop what the run started. Kill what you started, never by process name. Cleanup removes instances, browser sessions, saved sign-ins and scratch state, never the evidence.

A helper script that verify.md uses is executable, lives in the repo, and verify.md shows how to call it.

### Browser

- Install Playwright CLI once per machine: `npm install -g @playwright/cli@latest`. Run `playwright-cli --help` before you write steps. Never write command names from memory.
- Give each worktree its own named session: `playwright-cli -s=<name derived from the worktree path> <command>`, or set `PLAYWRIGHT_CLI_SESSION`. Two worktrees never share a session.
- Use an in-memory session. Never attach to the dev's own Chrome or Chrome profile, and never use an extension or attach mode.
- Snapshots for actions, screenshots for proof. `tracing-start` and `tracing-stop` give a trace for a multi-step flow.

### Sign-in

- Sign in through the real login page once per role, then save the session: `playwright-cli state-save .verify/auth/<role>.json`. Drive steps load it with `state-load`.
- Never sign in with a test-only endpoint or a direct database write.
- Saved sessions hold live tokens. Keep them in a gitignored folder. Cleanup deletes them.
- Use test accounts only. Never use the dev's own account.

### Staging

Add this part only when the project has a staging or preview environment. It lets a person without a local stack, for example a PM, run `/verify sweep staging`.

- List the URL of each app and a read-only Doctor for it, for example the health URL and each login page answering 200.
- Write the write policy in plain words. The default is read-only: no orders, bookings, sign-ups, messages or payments. A step that writes stays not checked on staging.
- Writes are allowed only when the project has dedicated staging test accounts and the dev wrote down which test data is allowed. List those accounts and that data here, never their passwords. Passwords come from the env.
- Use a session name of its own for staging, never the local one.
- Never run reset, seed or cleanup commands against staging.

## 3. Write a driver when the app needs one

Write a driver when any of these is true: the app needs more than 3 commands to start, it has several services, it shares a service with other runs, or more than one agent may verify at the same time. Otherwise skip this step.

When the repo already has a script that starts an isolated stack, for example for its e2e tests, wrap that script and add only what is missing. Write a new one only when nothing fits.

The driver is one script in the repo, for example `scripts/verify/<app>`, in the repo's own language. It has a fixed set of commands and `--help` lists them:

- `start`: starts this worktree's instance and waits until it is usable.
- `doctor`: read-only. Reports who owns the port (process and folder), whether that instance belongs to this worktree, the commit it runs, and the health of each shared service.
- `stop`: removes everything this worktree started: processes by their saved ID, containers, networks and volumes by this worktree's project name, browser sessions, and saved sign-ins. `start` writes those into a ledger file, and `stop` works from that file. Running `stop` twice is safe. Never stop by process name or port alone.
- `info`: prints the URL, ports, data folder and browser session of this worktree's instance.
- `reset`: returns this instance to the baseline seed, so a state that shows only once (an empty list before the first item) can be driven again.
- `sign-in <role>`: covers every role that has its own surface, for example customer, admin and operator. A role the driver cannot sign in leaves its features out of the map.
- `browser <args>`: runs `playwright-cli` with this worktree's session name added.
- Other drive helpers the feature map needs, for example `seed <name>` or `cli -- <command>`.

Rules:

- Give each worktree its own instance. Derive the data folder, browser session and container project name from the worktree path. For ports, derive them too, or keep a runner that picks free ports itself and record the chosen ports for `info`.
- Check the container runtime's shared resources as well: networks, address pools, volumes and name prefixes. Give each worktree its own network, and have `doctor` report when the runtime runs out of them.
- Refuse to drive an instance this worktree did not start, unless the dev passes it on purpose.
- `start` refuses to run when the ledger lists processes or containers that still run. Run `stop` first. A second `start` must never overwrite a live ledger.
- Never restart or reset a shared service. `doctor` reports a broken shared service, and the run stops there.
- Start the app with every live key from section 1 set to empty, or to a test key the project provides for that purpose. Never copy a live key from the dev's env file. Turn off the matching feature flags when the app has them. verify.md lists the blanked keys.
- A flow that needs a blanked key is not checked. It goes in the feature's `Gotchas` with the key it needs. Never fake the outside service to make the flow pass.

verify.md documents the commands, not the script's code. The feature files call the driver, not loose commands.

## 4. Seed the feature map

Create `features/README.md` and one file per user-facing feature. Start with the top 3 to 5, from routes, commands, menus or docs. Copy the shape of `feature-map-example/`:

- The README holds the baseline state, the driving rules, the proof rules, the index and the sweep order: the order in which `/verify sweep` walks the features.
- `features/journeys.md` holds the flows that cross several features, for example sign up, then create, then share. A sweep ends with it.
- Each feature file has an H1, one paragraph on what the user sees, then exactly four H2s in this order: `Sub-features`, `How to get to it (user POV)`, `Driving it with <harness>`, `Gotchas`.
- Each sub-feature has a short ID, for example `search-empty`.
- List every entry point a user has, not only the convenient one.
- Start each drive step that changes stored data with `(writes)`. A staging sweep skips the marked steps unless the staging write policy allows them.

If the seed data lacks a precondition a drive step needs, the step fails and the reason goes in `Gotchas`. Never weaken the step to make it pass.

## 5. Prove it once

Run your own instructions end to end: Launch, Doctor, drive ONE feature, capture evidence, Cleanup. With a driver, also start a second worktree's instance next to the first and check that `doctor` tells them apart. After cleanup, check the evidence still exists. Fix what fails, and run Cleanup after every failed attempt so no processes, ports or browser sessions stay behind. A verify.md that was never run is a draft.

Then drive each other seeded feature once, one entry point each, so every entry point in the map has run at least once. With a Staging part, run its Doctor and one read-only drive.

If you proved it in a stand-in (a container instead of a fresh machine, a local stack instead of a remote one), list every step the stand-in did that the real target will not. Those steps stay unverified.

## 6. Check git sees the files

- Run `git check-ignore -v docs/agents/verify.md features/README.md <driver path>`. Each file must print nothing. A repo that ignores `docs/` or `scripts/` hides the setup from every other worktree.
- When a file is ignored, add a narrow exception to `.gitignore`. Do not remove the repo's own ignore rule.
- Run `git check-ignore -q` on the evidence folder, the saved sign-ins and the browser output folder (`.playwright-cli/`). Each must be ignored. Add them to `.gitignore` when they are not.
- Run `git status` and check that no env file, saved sign-in or evidence file shows as new.

## 7. Hand off

Report the files you wrote, the features you seeded, what you proved and what stays unverified. List the blanked keys and the flows they leave not checked. Mention `/verify audit` for keeping the map honest when the app changes.
