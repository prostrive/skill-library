---
name: setup-pre-commit
description: Add a pre-commit hook that formats staged files and runs the type check and tests. Uses the hook tool and package manager the repo already has.
disable-model-invocation: true
---

<!-- Based on mattpocock/skills: skills/misc/setup-pre-commit (MIT) -->

# Set up pre-commit checks

Add a pre-commit hook that formats the staged files, then runs the type check and the tests. Reuse what the repo already has. Add a new tool only when nothing fits.

## 1. Detect

- **Package manager**: `pnpm-lock.yaml` is pnpm, `yarn.lock` is yarn, `bun.lockb` or `bun.lock` is bun, `package-lock.json` is npm. Read `packageManager` in `package.json` if it is set. Default to npm.
- **Hook tool**: `lefthook.yml` or `lefthook.yaml` is lefthook. A `.husky/` folder is husky. A `pre-commit` entry in `package.json` (`simple-git-hooks`) or `.pre-commit-config.yaml` counts too. Use the tool you find.
- **Formatter**: a Prettier config, a Biome config (`biome.json`), or a `format` script. Use the one you find.
- **Scripts**: the `typecheck` (or `check`, `tsc`) and `test` scripts in `package.json`. In a monorepo, read the root scripts and the task runner (Turborepo, Nx).
- **Existing hook**: if a pre-commit hook exists, extend it. Do not replace it.

**Done when** you know the package manager, the hook tool, the formatter and which checks the repo can run.

## 2. Install what is missing

Only when the repo has no hook tool: install husky and lint-staged as dev dependencies with the detected package manager, then run `<pm> exec husky init`. That adds the `prepare` script and `.husky/`.

Only when the repo has no formatter: install Prettier and add a `.prettierrc` with the defaults below. Tell the dev you added it.

```json
{ "singleQuote": false, "semi": true, "trailingComma": "es5", "printWidth": 80 }
```

## 3. Write the hook

The hook runs, in this order:

1. The formatter on staged files only. With lint-staged: a `.lintstagedrc` of `{ "*": "prettier --ignore-unknown --write" }`, or the Biome equivalent `biome check --write --staged`.
2. The type check, if the repo has a script for it.
3. The tests, if the repo has a script for it and they finish in under about a minute. If they take longer, leave them out and say so. A slow hook gets skipped with `--no-verify`.

Examples, with `<pm>` as the detected package manager:

- husky, `.husky/pre-commit`:
  ```
  <pm> exec lint-staged
  <pm> run typecheck
  <pm> run test
  ```
- lefthook, `lefthook.yml`:
  ```yaml
  pre-commit:
    commands:
      format:
        glob: "*"
        run: <pm> exec prettier --ignore-unknown --write {staged_files}
        stage_fixed: true
      typecheck:
        run: <pm> run typecheck
      test:
        run: <pm> run test
  ```

Leave out a line for a script the repo does not have, and tell the dev.

## 4. Check it

- The hook file exists. For husky, it is executable.
- Run the formatter step once by hand (`<pm> exec lint-staged`, or `lefthook run pre-commit`). It must exit 0.
- Make one commit with the changed config files. Do not use `--no-verify`. The commit runs the new hook.

**Done when** the commit passed through the new hook.

Report the tool you used, the checks the hook runs, and the checks you left out with the reason.
