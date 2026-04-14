import os
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]  # .../boutique_virtual_suite_pro
backend_root = project_root / "backend"

sys.path.insert(0, str(backend_root))

# Load .env if present
env_path = backend_root / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        if not line.strip() or line.strip().startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())

from app import create_app  # noqa: E402

application = create_app()

