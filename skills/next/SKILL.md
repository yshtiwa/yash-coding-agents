---
name: next
description: Tells the user the one next step and the exact thing to type. Use when the user asks "what's next", "where am I", "what do I do now", or seems unsure how to continue.
---

# Next

The user is not an engineer and does not know the order of work. Look at the
repo and tell them the **one** next step. Never give a menu.

## Look first

Run these and read the results. Do not ask the user what state things are in.

1. `git status --short`, `git branch --show-current`, `git log --oneline -5`
2. The test command from the repo's `CLAUDE.md` (for example `uv run pytest -q`)
3. The tickets. Read `docs/agents/issue-tracker.md` if it exists to find where
   they live. Note each ticket's status and what blocks it.

## Decide

Take the first row that is true.

| What you find | The next step |
|---|---|
| Tests fail | Fix them. Say which test and why it fails, then fix it. |
| Changed files, tests pass, no explain-back done for this ticket | `/explain` |
| Changed files, explain-back done | `/pr` |
| Clean tree, a branch that is not merged | Open or merge its pull request. Give the commands. |
| Clean tree, a ticket is unblocked | `/ticket NN` for the lowest-numbered unblocked ticket |
| A ticket is open and its check is written, no code yet | `/build` |
| No tickets left in this slice | Say the slice is done. Suggest a demo to the reviewer, then planning the next slice. |
| No tickets exist at all | Planning comes first. Point to the repo's planning skills. |

If a person other than the user is blocking (a review, a decision, missing
data), say who and what to ask them, as a message the user can paste.

## Answer in this shape

```
Where you are: <one sentence>
Next step: <one action in plain words>
Type this: <the exact command or slash command>
Why: <one sentence>
```
