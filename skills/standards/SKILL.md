---
name: standards
description: The engineering standards every change must meet. Read before writing or reviewing code. Used by /build, /explain and /pr, and by the judge agent.
---

# Engineering standards

These are the habits a seasoned engineer applies without being asked. They are
language-neutral. Where the repo's own `CLAUDE.md`, `AGENTS.md` or a reviewer's
written rule says something different, **the repo wins**. Say so when it happens.

## 1. Shape of the code

- **Small functions, one job each.** If describing it needs "and", split it.
- **Pure in the middle, input and output at the edges.** Logic takes plain data
  and returns plain data. Reading files, the network, the clock and random
  numbers happen only at the outer edge and are passed in.
- **The code reads like the diagram.** One top-level function per stage calls
  the small ones in order.
- **Use the project's words.** Names come from the glossary. No synonyms.
- **Subtract before you add.** Prefer deleting or reusing code over new code.
  Make the smallest change that does the job.
- **No abstraction until the third use.** Two similar things can stay separate.
- **No knowledge buried in code.** Business meaning, thresholds and mappings
  live in named settings or data files, never as bare numbers in logic.

## 2. Tests

- **Test first.** See the test fail for the right reason before writing code.
- **Test behaviour at a boundary.** Given this input, is the output exactly
  what the next step expects? Never test how a function works inside.
- **Test our logic, not a library.** No test that saves a thing and reads it
  back to prove the library works. Check an outside boundary by hand once.
- **No tests that cannot fail.** A test that repeats the code's own formula, or
  asserts what it just set up, proves nothing.
- **Cover the edges:** none, one, many, the boundary value, and bad input.
- **Repeatable.** Same result every run. No real clock, network or shared state.
- **Expected values are written by hand**, not computed by the code under test.

## 3. Errors and data

- **Our mistake stops the run loudly.** A gap in our own config is an error
  that names what is missing and where. Never a silent default.
- **Outside input degrades gracefully.** One bad row from outside is flagged
  and set aside; it does not block the rest.
- **Never swallow an error.** No empty `except`, no ignored return value.
- **Check input where it enters,** then trust it inside.
- **Money is exact decimals.** Never floating point.
- **Dates are explicit.** "Today" is passed in. Time zones are stated.
- **Raw input is never changed.** Everything else can be rebuilt from it.
- **Safe to run twice.** Running again gives the same result, with no duplicates.

## 4. Safety and privacy

- **No secrets** in code, tests, commits, logs or prompts.
- **No real personal or patient data** in tests, fixtures, logs, error
  messages or anything sent to a hosted model. Synthetic data only unless the
  repo says otherwise in writing.
- **Treat outside input as untrusted.** Validate it; never run it.
- **Few dependencies.** Each new one needs a reason. Versions are pinned.
- **One-way doors need a person.** Deleting data, changing a schema, sending
  anything outside, or anything that cannot be undone: stop and ask.

## 5. The change itself

- **One logical change per commit and per pull request.**
- **Small.** Aim for about 100 changed lines. Over 150, split it or say why not.
- **No drive-by edits.** Do not tidy unrelated code in the same change.
- **No dead code.** No commented-out blocks, no unused functions, no stubs.
- **Comments say why, not what.** One short docstring per function. No comment
  that records history ("changed because X said so").
- **The commit message says what changed and why,** in the repo's format.
- **The pull request shows proof:** what was run, the output, and what was not
  checked.
- **Decisions are written down.** A choice that is hard to reverse, surprising,
  and a real trade-off gets a short decision record.
- **Every correction becomes a check.** When a reviewer or the user corrects
  something, add a test, a lint rule or a setting that enforces it. A line in a
  notes file enforces nothing.

## 6. Excuses, and the answer to each

| The excuse | The answer |
|---|---|
| "This is too simple to test." | Simple code is the cheapest to test. Write it. |
| "The tests pass, so it works." | Run the real thing and show the output. |
| "I checked it by hand." | Then the check is lost. Put it in a test. |
| "I'll clean this up later." | Later does not come. Do it now or write a ticket. |
| "It's only a small extra fix." | It is a second change. Separate commit. |
| "A default is safer than an error." | A default hides our mistake. Stop loudly. |
| "The reviewer will catch it." | The reviewer's time is the scarce thing. Catch it first. |
| "I added a comment explaining the workaround." | Fix the cause, or write a ticket. |

## Where these come from

Common industry practice, three public skill packs (Matt Pocock, Lauren Tan's
pstack, Addy Osmani's agent-skills) and the user's lead engineer. They are a
starting point for the lead engineer to correct, not a rulebook they approved.
