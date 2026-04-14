from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from ..db import get_session
from ..models import Moodboard

router = APIRouter()


@router.get("/user/moodboard")
def get_mood(user_name: str = "Guest", session: Session = Depends(get_session)):
    row = session.exec(select(Moodboard).where(Moodboard.user_name == user_name)).first()
    return {"ok": True, "item": row}


@router.post("/user/moodboard")
def set_mood(payload: dict, session: Session = Depends(get_session)):
    user_name = payload.get("user_name") or "Guest"
    mood_key = payload.get("mood_key") or "festive"
    row = session.exec(select(Moodboard).where(Moodboard.user_name == user_name)).first()
    if not row:
        row = Moodboard(user_name=user_name, mood_key=mood_key)
        session.add(row)
    else:
        row.mood_key = mood_key
    session.commit()
    return {"ok": True, "item": row}

