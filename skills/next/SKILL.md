---
name: next
description: Tells the user the one next step and the exact thing to type. Use when the user asks "what's next", "where am I", "what do I do now", starts a new session on existing work, or seems unsure how to continue.
---

# Next

The user is not an engineer and does not know the order of work. Look at
the repo and name the **one** next step. Never a menu.

## Look first

Find out from the repo; do not ask the user what state things are in. A
status written in a file is a claim; check it against what is really there.

1. `git status --short`, `git branch --show-current`, `git log --oneline -5`
2. `.agent-notes/handoff.md`, if it exists.
3. The tickets. `docs/agents/issue-tracker.md` says where they live; with no
   such file, look in `docs/tickets/`. Read each ticket's `Progress:` line
   (ready, claimed, built, explained, done) and its blockers. A ticket with
   no `Progress:` line is ready. If its code is already on disk, it was
   built before these skills were in use: the next step is `/ticket` for
   that ticket, to write its check; `/build` then starts from proving the
   tests.
4. The test suite, using the repo's own command (the repo's `CLAUDE.md`,
   then its build or CI file).
5. If the repo uses pull requests: whether one is open, whether its checks
   pass, and whether the reviewer has approved it.

## Decide

Take the first row that is true.

| What you find | The next step |
|---|---|
| Something in the data looks real, or a secret is in the changed files | Stop. Tell the user what and where. Nothing else until it is dealt with. |
| A handoff note exists | Follow "Pick up" in the `handoff` skill, then continue from the step the note names. |
| The repo has no rules file (`CLAUDE.md` or `AGENTS.md`) | `/briefing` |
| A ticket's `Progress:` claims more than the repo shows (marked built or explained, but tests are red, or the code does not do what the ticket says) | Treat it as claimed: `/build`. If the ticket and the code disagree about what was wanted, give a decision card first. |
| A ticket is claimed, `Stakes: high`, with no `## Design` section | `/design` |
| A ticket is claimed and not yet built (tests may be red; that is normal mid-build) | `/build` |
| Tests fail and no ticket is in progress | `/bugfix` |
| A ticket is built, `Stakes: high`, and `.agent-notes/NN-security.txt` is missing or says `open` | `/security` |
| A ticket is built, not explained | `/explain` |
| A ticket is explained, and its changes are not yet committed | `/pr` |
| A pull request has failing checks or new comments | `/pr` |
| A pull request is approved and not merged | Give the user the merge command the repo's rules allow. |
| Changed files that belong to no ticket | They are their own small change. Say which files, and use `/pr`. |
| No proof recipe yet, and something can be run | `/proof` |
| Three tickets done since the last checkpoint in `.agent-notes/checkpoints.md` | Checkpoint: run all tests and the real run end to end, show the user, add a dated line to that file. |
| A ticket is ready and not blocked | `/ticket` |
| There are tickets, and every remaining one waits on a person or on a review | Say who is being waited on, and give the user the message to send. |
| No tickets at all | `/kickoff` |
| All tickets in this slice are done | In order, the first not yet done since the last ticket: `/proof` to refresh the recipe; `/lessons`; `/release` if nothing yet runs the checks automatically on each change; then tell the user to show the reviewer, and `/kickoff` for the next slice. |

A pull request that is only waiting for review needs nothing from the
user; carry on down the table.

If the user arrives with a new request instead of asking where they are,
size it first (standards section 10): tiny goes to `/quick`, a bug to
`/bugfix`, something slow to `/speed`, new work to `/ticket` or `/kickoff`.
A request to see the whole plan or its progress goes to `/visualize`.

## Sessions

Say this when it applies:

- **Between tickets** (after `/pr`, before the next `/ticket`): start a new
  session. A fresh one makes fewer mistakes.
- **In the middle of a ticket** and the session is long: `/handoff` first,
  then a new session.

## Finish: answer in this shape

```
Where you are: <one sentence, with the ticket title>
Next step: <one action in plain words>
Type this: <the exact command or slash command>
Why: <one sentence>
```

If the user must decide something first, give a decision card instead: the
call, your pick, what it changes, the evidence, the risk.
