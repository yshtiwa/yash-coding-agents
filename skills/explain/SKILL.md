---
name: explain
description: Walk the user through the change just built, in plain English, then check they can answer for it. Use after /build, or when the user says "explain this change" or "what did you build".
---

# Explain

The user did not type this code, but their name is on it and a reviewer will
ask them about it. This step makes the change theirs. It takes about five
minutes. Do not skip it and do not shorten it to a summary.

The user learns from pictures and full sentences. No jargon without a
plain-words meaning the first time it appears.

## 1. Show the change

Look at the real diff (`git diff` and new files). Then give:

- **One picture.** A small text diagram of what goes in, what happens, and what
  comes out, using this change's real example.
- **The walk-through.** One short paragraph per file: what it is for and what
  changed. Link each file.
- **Three lines worth knowing.** The three lines a reviewer is most likely to
  ask about, each with what it does and why it is written that way.
- **What it does not do yet,** and which ticket brings it.

## 2. Ask three questions

Ask the three questions a careful reviewer would ask about this change, **one
at a time**. Mix them: one "what does this do", one "why this way and not
another", one "what happens if" (bad input, an empty file, a missing setting).

After each answer:

- If it is right, say so in one line and add anything they missed.
- If it is wrong or partial, give the full answer straight away, plainly. This
  is not an exam; give full help.
- If they cannot answer because the code is hard to follow, that is a fault in
  the code. Rewrite that part more simply, run the tests again, and say what
  you changed.

## 3. Write it down

Add two or three sentences in the user's own words to the ticket under
`## What I can say about this`, built from their answers. Short, casual, first
person. Edit their words; do not replace them.

## Finish

```
You can answer for this change.
Next step: package it for review.
Type this: /pr
```
