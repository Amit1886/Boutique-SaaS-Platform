from __future__ import annotations

from fastapi import Header, HTTPException

from .config import get_settings


def require_admin(x_admin_token: str | None = Header(default=None)) -> None:
    settings = get_settings()
    if not x_admin_token or x_admin_token.strip() != settings.admin_token:
        raise HTTPException(status_code=401, detail="admin token required")

