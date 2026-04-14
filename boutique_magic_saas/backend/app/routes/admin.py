from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from ..db import get_session
from ..models import FestivalTheme, UXFlags
from ..security import require_admin

router = APIRouter()


@router.get("/admin/uxflags")
def list_flags(session: Session = Depends(get_session), _=Depends(require_admin)):
    rows = session.exec(select(UXFlags).order_by(UXFlags.key.asc())).all()
    return {"ok": True, "items": rows}


@router.post("/admin/uxflags/{key}")
def set_flag(key: str, payload: dict, session: Session = Depends(get_session), _=Depends(require_admin)):
    enabled = bool(payload.get("enabled", True))
    row = session.exec(select(UXFlags).where(UXFlags.key == key)).first()
    if not row:
        row = UXFlags(key=key, enabled=enabled)
        session.add(row)
    else:
        row.enabled = enabled
    session.commit()
    return {"ok": True, "item": row}


@router.get("/admin/festivals")
def list_festivals(session: Session = Depends(get_session), _=Depends(require_admin)):
    rows = session.exec(select(FestivalTheme).order_by(FestivalTheme.start_date.desc())).all()
    return {"ok": True, "items": rows}


@router.post("/admin/festivals")
def create_festival(payload: dict, session: Session = Depends(get_session), _=Depends(require_admin)):
    obj = FestivalTheme(**payload)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return {"ok": True, "item": obj}

