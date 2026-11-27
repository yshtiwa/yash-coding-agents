# What this pack takes from each source, and why

Every file in three skill packs was read before this was written: Matt
Pocock's skills (about 190 files), pstack (about 150 written files; about 400 code and
test-fixture files inside its `statechart` skill were skipped), and Addy
Osmani's agent-skills (about 230 files). This page records the choices so a
reviewer can disagree with them.

## Taken from each

**Matt Pocock's skills** (the question: do we agree on what we are building?)

- Questions in rounds through a tree of decisions; "yes" accepts the
  recommendation; facts are looked up, decisions are asked. → `kickoff`, `ticket`
- Specs and tickets describe behaviour, never file paths. Tickets are thin
  end-to-end threads with blockers. → `kickoff`
- Where the tests will sit is agreed before building. → `ticket`
- Named kinds of bad test, and "one test, then its code". → `standards/tests.md`
- Review on two separate questions: does it match the ticket, does it meet
  the standards. Twelve classic code smells as judgement calls. → `build`
- Debugging starts with one command that fails; ranked theories before
  testing. → `bugfix`
- Handoff between sessions; one ticket per session. → `handoff`, `next`
- The reviewer holds the standards; mechanical rules become checks. → `lessons`

**pstack by Lauren Tan** (the question: can you prove it works?)

- Proof is the real thing run on real input. A written recipe for running
  it, proven once. → `proof`, `build`
- Three verdicts, with "inconclusive" not a pass; claims labelled measured
  or inferred. → `standards`
- "A check you have never seen fail proves nothing": break the code on
  purpose once. → `build`
- The two-edit test for tests. → `standards/tests.md`
- Root cause: is the state that broke allowed to exist? Stop after two
  failed fixes and test the shared assumption. → `bugfix`
- A judge blocks only on what it can show; its bar is the written bar. → `build`
- Corrections become checks, strongest enforcer first. → `lessons`
- The 30-second reader question; moves that hide a bug. → `review-checklist`

**agent-skills by Addy Osmani** (the question: did we follow the whole process?)

- The excuses table. → `standards`
- A standing definition of done, separate from each ticket's check. → `standards`
- "Guard the bar": search the diff for skipped tests and silenced checks. → `build`, `pr`
- The judge gets the work and the requirement, never the author's
  reasoning; findings carry a severity. Findings are checked, not obeyed. → `build`
- Interview: say what you think they want and how sure you are; stop when
  you can predict the next three answers; only a clear yes counts. → `kickoff`
- Privacy: label each field; scan that prints file names only; AI output
  is outside input. Logging rules. → `standards/data-and-privacy.md`
- Risk and "how to undo this" in every pull request. → `pr`

## Where the sources disagree, and what this pack does

| Question | The sources | This pack |
|---|---|---|
| Who runs git? | All three let the agent commit; pstack lets it push and merge | The user runs every git command. Not negotiable here. |
| Plan first? | Matt and Addy: yes. pstack: no, prototype instead | Plan first. The user cannot read code as a spec. Small experiments settle what talking cannot. |
| Ask the user? | pstack: never block on the human | Ask about intent and anything that cannot be undone. Look up facts. |
| Score or findings? | Matt and pstack refuse a number; the lead engineer wants 8 out of 10 | Both. Findings first, scores from the findings, and a nit can never fail a change. |
| Obey the judge? | The first draft said "do not argue". All three say check each finding | Fix it, or show the evidence that disproves it. Everything not fixed is shown to the user. |
| How big is a change? | Addy: 300 lines is fine. Matt: one session's worth | About 100 non-test lines; split past 150. The lead engineer's number. |
| Small functions? | Matt and pstack warn against many tiny pass-through functions | Small functions that each do one named job. A function that only forwards goes. |
| Tests at which level? | Matt: one high place only. The lead engineer: unit tests of our logic | Unit tests of our own logic at function boundaries, plus one real run. |
| Always test first? | pstack: skip when a test is costly | Always, for our own logic. Pure wiring is covered by the real run and said so. |
| Comments? | pstack deletes almost all | One short docstring per function. No comment that repeats code or tells history. |
| A rule in CLAUDE.md? | All three: weakest option | Last resort, after structure, lint, test and pre-commit check. |
| Safe default or error? | Addy allows a fallback | Our own mistake stops the run loudly. |

## Left out on purpose

- Running many agents at once, several AI vendors, agents that merge their
  own work overnight. These need a large budget and long-earned trust.
- Anything for websites: browsers, accessibility, page speed, components.
- TypeScript, React and JavaScript tooling. The pack stays language-neutral.
- Formal proof tools. Launch and rollout practices for large products.
- Public open-source repo upkeep: triage labels, issue forms, release tools.

## Open questions for the lead engineer

1. Is 8 out of 10 with cited findings the bar you want, or findings only?
2. Small functions: is "one named job; no pure pass-throughs" your rule?
3. Comments: one docstring per function, or fewer?
4. Commit format, and squash or keep each commit?
5. Does this repo need the optional git guard turned on?
