---
name: catch-up
description: Tell the dev what comes next and every decision that waits on them, with enough context to decide from the reply alone.
disable-model-invocation: true
---

<!-- Based on backnotprop/pstack: skills/ketchup (MIT) -->

# Catch-up

The dev lost track of this session, or comes back to the work after a break. Tell them what happens next and what waits on them. Spend the words on what is ahead, not on what is done.

## Gather

Keep this turn read-only. Do not change code, start jobs or post anything.

1. Find the last message the dev wrote before `/catch-up`. Notifications and subagent reports are not their messages. Assume they remember that message and nothing after it.
2. If `.claude/handoffs/` has a note from the last few days about this work, read the newest one.
3. Check the live state of each PR, CI run, ticket and subagent this work touched, with `git`, `gh` and the tracker. Live state wins over the handoff note and over your memory.
4. Check every number you will give against its source.

A decision item is something only the dev can do: a product choice, an approval, a merge, an action that cannot be undone, or access you do not have. Work you can do yourself is not a decision item. Do not make up decisions to fill the reply.

## Write the reply

Use plain words and short sentences. Say what changes for the user of the product, not how you did it. Leave out hashes, paths and commands unless the dev needs one to act. Call each PR, branch or agent by a name the dev knows.

1. **One opening line:** what waits on the dev, or "nothing waits on you".
2. **Done:** one line in total about what is finished since their last message. No list.
3. **Next:** what comes next, in order. For each step, say who does it: you or the dev. Name any work you can still do yourself.
4. **Decisions:** one bullet per decision. Each bullet has:
   - the decision, in the words the dev would use
   - your pick
   - what it changes for users
   - the evidence behind your pick
   - the risk, also when it is low ("Low risk: only the label text changes")
   - the link or number of the PR, ticket or agent it is about

   For a choice between options, give each option with what it gets and what it costs. When several items share one decision, for example 4 PRs to merge, write the decision and your pick once, then one line per item, riskiest first.

Give each decision about 30 words. Never drop a decision or replace it with a count or a link to stay short. The reply alone is enough to decide.

Say what waiting costs only when it is more than a delay, for example a deadline or lost data.
