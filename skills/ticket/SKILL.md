---
name: ticket
description: Open one ticket before any code is written. Use as "/ticket" for the next ticket in line, "/ticket 05" to pick one, or when the user says "start the next ticket". Not for a tiny change with no logic; that is /quick.
---

# Ticket

No code is written until this is done. One ticket is one small change. Read
`../standards/SKILL.md` section 7 first.

## 1. Find it and say it back

Read `docs/agents/issue-tracker.md` to learn where tickets live; with no such
file, look in `docs/tickets/`. If there are no tickets at all, stop: the
`kickoff` skill comes first. With no number given, take the lowest-numbered
ticket whose `Progress:` is not done and that is not blocked. If its blockers are unfinished, stop and say which. Work on the
existing ticket file; write a new one only when none exists for the work.

Then tell the user, in your own words: **the ticket's title, what it asks
for, and the smallest change that would meet it.** A misreading caught here
costs nothing.

## 2. Read around it

The repo's `CLAUDE.md`, the glossary, decision records for this area, the
proof recipe (`docs/agents/proof.md`) if there is one, and the code the
ticket will touch. Note the kind of change: **new behaviour, bug, or
structure only.** A bug goes to the `bugfix` skill instead.

Note the **stakes** too (standards section 10), and write them in the
ticket as `Stakes: normal` or `Stakes: high`. Tiny work does not need a
ticket: say so and point to `/quick`.

*Done when* you can list your assumptions as numbered lines. Show them.

## 3. Ask until nothing is unclear

- Ask in **small rounds**: up to three questions that do not depend on each
  other, each with your recommended answer and the plain reason, worded so
  "yes" accepts it. Then the follow-ups those answers opened.
- **No limit on the number of questions.** The limit is scope: every question
  is about this ticket. A question about a later ticket is written into that
  ticket as a note.
- **Ask only what needs a person's judgement.** Anything the repo or a
  command can answer, look up.
- **A technical choice the user cannot judge** is yours. State it and record
  it as "agent decision, for the reviewer to check".
- **A question for the reviewer** becomes a short message the user can send.
- Always ask yourself, and the user if unsure: **what, other than the two of
  us, would show the result is right?**

*Done when* you can say the plan back and the user gives a clear yes.

## 4. Write the check into the ticket

Add `## Decisions` as a table (decision, why, who decided). Then add
`## How we will know it works`:

- **Cases:** one for each line of the ticket's "Done when" list, each as
  input and expected output, in plain words. For each,
  one line on what you would see if it were false. A case that could not
  fail today is not a case.
- **Where the tests sit:** which function or stage each case is tested at,
  and what that place cannot catch.
- **The proof:** the one real command to run, what its output must show,
  and that it reports how many items it handled and how many errors.
- **Must not change:** existing behaviour this ticket has to leave alone.
- **Out of scope:** what is deliberately left for later.

Add these when they apply:

- A new or moved **data field:** its label (non-personal, personal,
  sensitive), why it is kept, how long.
- A step that **writes or sends:** what happens if it runs twice, or stops
  halfway.
- **Structure-only change:** how the current output will be recorded first.
- New code that can fail in use: **the questions someone will ask when it
  breaks,** so the logs can answer them.

## 5. Size it

Use the size rule in the standards (section 5). Propose a split when: the title
needs "and", there are more than four cases, it touches two separate areas,
or you cannot say what could be demoed when it is done.

## 6. Claim it

Set the ticket's `Progress:` line to `claimed` (add the line if it is
missing; leave any other status line the repo uses alone). If the repo works
through pull requests, work out the branch command, for example
`git switch -c feat/02-routine-adjustments`, following the repo's naming.

## Finish

```
Ticket: <title>
Will build: <one sentence>
Proof will be: <the command>
Stakes: <normal | high, and why>
First, run this yourself: <the branch command, if the repo uses branches>
Next step: <normal: "build it" | high: "settle the design first">
Type this: </build | /design>
```
