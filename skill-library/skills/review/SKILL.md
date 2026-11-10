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
2. `git fetch` the head and base refs. Diff against the PR's own base, not the default branch. A stacked PR targets another feature branch: `git diff origin/<base>...origin/<head>`.
3. Check that the diff is not empty and the refs resolve. Fail here, not inside the subagents.
4. Check the PR head out as a detached worktree: `git worktree add --detach <tmp>/review-<n> origin/<head>`. Read new files in full from there, not from diff hunks. You need real line numbers. Remove the worktree when you are done.
5. Get the ticket. `docs/agents/tracker.md` says where tickets live. The branch name or PR body usually holds the ticket ID. Read its scope and acceptance criteria. Read the sibling tickets it links to. They often state behavior the ticket leaves implicit.
6. Read `docs/agents/review.md` if it exists. It adds project checks or a third reviewer, for example a parity check against a legacy system. Follow it.
7. If the project numbers migrations or other ordered files, check the numbers against the default branch, whatever the base. A stacked PR collides there.

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

Before you write, list every file in the diff and name who read it. Read any file nobody read.

## 5. Write the comments

- Plain English. Active voice. One idea per sentence. No hedging. Say the problem, then the evidence, then what to do.
- Only comment on files in the PR.
- Every comment carries `path:line`, and the line is right.
- A comment that says "same as the sibling" must hold for this case. Check the comparison before you lean on it.

## Output

First line: `Approve`, `Approve after fixes` or `Block`, and the one reason.

Then the comments grouped by file, files in path order, lines ascending. Tag each comment `blocking` or `worth fixing` inline. No nits.

Then "Needs a decision": each divergence with no recorded decision, ordered by user impact, with the current behavior as the fallback and your recommendation.

Then the tracker mapping: what is out of scope and already ticketed, and what is a gap with no ticket.

Leave out any section that is empty. No preamble. No closing summary.
