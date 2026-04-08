#!/usr/bin/env bash
set -euo pipefail

# PythonAnywhere deploy script (run in a Bash console on PythonAnywhere)
#
# Usage:
#   cd ~/boutique_ai_saas
#   bash scripts/pythonanywhere/deploy.sh

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$APP_DIR"

echo "[1/5] Ensure folders"
mkdir -p media staticfiles env logs

echo "[2/5] Pull latest code"
git pull --ff-only

echo "[3/5] Install deps"
if [[ ! -d ".venv" ]]; then
  python3 -m venv .venv
fi
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo "[4/5] Migrate + collectstatic"
python manage.py migrate --noinput
python manage.py collectstatic --noinput

echo "[5/5] Reload web app"
echo "On PythonAnywhere: click Reload on the Web tab, OR touch your wsgi file."
python -c "from pathlib import Path; Path('boutique_ai_saas/wsgi.py').touch()"

echo "Done."

