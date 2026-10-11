#!/usr/bin/env bash
# Review a post/tool against profile.md. Usage: ./review.sh <case-dir>
# Put the post text, screenshots and any README snapshots in the case dir first.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
[ -f "$here/profile.md" ] || { echo "No profile.md: copy profile.example.md to profile.md and fill it in." >&2; exit 1; }
dir="$(cd "${1:?usage: ./review.sh <case-dir>}" && pwd)"
cd "$dir"
echo "The user's setup is in $here/profile.md. The case directory is $dir. Read the profile and every file in the case directory, then give your review." |
  claude -p --setting-sources "" --no-session-persistence --model claude-sonnet-5-5 --effort medium \
    --system-prompt-file "$here/prompts/v2.md" --tools Read,Glob --allowedTools Read,Glob --add-dir "$here"
