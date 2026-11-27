---
name: kickoff
description: Plan a new piece of work before any ticket exists. Use when the user wants to start a new feature, slice or project, says "let's plan", or when /next finds no tickets.
---

# Kickoff

Turns an idea into a short set of tickets. No product code is written here. If you
feel the pull to start building, the planning is finished: write the tickets
and stop.

Read `../standards/SKILL.md` section 7 first. Keep the whole kickoff in one
session so each part builds on the last.

## 1. Read before asking

Read the repo's `CLAUDE.md`, the glossary, decision records, and the code the
work will touch. Find the test and run commands. Anything the repo can answer
is never asked of the user.

*Done when* you can describe how the relevant part works today, with files
you opened.

**Set up the two places the skills write to,** if they are missing:

- `docs/agents/issue-tracker.md`: one short file saying tickets live in
  `docs/tickets/` as `NN-title.md`, one file each, and that each carries a
  `Progress:` line. If the repo already has this file, follow it instead.
- `.agent-notes/`: a folder for working notes (handoff, build logs, learning
  notes, checkpoints). Add it to the repo's ignore file so it is never
  committed.

`GLOSSARY.md` and `docs/adr/` are created the first time a term or a
decision is settled, not before.

## 2. Say what you think they want

One sentence: what you believe the user wants, and how sure you are as a
percentage. Under about 70 percent, say what is missing.

## 3. Ask until nothing is assumed

Think of the decisions as a tree: some can only be made after others.

- Ask in **small rounds**: up to three questions that do not depend on each
  other. Wait. Then ask the next round the answers opened up.
- Each question carries **your recommended answer and the plain reason**,
  worded so that "yes" accepts it.
- **There is no limit on the number of questions.** Follow every answer that
  opens a new one. If several rounds pass and nothing is settling, say so and
  step back to the goal.
- **If the user's words and the code disagree,** show both and ask which is
  right.
- **Test each idea with a made-up concrete case** at its edge.
- **A technical choice the user cannot judge** is yours to make. Say what you
  chose and why, and record it as "agent decision, for the reviewer to check".
- **A question only the reviewer or another person can answer** becomes a
  short message for the user to send: purpose, context, the questions in
  order of importance, one idea each.
- **A question that talking cannot settle** gets a tiny throwaway experiment
  in a git-ignored scratch folder. Bring back the answer; never the code.
- Update the glossary the moment a term settles. Record a decision only when
  it passes the three-part test in the standards.

*Done when* you could predict the user's answer to your next three questions.

## 4. Confirm

Say it back in six lines: **Outcome, User, Why now, How we will know it
worked, Limits, Out of scope.** "Out of scope" is never empty. Only a clear
yes counts. "Whatever you think" means ask again with two concrete options.

## 5. Spec, only if needed

If the work is three tickets or more, write a spec from `spec-template.md`
in the place the repo keeps specs (see `docs/agents/issue-tracker.md` if it
exists). The spec only records what was settled; it asks nothing new. For
one or two tickets, skip it.

## 6. Tickets

Write one file per ticket from `ticket-template.md`.

- **The first ticket is a thin thread through every stage:** ugly but working
  end to end. Later tickets widen it.
- **Each ticket is a full path, not a layer,** and can be shown working on
  its own. Ask: "what can I demo when this is done?"
- **Small:** the size rule in the standards (section 5). Split when the title
  needs "and", the check needs more than four cases, or it touches two
  separate areas.
- **Each ticket lists what must finish before it.**
- **Riskiest first,** so a wrong idea fails cheaply.
- **A tidy-up that makes the real change easy goes first,** as its own ticket.
- **A wide rename or format change** is three tickets: add the new, move
  everything over, remove the old.
- **If the repo has no test runner, formatter, linter or ignore file,** the
  first ticket (00) sets them up, with checks that run before each commit
  and the scan for secrets and personal data.
- **Every third ticket is followed by a checkpoint:** all tests, the real
  run end to end, and a look by the user.

Show the list (title, what it delivers, blocked by). Ask the user whether
the order is right and whether anything is missing or unwanted. Sizing is
your job, not theirs. Repeat until the user says yes.

## Finish

```
Planned: <N> tickets for <one-sentence goal>
Not doing: <the out-of-scope list>
To see the plan as a picture: /visualize
Next step: open the first ticket.
Type this: /ticket
```
