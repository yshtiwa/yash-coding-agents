---
name: explain
description: Walk the user through the change just built and check they can answer for it in review. Use after /build or /bugfix, or when the user says "explain this change", "what did you build", or "you lost me".
---

# Explain

The user did not type this code, but their name is on it and a reviewer will
ask them about it. This step makes the change theirs. It takes about five
minutes. A summary does not replace it.

The user learns from pictures and full sentences, and is not a programmer.

## 0. Start from what they know

Read `.agent-notes/learning-notes.md` if it exists: what the user has
already shown they understand, and what was corrected before. State in one
line what you will take as known. Every other idea is introduced in plain
words before you lean on it.

## 1. Show the change

Look at the real diff (`git diff HEAD` and new files). Then:

- **Build the picture up in parts.** Start with the smallest complete version
  (one input, what happens, one output, using this change's real example).
  Add one part at a time. Pick the picture that fits: a flow of boxes, a
  before-and-after of the data, a tree of which function calls which, or a
  sketch of the files.
- **The walk-through.** One short paragraph per file: what it is for and
  what changed. Link each file.
- **Three lines worth knowing.** The three a reviewer is most likely to ask
  about: what each does and why it is written that way.
- **What was traded off,** and what this does not do yet.

## 2. Ask, one question at a time

Ask before you tell. Four questions, mixed:

1. What does this do? (one specific part)
2. Why this way and not another?
3. What happens if the input is bad, empty or missing?
4. Make the case: how do we know this fixes the cause, or meets the ticket,
   and is not only passing the tests?

Write questions so the wording does not give the answer away.

After each answer:

- Right: say so in one line and add what was missed.
- Wrong or partial: give the full answer straight away, plainly. This is not
  an exam.
- They cannot answer because the code is hard to follow: that is a fault in
  the code. Note it and carry on with the other questions. At the end, go
  back to `/build` step 3 to simplify that part once, then explain only
  what changed. If it is still hard to follow, stop with a decision card.

## "You lost me"

Whenever the user says they are lost, or asks for it plainly: say the last
thing again in three short parts. More background first. Then simpler words.
Then the glossary terms it used, each defined.

## 3. Write it down

- In the ticket, under `## What I can say about this`: two or three sentences
  in the user's own words, built from their answers. Short, casual, first
  person. Edit their words; do not replace them.
- In `.agent-notes/learning-notes.md`: one line on what they showed they
  understand and one on anything that was corrected. Evidence only, no
  praise.
- Save the diff fingerprint (standards section 6) in `.agent-notes/` as
  `NN-explained.txt`.
- Set the ticket's `Progress:` to `explained`.

## Finish

Be honest about how it went. If two or more answers needed the full
explanation, offer one more pass on those parts before moving on.

```
Explained: <ticket title>
You answered on your own: <n> of 4. Worth re-reading: <parts, or "nothing">
Next step: package it for review.
Type this: /pr
```
