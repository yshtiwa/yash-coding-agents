# Security checklist

Walk each block that applies. Skip a block only by saying why it does not
apply.

## Input

- Every outside input is checked at the edge against a written shape:
  required fields, lengths, ranges, allowed values. Allow-list, not block-list.
- Code after the edge uses only the checked value.
- No command, query or file path is built by joining text with input.
- A file's contents are checked when they matter; its name proves nothing.
  File size is capped.
- A reply from an outside service is checked like any other input.
- An unknown value is refused, not mapped to a default.

## Identity and permission (when there are users or logins)

- Every protected action checks who is asking.
- Every access to a record checks that this person may see **this** record,
  not only that they are logged in.
- Keys and service accounts hold the least permission that works.
- Checks done in a browser or client are repeated on the server.

## Secrets

- Read from the environment. An example settings file with placeholders is
  committed; the real one is on the ignore list.
- None in code, tests, logs, error messages, commit messages or prompts.
- A missing required secret stops the program at start with a clear message.
- The automated pipeline holds no production secrets.

## Personal and sensitive data

- Each field is labelled non-personal, personal or sensitive, with why it
  is kept and for how long.
- Only what is needed is collected.
- None in logs, errors, analytics or test fixtures.
- Deleting one person's data reaches copies, caches and backups.
- Nothing personal goes to a hosted AI model or outside service without a
  written agreement.
- Output files and temporary files that hold personal data: it is written
  down where they go, who can read them, and when they are deleted. They
  are protected in storage and in transit.

## Deleting, moving, overwriting

- The target is under an allowed folder, at least one level inside it, and
  was created by this program.
- On any failed check it stops. It never falls back to a wider path.
- A dry run shows what it would do.

## AI model features

- Model output is checked for shape before use, and never passed to a
  command, a query, a file path or anything that runs it.
- Every number, date and name a model produced is checked against the source.
- Text that enters the model's context from outside can carry instructions.
  The system prompt is not a lock. Keep secrets and other people's data out.
- Tools the model can call are limited; destructive ones need a person's yes.
- Calls are capped in size, rate and depth.

## Dependencies

- One lock file, committed. Versions pinned.
- The ecosystem's own audit tool is run before each release. Findings are
  sorted by whether the weak code can actually be reached.
- Each finding left unfixed has a written reason and a date to look again.
- A new package: checked for a look-alike name, its age and who owns it.
- Scripts a package runs at install time are read before they are allowed.
- An audit tool's forced fixes are never applied automatically.

## Errors and logs

- Errors shown to a user say what to do, not how the inside works.
- Every error path is handled; nothing is swallowed.
- Under failure the system refuses rather than lets through.
- There is a record of who did what for actions that matter.

## Excuses

| The excuse | The answer |
|---|---|
| "It's an internal tool." | Internal tools get broken into; attackers pick the weakest door. |
| "We'll add security later." | Later is far harder than now. |
| "Nobody would attack this." | Automated scanners attack everything. |
| "The framework handles it." | It gives tools, not guarantees. |
| "It's only a prototype." | Prototypes become the product. |
| "It's just text from the model." | That text can be a command. |
| "The audit passed." | Audits know only published problems. |
| "Collect it now, we may need it." | Data you do not hold cannot leak. |
