---
name: bugfix
description: Find and fix a bug or a failing test by reproducing it first. Use when tests fail, something behaves wrongly, a run crashes, or the user says "this is broken" or "why is this happening".
---

# Bugfix

Work stops on anything else until the failure is understood. Read
`../standards/SKILL.md` and `../standards/data-and-privacy.md` first. You do
not commit; the user does.

## 1. Say the problem back

In your own words: what happens now, and what should happen instead. Do not
adopt the user's theory of the cause yet.

## 2. One command that fails

Before any theory, get **one command that fails on this exact bug**. In
order of preference: a failing test at the place the bug shows; the real
command on a small fixed input, compared with the right output; a tiny
script around one function.

*Done when* the command is named, has been run with its output shown, fails
every time, takes seconds, and you can run it unattended.

If you catch yourself reading code to form a theory before this exists,
stop. If it cannot be built, say what you tried and ask the user for a
synthetic or scrubbed input that shows it, or permission to add temporary
logging. Do not guess. Real personal data is never pasted into the chat.

Confirm it is the failure the user described, not a nearby one.

## 3. Shrink it

Remove inputs, data and steps one at a time, re-running after each. *Done
when* removing any remaining piece makes the failure go away.

## 4. Theories, then tests of them

Write **three to five ranked theories** before testing any. Each in the form:
"If X is the cause, then changing Y makes it pass." A theory with no
prediction is dropped. Show the list to the user in plain words and carry
on; they may know something that rules one out, and need not rank them.

Test them by halving: each check should rule out as many remaining theories
as possible. Change one thing at a time. Tag every temporary debug line with
one unique marker (for example `DEBUG-7c2`) so one search removes them all.

## 5. Find the cause, not the symptom

Ask "why" until the answer is a wrong decision in the code. Then ask: **is
the state that triggered the failure allowed to exist?**

- Yes: handle it where it broke.
- No: find what produced it and fix that. A guard at the point of failure
  would hide the bug.

Search for the same fault elsewhere and list each place.

## 6. Fix

1. Turn the shrunk failure into a test. Watch it fail.
2. Apply the smallest fix. Watch it pass.
3. Run the whole suite.
4. Run the **original** failing command from step 2. It must now pass. A
   unit test alone does not prove the bug is gone.

No new guards, retries, defaults or swallowed errors unless the cause
analysis calls for one.

**After two fixes that did not work:** stop. Write, in one sentence, the
assumption both fixes shared. Test that assumption directly before a third.

## 7. Clean up

- All tagged debug lines and throwaway scripts removed.
- Any secret or personal value replaced in everything shown.
- Propose the cheap always-on signal (a clearer error, one log line, an
  assertion) that would have shown this cause at first look.

## 8. Finish it like a build

A fix is a change like any other and must pass the same bar.

1. Write a ticket for it from the kickoff skill's `ticket-template.md`
   (Kind: bug), unless it belongs to the ticket in progress. Its check is
   the failing command from step 2 and the test from step 6. Set
   `Progress: claimed`, and `Stakes:` by the table in standards section 10.
2. Run steps 2 to 6 of the `build` skill on the fix: prove the test bites,
   tidy, guard the bar, prove it runs with a verdict, and the fresh judge.
3. Set `Progress: built`.

## Finish

```
Bug: <what was wrong, one sentence>
Cause: <the wrong decision in the code, with file and line>
Theory that proved right: <which>
Fix: <one sentence>
Proof: VERIFIED; test failed before, passes now; original command now passes
Judge: passed in round <n>
Same fault elsewhere: <places, or "none found">
Would have caught it: <the signal you propose>
Not checked: <or "nothing">
Next step: <normal: "explain it back" | high stakes: "check it for security and privacy first">
Type this: </explain | /security>
```

If this bug came up in the middle of another ticket and the fix is not part
of that ticket, say so: it is its own change and its own commit.
