---
name: ticket
description: Open one ticket before any code is written. Asks only the questions this ticket needs and ends with a written check for how we will know it works. Use as "/ticket 02" or when the user says "start the next ticket".
---

# Ticket

No code is written until this is done. One ticket is one small change.

## Steps

1. **Find the ticket.** Read `docs/agents/issue-tracker.md` if it exists. Open
   the ticket the user named, or the lowest-numbered unblocked one. If its
   blockers are not finished, stop and say which.
2. **Read around it.** The repo's `CLAUDE.md`, the glossary, any decision
   records for this area, and the code the ticket will touch.
3. **Ask only what blocks this ticket.** At most three questions, one at a
   time, each with your recommended answer first. If nothing blocks, ask
   nothing. Questions about later tickets wait for those tickets.
4. **Write the check into the ticket** under a heading `## How we will know it works`:
   - the test cases, each as input and expected output, in plain words;
   - the one real command that will be run as proof, and what its output
     should show;
   - what is deliberately not in this ticket.
5. **Guess the size.** If it looks like more than about 150 changed lines,
   propose a split before starting.
6. **Mark the ticket as claimed** in the way the tracker file describes.

## Branch

If the repo works through pull requests, give the user the command to start a
branch, for example `git switch -c feat/02-routine-adjustments`. Follow the
repo's naming if it has one. Do not create the branch yourself unless the repo's
rules say you may.

## Finish

End with:

```
Ticket NN is ready: <one sentence of what will be built>
Next step: build it.
Type this: /build
```
