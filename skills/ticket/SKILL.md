---
name: ticket
description: Open one ticket before any code is written. Asks every question this ticket needs, then adds a written check to the ticket for how we will know it works. Use as "/ticket" for the next ticket in line, "/ticket 05" to pick one, or when the user says "start the next ticket".
---

# Ticket

No code is written until this is done. One ticket is one small change.

## Steps

1. **Find the ticket.** Read `docs/agents/issue-tracker.md` if it exists. With
   no number given, take the lowest-numbered ticket that is not done and not
   blocked, and say which one you picked and why. With a number, open that
   one. If its blockers are not finished, stop and say which. Work on the
   existing ticket file; only write a new ticket when none exists for the work.
2. **Read around it.** The repo's `CLAUDE.md`, the glossary, any decision
   records for this area, and the code the ticket will touch.
3. **Ask until nothing is unclear.** One question at a time, each with your
   recommended answer first. Follow up on any answer that opens a new
   question. There is no limit on the number of questions. The only limit is
   scope: every question must be about this ticket. A question about a later
   ticket is written into that ticket as a note, not asked now. If an answer
   changes a term or a hard-to-reverse decision, update the glossary or add a
   decision record.
4. **Update the ticket in place.** Record the answers under `## Decisions`,
   then add the check under a heading `## How we will know it works`:
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
