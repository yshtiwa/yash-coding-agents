---
name: build
description: Build one opened ticket. Test first, then code, then run the real thing as proof, then a fresh judge scores it. Stops and reports on any failure. Use after /ticket, or when the user says "build it" or "implement this ticket".
---

# Build

You write all the code. The user reads it afterwards. Read
`~/.claude/skills/standards/SKILL.md` and the repo's `CLAUDE.md` before the
first line. Where they differ, the repo wins.

If the ticket has no `## How we will know it works` section, stop and run
`/ticket` first.

## 1. Test first

For each case in the ticket's check, one at a time:

1. Write the test. Run it. Confirm it fails for the right reason.
2. Write the least code that makes it pass.
3. Run the whole test suite. Everything passes before the next case.

If a test-driven-development skill is installed in this session, follow it for
the details of what makes a good test.

## 2. Tidy

Run the repo's formatter and linter. Fix what they flag in the files this
ticket touched. Leave other files alone and list anything you left.

## 3. Prove it runs

Tests passing is not proof. Run the real command named in the ticket on real
input and paste the output. Compare it, line by line, with what the ticket said
it should show. If it differs, it is not done.

## 4. Judge

Start a **fresh sub-agent** that has not seen your work. Give it only: the
diff, the ticket, the standards file and the repo's `CLAUDE.md`. Ask it to
score the change out of 10 on each of:

- tests (do they test behaviour, could they fail, are edges covered)
- naming and comments
- structure (small functions, input and output at the edges)
- duplicated code
- matches the ticket, nothing extra

Any score below 8: fix what it named, run the tests and the proof again, and
judge again with another fresh sub-agent. **Stop after 3 rounds** and report
what is still below 8. Do not argue with the judge; fix or report.

## 5. Stop conditions

Stop and tell the user, in plain words, if:

- a test cannot be made to pass without changing what the ticket asked for;
- the change passes about 150 lines (propose where to split);
- the work needs a decision that is hard to undo;
- anything in the data looks real instead of synthetic.

Never commit, push or merge. The user does that.

## Finish

Report in this shape, then stop:

```
Built: <one sentence>
Tests: <N passed>
Proof: <the command, and the output or its key lines>
Judge: <the five scores, and the round number>
Not checked: <anything you could not verify, or "nothing">
Changed lines: <number>
Next step: explain it back, so you can answer for it in review.
Type this: /explain
```
