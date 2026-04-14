from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from .config import get_settings


def ensure_upload_dir() -> Path:
    settings = get_settings()
    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    return settings.upload_dir


async def save_upload(file: UploadFile, *, prefix: str) -> str:
    upload_dir = ensure_upload_dir()
    suffix = Path(file.filename or "").suffix.lower() or ".bin"
    name = f"{prefix}_{uuid4().hex}{suffix}"
    out = upload_dir / name
    content = await file.read()
    out.write_bytes(content)
    # return relative path from upload dir base
    return name

