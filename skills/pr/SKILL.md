---
name: pr
description: Package a finished change for review. Checks the size and the standards, writes the commit message and the pull request description with the proof in it, and gives the user the exact commands. Never commits or pushes. Use after /explain, or when the user says "commit this" or "open a PR".
---

# PR

The goal is a change a reviewer can accept on the first read. You prepare
everything; **the user runs every git command.** Never commit, push, merge or
open a pull request yourself, even if asked in passing. Give the command.

## 1. Gate

Check each one. If any fails, stop and say which, with the fix.

- The whole test suite passes right now. Run it.
- The linter and formatter pass on the changed files.
- The change is one logical thing. If two, split into two commits and say so.
- Changed lines are about 150 or fewer, or the reason for more is written down.
- No secrets, no real personal data, no files that the repo ignores on purpose.
- No leftover debug prints, stubs, or commented-out code.
- The ticket has its proof and the `## What I can say about this` section. If
  the second is missing, run `/explain` first.

## 2. Commit message

Follow the repo's format. If it has none, use:

```
<type>: <what changed, under 60 characters>

<one or two sentences on why>
```

where type is one of feat, fix, test, docs, chore, refactor.

## 3. Pull request description

Write it for a reviewer who reads every line and has ten minutes.

```
## What
<two sentences>

## Why
<the ticket, in one sentence>

## How I checked it
<the test count, the real command that was run, and its key output>

## Not checked
<anything unverified, or "Nothing">

## Where to look first
<the one file or function that matters most>
```

Write it in the user's voice: short, plain, first person.

## 4. Hand over the commands

Give each command in its own code block, in order: `git add` with the exact
files (never `git add .`), `git commit`, and, only if the repo uses pull
requests, the push and the `gh pr create` command with the description above.
Before the push command, say plainly that pushing sends the code to the
remote, and name the remote.

## 5. Corrections become checks

If this pull request comes back with review comments, for each comment: fix
it, then add a test, a lint rule or a setting so it cannot happen again. If the
comment is a general rule, propose one line for the repo's `CLAUDE.md` as well.

## Finish

```
Ready for review: <the commit subject line>
Next step: run the commands above, in order.
After that, type: /next
```
