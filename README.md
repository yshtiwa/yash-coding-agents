# Yash's coding agents

Six small Claude Code skills that take one ticket from "not started" to "ready
for review". They sit on top of whatever planning skills a repo already uses.

| Type this | What it does |
|---|---|
| `/next` | Looks at the repo and says the one next step and what to type |
| `/ticket` | Opens the next ticket in line: questions until nothing is unclear, then a written check added to the ticket. `/ticket 05` picks a specific one |
| `/build` | Test first, code, real run as proof, fresh judge scores it |
| `/explain` | Plain-English walk-through, then three reviewer questions |
| `/pr` | Size and standards gate, commit message, PR description, commands |
| `/standards` | The engineering standards the others read |

The order for one ticket: `/ticket` → `/build` → `/explain` → `/pr`. Lost at any
point: `/next`.

## Install

```bash
./install.sh
```

This links each skill into `~/.claude/skills/`, so every Claude Code session on
this machine has them. Editing a file here changes the skill; start a new
session to be sure it is picked up.

## Rules these skills keep

- The agent writes the code. The person explains it back before it is committed.
- The agent never commits, pushes or merges. It hands over the commands.
- A repo's own `CLAUDE.md` beats anything written here.
