from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from ..db import get_session
from ..models import UXFlags

router = APIRouter()


@router.get("/uxflags")
def uxflags(session: Session = Depends(get_session)):
    rows = session.exec(select(UXFlags).order_by(UXFlags.key.asc())).all()
    return {"ok": True, "items": rows}

