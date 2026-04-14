from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from ..db import get_session
from ..models import FestivalTheme

router = APIRouter()


@router.get("/theme/festival")
def current_festival(session: Session = Depends(get_session)):
    today = date.today()
    rows = session.exec(select(FestivalTheme)).all()
    active = None
    for t in rows:
        if t.start_date <= today <= t.end_date:
            active = t
            break
    return {"ok": True, "active": active, "all": rows}

