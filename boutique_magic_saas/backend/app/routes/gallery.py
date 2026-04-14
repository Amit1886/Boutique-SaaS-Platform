from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from ..db import get_session
from ..models import SavedLook

router = APIRouter()


@router.get("/gallery/looks")
def list_looks(session: Session = Depends(get_session)):
    rows = session.exec(select(SavedLook).order_by(SavedLook.id.desc())).all()
    return {"ok": True, "items": rows}


@router.post("/gallery/save")
def save_look(payload: dict, session: Session = Depends(get_session)):
    obj = SavedLook(**payload)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return {"ok": True, "item": obj}

