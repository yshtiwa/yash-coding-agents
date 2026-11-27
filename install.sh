#!/bin/sh
# Link every skill in this repo into ~/.claude/skills so all sessions see it.
here="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$HOME/.claude/skills"
for dir in "$here"/skills/*/; do
  name="$(basename "$dir")"
  target="$HOME/.claude/skills/$name"
  if [ -e "$target" ] && [ ! -L "$target" ]; then
    echo "skipped $name: a different skill with that name is already installed"
    continue
  fi
  ln -sfn "${dir%/}" "$target"
  echo "linked $name"
done
