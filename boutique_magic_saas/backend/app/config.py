from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    base_dir: Path
    env: str
    database_url: str
    upload_dir: Path
    admin_token: str
    cors_origins: list[str]


def get_settings() -> Settings:
    base_dir = Path(__file__).resolve().parents[2]  # backend/
    load_dotenv(base_dir / ".env")

    env = os.environ.get("APP_ENV", "dev").strip()
    database_url = os.environ.get("DATABASE_URL", "sqlite:///../database/app.sqlite3").strip()
    upload_dir_raw = os.environ.get("UPLOAD_DIR", "../uploads").strip()
    upload_dir = (base_dir / upload_dir_raw).resolve()
    admin_token = os.environ.get("ADMIN_TOKEN", "change-me").strip()
    origins = [o.strip() for o in os.environ.get("CORS_ORIGINS", "").split(",") if o.strip()]
    return Settings(
        base_dir=base_dir,
        env=env,
        database_url=database_url,
        upload_dir=upload_dir,
        admin_token=admin_token,
        cors_origins=origins or ["http://127.0.0.1:5174"],
    )

