#!/bin/sh
# Tier 3: behaviour. Builds small throwaway repos in known states, runs /next
# in each, and checks it names the right skill. Costs tokens; takes a few minutes.
# Usage: evals/run-next-scenarios.sh
root="$(mktemp -d)"
g() { git -c user.name=eval -c user.email=eval@example.com "$@"; }

base() { # $1 = folder name. A tiny word counter with one passing test.
  d="$root/$1"; mkdir -p "$d/docs/agents" "$d/docs/tickets" "$d/src" && cd "$d" || exit 1
  g init -q
  cat > CLAUDE.md <<'X'
# Demo

A tiny word counter.

## Commands

- Run all tests: `sh test.sh`
- Run it: `sh src/count.sh FILE`

This repo does not use pull requests; work is committed on the main branch.
X
  cat > docs/agents/issue-tracker.md <<'X'
# Issue tracker

Tickets live in `docs/tickets/` as `NN-title.md`. Each has a `Progress:` line: ready, claimed, built, explained or done.
X
  cat > docs/agents/proof.md <<'X'
# Proof

## Launch
None needed.

## Journeys
- Count words: `sh src/count.sh README.md` prints a number.
X
  printf '#!/bin/sh\nwc -w < "$1"\n' > src/count.sh
  cat > test.sh <<'X'
#!/bin/sh
mkdir -p .agent-notes
printf 'a b c\nd\ne\n' > .agent-notes/_t.txt
[ "$(sh src/count.sh .agent-notes/_t.txt | tr -d ' ')" = "5" ] || exit 1
X
  printf '.agent-notes/\n' > .gitignore
  echo "# Demo" > README.md
}

ticket() { # $1 = progress, $2 = stakes, $3 = extra sections
  cat > docs/tickets/01-count-lines-flag.md <<X
# 01: Count lines with a flag

**Progress:** $1
**Kind:** new behaviour
**Stakes:** $2
**Blocked by:** nothing

## What to build

Today the tool prints the word count. After this, running it with \`-l\` before the file name prints the line count instead. Without \`-l\` it behaves as before.

## Done when

- [ ] With \`-l\`, a three-line file prints 3.
- [ ] Without \`-l\`, the word count is unchanged.

## How we will know it works

- Case: \`-l\` on a file with three lines gives 3.
- Case: no flag on a five-word file gives 5.
- Proof: \`sh src/count.sh -l README.md\`
$3
X
}
commit() { g add -A && g commit -q -m "chore: baseline"; }

change() { # a working change that matches the ticket, with a test for it
  printf '#!/bin/sh\nif [ "$1" = "-l" ]; then wc -l < "$2"; else wc -w < "$1"; fi\n' > src/count.sh
  cat >> test.sh <<'X'
[ "$(sh src/count.sh -l .agent-notes/_t.txt | tr -d ' ')" = "3" ] || exit 1
X
}
broken_change() { printf '#!/bin/sh\nwc -w < "$1"\nwc -l < "$1"\n' > src/count.sh; }
note() { mkdir -p .agent-notes && printf '%s\n' "$2" > ".agent-notes/$1"; }
SAID='
## What I can say about this

I added a -l flag. With it the tool counts lines, without it nothing changes.'

base a-no-tickets;        commit
base b-ready;             ticket ready normal;   commit
base c-claimed;           ticket ready normal;   commit; ticket claimed normal;   change
base d-built;             ticket ready normal;   commit; ticket built normal;     change; note 01-judged.txt "round 1, passed"
base e-explained;         ticket ready normal;   commit; ticket explained normal "$SAID"; change; note 01-judged.txt "round 1, passed"; note 01-explained.txt "explained"
base f-tests-fail;        ticket ready normal;   printf '#!/bin/sh\nexit 1\n' > test.sh; commit
base g-no-rules-file;     rm CLAUDE.md;          commit
base h-says-built-but-red; ticket ready normal;  commit; ticket built normal;     broken_change
base i-high-no-design;    ticket ready high;     commit; ticket claimed high
base j-high-no-security;  ticket ready high;     commit; ticket built high '
## Design

One script, one flag. No new parts.'; change; note 01-judged.txt "round 1, passed"

expect() { case "$1" in
  a-*) echo kickoff;; b-*) echo ticket;; c-*) echo build;; d-*) echo explain;;
  e-*) echo pr;; f-*) echo bugfix;; g-*) echo briefing;; h-*) echo build;;
  i-*) echo design;; j-*) echo security;; esac; }

for d in "$root"/*/; do
  name="$(basename "$d")"
  ( cd "$d" && claude -p "/next" --allowedTools "Read" "Glob" "Grep" "Bash(git status:*)" "Bash(git log:*)" "Bash(git branch:*)" "Bash(git diff:*)" "Bash(sh test.sh)" "Bash(ls:*)" "Bash(cat:*)" < /dev/null > "$root/$name.out" 2>&1 ) &
done
wait
pass=0; total=0
for d in "$root"/*/; do
  name="$(basename "$d")"; want="$(expect "$name")"; total=$((total + 1))
  line="$(grep -i "type this" "$root/$name.out" | head -1)"
  if printf '%s' "$line" | grep -Eq "/$want([^a-z]|\$)"; then pass=$((pass + 1)); echo "ok    $name -> /$want"
  else echo "MISS  $name: wanted /$want, got: ${line:-no 'Type this' line}"; fi
done
echo "next scenarios: $pass of $total (outputs in $root)"
[ "$pass" = "$total" ]
