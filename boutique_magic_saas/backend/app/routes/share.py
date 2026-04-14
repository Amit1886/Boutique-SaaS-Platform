from __future__ import annotations

from datetime import datetime
from urllib.parse import quote

from fastapi import APIRouter

router = APIRouter()


@router.post("/look/share")
def share(payload: dict):
    user_name = payload.get("user_name") or "Guest"
    look_name = payload.get("look_name") or "My Look"
    price = payload.get("price") or ""
    text = f"{look_name} | {user_name} | {price} | {datetime.now().strftime('%Y-%m-%d')}"
    wa = f"https://wa.me/?text={quote(text)}"
    return {"ok": True, "whatsapp_url": wa, "text": text}

