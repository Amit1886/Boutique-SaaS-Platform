#!/usr/bin/env bash
set -euo pipefail

MSG="${1:-auto update}"

git add -A
if [[ -z "$(git status --porcelain)" ]]; then
  echo "No changes to commit."
  exit 0
fi

TS="$(date +'%Y-%m-%d %H:%M:%S')"
git commit -m "${MSG} (${TS})"
git push origin main

