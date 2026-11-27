# Yash's coding agents

Eleven Claude Code skills that take a piece of work from an idea to a change
a reviewer can accept. The agent writes the code. The person decides, checks,
explains it back, and runs every git command.

They merge the best practices of three public skill packs with a lead
engineer's own rules. See [DECISIONS.md](DECISIONS.md) for what was taken
from each and why.

## Methodology

### The problem it solves

An AI agent can now write most of the code. Two things still go wrong:

1. **It builds the wrong thing.** The person thought the agent understood;
   it did not.
2. **It says it is done when it is not.** Tests pass, but the real thing was
   never run, or a test was quietly weakened to go green.

And a third, for anyone who is not a full-time programmer: **the person
cannot answer for code they did not write**, so review turns into guesswork.

The pack is built around closing those three gaps, in that order.

### Three roles, kept apart

| Role | Does | Never does |
|---|---|---|
| **The person** | Decides what to build, answers questions, explains the change back, runs every git command | Types code, ranks technical options they cannot judge |
| **The builder agent** | Looks up facts, writes tests and code, runs the real thing, fixes findings | Commits, pushes, merges, or marks its own work as reviewed |
| **The judge agent** | Reads the change fresh and tries to break it | Sees the builder's reasoning, changes files, starts other agents |

Splitting builder and judge matters most. An author checks what it *meant*
to build. A fresh reader checks what is actually there.

### Seven principles

1. **Agree before building.** Every ticket starts with questions, asked in
   small rounds, each with a recommended answer. There is no question limit;
   the limit is scope. Facts are looked up by the agent, never asked.
2. **Small, whole slices.** A ticket is a thin path through every stage, not
   one layer, and about 100 changed lines. The first ticket is ugly but runs
   end to end; later tickets widen it.
3. **A test first, and a test that can fail.** One test, then the code for
   it, then the next. After the tests pass, the agent breaks the code on
   purpose once to show a test catches it. A check never seen failing
   proves nothing.
4. **Proof is the real thing running.** Tests passing is not proof, and
   neither is the agent's own summary. The real command runs on real
   (synthetic) input, the output is shown, and the verdict is one of three:
   VERIFIED, NOT VERIFIED, or INCONCLUSIVE. Inconclusive is not a pass.
5. **Judged by a fresh agent, findings before scores.** The judge lists what
   is wrong, each with a file, a line and the rule it breaks, then scores
   from those findings. The builder fixes each one or shows the evidence
   that it is wrong; nothing is silently dropped. Three rounds at most.
6. **The person can answer for it.** Before anything is committed, the agent
   walks through the change in plain English and pictures, then asks the
   questions a reviewer would ask. Code the person cannot follow is treated
   as a fault in the code, and simplified.
7. **Every correction becomes a check.** A mistake caught once should fail
   automatically next time: first by changing the code's shape, then a lint
   rule, then a test, then a pre-commit check. A note in a rules file is the
   last resort, because nothing fails when an agent ignores it.

### The loop for one ticket

```
              ┌──────────────────────── /next tells you where you are ───┐
              v                                                          │
/kickoff ──> /ticket ──> /build ─────────────────────> /explain ──> /pr ─┘
 plan the     agree the   1 test first, one case       walk-through  final gate,
 work, cut    check:      2 break it on purpose        and four      commit message,
 tickets      cases,      3 tidy                       reviewer      PR text, the
              proof,      4 search the diff for        questions     commands for
              limits        a lowered bar                            you to run
                          5 run the real thing
                          6 fresh judge, up to 3 rounds
```

Bugs take a side road: `/bugfix` reproduces the failure with one command
before any theory, writes three to five testable guesses, finds the cause
rather than the symptom, then rejoins the loop at `/explain`.

### The bars a change must clear

- **The ticket's own check:** did we build what was asked?
- **A standing definition of done**, the same for every change: tests that
  fail without the change, the whole suite green, edge cases handled, no
  lowered bar, within the size rule, docs still true, no secrets or real
  personal data, a written way to undo it, explained back.
- **The judge:** every score 8 or more out of 10, and no "must fix" open.

### What it deliberately does not do

- Let the agent commit, push or merge. The person stays in charge of what
  enters the codebase.
- Run many agents in parallel, or overnight. One builder and one judge per
  ticket keeps cost and risk small.
- Skip planning. The person may not be able to read code as a spec, so the
  plan is written in words first.

The full reasoning, including where the three source packs disagree and
which way this pack went, is in [DECISIONS.md](DECISIONS.md).

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

### Swapping out another skill pack in one project

If a project already uses another pack with similar names (for example Matt
Pocock's skills), turn that pack off for that project only. Create
`.claude/settings.local.json` in the project:

```json
{
  "enabledPlugins": {
    "mattpocock-skills@claude-plugins-official": false
  }
}
```

Use the plugin's own name, as listed by `/plugin`. Then replace the project's
`## Agent skills` section in `CLAUDE.md` with a short note naming these skills,
and add `.agent-notes/` to the project's ignore file. Start a new session.
Existing tickets keep working: these skills add a `Progress:` line beside any
status line already there.

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
