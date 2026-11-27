---
name: design
description: Settle the shape of a change before any code is written. Use when a ticket adds a new module, a new data shape, a new interface between parts, a stored format, or changes something other code depends on; or when the user asks "how should this be built?" or "what's the architecture?". Not for a change that stays inside one function.
---

# Design

Most tickets need no design step: the shape is obvious and local. Use this
when a wrong shape would be costly to change later. No product code is
written here. Read `../standards/SKILL.md` first, and `interfaces.md` beside
this file when the change adds or alters an interface or a stored format.

## 1. Trace what it touches

List every part the change reaches: the functions that call it, the data it
reads and writes, the files or services at the edges. Read them; do not
guess. *Done when* you can draw it as boxes and arrows from files you opened.

## 2. Name the data first

Write the shapes that go in and come out, as named types with their fields.
Give two values of the same basic kind but different meaning (two kinds of
ID, an amount and a count) their own types so they cannot be swapped. A
value from outside has no type until one function at the edge has checked it.

## 3. Sketch two shapes

Two genuinely different ways to build it: where the pieces sit, what each
one knows, what the signatures are. A few lines each, no code bodies. The
first idea is rarely the best one; the second is what shows why.

## 4. Pick one, by these tests

- **One owner.** Each piece of state is held and changed in one place.
- **One way.** There is one way to do each thing, not two.
- **Callers know least.** What a caller must know to use it correctly is
  small: few entry points, simple parameters, no required order of calls.
- **The deletion test.** Imagine deleting each new piece. If its logic would
  spread across callers, it earns its place. If nothing is lost, drop it.
- **A swap point needs two real users.** Something behind an interface
  "so it can be replaced" is worth it only when two things really sit behind
  it (the real one and a test stand-in count).
- **It removes branches.** A structure (a table, a set of named states) is
  right when it deletes if/else chains or makes a wrong state impossible.
  Keep plain code when the shape is clear and unlikely to grow.

Say which you picked and the one-sentence reason the other lost.

## 5. Ask what it could break

- **The one fact this is safe because of.** Name it. Then show it: a line
  you can point to, or better, a command you ran.
- **Look where a text search stops:** the pinned version of a library, the
  order things happen in, the exact shape of a file or message, a setting.
- **What happens if it runs twice, or stops halfway?**
- **Who else depends on the thing being changed?** If anything does, plan
  the change in three steps (see `interfaces.md` beside this file): add,
  move over, remove.
- **If the stakes are high,** do steps 1 to 3 of the `security` skill now,
  on the design: where trust changes hands, what is worth protecting, how
  it could go wrong. A flaw found here costs minutes; found later, days.

## 6. Write it down

Add `## Design` to the ticket (or the spec, if it spans tickets):

- a small picture of the chosen shape;
- the data shapes;
- the choice, and the option turned down, with why;
- the safety fact and how far it was checked: said so / pointed at the
  line / walked the failure / ran it;
- risks that are real, and risks you checked and cleared, as two lists;
- anything that cannot be undone.

If the choice is hard to reverse, surprising to a later reader, and a real
trade-off, also write a decision record. Mark technical choices the user
cannot judge as "agent decision, for the reviewer to check".

If the design changes the ticket's cases, adds cases, or pushes it past the
size rule, say so: the ticket's check must be rewritten or the ticket split
before building.

Then explain the picture to the user in plain words and ask one question:
does this match what they want the system to do?

## Finish

```
Design: <one sentence on the shape chosen>
Turned down: <the other shape, and why>
Safe because: <the fact, and how far it was checked>
For the reviewer to check: <agent decisions, or "none">
Next step: <the ticket's check exists and no case changed: "build it" | otherwise: "rewrite the check for this ticket">
Type this: </build | /ticket>
```
