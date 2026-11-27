---
name: release
description: Set up CI/CD (the automated checks that run on every change), or get a change safely into use. Use when a repo has no CI pipeline, when the user says "set up CI", "add a pipeline", "deploy this", "ship it" or "release", when a change is about to reach real users, or when the pipeline is slow or failing. Not for packaging one change for review; that is /pr.
---

# Release

Two jobs: **the pipeline** (automatic checks on every change) and **the
release** (getting a change to users without surprises). Every release
should be undoable, watchable and gradual.

You write pipeline files and checklists. You never deploy, never touch a
production system, and never handle a real secret. Those steps are handed
to the user as a short numbered list. Read `../standards/SKILL.md` first,
and `checklist.md` beside this file before a release.

## A. The pipeline

Read what the repo already has (a CI file, a build file, pre-commit
settings). Fix what is missing; do not add a second system.

The gates, cheapest first, each one blocking the next:

1. Formatter and linter.
2. Static checks the language offers, such as type checks.
3. Unit tests.
4. Build or package.
5. Slower tests that cross parts.
6. The dependency audit.

Rules:

- It runs on every pull request and every push to the main branch.
- A failure blocks the merge. **No gate is skipped:** fix the code, not the
  rule; fix the test, not skip it.
- A test that fails only sometimes is a bug to find.
- The pipeline holds no production secrets. Test credentials come from the
  pipeline's secret store.
- Aim under ten minutes. If slower: cache dependencies, run jobs side by
  side, run only what changed, move slow tests off the main path.
- The same fast checks (format, lint, unit tests, the secrets scan) also
  run before each commit on the user's machine.
- A new rule the code already breaks: record today's count and forbid it
  from rising. Never add a gate that is red on day one.

**Package it, then prove it.** The pipeline files are a support change:
they go through `/pr` first. Once the user has pushed them, prove the
pipeline works: a deliberately failing change on a branch must turn it
red, and the fix must turn it green. Hand the user the commands.

**Protect the main branch.** Give the user the steps, as a numbered list,
to require the checks and a review before anything merges, and to forbid
force-pushing to the main branch. Only a person can set this.

If merging to the main branch releases automatically, the main branch must
always be fit to release. That makes the pipeline the last line of defence.

## B. Before a release

Walk `checklist.md`. The parts that matter most:

- **A way back, written before going forward:** what triggers it, the exact
  steps, how to check it worked, who to tell, what happens to data already
  written. A release with no way back does not go.
- **A switch for anything risky.** New behaviour ships switched off, is
  turned on for a few people first, then widened. Each switch has an owner
  and a removal date. Both states are tested.
- **A change to stored data** goes out in separate steps (see
  `../design/interfaces.md`), the destructive step last and alone.
- **The people whose work changes are told first:** a short note on what
  changes, and a walk-through when a screen or a routine changes. They can
  ask for the switch to stay off until they are ready.
- **Signals exist** to answer "is it working?": the two to four questions
  someone will ask when it breaks, each answerable from logs or counts.

## C. Going out, and the first hour

Give the user the release steps as a numbered list. Then, with them:

1. The health check answers.
2. Errors are no higher than before.
3. The main thing a user does works, tried by hand.
4. Logs are arriving and readable.
5. The way back is ready.

**For a batch job** (a run that starts, does its work and ends), the first
real run is the first hour: the count of items in equals the count out plus
the count set aside; the output is read back and looks right; and it is
compared with the last good run. A line of the checklist that does not
apply is marked "not needed", with why.

Go back at once if errors more than double, something gets much slower,
data looks wrong, or a security hole appears. Going back is not failure;
leaving a broken release out is.

Pressure does not change a failed gate. If someone asks to release anyway,
the answer is "not yet", with the concrete steps that would make it a yes.

## Finish

```
Release: <pipeline set up | checklist walked | released>
Gates: <which exist, which were added>
Proven: <the red-then-green run, or "not yet">
Way back: <written at path | missing>
For you to do: <the numbered steps only a person can do>
Not checked: <or "nothing">
Next step: <one action>
Type this: </pr | /next>
```
