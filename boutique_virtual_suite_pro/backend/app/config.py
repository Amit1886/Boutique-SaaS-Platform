from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class Config:
    def __post_init__(self) -> None:
        load_dotenv()

    SECRET_KEY: str = os.environ.get("SECRET_KEY", "dev-secret")
    JWT_SECRET_KEY: str = os.environ.get("JWT_SECRET_KEY", "dev-jwt-secret")

    SQLALCHEMY_DATABASE_URI: str = os.environ.get("DATABASE_URL", "sqlite:///../database/bvp.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    CORS_ORIGINS: list[str] = [o.strip() for o in (os.environ.get("CORS_ORIGINS", "")).split(",") if o.strip()] or [
        "http://127.0.0.1:5173"
    ]

