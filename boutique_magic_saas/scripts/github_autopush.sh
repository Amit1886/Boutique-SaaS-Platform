#!/usr/bin/env bash
set -euo pipefail

repo="${1:-}"
if [[ -z "$repo" ]]; then
  echo "Usage: ./scripts/github_autopush.sh https://github.com/<user>/<repo>.git"
  exit 1
fi

git init
git add .
git commit -m "Boutique Magic SaaS Full Build" || true
git branch -M main
git remote remove origin 2>/dev/null || true
git remote add origin "$repo"
git push -u origin main

