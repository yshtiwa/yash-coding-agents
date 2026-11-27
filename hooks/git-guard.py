#!/usr/bin/env python3
"""Block git commands that the user, not the agent, is meant to run.

A Claude Code PreToolUse hook for the Bash tool. It reads the tool call as
JSON on standard input. Exit code 2 blocks the call and shows the message to
the agent. If the input cannot be read, it blocks: failing closed is safer.

It looks for the word `git` anywhere in the command, including inside quoted
text handed to `bash -c`, `eval` and the like. That means a command that only
mentions a blocked git command in text is blocked too. That is on purpose: a
wrong block costs one message; a wrong pass can lose work.
"""

import json
import os
import re
import sys

# git subcommands that only read, or only stage. Everything else is blocked.
READ_ONLY = {
    "status", "diff", "log", "show", "add", "blame", "ls-files", "ls-tree",
    "rev-parse", "rev-list", "describe", "shortlog", "grep", "cat-file",
    "check-ignore", "remote", "fetch", "help", "version", "--version",
    "merge-base", "name-rev", "for-each-ref", "show-ref", "diff-tree",
    "whatchanged", "reflog", "count-objects",
}
# subcommands that are read-only only in some forms
BRANCH_WRITE_FLAGS = {"-d", "-D", "-m", "-M", "-f", "-c", "-C", "--delete", "--move", "--force", "--copy"}
TAG_WRITE_FLAGS = {"-d", "-a", "-s", "-f", "--delete", "--force"}
GIT_OPTIONS_WITH_VALUE = {"-C", "-c", "--git-dir", "--work-tree", "--namespace"}
GH_BLOCKED = {("pr", "create"), ("pr", "merge"), ("pr", "close"), ("repo", "delete"), ("release", "create")}

MESSAGE = (
    "Blocked: the user runs this command, not the agent. "
    "Give the user the exact command in a code block and stop. "
    "If the command only mentioned git in text, say so and rephrase it."
)


def words_of(command: str) -> list[str]:
    """Split a shell command into bare words, looking inside quotes too."""
    return [w for w in re.split(r"[\s;&|()`{}<>\"'$!]+", command) if w]


def git_call_blocked(args: list[str]) -> bool:
    """True when the words after `git` name a command the user must run."""
    while args and args[0].startswith("-") and args[0] != "--version":
        args = args[2:] if args[0] in GIT_OPTIONS_WITH_VALUE else args[1:]
    if not args:
        return False
    sub, rest = args[0], args[1:4]
    if sub == "branch":
        named = [a for a in rest if not a.startswith("-")]
        return bool(BRANCH_WRITE_FLAGS & set(rest)) or bool(named)
    if sub == "tag":
        named = [a for a in rest if not a.startswith("-")]
        return bool(TAG_WRITE_FLAGS & set(rest)) or bool(named)
    if sub == "stash":
        return not (rest and rest[0] in {"list", "show"})
    if sub == "config":
        return not (rest and rest[0] in {"--get", "--list", "-l", "--get-all"})
    if sub == "remote":
        return bool(rest) and rest[0] not in {"-v", "show", "get-url"}
    return sub not in READ_ONLY


def is_blocked(command: str) -> bool:
    """True when any git or gh call in the command is one the user must run."""
    words = words_of(command)
    for i, word in enumerate(words):
        name = os.path.basename(word)
        if name == "git" and git_call_blocked(words[i + 1 : i + 8]):
            return True
        if name == "gh" and tuple(words[i + 1 : i + 3]) in GH_BLOCKED:
            return True
    return False


def main() -> int:
    try:
        call = json.load(sys.stdin)
        command = call["tool_input"]["command"]
        if not isinstance(command, str):
            raise TypeError("command is not text")
    except (json.JSONDecodeError, KeyError, TypeError, AttributeError):
        print("Blocked: the git guard could not read the tool call.", file=sys.stderr)
        return 2
    if is_blocked(command):
        print(MESSAGE, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
