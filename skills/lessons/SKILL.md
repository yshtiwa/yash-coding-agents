---
name: lessons
description: Turn a correction or a hard session into a lasting check, so the same mistake cannot happen again. Use after review comments are handled, after a ticket that went badly, at the end of a slice, or when the user says "make sure this never happens again".
---

# Lessons

A rule in a notes file enforces nothing: nothing fails when an agent skips
it. This skill turns what went wrong into something that fails.

## 1. Collect

List what was corrected or went wrong, each in one line with where it
happened: review comments, findings the judge kept raising, fixes that were
tried and dropped, time lost. For each, ask: **what in the setup would have
stopped this before it was written?**

Keep a lesson only if it will still matter in six months and changes what
the agent does. One bad session is not a pattern; a mistake counts as a
class when it has happened twice, or when the reviewer said it as a rule.

## 2. Choose the strongest enforcer

Take the first that can work.

1. **Structure:** change the code's shape so the mistake cannot be written
   (one place to do the thing, a type that cannot hold the bad value).
2. **A lint or type rule** whose error message says what to do instead.
3. **A test.**
4. **A pre-commit check** (format, lint, tests on staged files, the
   secrets-and-personal-data scan).
5. **A written rule,** only for a judgement call no tool can check. It goes
   in the repo's `CLAUDE.md`, with one example of the mistake.

If it became a check, do not also write a note about it.

## 3. Prove the check works

Run the new check against the real past mistake: it must fail. Run it on
the corrected code: it must pass. A check never seen failing proves nothing.

If the codebase already breaks a new rule in many places, record today's
count and forbid it from rising. Never set a bar the build fails on day one.

## 4. Keep the table

Add each to `docs/agents/checks.md`:

| Rule | Enforced by | Command that runs it | Added because |
|---|---|---|---|

## 5. Ask before changing anything

Show the user three lists: **Accept** (with the enforcer for each),
**Reject** (with the reason), **Later** (as tickets). Make only the changes
the user says yes to. Each check is its own small change: it goes through
`/pr` as a support change.

## Finish

```
Lessons: <N> accepted, <N> rejected, <N> for later
Next step: <"package the new check" or "carry on">
Type this: </pr or /next>
```
