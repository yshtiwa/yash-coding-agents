# Review checklist

What a careful reviewer looks for in a diff. The judge reads this in full.
Skip anything the repo's own tools already enforce.

## A. Moves that lower the bar (always Must fix)

Search the diff for each. Any one is a failure until explained.

- A test deleted, skipped or marked as expected to fail.
- An assertion removed or loosened.
- A new comment or setting that silences the linter or type checker.
- A threshold lowered, a limit raised, an item added to an ignore list.
- A stub, a placeholder return, an empty error handler.
- A fixture or expected value edited so the code passes.

## B. Moves that hide a bug (Must fix unless the ticket asked for it)

- A new guard ("if this is empty, return") around a state that should never
  happen. Ask what produced the state.
- A retry added around something that fails.
- An error caught and dropped, or a narrow check widened to catch everything.
- A value clamped or defaulted to keep going.
- A silent fallback when configuration is missing.

## C. Does it match the ticket

Report in three lists, quoting the ticket line each time.

- **Missing:** asked for, not done or half done.
- **Not asked for:** in the diff, not in the ticket.
- **Looks wrong:** done, but not the way the ticket describes.

## D. Structure (judgement calls; say "possible")

- Nesting three or more levels deep.
- A function longer than about 50 lines, or one that does two jobs.
- A true/false parameter that switches behaviour.
- A name that does not say what the thing does or holds.
- The same logic in two places in non-test code.
- A function that reaches into another object's data more than its own.
- The same few values always passed together (they want one named type).
- A bare text or number standing in for a domain idea.
- The same branch-on-kind repeated in several places.
- One logical change forcing edits in many files.
- A layer that only passes calls along.
- Parameters or abstraction for needs the ticket does not have.
- State shared wider than it needs to be.

For each one, name the fix, not only the problem. Ask: does the suggested
change reduce complexity, or only move it?

## E. The 30-second question

Pick two values the change introduces. Can a new reader say where each comes
from and what can change it within 30 seconds? If not, say where they got lost.

## F. Tests

- Apply the two-edit check from `tests.md` to each new test.
- Are the edges covered: nothing, one, many, boundary, bad input?
- Is anything of ours untested? Is anything tested that is not ours?
- Repeated setup inside tests is fine. Do not ask for shared test helpers.

## G. Safety and data

- Any secret, or any value that looks like real personal data.
- A new field with no label (non-personal, personal, sensitive).
- Outside input used before it is checked.
- Personal values or whole rows in a log line or error message.
- A step that writes or sends with no answer to "what if it runs twice?"
- A step that cannot be undone, with no sign the user agreed.

## What does not count against this change

A problem that was already there before this diff. Give it one line under
"Already there" so it can become its own ticket. It lowers no score.
