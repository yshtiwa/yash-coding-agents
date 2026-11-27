#!/bin/sh
# Tier 1: free, instant checks on the shape of every skill.
cd "$(dirname "$0")/.." || exit 1
fail=0
say() { echo "FAIL: $1"; fail=1; }
for dir in skills/*/; do
  name="$(basename "$dir")"
  f="$dir/SKILL.md"
  [ -f "$f" ] || { say "$name has no SKILL.md"; continue; }
  [ "$(sed -n 1p "$f")" = "---" ] || say "$name: no frontmatter"
  [ "$(sed -n 2p "$f")" = "name: $name" ] || say "$name: name line does not match its folder"
  desc="$(sed -n 3p "$f")"
  case "$desc" in description:*) ;; *) say "$name: line 3 is not the description" ;; esac
  len=$(printf '%s' "$desc" | wc -c)
  [ "$len" -le 520 ] || say "$name: description is $len characters (limit 520)"
  case "$desc" in *"Use when"*|*"Use as"*|*"Use for"*|*"Use once"*|*"Use after"*|*"Read before"*) ;; *) say "$name: description does not say when to use it" ;; esac
  lines=$(wc -l < "$f")
  [ "$lines" -le 210 ] || say "$name: $lines lines (limit 210)"
  if [ "$name" != "standards" ]; then
    grep -q "^## Finish" "$f" || say "$name: no Finish section"
    grep -q "Type this" "$f" || say "$name: Finish does not tell the user what to type"
  fi
  # every file a skill points at must exist
  for ref in $(grep -o '`[A-Za-z./-]*\.md`' "$f" | tr -d '`' | sort -u); do
    case "$ref" in
      ../*) [ -f "$dir/$ref" ] || say "$name: points at missing $ref" ;;
      */*|NN-*|CLAUDE.md|AGENTS.md|GLOSSARY.md|README.md|SKILL.md|handoff.md|proof.md|checks.md) ;;
      *) [ -f "$dir/$ref" ] || [ -f "skills/kickoff/$ref" ] || say "$name: points at missing $ref" ;;
    esac
  done
  # every /skill named in a "Type this" line must exist
  for cmd in $(grep "Type this" "$f" | grep -o '/[a-z][a-z]*' | sort -u); do
    [ -d "skills/${cmd#/}" ] || say "$name: Type this names $cmd, which is not a skill"
  done
done
# no em dashes anywhere (the character is written here as an escape so this file passes)
if git ls-files | xargs grep -l "$(printf '\342\200\224')" 2>/dev/null | grep -q .; then say "an em dash is present"; fi
[ $fail = 0 ] && echo "structure: all checks passed ($(ls skills | wc -l | tr -d ' ') skills)" || echo "structure: FAILED"
exit $fail
