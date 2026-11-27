# Data, privacy and safe operation

## Personal data

- **Label every field when it is added:** non-personal, personal (names,
  contact details, identifiers), or sensitive (health, money, anything that
  could harm someone if leaked). Write the label, why the field is kept, and
  how long, next to where the field is defined.
- **Synthetic data only** in tests, fixtures, logs, error messages, commit
  messages and anything shown to an AI model. If data looks real, stop and
  tell the user before doing anything else.
- **Know what is synthetic.** Fixture folders carry a short note naming how
  the data was generated. Data with no such note is treated as real.
- **Sending personal data to a hosted AI model is sharing it.** It needs a
  written agreement. Without one, it does not go.
- **Before a commit, scan every changed and new file** for secrets and for
  personal-looking values (ID patterns, the repo's own sensitive field
  names). The scan prints file names and line numbers only, never the values.
- **A leaked secret is changed first,** then removed from the code.

## Input from outside

- **Check it once, where it enters:** shape, required fields, ranges, allowed
  values. Use an allow-list. After that, inner code uses the checked value
  and does not check again.
- **A value we do not recognise is refused,** flagged and set aside. Never
  mapped to a default.
- **A file written by another process or person is outside input,** even if
  an earlier stage of ours wrote it somewhere shared.
- **A file's name or extension proves nothing** about its contents.
- **Never build a command, a query or a file path by joining text with
  input.**
- **Output from an AI model is outside input.** Check its shape before use.
  Check every number, date and name it produced against the source text.
  A model's confidence is not evidence.

## Errors

- A gap in our own configuration stops the run with a message naming the
  missing thing and where it belongs.
- One bad item from outside is recorded and skipped; the run continues and
  the summary counts what was skipped.
- No error is swallowed. No empty handler, no ignored return value.
- A narrow error check is never widened into a catch-all.
- When nothing could be read, say "could not check", never "no problems".

## Safe to run twice

- Ask of every step that writes or sends: **what happens if this runs twice?
  What if it stops halfway?**
- Compare what is there with what should be there, and apply only the
  difference.
- Write to a temporary file, then rename it into place.
- An operation that sends something outside records its intent first, and
  has three outcomes: done, failed, unknown. Unknown is checked, not retried
  blind.

## Deleting, moving, overwriting

- The target must sit under an allowed folder, at least one level inside it,
  and be something this program created.
- If any check fails, log it and stop. Never fall back to a wider path.
- Anything destructive supports a dry run that shows what it would do.

## Steps that cannot be undone

Deleting data, changing a stored format, sending anything outside, adding a
new kind of sensitive data, adding an outside service. Each needs the user's
yes first, and a written way back.

Changing a format or a widely used name goes in three separate changes:
add the new form beside the old; move every user over; remove the old form
last. Tests stay green between each.

## Logs

- Before adding logs, write the two to four questions someone will ask when
  this breaks. Log what answers them.
- A log line is a named event with a few fields, not a sentence.
- Every line carries a run ID, and which entry point wrote it.
- Levels mean something fixed. "Error" means a promise broke and someone may
  need to act.
- Log counts and identifiers. Never whole rows, never personal values.
- Check the logging by forcing a failure and finding it from the logs alone.

## Dependencies

- Each new one needs a stated reason. Check its name for look-alikes.
- One committed lock file. Versions pinned.
- For a library call you have not used in this repo before, read the pinned
  version's documentation. Mark anything unverified as "not checked".

## Speed

Measure first. Change one thing. Measure again. No gain means revert.
