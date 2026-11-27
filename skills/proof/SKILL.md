---
name: proof
description: Create or refresh the repo's proof recipe, the written way to run the real thing and show it works. Use once when a repo first has something runnable, at the end of each slice, or when the user says "set up the proof" or "the proof recipe is out of date".
---

# Proof

Every ticket needs to run the real thing. Without a written recipe each
ticket reinvents how. This skill writes the recipe once and keeps it true.

The recipe is one file: `docs/agents/proof.md`. It is written for an agent
that has never seen this repo and is in the middle of another task. This
skill edits only that file and helper scripts for it. Product code is not
touched here; a broken product is reported, not patched.

## Create

Answer these from the repo, not from the user:

- **What does a user touch?** A command, a file drop, a screen.
- **How is it started?** The repo's own documented command.
- **How is it driven?** Existing commands and test inputs first.
- **What can be seen as evidence?** Output, files written, exit code.

If the repo does not build or run as it stands, stop and report that first.

Write the file with exactly these sections, no placeholders left:

- **Launch:** the exact command, and how to tell it is ready to use. For a
  short command-line tool: how to set up once, then run.
- **Doctor:** one read-only check that answers "is this worth driving?" Run
  it first whenever something looks off.
- **Journeys:** the three to five things a user does most. For each: one
  sentence of what the user sees, the exact command, the input it uses, and
  the observable result that proves it worked. For anything that writes, a
  second read-only step that looks at what was stored.
- **Evidence:** what to capture (command, output, errors, exit code, counts)
  and where to keep it.
- **Cleanup:** remove only what this run created. Never the evidence.
- **Traps:** things that waste or spoil a run.

Rules for the recipe:

- Synthetic input only. Name the fixture files.
- Use the path a real user takes, not an internal shortcut.
- If a journey cannot pass as the product stands, record it as failing with
  the reason. Never soften a journey until it passes.

**Prove it before handing it over:** run Launch, Doctor and one Journey as
written, capture the evidence, run Cleanup, and confirm the evidence is still
there. A recipe that was never run is a draft.

## Refresh

Run at the end of a slice, or when a ticket adds a journey.

1. Read each journey against the code and note what has drifted.
2. Run every journey as written.
3. Sort what you find: the description is out of date (fix the recipe); the
   recipe cannot drive something that works (fix the recipe, run it again);
   the product is broken (report it, as a new ticket).

End with one of three results: **clean** (nothing to change), **changed**
(list what), or **blocked** (say exactly what blocked it).

## Finish

```
Proof recipe: <created | clean | changed | blocked>
Journeys: <N>, <N> verified by running
Product problems found: <or "none">
Next step: <created or changed: "package it as its own small change" | clean or blocked: "carry on">
Type this: </pr | /next>
```
