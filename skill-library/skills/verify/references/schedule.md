# /verify schedule

Set up scheduled runs of `/verify audit` and `/verify sweep staging` on one always-on machine, for example a team Mac mini. A laptop is the wrong place: the runs stop when it sleeps.

## 1. Check the machine

Run these on the machine. Stop and report what is missing.

- `claude --version` works, and Claude Code is signed in as a team account, not a person's account.
- `gh auth status` works, with a token that may comment on PRs and open PRs in the project repo.
- The container runtime and `playwright-cli` work, if verify.md needs them.
- The project's test env file is on the machine, in the path verify.md names. Never copy a dev's own env file.
- The machine does not sleep: `pmset -g | grep -E '^ *sleep'` prints `0` on macOS.

## 2. Write the Schedule part of verify.md

Add a `## Schedule` section to `docs/agents/verify.md`:

- Which runs, and when. Default: `/verify audit` every Monday at 06:00, `/verify sweep staging` every weekday at 07:00 when verify.md has a Staging part.
- The machine name, from `hostname -s`.
- Where the report goes. Use a channel the project already has: a Slack webhook in an env var, or a ticket in the tracker from `docs/agents/tracker.md`. Name the env var, never its value.
- Who reads it, for example the PM who owns QA.

## 3. Write the runner

Write `scripts/verify/scheduled-run` in the project repo. It takes one argument, `audit` or `sweep-staging`, and does this:

1. Takes a lock file, so two runs never overlap. If the lock is held, it exits and logs why.
2. Runs `git fetch origin` in a clone that only the runner uses. Never the dev's checkout.
3. Makes a new worktree at `origin/<default branch>`.
4. Runs Claude Code headless in that worktree: `claude -p "/verify audit"` or `claude -p "/verify sweep staging"`. Allow only the tools the run needs with `--allowedTools`: the driver, `playwright-cli`, `git`, `gh`. Never use `--dangerously-skip-permissions`.
5. Saves the final report to `.verify/scheduled/<date>-<mode>.md`.
6. Sends the report where the Schedule part says.
7. Removes the worktree and releases the lock, also when a step fails.

## 4. Install the schedule

On macOS, write a launchd agent in `~/Library/LaunchAgents/` with one `StartCalendarInterval` per run. It calls the runner with the right argument and logs stdout and stderr to `.verify/scheduled/`. Load it with `launchctl bootstrap gui/$(id -u) <plist>`. On Linux, use a cron line or a systemd timer.

The launchd agent lives on the machine, not in the repo. verify.md says where it is and how to remove it.

## 5. Prove it once

Run the runner by hand for each mode. Check that the report arrived where the Schedule part says, that the worktree is gone, and that no container, process or browser session is left. Then run `launchctl kickstart gui/$(id -u)/<label>` once and check the same things.

## Rules

- A scheduled audit opens its PR like any audit. It never merges.
- A scheduled sweep only reads on staging, unless the staging write policy allows more.
- A run that fails still sends a report that says it failed, and why.
