# Yash's coding agents

Eleven Claude Code skills that take a piece of work from an idea to a change
a reviewer can accept. The agent writes the code. The person decides, checks,
explains it back, and runs every git command.

They merge the best practices of three public skill packs with a lead
engineer's own rules. See [DECISIONS.md](DECISIONS.md) for what was taken
from each and why.

## The path

```
/kickoff  ->  /ticket  ->  /build  ->  /explain  ->  /pr
 plan the      open one     test, code,   you can      package it
 work          ticket       prove, judge  answer for   for review
                                          it
```

Lost at any point: type `/next`.

| Type this | What it does |
|---|---|
| `/next` | Looks at the repo and says the one next step and what to type |
| `/kickoff` | Plans new work: questions, a short spec if needed, small tickets |
| `/ticket` | Opens the next ticket: questions until nothing is unclear, then a written check |
| `/build` | Test first, code, prove the tests can fail, run the real thing, fresh judge |
| `/bugfix` | Reproduce first, find the cause, fix it, prove it |
| `/explain` | Walk-through in plain English, then the questions a reviewer would ask |
| `/pr` | Final gate, commit message, description, the commands; handles review comments |
| `/proof` | Writes and refreshes the repo's recipe for running the real thing |
| `/handoff` | Saves where things stand so a new session can pick up |
| `/lessons` | Turns a correction into a check that fails next time |
| `/standards` | The engineering standards the others read |

## Install

```bash
./install.sh
```

This links each skill into `~/.claude/skills/`, so every Claude Code session
on this machine has them. Editing a file here changes the skill; start a new
session to be sure it is picked up. On another machine: clone, then run the
same command.

`hooks/` holds an optional guard that blocks the agent from running git
commands that are yours. It is off by default. See `hooks/README.md`.

## Rules these skills keep

- The agent writes the code. The person explains it back before it is committed.
- The agent never commits, pushes or merges. It hands over the commands.
- Tests passing is not proof. The real thing is run and the output shown.
- A fresh agent that did not write the code judges it, up to three rounds.
- A repo's own `CLAUDE.md`, and its reviewer's written rules, beat anything here.

## What a repo needs

Nothing to start: `/kickoff` creates what is missing. The skills use:

| File | Used for |
|---|---|
| `CLAUDE.md` | The repo's own rules and commands |
| `docs/agents/issue-tracker.md` | Where tickets live (default `docs/tickets/`; written by `/kickoff`) |
| `.agent-notes/` | Working notes: handoff, build logs, learning notes. Git-ignored |
| `docs/agents/proof.md` | How to run the real thing (written by `/proof`) |
| `docs/agents/checks.md` | Which rule is enforced by which check (written by `/lessons`) |
| `GLOSSARY.md`, `docs/adr/` | The project's words and its decisions |

## Credits

Ideas from three MIT-licensed packs, rewritten in original words:
[Matt Pocock's skills](https://github.com/mattpocock/skills),
[pstack by Lauren Tan](https://github.com/cursor/plugins/tree/main/pstack) and
[agent-skills by Addy Osmani](https://github.com/addyosmani/agent-skills).
