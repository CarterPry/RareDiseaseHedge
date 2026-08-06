#!/usr/bin/env bash
# Commit and push whatever has changed. Usage: scripts/sync.sh "message"
set -euo pipefail
cd "$(dirname "$0")/.."
MSG="${1:-checkpoint}"
# Refuse to push if anything looks like a credential slipped in.
if git diff --cached --name-only >/dev/null 2>&1; then git add -A; fi
if grep -rInE 'sk-ant-[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{30,}|-----BEGIN [A-Z ]*PRIVATE KEY-----' \
     --exclude-dir=.git . >/dev/null 2>&1; then
  echo "ABORT: possible credential in working tree. Not pushing." >&2
  grep -rInE 'sk-ant-[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{30,}' --exclude-dir=.git . >&2 || true
  exit 1
fi
if git diff --cached --quiet; then echo "nothing to commit"; exit 0; fi
git -c user.name="Carter Pry" -c user.email="carterpry@gmail.com" \
    commit -q -m "$MSG

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
git push -q origin main
echo "pushed: $(git log --oneline -1)"
