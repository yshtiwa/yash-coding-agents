# Interfaces and changing them

An interface is everything a caller must know to use something correctly:
the inputs and outputs, and also the order of calls, the errors it can
raise, the settings it needs.

## Designing one

- **Write the contract before the code:** inputs, outputs, errors.
- **One way to report errors,** the same everywhere. Never a mix of raising,
  returning nothing and returning an error value.
- **Check input at the edge:** from a user, an outside service, a file, a
  setting. Inside, trust the checked value.
- **Different shapes for what goes in and what comes out.**
- **Assume every visible behaviour will be relied on,** including the order
  of results and the wording of errors. Show only what you mean to keep.
- **Design so it can grow by adding.** A new optional field is safe. A
  changed type or a removed field breaks someone.
- **One version at a time.** Extend the thing; do not fork it.
- **Plan how it will be removed** while designing it.
- **State open questions.** Do not invent a requirement to fill a gap.

## Operations that change something

- **Safe to repeat.** Give each operation a key that comes from what is
  being done (the ID of the file, the claim, the order), never from the
  attempt (a random value, the time).
- **Claim the key in one step.** "Check, then act" lets two runs both pass
  the check.
- **The same key with different contents fails loudly.**
- **Three outcomes, not two:** done, failed, unknown. A timeout tells you
  nothing. Record the intent before calling out, and check on "unknown"
  instead of retrying blind.
- **No queue delivers exactly once** across a crash. Design for "at least
  once".
- **Leftovers can be told apart.** Anything a stopped run leaves behind (a
  lock, a temporary file, a half-written record) must be recognisable as
  stale by the next run.

## Changing something others depend on

Never change it in place. Three separate changes, each one small, each with
tests green and a written way back:

1. **Add** the new form beside the old.
2. **Move** every user over, in batches. Old and new both work throughout.
3. **Remove** the old form, alone, only after a search shows nothing uses it.

For stored data: add the new field; write both; copy old records across in
small batches; switch reading to the new field; stop writing the old; drop
the old in a later change. The dropping step is never bundled with anything.

## Removing something

- Check that nothing uses it by measuring, not by assuming.
- If a replacement is needed, build and prove it first.
- The owner of the thing being retired does the moving work.
- Remove the code, its tests, its docs and its settings together.
- Code with no owner that others still use gets an owner or a retirement
  plan. It does not get new features.
