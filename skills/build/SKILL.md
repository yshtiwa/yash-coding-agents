---
name: build
description: Build one opened ticket to the point where it is proven and judged. Use after /ticket, or when the user says "build it" or "implement this ticket", even when the change looks small.
---

# Build

You write all the code. The user reads it afterwards. Before the first line,
read `../standards/SKILL.md`, `../standards/tests.md`, the repo's `CLAUDE.md`,
and `../standards/data-and-privacy.md` whenever the ticket touches data,
files or logs. Where they differ, the repo wins.

You own this change until the report at the end. You do not commit, push or
merge; the user does.

After each numbered step, update the ticket's line to
`Progress: claimed (build step N done)`, so a sudden stop can be picked up.

## 0. Before touching anything

- The ticket needs `## How we will know it works`. If it has a "Done when"
  list but not that section, stop: the `ticket` skill writes it. If the code
  for this ticket already exists and its tests pass, write nothing new and
  go to step 2.
- Say the ticket's title and the smallest change that meets it.
- Find the repo's real commands for one test, the whole suite, the linter
  and the formatter (the repo's `CLAUDE.md`, then its build or CI file).
- If the repo uses branches, check you are on this ticket's branch. If not,
  give the user the command and wait.
- Run the whole suite. It must pass before you start. If it fails, stop:
  that is a bug to fix first, with the `bugfix` skill.

## 1. Test first, one case at a time

For each case in the ticket's check:

1. Write one test. Run it. See it fail for the right reason.
2. Write the least code that makes it pass.
3. Run the whole suite. All green before the next case.

Keep a build log in `.agent-notes/` (one file per ticket): each fork you
take, each approach you drop, each thing you revert, with why. The judge
does not see this file.

**Structure-only ticket:** record the current output first. Take small steps,
suite green after each. Add no behaviour. At the end the output is identical.

Restructuring beyond what a case needs waits for step 3.

## 2. Prove the tests bite

Break one thing this change added. Run the tests: at least one fails. Put it
back: all pass. If nothing failed, write the missing test.

## 3. Tidy

- Run the formatter and linter on the files this ticket touched.
- Look only at code this ticket touched for: nesting three levels deep, a
  function over about 50 lines, a true/false switch parameter, a vague name,
  a comment that repeats the code, a function that only passes calls on. Fix
  one at a time, tests unchanged and green after each. If a fix does not make
  it clearly easier to read, undo it.
- Anything outside the ticket goes on the **Noticed, not touched** list.

## 4. Guard the bar

Read your own diff for section A of `../standards/review-checklist.md`
(skipped tests, removed assertions, silenced rules, stubs, edited expected
values). Undo any you find, or stop and ask.

## 5. Prove it runs

Tests passing is not proof.

1. If `docs/agents/proof.md` exists, follow its Launch and Doctor steps.
2. Run the ticket's proof command on real (synthetic) input. Paste the output.
3. Compare it, line by line, with what the ticket said it must show.
4. Check the work happened: the count of items handled, the count of errors,
   and for anything written, read the stored result back.
5. Re-run any existing journey in `proof.md` that this change could affect.
   If this ticket adds something a user can now do, add it to `proof.md` as
   a new journey.
6. Give the verdict: **VERIFIED, NOT VERIFIED or INCONCLUSIVE.** If the check
   itself looks wrong, suspect how you observed it before you suspect the code.

Anything but VERIFIED: fix and repeat this step, or go to "Stop and ask".
The judge is not called on unproven work.

## 6. Judge

Start one **fresh sub-agent** using the brief in `judge-brief.md`, filled in.
Give it the ticket, the standards folder, the repo's `CLAUDE.md` and your
proof output. Do not give it your reasoning, your summary or the build log.

When it reports, check each finding against the code, in this order:

- **Fix:** it is right. Fix it.
- **Disproved:** you can point to the code or a command output that shows it
  is wrong. Keep the evidence.
- **Trade-off:** it is right and so is the current choice. Make the call
  yourself, give the plain reason, and record it as "agent decision, for the
  reviewer to check".
- **Already there:** not this change. One line for a future ticket.

Every finding you did not fix goes in the report with its reason. If you are
dismissing more than half of the Must fix and Should fix findings, say so
plainly: you may be defending the work instead of checking it.

**It passes when** every score is 8 or more **and** no Must fix finding is
open (each is fixed or disproved with evidence).

After any fix: re-run the suite and the proof, then judge again with a new
fresh sub-agent, asking it to re-check only what failed and what the fixes
touched. Do not judge an unchanged diff twice. **Stop after 3 rounds.** If
two rounds fail on the same point, stop sooner: the approach is wrong, not
the polish.

After the judge finishes, run `git status` and confirm it changed no files.

When it passes, save the diff fingerprint (standards section 6) and the
round number in `.agent-notes/` as `NN-judged.txt`.

## Stop and ask

Stop with a decision card (the call, your pick, what it changes, the
evidence, the risk), and leave the ticket at `Progress: claimed`, when:

- the proof is not VERIFIED and you cannot make it so;
- the judge has not passed after 3 rounds, or failed twice on one point;
- a case cannot pass without changing what the ticket asked for;
- an expected value in the ticket looks wrong;
- the change is over the size rule;
- the work needs a step that cannot be undone;
- anything in the data looks real instead of synthetic;
- two fixes for the same failure have not worked.

## Finish

Only when the proof is VERIFIED and the judge has passed: set
`Progress: built`. Report in this shape, then stop:

```
Built: <ticket title>, <one sentence>
Tests: <N passed>; tests shown to fail when the code is broken: yes
Proof: VERIFIED <command, key output lines, items handled, errors>
Judge: passed in round <n>; scores: ticket <n>, tests <n>, naming <n>,
       structure <n>, duplication <n>, safety and data <n>
Findings not fixed: <each with its reason, or "none">
Not checked: <or "nothing">
Noticed, not touched: <or "nothing">
Worth your attention: <the one part most worth a close look>
Changed lines: <non-test> + <test>
Next step: explain it back, so you can answer for it in review.
Type this: /explain
```
