---
name: handoff
description: Save where the work stands so a new session can pick it up without losing anything. Use when the user says "pause", "hand off", "I'm stopping for today", when a session has grown long in the middle of a ticket, or before switching to a new session mid-work.
---

# Handoff

A new session starts with nothing. What is not written down is lost. The
best time for a new session is between tickets, after `/pr`; then no
handoff is needed. Use this when work must stop in the middle.

## Write the note

Save it as `.agent-notes/handoff.md`. Make sure `.agent-notes/` is in the
repo's ignore file, so the note survives a restart and is never committed. Keep it short. Point to files;
do not copy their contents. Replace any secret or personal value.

```
# Handoff, <date>

Ticket: <title and path>
Goal, in one sentence:
Step reached: <ticket | build step n | judge round n | explain | pr>

Done and verified: <what, and the command that showed it>
Done, not verified: <what>
Tried and dropped: <what, and why; so it is not tried again>
Decisions made this session: <point to the ticket's Decisions table>
Waiting on a person: <who, for what>

Files changed, uncommitted: <list from git status>
Next action: <the one next thing>
Type this to continue: <the skill>
Traps: <anything that wasted time>
```

Tell the user the path of the note. Do not paste its text.

## Pick up

When a session starts from a handoff note:

1. Read the note, then the ticket it points to.
2. Run `git status` and the test suite. The note is a claim about an earlier
   moment; the files are the truth.
3. Do not redo work the note says is done. Do re-run its proof before
   building on it.
4. Count only approvals that are written in a file. If the note says the
   user agreed to something and no file shows it, ask again.
5. When the work is back under way, delete the note.

## Finish

```
Saved: .agent-notes/handoff.md
Next step: start a new session and continue from the note.
Type this in the new session: /next
```
