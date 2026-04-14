#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BACKEND="$ROOT_DIR/backend"

cd "$BACKEND"
source "${VENV_PATH:-$HOME/.virtualenvs/bvp}/bin/activate"
pip install -r requirements.txt
flask --app run.py db upgrade
flask --app run.py seed

echo "Backend deployed. Reload your web app in PythonAnywhere Web tab."

