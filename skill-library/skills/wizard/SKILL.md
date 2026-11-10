---
name: wizard
description: Write an interactive bash script that walks a person through steps only they can do, such as dashboards, credentials, CI secrets or consoles the agent cannot reach. Use when the next step needs a person to click, log in or copy a value.
---

<!-- Based on mattpocock/skills: skills/engineering/wizard (MIT) -->

# Wizard

A wizard is a bash script that walks a person through a manual procedure, one stage at a time. It opens each URL, says what to click and copy, captures each value, writes it where it belongs (`.env`, GitHub secrets), confirms each stage and shows how many stages are left.

Use it when the agent cannot do the step itself: a third-party dashboard, a login, a console with no CLI or API access, a secret the agent may not see, a one-off cutover. Do every step the agent can do itself with a CLI or an API. A wizard step is only for what is left.

[references/template.sh](references/template.sh) holds the wizard library: stage progress, confirm gates, URL opening on every OS, hidden secret entry, `.env` upserts that can run twice, `gh secret` and `gh variable` writes, and a closing summary. Your job is to scope the procedure and write its stages. Never edit the library above the `STAGES` marker.

A wizard is for one run by default. Save it under `scripts/` or a scratch path and delete it when the job is done. Commit it only when the dev wants a setup path that others will run again.

## 1. Scope the procedure

Read the repo before you ask anything:

- For setup: `.env`, `.env.example`, `.env.*`, `README`, `docker-compose*`, the framework config and `.github/workflows/*`. Every `secrets.*` and `vars.*` reference is a value the wizard must produce.
- For a migration or cutover: the current state, the target state and the irreversible actions between them.

Show the dev the ordered list of stages and the values each one produces. The dev can add, drop or reorder stages.

**Done when** every stage has a name and an order, and for each value you know where the person gets it, where it is written (`.env`, a GitHub secret, both or nowhere) and whether it is secret.

## 2. Map each stage

For each stage, write the exact path a person follows: the URL, what to click, where the value shows, which variable it fills. Example: "Dashboard, Developers, API keys, Reveal test key, copy". If you do not know the current UI or the exact command, check the docs or ask the dev. Never invent a step.

**Done when** a stranger could follow every stage.

## 3. Write the wizard

Copy `references/template.sh` to the target path. Replace the example stage with one `stage` per step, in dependency order. Use the helpers: `stage`, `say`, `step`, `open_url`, `ask`, `ask_secret`, `write_env`, `set_secret`, `set_var`, `pause`, `confirm`. Set `TOTAL_STAGES` to the number of stages.

- Open the URL before you ask for its value.
- Use `ask_secret` for every secret.
- Use `write_env` for every value that must persist.
- Use `set_secret` only for values CI needs.
- Use `confirm` before every irreversible action.
- Keep one task per stage. Each stage clears the screen.

## 4. Check it and hand it over

- Run `bash -n <script>`, and `shellcheck <script>` if it is installed.
- Run `chmod +x <script>`.
- Do not run it yourself. It opens browsers and waits for a person. Trace it instead: every value from step 1 is captured and lands where step 1 says, and every `set_secret` name matches a `secrets.*` reference in CI.
- Tell the dev the command to run. If the wizard stays in the repo, link it from the README.

**Done when** `bash -n` passes and the trace finds no missing or misnamed value.
