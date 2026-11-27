# Optional: the git guard

The skills tell the agent never to commit, push or merge. That is a request.
This hook makes it a rule: Claude Code runs it before every shell command and
blocks the git commands that are yours to run.

It is **not installed by default**, because it would also block agents in
your other projects that are meant to commit. Turn it on per project.

## Turn it on for one project

Add this to that project's `.claude/settings.json` (create the file if it is
not there). Use the real path to this repo on your machine.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$HOME/Documents/Claude Projects/yash-coding-agents/hooks/git-guard.py\""
          }
        ]
      }
    ]
  }
}
```

Start a new session afterwards.

## What it blocks

Every git command that changes history, branches or files: `commit`, `push`,
`pull`, `merge`, `rebase`, `reset`, `revert`, `checkout`, `switch`, `restore`,
`clean`, `stash`, `rm`, `apply`, creating or deleting branches and tags, and
changing git settings. Also `gh pr create`, `gh pr merge` and `gh pr close`.

It looks inside quoted text too, so `bash -c "git push"` is caught.

## What it allows

Commands that only read or stage: `git status`, `diff`, `log`, `show`, `add`,
`branch` (listing), `tag` (listing), `stash list`, `gh pr view`.

## Limits

- It reads the command text. A git command inside a script file that the
  agent runs is not seen.
- A command that only mentions a blocked git command in text (for example
  searching the docs for "git commit") is blocked too. That is on purpose.
- If the hook cannot read its input, it blocks.

Run `hooks/test-guard.sh` to check it against about 60 sample commands. It
is a guard, not a guarantee.
