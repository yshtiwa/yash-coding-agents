# Release checklist

Mark each line done, not needed (with why), or blocked.

## The change

- All pipeline gates are green on the exact version being released.
- It has been reviewed and approved by a person.
- No debug output, leftover notes to self, or switched-off checks.
- Errors are handled; nothing is swallowed.

## Safety

- The security skill has been run for anything touching outside input,
  personal data, logins, money or a new dependency.
- The dependency audit is clean of reachable serious findings.
- No secret is in the code, the pipeline settings or the logs.

## Running it

- Settings for the target environment are set from files in the repo, not
  typed from memory.
- Changes to stored data are ready and each has a tested way back.
- There is a health check that says "ready to use", not only "running".
- Logs and error reports are arriving from the target environment.

## Signals

- The two to four questions someone will ask when this breaks are written.
- Each can be answered from a named log event or a count.
- Every log line carries a run ID and which entry point wrote it.
- An alert, if any, is about something a user would feel, says what to
  check first, and has been fired once on purpose.
- A forced failure was found from the logs alone.

## The way back

- What would trigger it.
- The exact steps.
- How to check it worked.
- Who is told.
- What happens to data written in between.
- Roughly how long it takes.

## People

- Those whose work changes have a short note: what changes, when, what to do.
- A walk-through exists when a screen or routine changes.
- Someone is watching for the first hour, and knows it.

## Switches

- New risky behaviour is behind a switch, off by default.
- The switch has an owner and a date to remove it.
- Both states are tested. Switches are not nested inside each other.

## Excuses

| The excuse | The answer |
|---|---|
| "It works on the test system." | Real use has different data and edge cases. |
| "No switch needed for this." | A switch is the cheapest way back there is. |
| "We'll watch it later." | Then you learn from complaints. |
| "Going back is admitting failure." | Leaving it broken is the failure. |
| "The pipeline is slow; skip it this once." | Speed it up. Skipped checks are where breaks hide. |
| "The test is flaky; run it again." | A flaky test is hiding a real bug. |
| "They want it out today." | A deadline cuts scope, not checks. |
