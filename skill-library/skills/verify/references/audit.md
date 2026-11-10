# /verify audit

Check that `docs/agents/verify.md` and the feature map in `features/` still match the app. Cover every feature file from the source and drive every feature live. You do not need to run every single bullet.

## Outcomes

End with exactly one, and say which:

- **clean:** every feature got source and live coverage. Nothing to fix. No branch, no PR.
- **changed:** one PR with proven fixes to verify.md, `features/` or the harness scripts verify.md owns.
- **blocked:** coverage could not finish, or a proven fix could not ship safely. Say exactly what blocked it.

## Edit scope

Edit only `docs/agents/verify.md`, `features/` and the helper scripts verify.md uses. Never edit product code in an audit. When the map describes behavior the app no longer has, decide which it is:

- **Doc drift:** the map is wrong. Fix the map.
- **Harness gap:** the app works but the harness cannot drive it. Fix the harness.
- **Product regression:** the app is broken. Report it to the dev. Keep it out of the PR.

## Pass

1. **Find the target.** If `docs/agents/verify.md` or `features/` is missing, stop and point at `/verify setup`.
2. **Index check.** Read `features/README.md` and list the files next to it. Fix missing, extra, duplicate or dead index entries.
3. **Source wave.** Start one read-only subagent per feature file, all at once, each with a fresh context. Each one explains how the feature works from the source, flags likely drift with `path:line` citations, and returns one live recipe. Subagents never drive the app and never edit files. Return shape: summary, source entry points, likely drift or none, one recipe.
4. **Reconcile.** Every feature file needs a returned summary. Merge recipes that share an app state. Spot-check the cited drift. Look at recent commits for user-facing surfaces the map does not list, and name a concrete source path before you call one missing.
5. **Live pass.** Required even when the source looks clean. You drive, not the subagents. Follow the Launch model in verify.md: one long-lived instance driven in order for servers and UIs, or a fresh isolated session per drive for short-lived CLIs. Drive every feature at least once. Hold three rules for the whole pass:
   - Run Doctor before the first drive, on each fresh session, and after any failed drive. When Doctor cannot see the problem (a stuck UI on a healthy process), reset to a known state or relaunch.
   - Evidence captured so far survives every cleanup. Check it at its location.
   - Nothing a drive started outlives its use. Clean up after failed attempts too. On a shared instance, clean up what you left, not the instance.

   A Doctor failure caused by drift is drift: fix it, restart only what the fix invalidated, and retry once before you call the pass blocked. A feature you cannot reach is `verified-unreachable` only with the exact prerequisite (sign-in, entitlement, OS, external state) and the route you tried. If the map does not mention that prerequisite, that is drift too. Drive every harness fix live again before it ships.
6. **Ship or stop.** For `changed`, open one PR with proven fixes. Read every changed file again first. For `clean` or `blocked`, open no PR and report the outcome and the coverage.

Keep short run notes (features covered, unreachable prerequisites, confirmed drift, outcome) in a scratch folder. Do not commit them.
