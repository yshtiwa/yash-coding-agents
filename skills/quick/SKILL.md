---
name: quick
description: Make a tiny, safe change without the full ticket process. Use for a typo, wording, a comment, a rename with no change in behaviour, a display setting, or a one-line fix the user has already pinned down. Not for anything that adds or changes logic, touches data handling, security, money or a stored format, or reaches past about 20 lines.
---

# Quick

Ceremony should match the stakes. A typo does not need a ticket, a judge
and an explain-back. This is the short path for changes that cannot
surprise anyone.

## 1. Check it really is tiny

All of these must be true. If any is not, stop and say which; the next step
is `/ticket`.

- About 20 changed lines or fewer, in one or two files.
- No new or changed logic: no new branch, calculation, rule or mapping.
- It does not touch how data is read, checked, stored or sent.
- Nothing about security, personal data, money or a stored format.
- It can be undone by reverting one commit.

A setting counts as tiny only when it is not a business rule or a
threshold: a label, a display value, a path. A setting that changes what
the program decides is logic, and takes a ticket.

## 2. Say it back

One sentence: what will change and where. Then do it.

## 3. Make the change

Only what was asked. Anything else you notice goes on a list for the user.

## 4. Check

- Run the whole test suite, the linter and the formatter. All pass.
- If behaviour changed in a way a user could see, run the real thing once
  and show the output.
- Read your own diff: is it only what was asked?

If a test fails, this was not tiny after all. Stop; the next step is
`/bugfix` or `/ticket`.

## 5. Show it

Show the diff and say in two or three plain sentences what changed and why
it is safe. No questions to answer; the user reads it and says yes or no.

## Finish

```
Quick change: <one sentence>
Files: <list>   Lines changed: <n>
Checks: tests <N passed>, lint clean
Noticed, not touched: <or "nothing">
Next step: package it.
Type this: /pr
```

`/pr` treats this as a support change: no judge and no explain-back. It
checks the five conditions above against the diff again, and the scan and
one-change-per-commit still apply.
