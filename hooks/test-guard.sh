#!/bin/sh
# Check the git guard against commands it must block and commands it must allow.
here="$(cd "$(dirname "$0")" && pwd)"
run() {
  python3 -c 'import json,sys;print(json.dumps({"tool_name":"Bash","tool_input":{"command":sys.argv[1]}}))' "$1" \
    | python3 "$here/git-guard.py" 2>/dev/null
  echo $?
}
fail=0
while IFS= read -r c; do
  [ -z "$c" ] && continue
  [ "$(run "$c")" = 2 ] || { echo "MISSED: $c"; fail=1; }
done <<'BLOCK'
git commit -m x
cd r && git push origin main
git -C /tmp/x commit -am y
git reset --hard
git checkout .
git branch -D old
git branch -f main
git branch newone
git stash
FOO=1 git merge main
echo $(git push)
/usr/bin/git rebase main
bash -c "git push"
sh -c 'git commit -m x'
eval "git push"
xargs git push
timeout 5 git push
nohup git push
sudo -u me git push
env -i git push
! git push
if true; then git push; fi
true & git push
git update-ref x y
git rm a.py
git apply p.diff
git config alias.c commit
git commit-tree x
git filter-branch
gh pr create --title x
gh pr merge 3
git tag v1
git switch -c feat/x
git pull
git clean -fd
git restore .
BLOCK
while IFS= read -r c; do
  [ -z "$c" ] && continue
  [ "$(run "$c")" = 0 ] || { echo "WRONGLY BLOCKED: $c"; fail=1; }
done <<'ALLOW'
git status --short
git diff HEAD
git log --oneline -5
git add src/a.py
git branch --show-current
git branch
git stash list
uv run pytest -q
grep -r commit docs
git show HEAD
git tag
git tag -l
legit commit
digit commit
git remote -v
git config --get user.name
git rev-parse HEAD
gh pr view 3
gh pr list
(git diff HEAD -- . ':(exclude)docs/tickets'; git status --short) | shasum
git ls-files
ALLOW
[ "$(printf 'x' | python3 "$here/git-guard.py" 2>/dev/null; echo $?)" = 2 ] || { echo "bad input passed"; fail=1; }
[ $fail = 0 ] && echo "git guard: all checks passed" || echo "git guard: FAILED"
exit $fail
