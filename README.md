# Yash Coding Skills

Eighteen skills for Claude Code that take a piece of software work from an
idea to a change a reviewer can accept. The AI agent writes the code. You
decide what gets built, check it, explain it back, and run every command
that changes the codebase.

You do not need to be a programmer to use them. Every skill ends by telling
you the next thing to type.

**In this guide**

1. [Start here](#1-start-here)
2. [Words you will see](#2-words-you-will-see)
3. [Which skill do I use?](#3-which-skill-do-i-use)
4. [How big is my change?](#4-how-big-is-my-change)
5. [The main path, step by step](#5-the-main-path-step-by-step)
6. [Every skill in detail](#6-every-skill-in-detail)
7. [I'm stuck](#7-im-stuck)
8. [Files the skills keep in your repo](#8-files-the-skills-keep-in-your-repo)
9. [Methodology](#9-methodology)
10. [How the skills are tested](#10-how-the-skills-are-tested)
11. [Install, swap and extras](#11-install-swap-and-extras)
12. [Credits and license](#12-credits-and-license)

---

## 1. Start here

1. Install once (see [section 11](#11-install-swap-and-extras)).
2. Open your project in Claude Code.
3. Type `/next`.

`/next` looks at your project and tells you the one thing to do now and
exactly what to type. Whenever you are unsure, type `/next` again.

A normal day looks like this:

```
/next      ->  "Ticket 03 is ready. Type /ticket"
/ticket    ->  asks you questions, writes down how we will know it works
/build     ->  writes the tests and the code, runs it for real, gets it judged
/explain   ->  walks you through it and asks what a reviewer would ask
/pr        ->  checks everything once more and hands you the commands to run
/next      ->  "Start a new session, then type /ticket"
```

## 2. Words you will see

| Word | What it means |
|---|---|
| **Repo** | The folder holding a project's code and its history. |
| **Agent** | The AI doing the work in Claude Code. |
| **Session** | One conversation with the agent. A new session remembers nothing unless it is written in a file. |
| **Ticket** | One small, written piece of work: what to build and how we will know it works. |
| **Test** | A small program that checks one piece of code does what it should. |
| **Test suite** | All the tests together. "Green" means all pass; "red" means one fails. |
| **Lint / formatter** | Tools that check the code's style and tidy its layout. |
| **Diff** | The exact lines that changed. |
| **Commit** | A saved snapshot of changes, with a message saying what and why. |
| **Branch** | A separate line of work, so unfinished changes do not disturb the main one. |
| **Pull request (PR)** | A request to add your branch's changes to the main code, which someone reviews first. |
| **Review** | Another person (or a fresh agent) reading the change before it is accepted. |
| **CI / pipeline** | Checks that run automatically on every change, on a server. |
| **Deploy / release** | Putting a change where real users get it. |
| **Proof** | Running the real program on real (made-up) input and showing the output. Stronger than tests alone. |
| **Judge** | A second, fresh agent that did not write the code and tries to find what is wrong with it. |
| **Synthetic data** | Made-up data that looks real. The only kind allowed in tests and examples. |
| **Slice** | A batch of related tickets that together deliver one working feature. |
| **Spec** | A short written description of what a piece of work must do, agreed before building. |
| **Sub-agent** | A second agent the main one starts for one job, such as the judge. It starts with no memory of the conversation. |
| **Dependency** | Code written by someone else that the project uses. A **dependency audit** checks those for known security problems. |
| **Pre-commit check** | A check that runs on your computer just before a commit is saved, and stops it if something is wrong. |
| **Switch (feature flag)** | A setting that turns a new behaviour on or off without changing the code, so it can be released switched off. |
| **Stored format** | The shape in which data is saved to a file or database. Changing it can break anything that reads the old shape. |
| **Stakes** | How much a mistake in this change would cost. It decides how much checking the change gets. |

## 3. Which skill do I use?

| I want to... | Type |
|---|---|
| Know what to do next | `/next` |
| See the whole plan and how far along it is, as a picture | `/visualize` |
| Plan a new feature or a new project | `/kickoff` |
| Start the next piece of planned work | `/ticket` |
| Decide how something should be built before building it | `/design` |
| Have the agent write the code for an open ticket | `/build` |
| Fix a typo, some wording, a rename, one setting | `/quick` |
| Fix something that is broken or a failing test | `/bugfix` |
| Understand what was just built | `/explain` |
| Save the work and send it for review | `/pr` |
| Deal with review comments or failing checks on a pull request | `/pr` |
| Check a change is safe (security, privacy) | `/security` |
| Make something faster | `/speed` |
| Set up automatic checks, or put a change into real use | `/release` |
| Write down how to run the real program, for every later ticket | `/proof` |
| Stop for the day in the middle of something | `/handoff` |
| Make sure a mistake cannot happen again | `/lessons` |
| Stop the agent guessing about this repo | `/briefing` |
| Read the rules every change must meet | `/standards` |

## 4. How big is my change?

The process should cost about what a mistake would cost. The agent sizes
the change for you; this table is so you can check it.

| Size | What it looks like | Path |
|---|---|---|
| **Tiny** | A typo, wording, a rename that changes no behaviour, one setting. About 20 lines. No new logic. | `/quick` then `/pr` |
| **Normal** | New or changed logic that fits the way the code is already shaped. | `/ticket` → `/build` → `/explain` → `/pr` |
| **High stakes** | Touches personal or sensitive data, money, logins, a stored file format, an outside service, something that cannot be undone, or a new shape other code will rely on. | `/ticket` → `/design` → `/build` → `/security` → `/explain` → `/pr` |

If it is between two sizes, use the bigger one. You can always ask for the
bigger path. Only you can ask for the smaller one.

## 5. The main path, step by step

### `/ticket`: agree what will be built

- **You type:** `/ticket` (the next one in line) or `/ticket 05` (a specific one).
- **The agent:** says the ticket back in its own words, reads the code
  around it, then asks you questions in small groups. Each question comes
  with its suggested answer, so "yes" is enough when you agree.
- **You are asked:** only things that need your judgement. It looks up
  facts itself. Technical choices you cannot judge it makes itself and
  marks "for the reviewer to check".
- **You get:** a section in the ticket called "How we will know it works":
  the test cases, the real command that will prove it, what must not
  change, and what is left out on purpose.
- **It stops when:** you say a clear yes to its summary.

### `/build`: write it, prove it, judge it

- **You type:** `/build`. Then you mostly watch.
- **The agent, in order:**
  1. writes one test, sees it fail, writes the code to pass it, repeats;
  2. breaks the code on purpose once, to show a test catches it;
  3. tidies up, only inside this ticket's code;
  4. searches its own changes for shortcuts (skipped tests, silenced checks);
  5. runs the real program and compares the output with the ticket;
  6. hands the change to a fresh judge agent, and fixes what it finds, for
     up to three rounds.
- **You get:** a short report: tests passed, proof VERIFIED, the judge's
  scores, anything not fixed and why, and the one part worth your attention.
- **It stops and asks you when:** the proof fails, the judge will not pass
  it after three rounds, the change is getting too big, or something cannot
  be undone. It gives you a short "decision card": the choice, its pick,
  what changes, the evidence, the risk.

### `/explain`: make it yours

- **You type:** `/explain`.
- **The agent:** shows the change as a picture built up one part at a time,
  walks through each file, and points out the three lines a reviewer is
  most likely to ask about.
- **You are asked:** four questions, one at a time. If you get one wrong,
  it tells you the answer straight away. It is not an exam.
- **You get:** two or three sentences in the ticket, in your own words,
  that you can say in review.
- **Say "you lost me"** at any point and it explains again more simply.

### `/pr`: package it for review

- **You type:** `/pr`.
- **The agent:** runs every check one last time, scans for secrets and
  personal data, writes the commit message and the pull request
  description, and saves both to files.
- **You get:** the exact commands to run, in order. You run them; the agent
  never does.
- **Later, when the reviewer comments:** type `/pr` again. It handles each
  comment, then suggests `/lessons`.

## 6. Every skill in detail

### `/next`
- **Use it when** you start a session, finish a step, or feel lost.
- **What happens:** it reads the project's state (changed files, tickets,
  tests, open pull requests) and picks the one next step.
- **You get:** "Where you are / Next step / Type this / Why".

### `/visualize`
- **Use it when** you want the big picture: every slice, every ticket,
  what is done and what comes next. Good after `/kickoff` and at any point
  you lose track.
- **What happens:** it reads the ticket files, checks their labels against
  what is really in the repo, and draws one page: a progress bar for the
  whole project, one for each slice, and a map of tickets from left to
  right in the order they unblock each other. Green is done, amber is in
  progress, blue can start now, grey is waiting.
- **You get:** `.agent-notes/overview.html`, a page that opens in any
  browser with no network. Run the skill again to refresh it.
- **On a shared board:** if you ask, and a connector for a whiteboard tool
  such as Miro is set up, it can draw the same picture there. It tells you
  exactly what it will send and waits for your yes.
- **It changes nothing** in the project.

### `/kickoff`
- **Use it when** starting a new feature, slice or project, before any
  ticket exists.
- **Not for** work that already has tickets.
- **What happens:** it reads the project, tells you what it thinks you want
  and how sure it is, then asks questions in small rounds until nothing is
  assumed. It writes a short spec if the work is three tickets or more, and
  cuts the work into small tickets, riskiest first.
- **You get:** a list of tickets, each one small and able to be shown
  working on its own, plus a "not doing" list.
- **Next:** `/ticket`.

### `/ticket`
See [section 5](#5-the-main-path-step-by-step). **Not for** tiny changes
(use `/quick`) or bugs (use `/bugfix`).

### `/design`
- **Use it when** a ticket adds a new part, a new shape of data, a new way
  for two parts to talk, a stored format, or changes something other code
  relies on.
- **Not for** changes that stay inside one function.
- **What happens:** it traces what the change touches, names the data
  first, sketches **two** different ways to build it, picks one by six
  fixed tests (for example: one owner for each piece of state; one way to
  do each thing; callers need to know as little as possible), and asks what
  it could break. For high-stakes work it also asks the security questions
  now, before any code exists.
- **You get:** a "Design" section in the ticket with a small picture, the
  choice, and the option turned down with the reason.
- **Next:** `/build`, or `/ticket` again if the design changed what the
  ticket must check.

### `/build`
See [section 5](#5-the-main-path-step-by-step).

### `/quick`
- **Use it when** the change is tiny: a typo, wording, a rename, one setting.
- **Not for** anything that adds or changes logic, or touches data,
  security, money or a stored format.
- **What happens:** it checks the change really is tiny, makes it, runs the
  tests, the linter and the formatter, and shows you the diff with two or
  three sentences on why it is safe.
- **If it turns out not to be tiny,** it stops and sends you to `/ticket`
  (or `/bugfix` if a test broke).
- **Next:** `/pr`.

### `/bugfix`
- **Use it when** a test fails, a run crashes, or something behaves wrongly.
- **What happens:** before any theory, it gets **one command that fails**
  on this exact bug. It shrinks the failure, writes three to five testable
  guesses, and finds the cause, not just the symptom. It fixes it, proves
  the original failure is gone, and then has the fix judged like any change.
- **You get:** the cause with file and line, the fix, the proof, and the
  cheap signal that would have shown the problem sooner.
- **Next:** `/explain`.

### `/explain`
See [section 5](#5-the-main-path-step-by-step).

### `/pr`
See [section 5](#5-the-main-path-step-by-step). Small supporting changes
(docs, a new check, the proof recipe, a `/quick` change) take a lighter
lane with no judge and no explain-back.

### `/security`
- **Use it when** work takes input from outside, handles personal or
  sensitive data, logins, money, secrets, a new dependency, an outside
  service, or an AI model. Also before a release.
- **What happens:** it lists every place data enters from outside, names
  what is worth protecting, asks six plain questions of each entry point
  (can someone pretend to be someone else, change data, deny what they did,
  leak data, stop it working, do more than they should), and walks a
  checklist against the change.
- **You get:** findings with file and line, sorted into must fix, should
  fix, and decisions that need your yes. They are written into the ticket.
- **It changes no code.** Fixes go back through `/build`, and the fix is
  then re-checked once.

### `/speed`
- **Use it when** something is measurably slow or costly, or a ticket
  states a speed target.
- **Not for** a hunch that something might be slow.
- **What happens:** it measures first (at least five runs), finds the one
  biggest cost, changes one thing, and measures again the same way. A
  change that is not clearly faster is undone.
- **You get:** before and after numbers, what was kept, what was tried and
  undone, and a check that stops it getting slow again.
- **Next:** `/explain`.

### `/release`
- **Use it when** the repo has no automatic checks, when a change is about
  to reach real users, or when the pipeline is slow or failing.
- **Not for** packaging one change for review (that is `/pr`).
- **What happens:** it sets up checks that run on every change (style,
  tests, build, dependency audit), cheapest first, and proves they work by
  making them fail once. Before a release it walks a checklist: a written
  way back, a switch to turn risky behaviour off, the people affected told
  in advance, signals to tell whether it is working.
- **It never deploys.** Steps only a person can do are handed to you as a
  numbered list.

### `/proof`
- **Use it** once when a repo first has something that runs, and again at
  the end of each batch of tickets.
- **What happens:** it writes `docs/agents/proof.md`: how to start the
  program, how to tell it is healthy, the three to five things a user does
  most with the exact command and the result that proves each, and how to
  clean up. Then it runs the recipe once to prove it.
- **Why:** so every later ticket can run the real thing the same way.

### `/handoff`
- **Use it when** you must stop in the middle of a ticket, or a session has
  grown long.
- **What happens:** it writes a short note: the goal, the step reached,
  what is done and checked, what was tried and dropped, and the next action.
- **Next:** start a new session and type `/next`. It finds the note.
- **Not needed** between tickets. Just start a new session.

### `/lessons`
- **Use it** after review comments, after a ticket that went badly, or at
  the end of a batch of tickets.
- **What happens:** it lists what went wrong and, for each, picks the
  strongest thing that would stop it next time: change the code's shape, a
  lint rule, a test, a pre-commit check, and only last a written rule. It
  proves each new check fails on the old mistake.
- **You decide** which to accept. Nothing changes without your yes.

### `/briefing`
- **Use it when** starting in a new repo, or when the agent keeps breaking
  conventions, inventing commands or forgetting things.
- **What happens:** it sets up or trims the repo's rules file (`CLAUDE.md`)
  to about two screens: what the project is, the commands, the layout, the
  limits, one example of good code. It tests the file by giving it to a
  fresh agent.

### `/standards`
- **Use it when** you want to read the rules themselves.
- **What it is:** the engineering standards every other skill reads: how
  code is shaped, what a good test is, how errors and data are handled,
  privacy, what counts as proof, the definition of done, and the common
  excuses with the answer to each.

## 7. I'm stuck

| What is happening | What to do |
|---|---|
| I do not know what to do | `/next` |
| I have lost track of the whole plan | `/visualize` |
| I do not understand what the agent just said | Say "you lost me". It repeats it more simply. |
| The agent asks me something I cannot judge | Say so. It should make the call itself and mark it "for the reviewer to check". |
| The agent wants to commit or push for me | Say no. It should hand you the command. To enforce this, turn on the git guard ([section 11](#11-install-swap-and-extras)). |
| Tests are red | If a ticket is in progress, that is normal: `/build` continues. Otherwise `/bugfix`. |
| The judge keeps failing the change | After three rounds the agent must stop and give you a decision card. Usually the ticket is too big or the approach is wrong. |
| The change got much bigger than expected | Ask the agent to split the ticket. The limit is about 100 lines of non-test code. |
| The session is long and the agent is getting muddled | `/handoff`, then a new session, then `/next`. |
| The agent keeps getting this repo's conventions wrong | `/briefing` |
| The same mistake keeps coming back | `/lessons` |
| A command the agent gave me failed | Paste the exact error back to it. Do not retype from memory. |
| Something in the data looks real | Stop. Tell the agent. Nothing else until it is dealt with. |
| A secret (a key or password) ended up in the code | Tell the agent. It will tell you to change the secret first, then remove it. |
| The reviewer asked for changes | `/pr` |
| I have to stop right now | `/handoff` if mid-ticket. Otherwise just stop. |
| A skill did something odd | Note which one and what it did. Skills are plain text files in `skills/`; they can be fixed. |

## 8. Files the skills keep in your repo

You never have to create these. `/kickoff` and the other skills make them
as they are first needed.

| File or folder | What it is | Committed? |
|---|---|---|
| `CLAUDE.md` | The repo's rules and commands, read at the start of every session | Yes |
| `docs/agents/issue-tracker.md` | Says where tickets live (default `docs/tickets/`) | Yes |
| `docs/tickets/NN-title.md` | One file per ticket, with a `Progress:` line | Yes |
| `docs/agents/proof.md` | How to run the real program (from `/proof`) | Yes |
| `docs/agents/checks.md` | Which rule is enforced by which check (from `/lessons`) | Yes |
| `GLOSSARY.md` | The project's words, one meaning each. Created the first time a term is settled | Yes |
| `docs/adr/` | Decision records: choices that are hard to reverse. Created with the first such decision | Yes |
| `.agent-notes/` | Working notes: handoff, build logs, what you have learned, the overview picture | No (ignored) |

A ticket's `Progress:` line moves through: `ready` → `claimed` → `built` →
`explained` → `done`.

## 9. Methodology

### The problem

An AI agent can write most of the code. Three things still go wrong:

1. **It builds the wrong thing.** You thought it understood. It did not.
2. **It says it is done when it is not.** Tests pass, but the real program
   was never run, or a test was quietly weakened.
3. **You cannot answer for code you did not write,** so review becomes
   guesswork.

The skills are built to close those three gaps.

### Three roles, kept apart

| Role | Does | Does not |
|---|---|---|
| **You** | Decide what to build, answer questions, explain the change back, run the commands that change the codebase | Type code, or rank technical options you cannot judge |
| **The builder agent** | Looks up facts, writes tests and code, runs the real thing, fixes findings | Commit, push, merge, or review its own work |
| **The judge agent** | Reads the change fresh and tries to break it | See the builder's reasoning, change files, start other agents |

An author checks what it meant to build. A fresh reader checks what is
actually there. That is why builder and judge are separate.

### Eight principles

1. **Agree before building.** Questions first, in small rounds, each with a
   suggested answer. No limit on questions; the limit is scope.
2. **Small, whole slices.** A ticket is a thin path through every stage,
   about 100 changed lines, that can be shown working on its own.
3. **A test first, and a test that can fail.** After the tests pass, the
   code is broken on purpose once to show a test catches it.
4. **Proof is the real thing running.** The verdict is VERIFIED, NOT
   VERIFIED or INCONCLUSIVE. Inconclusive is not a pass.
5. **Judged by a fresh agent.** Findings first, each with a file, a line
   and the rule broken; scores come from the findings. Three rounds at most.
6. **You can answer for it.** A normal or high-stakes change is not
   committed until you have had it explained and been asked what a
   reviewer would ask. (A tiny change is shown to you as a diff instead.)
7. **Every correction becomes a check.** A mistake caught once should fail
   automatically next time. A written rule is the last resort.
8. **Effort matches the stakes.** A typo takes the short path; a change to
   stored data takes design and a security check as well.

### What "done" means

For a normal or high-stakes change, three bars, all required. A tiny change
skips the judge and the explain-back but keeps every other check.

- **The ticket's own check:** did we build what was asked?
- **The standing definition of done:** new tests that fail without the
  change; all tests, lint and format green; edge cases handled; no lowered
  bar; within the size rule; docs still true; no secrets or real personal
  data; a written way to undo it; explained back.
- **The judge:** every score 8 or more out of 10, and no "must fix" open.

### What it covers

| Stage of software work | Skill |
|---|---|
| Requirements and planning | `/kickoff`, `/ticket` |
| Seeing the plan and its progress | `/visualize` |
| Architecture and interface design | `/design` |
| Building and testing | `/build`, `/quick` |
| Verifying it really works | `/build` step 5, `/proof` |
| Code review | the judge inside `/build`; `/pr` for human review |
| Debugging | `/bugfix` |
| Security and privacy | `/security`, `standards/data-and-privacy.md` |
| Speed | `/speed` |
| Automatic checks, release, monitoring, changing stored data safely | `/release`, `design/interfaces.md` |
| What the agent is told, and keeping sessions clear | `/briefing`, `/handoff` |
| Learning from mistakes | `/lessons` |

### What it deliberately leaves out

- Agents that commit, push or merge on their own.
- Many agents working at once, or overnight.
- Tools specific to one programming language. The skills work for any.

Where the three source packs disagree and which way these skills went is
written up in [DECISIONS.md](DECISIONS.md).

## 10. How the skills are tested

Tests for the skills themselves live in `evals/`.

| Check | What it shows | Cost |
|---|---|---|
| `evals/check-structure.sh` | Every skill is well-formed and every "type this" points at a real skill | Free, instant |
| `evals/run-triggers.sh` | 59 sample requests each reach the right skill, or no skill | One short agent call |
| `evals/run-next-scenarios.sh` | In ten small made-up repos, each in a known state, `/next` names the right step | Ten agent calls |
| `hooks/test-guard.sh` | The git guard blocks and allows the right commands | Free, instant |

The latest results are in [evals/RESULTS.md](evals/RESULTS.md), with what
has **not** been tested yet. These skills are new and have one user. Expect
rough edges, and treat a skill doing something odd as a bug to report.

## 11. Install, swap and extras

### Install

```bash
git clone https://github.com/yshtiwa/yash-coding-skills.git
```

```bash
cd yash-coding-skills && ./install.sh
```

This links each skill into `~/.claude/skills/`, so every Claude Code
session on that computer has them. Start a new session afterwards. To
update later, run `git pull` in the folder; the links pick up the changes.

### Using another agent tool

Each skill is a folder with a `SKILL.md` file, which is the open format
most agent tools read. Tools that install from a GitHub repo's `skills/`
folder should be able to use it, but that has not been tested here. Some
steps name Claude Code features (a "fresh sub-agent", the `claude` command
in the evals); other tools need their own equivalent.

### Swapping out another skill pack in one project

If a project already uses another pack, turn that pack off for that project
only. Create `.claude/settings.local.json` in the project:

```json
{
  "enabledPlugins": {
    "NAME-OF-THE-OTHER-PACK": false
  }
}
```

Use the pack's own name, as listed by `/plugin`. Start a new session.
Existing tickets keep working: these skills add a `Progress:` line beside
any status line already there.

### The git guard (optional)

The skills ask the agent never to commit, push or merge. The guard in
`hooks/` turns that request into a rule the agent cannot break. It is off
by default. See [hooks/README.md](hooks/README.md).

## 12. Credits and license

Ideas from three MIT-licensed skill packs, rewritten in original words:
[Matt Pocock's skills](https://github.com/mattpocock/skills),
[pstack by Lauren Tan](https://github.com/cursor/plugins/tree/main/pstack) and
[agent-skills by Addy Osmani](https://github.com/addyosmani/agent-skills).
[DECISIONS.md](DECISIONS.md) says what came from each.

Released under the [MIT License](LICENSE). Use it, change it, share it.
