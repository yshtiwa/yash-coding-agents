---
name: speed
description: Make something faster or lighter, with measurements before and after. Use when there is evidence something is slow or costly (a slow run, a slow page, a timeout, a bill), when a ticket states a speed requirement, or when the user says "this is slow" or "optimise this". Not for guesses that something might be slow.
---

# Speed

Work on speed only with evidence of a problem or a stated requirement.
Guessing which part is slow is wrong most of the time. Read
`../standards/SKILL.md` first. You do not commit; the user does.

## 1. Say what "fast enough" means

One sentence: what is slow, for whom, and the number that would count as
fixed. If there is no target, ask for one or propose one with a reason.

Unless this belongs to a ticket already in progress, write a ticket for it
from the kickoff skill's `ticket-template.md` (Kind: structure only). Its
check is the target number and "the real run's output is identical before
and after". Set `Progress: claimed`.

## 2. Measure first

- One command that produces the number, on realistic (synthetic) input.
- Run it at least five times. Record the middle value and the range.
- Check the measurement itself: **did it finish without errors, and did the
  work actually happen?** A run that skipped work, hit a cache or timed out
  early produces a fast, false number.
- Write down the machine and the conditions.

*Done when* the baseline number, its range and its command are written in
the ticket.

## 3. Find where the time goes

Use the language's profiler or timed sections. Name the **one** biggest
cost. Common ones:

- The same lookup repeated inside a loop, one item at a time.
- Reading or loading far more than is needed.
- Work redone that could be done once.
- Waiting on something outside, one call after another.
- For a screen: very large images or files sent to the browser, many
  requests that block the page, work done before anything is shown.

## 4. Change one thing

Fix the biggest cost only. Keep behaviour identical: existing tests pass
unchanged. A gain bought by skipping needed work (a dropped check, a cache
that serves stale data) is a bug, not a gain.

## 5. Measure again, the same way

Same command, same conditions, same number of runs.

| Result | Do |
|---|---|
| Clearly better than the range of noise, tests green | Keep. Put before and after in the commit message. |
| Inside the noise | Undo it. Kept code must be maintained forever. |
| Worse | Undo it. |
| Better, but a test fails or the real run's output differs | Undo it. |

"Undo it" means edit the files back. Git commands are the user's.

Repeat from step 3 until the target is met or the next biggest cost is not
worth its complexity. Say which.

## 6. Keep a record

In the ticket, one line per attempt, including the ones undone: the idea,
before and after, the verdict, why. Undone work leaves no trace in the
history, and will be tried again without this.

## 7. Guard it

Add the cheapest check that would catch it getting slow again: a count of
operations or a size limit is best, because it gives the same answer every
run. Use a time limit only if it is generous enough never to flicker.
Record today's number so it cannot quietly get worse.

## For a screen in a browser

Measure in a real browser on a realistic connection, not on the developer's
machine alone. Three things a person feels: how long until the main content
shows, how quickly it responds to a tap or click, and whether things jump
around while loading. Fix the biggest of those first.

## Finish

Then finish it like any change: steps 2 to 6 of the `build` skill, and set
`Progress: built`.

```
Speed: <what was slow>
Target: <number> | Before: <middle, range> | After: <middle, range>
Changed: <the one thing, or the list of kept changes>
Tried and undone: <list, or "none">
Guard: <the check added>
Verdict: <faster | no measurable difference | inconclusive>
Next step: explain it back.
Type this: /explain
```
