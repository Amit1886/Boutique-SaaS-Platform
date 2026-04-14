import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # .../boutique_magic_saas
BACKEND = ROOT / "backend"

sys.path.insert(0, str(BACKEND))

env_path = BACKEND / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        if not line.strip() or line.strip().startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())

from app.wsgi import application  # noqa: E402

