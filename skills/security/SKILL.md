---
name: security
description: Check a design or a change for security and privacy problems. Use when work takes input from outside, handles personal or sensitive data, logins or permissions, money, secrets, a new dependency, an outside service, or an AI model; before a release; or when the user asks "is this safe?" or "security review". Not for changes with none of those.
---

# Security

Five minutes of thinking here prevents the flaws no later fix can patch.
Read `../standards/data-and-privacy.md` first, and `checklist.md` beside
this file at step 4. You change no product code in this skill; you report.

## 1. Where trust changes hands

List every place data enters from somewhere this code does not control: a
user, a file, another program, an outside service, a setting, an AI model's
output. Trust follows **who wrote the value**, not how it arrived: a file
on a shared drive is outside input even if our own earlier step wrote it.

*Done when* each entry point is named with the file and function that
receives it. If you cannot name them, the work is not ready to secure.

## 2. What is worth protecting

Name the things an attacker or an accident could harm: personal and
sensitive records, money, secrets and keys, the ability to change or delete
data, the system staying up.

## 3. How it could go wrong

For each entry point, ask six questions. Write one line for each that applies.

| Ask | Meaning |
|---|---|
| Can someone pretend to be someone else? | Identity is not checked, or can be faked |
| Can data be changed on the way? | Input or stored data altered unnoticed |
| Can someone deny what they did? | No record of who did what |
| Can data leak? | To logs, errors, another user, an outside service, an AI model |
| Can it be made to stop working? | Huge input, endless loop, a locked resource |
| Can someone do more than they should? | Reaching another's records, or admin actions |

Then write the **abuse case** beside each use case ("a user uploads a file"
/ "a user uploads a file built to break the reader"). The abuse case
becomes a test, written first.

## 4. Check the change

Walk `checklist.md` against the diff or the design. Report each finding with
the file and line, why it matters in one plain sentence, and the fix.

## 5. Sort by who decides

- **Always, no question:** check all outside input at the edge; never build
  a command, query or path by joining text with input; secrets only from
  the environment; nothing sensitive in logs or errors; run the dependency
  audit before a release.
- **Needs the user's yes:** storing a new kind of sensitive data; a new
  outside service; a new login or permission scheme; a new dependency;
  sending any data to a hosted AI model.
- **Never:** a secret in code or history; a protection switched off for
  convenience; outside data run as code; internals shown to a user in an
  error.

## 6. If a secret has leaked

Change the secret first. Then remove it from the code. Then tell the user
that history may still hold it. Never paste the value anywhere.

## 7. Write it down

In the ticket, add or replace `## Security`: the entry points, the abuse
cases, each finding with its status (open or fixed), and each decision the
user said yes or no to.

Save the result in `.agent-notes/` as `NN-security.txt`: the word `clean` or
`open`, and the diff fingerprint (standards section 6).

If there is an open Must fix, set the ticket back to `Progress: claimed`.
The fix goes through `/build`, where each open finding becomes a case.
After that, this skill re-checks only the fix, once. If a Must fix is
still open then, stop with a decision card.

For a design with no code yet (called from the `design` skill), do steps
1 to 3 and 5 only, and write them into the ticket's `## Design` section.

## Finish

```
Security check: <what was checked>
Entry points: <each one, with the file that receives it>
Must fix: <findings with file:line and the fix, or "none">
Should fix: <or "none">
Needs your yes: <decisions for the user, or "none">
Not checked: <what could not be checked and why, or "nothing">
Next step: <open Must fix: "fix these" | clean, after a build: "explain it back" | otherwise "carry on">
Type this: </build | /explain | /next>
```

Findings that change product code go through `/build` like any other change.
