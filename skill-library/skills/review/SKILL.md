---
name: review
description: Review a PR, branch or diff and give a ship decision with verified, paste-ready comments. Two reviewer subagents check standards and hunt bugs in parallel, and you check the change against its ticket. Use when the user asks to review a PR, a branch or a diff.
---
<!-- Based on Prostrive pr-checker, mattpocock/skills: skills/engineering/code-review, backnotprop/pstack: skills/interrogate (MIT) -->

# Review

Review one change on two axes: does it hold up as code, and does it do what the ticket asked. Read and verify only. Never edit files. Never post to GitHub unless the user asks.

The goal is a ship decision, not a list of comments. A change with nothing wrong gets `Approve` and no comments. That is a good result.

## 1. Set up

1. Find the scope. A PR number: `gh pr view <n> --json title,body,headRefName,baseRefName,files,commits`. A branch or a fixed point the user names: diff it against that point. Nothing named: the current branch against its base branch.
2. `git fetch` the head and base refs. Diff against the PR's own base, not the default branch. A stacked PR targets another feature branch: `git diff origin/<base>...origin/<head>`. If the head branch is gone, for example after a merge, fetch `pull/<n>/head` and diff from the merge base with the base branch at the PR's first commit.
3. Check that the diff is not empty and the refs resolve. Fail here, not inside the subagents.
4. Check the PR head out as a detached worktree: `git worktree add --detach <tmp>/review-<n> origin/<head>`. Read new files in full from there, not from diff hunks. You need real line numbers. Remove the worktree when you are done. If you cannot create a worktree, for example in plan mode, read each file with `git show <head-sha>:<path>`.
5. Get the ticket. `docs/agents/tracker.md` says where tickets live. The branch name or PR body usually holds the ticket ID. Read its scope and acceptance criteria. Read the sibling tickets it links to. They often state behavior the ticket leaves implicit.
6. Read `docs/agents/review.md` if it exists. It lists the paths a person reads themselves, and it can add project checks or a third reviewer, for example a parity check against a legacy system. Follow it. The format is in [references/review-md.md](references/review-md.md).
7. If the project numbers migrations or other ordered files, check the numbers against the default branch, whatever the base. A stacked PR collides there.
8. Find the round. Look in the PR comments and the conversation for an earlier review of this change and the head commit it reviewed. No earlier review: round 1. Otherwise count up, and follow "Rounds" below.

## Rounds

- **Round 1** reads the whole change.
- **Round 2 and 3** read only the commits since the head commit of the last review: `git diff <last-reviewed-head>..origin/<head>`. Check that each earlier finding is fixed. Report a new finding only if the new commits caused it, or if it is blocking.
- **After round 3**, do not start another round. Say that the same kind of problem keeps coming back, name it, and tell the author to rethink the approach with the dev who owns the ticket.

## 2. Start the reviewers

Start both at once, each by its agent type: `skill-library:review-standards` and `skill-library:review-adversarial`. Their definitions pin model and effort, so do not pass a model override. Start each with a fresh context and brief it cold. Give each a word limit and tell it that no findings is a valid result. On a change that spans two stacks or more than about 30 files, start two `review-standards` agents split by stack.

**`review-standards`.** Give it the diff command, the worktree path, the conventions docs (`AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `docs/decision-records/`) and the nearest sibling code (the thing the PR copies). Tell it the sibling is the real yardstick. Tell it to skip any "don't fix these" gotchas and anything lint enforces. Ask for hard violations only, plus every new or changed test that would still pass if its behavior broke.

**`review-adversarial`.** Give it the diff command, the worktree path and a numbered list of the change's write paths and state transitions. Build that list yourself from the diff. Ask for BUG / OK / COULD NOT CONFIRM per item. Each BUG needs a concrete failing sequence. Ask it to prove a BUG with a run (a failing test or a short script against the real code) when that is cheap.

## 3. Check the spec yourself

While the reviewers run, walk the ticket's acceptance criteria one by one against the diff:
- criteria that are missing or partial
- behavior in the diff that nobody asked for
- criteria that look implemented but behave wrong

Quote the ticket line for each finding. If there is no ticket, say "no spec" in the output and skip this axis.

## 4. Verify before you write

Do not pass a finding straight through. Open the file and confirm each claim yourself. Reviewers overstate severity and sometimes invent a line number. Drop anything that does not survive.

- A BUG stays only if you can follow its failing sequence line by line in the PR head.
- A standards item stays only if it cites a written rule or a sibling line. "This could be cleaner" is not a finding.
- A divergence that the PR explains away still needs a check. Written down is not the same as agreed. A divergence with no recorded decision (ticket, ADR, spec) that changes money, permissions, deadlines, lockout or what a customer sees is `blocking, needs a decision`.
- If something is missing, check the tracker before you call it a gap. Name the ticket that covers it, or say no ticket covers it.
- Check if each problem already exists on the base branch (`git show origin/<base>:<path>`, `git blame`). If it does, tag it `pre-existing`. A pre-existing problem never blocks this PR.
- Name the whole class of a problem, not one line. Search the diff for every other place with the same problem and list them in the same comment, so the author fixes all of them in one round.

Before you write, list every file in the diff and name who read it. Read any file nobody read.

## 5. Write the comments

- Plain English. Active voice. One idea per sentence. No hedging. Say the problem, then the evidence, then what to do.
- Only comment on files in the PR.
- Every comment carries `path:line`, and the line is right.
- A comment that says "same as the sibling" must hold for this case. Check the comparison before you lean on it.

## Output

First line: `Approve`, `Approve after fixes` or `Block`, and the one reason.

Second line: `Round <n> of 3, reviewed up to <short head sha>`.

Then `Read yourself:` and the files in this diff that match the paths in `docs/agents/review.md`, each with the reason from that file. With no `review.md`, use these defaults: CI and deploy config, database migrations, auth and permission checks, and code that moves money. If no file matches, write `Read yourself: nothing beyond the evidence in the PR body`.

Then the comments grouped by file, files in path order, lines ascending. Tag each comment `blocking`, `worth fixing` or `pre-existing` inline. No nits.

Then "Needs a decision": each divergence with no recorded decision, ordered by user impact, with the current behavior as the fallback and your recommendation.

Then the tracker mapping: what is out of scope and already ticketed, and what is a gap with no ticket.

Leave out any section that is empty. No preamble. No closing summary.

## When a bug gets past review

When a bug that review missed shows up in QA or later, run `correct` on it. It turns the miss into a test or a lint rule, so the next review cannot miss it again.
