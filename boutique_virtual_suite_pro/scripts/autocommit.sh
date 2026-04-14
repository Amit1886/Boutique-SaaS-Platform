#!/usr/bin/env bash
set -euo pipefail

msg="${1:-auto update}"

git add -A
git commit -m "$msg" || true
git push

