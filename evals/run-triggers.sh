#!/bin/sh
# Tier 2: does each kind of request reach the right skill?
# One call to Claude Code, which must have these skills installed.
# Usage: evals/run-triggers.sh   (costs a little; takes about a minute)
here="$(cd "$(dirname "$0")" && pwd)"
skills="$(ls "$here/../skills" | tr '\n' ' ')"
work="$(mktemp -d)"
n=0
# drop blank lines, and mix the order so neighbours do not give the answer away
grep -v '^[[:space:]]*$' "$here/triggers.tsv" | awk 'BEGIN{srand(7)}{print rand() "\t" $0}' | sort -n | cut -f2- > "$work/rows"
{
  echo "Below are numbered requests a user might type. For each, name the ONE skill you would"
  echo "invoke first, choosing only from this list: $skills"
  echo "or answer none if no skill in that list fits. Judge by each skill's description as it"
  echo "is installed in this session. Do not invoke any skill. Reply with one line per request,"
  echo "exactly in the form 'N: name', and nothing else."
  echo
  while IFS="$(printf '\t')" read -r prompt want; do
    n=$((n + 1)); echo "$n. $prompt"; echo "$want" >> "$work/want"
  done < "$work/rows"
} > "$work/prompt"
(cd "$work" && claude -p "$(cat "$work/prompt")" < /dev/null > "$work/got" 2>/dev/null)
total=$(wc -l < "$work/want" | tr -d ' '); pass=0; i=0
while IFS= read -r want; do
  i=$((i + 1))
  got="$(grep -E "^$i: " "$work/got" | head -1 | sed -E "s/^$i: *//; s/[^a-z]//g")"
  if [ "$got" = "$want" ]; then pass=$((pass + 1)); else
    echo "MISS $i: wanted $want, got ${got:-nothing}: $(sed -n "${i}p" "$work/rows" | cut -f1)"
  fi
done < "$work/want"
echo "triggers: $pass of $total routed to the expected skill"
[ "$pass" = "$total" ]
