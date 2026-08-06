#!/usr/bin/env bash
# Auto-commit + push new/changed source files as agents produce them.
cd "$(dirname "$0")/.."
DEADLINE=$(( $(date +%s) + ${1:-3000} ))
while [ "$(date +%s)" -lt "$DEADLINE" ]; do
  if [ -n "$(git status --porcelain)" ]; then
    NEW=$(git status --porcelain | grep '^??' | sed 's/^?? //' | tr '\n' ' ')
    MOD=$(git status --porcelain | grep '^ M' | sed 's/^ M //' | tr '\n' ' ')
    DESC=""
    [ -n "$NEW" ] && DESC="new: $(echo $NEW | tr ' ' '\n' | wc -l | tr -d ' ') file(s)"
    [ -n "$MOD" ] && DESC="$DESC updated: $(echo $MOD | tr ' ' '\n' | wc -l | tr -d ' ') file(s)"
    ./scripts/sync.sh "Research checkpoint — $DESC

$(git status --porcelain | sed 's/^/  /' | head -25)" 2>&1 | tail -1
  fi
  sleep 90
done
echo "autosync window ended"
