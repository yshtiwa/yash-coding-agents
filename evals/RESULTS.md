# Eval results

Run on 26 November 2026 with Claude Code 2.1.311 (Claude Code), default model for the account.
Whether a skill is chosen for a request varies from run to run, so treat
these as a snapshot, not a guarantee.

## What passed

| Check | Result |
|---|---|
| `check-structure.sh` | All checks passed, 18 skills |
| `hooks/test-guard.sh` | All checks passed, about 60 commands |
| `run-next-scenarios.sh` | 10 of 10: `/next` named the right skill in every made-up repo |
| `run-triggers.sh` | 56 of 59 requests reached the expected skill |
| `visualize/build_overview.py` | Run on a real 12-ticket plan and on a mixed-state copy of it; both pictures were checked by eye |

In the scenarios, `/next` also did two things worth noting. Given a ticket
marked "built" while the tests were red, it refused to trust the label and
sent the work back to `/build`. Given a change that did not do what its
ticket said, it stopped and asked for a decision instead of moving on.

## What missed

| Request | Expected | Got | What it means |
|---|---|---|---|
| "set up CI for this repo" | `release` | no skill | Missed in three runs out of three |
| "add a pipeline that runs the tests on every pull request" | `release` | no skill | Same cause |
| "commit this" | `pr` | no skill | Passed in two earlier runs, missed in one |

For plain-English requests about CI, the agent does not reliably pick
`release` on its own. **Type `/release` directly.** Typing a skill's name
always works; these misses are only about the agent choosing a skill
unprompted.

## What has not been tested

- No skill other than `/next` has been run end to end by these evals. The
  others ask questions and write code, which needs a person or a much larger
  test rig.
- `/design`, `/security`, `/release`, `/speed`, `/briefing` and `/quick`
  are new and have not yet been used on real work.
- `/visualize`: the drawing script has been run for real, but the skill's
  own steps (checking labels against the repo, the shared-board option)
  have not. Plans with more than one slice have not been drawn.
- Nothing here measures whether the skills produce better code than no
  skills at all.
- Only Claude Code has been tried. Other agent tools are untested.
- The pressure cases (a deadline, "just do it") are written into the
  standards but are not tested.

## How to add to these

A new skill should arrive with at least three requests that should reach it
and two that should not, added to `triggers.tsv`. A change to `/next`'s
table should arrive with a scenario in `run-next-scenarios.sh`.
