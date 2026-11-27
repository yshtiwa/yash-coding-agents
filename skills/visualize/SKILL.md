---
name: visualize
description: Draw a one-page picture of the whole plan: every slice, every ticket, what is done, what is in progress and what comes next. Use when the user asks for the big picture, a bird's-eye view, a progress overview, "where are we overall?", or says "visualize"; after /kickoff; and at a checkpoint. Not for explaining one change; that is /explain.
---

# Visualize

A list of tickets hides the shape of the work. This skill draws it: one
page, readable at a glance, built from the ticket files themselves. It
changes nothing in the project. It only reads, then writes one picture.

The drawing is done by a script beside this file, `build_overview.py`, so
the picture is the same every time and nothing is invented.

## 1. Find the tickets

Read `docs/agents/issue-tracker.md` to learn where tickets live; with no
such file, look in `docs/tickets/`. Each folder of tickets is one slice. If
there are no tickets, stop: the next step is `/kickoff`.

## 2. Check the labels against the repo

A ticket's `Progress:` line is a claim. Before drawing, check it the way
`/next` does: `git status --short`, `git log --oneline -10`, and the test
suite.

- A ticket with no `Progress:` line whose code is already on disk: pass
  `--assume NN=claimed` to the script.
- A ticket marked further along than the repo shows: draw it as the repo
  shows, with `--assume`, and say so in the note.
- Anything a viewer would misread without context goes in one sentence
  passed as `--note`.

Do not edit the ticket files here. If a label is wrong, say which, and
leave fixing it to `/next`.

## 3. Gather the words

- **Title:** the project's name.
- **Goal:** one sentence from the spec or the rules file, in plain words.
- **Later slices:** work the spec names but that has no tickets yet. One
  `--later "Name: one line"` each.

## 4. Draw it

```
python3 <this skill's folder>/build_overview.py TICKETS_DIR [TICKETS_DIR ...] \
  --out .agent-notes/overview.html \
  --title "..." --goal "..." \
  [--later "Slice 2: ..."] [--assume 03=claimed] [--note "..."]
```

Make sure `.agent-notes/` is in the repo's ignore file. The page is
self-contained: it opens in any browser, with no network.

*Done when* the script prints how many slices and tickets it drew, and the
count matches the ticket files you found.

## 5. Show it

Open the file for the user (on a Mac, `open .agent-notes/overview.html`),
or give its path. Then say, in three short lines: how many tickets are
done out of how many; where they are now; what comes next.

How to read the picture:

- Each box is a ticket. Columns run left to right in the order tickets
  unblock each other. An arrow points from a ticket to the ones it unblocks.
- Green is done. Amber is in progress. Blue can start now. Grey and dashed
  is waiting on another ticket.
- The bar at the top is the whole project; each slice has its own.

## 6. On a shared board, only if asked

If the user asks for the picture on a shared whiteboard tool (such as
Miro) and a connector for that tool is available in this session:

1. Say exactly what would be sent: the slice names, the ticket numbers,
   titles and states, and the goal sentence. Nothing else.
2. Check that none of it is private: no real names, no client or company
   names, no data. If any is, stop and ask the user to reword it.
3. Wait for a clear yes. Then draw the same layout there: one frame per
   slice, one card per ticket, coloured by state, with the arrows.

A shared board is a copy. The ticket files stay the truth; redraw the board
after tickets move, and say when it was last drawn.

## Finish

```
Overview: <path to the page>
Done: <n> of <total> tickets | In progress: <n> | Can start now: <ticket numbers>
Labels that did not match the repo: <which, or "none">
Next step: <what /next would say>
Type this: /next
```
