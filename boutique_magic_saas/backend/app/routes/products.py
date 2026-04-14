from __future__ import annotations

from fastapi import APIRouter, Depends, File, UploadFile
from sqlmodel import Session, select

from ..db import get_session
from ..models import Accessory, Blouse, Saree
from ..security import require_admin
from ..storage import save_upload

router = APIRouter()


@router.get("/sarees")
def list_sarees(session: Session = Depends(get_session)):
    rows = session.exec(select(Saree).order_by(Saree.id.desc())).all()
    return {"ok": True, "items": rows}


@router.get("/blouses")
def list_blouses(session: Session = Depends(get_session)):
    rows = session.exec(select(Blouse).order_by(Blouse.id.desc())).all()
    return {"ok": True, "items": rows}


@router.get("/accessories")
def list_accessories(session: Session = Depends(get_session)):
    rows = session.exec(select(Accessory).order_by(Accessory.id.desc())).all()
    return {"ok": True, "items": rows}


@router.post("/sarees")
def create_saree(payload: dict, session: Session = Depends(get_session), _=Depends(require_admin)):
    obj = Saree(**payload)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return {"ok": True, "item": obj}


@router.post("/blouses")
def create_blouse(payload: dict, session: Session = Depends(get_session), _=Depends(require_admin)):
    obj = Blouse(**payload)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return {"ok": True, "item": obj}


@router.post("/accessories")
def create_accessory(payload: dict, session: Session = Depends(get_session), _=Depends(require_admin)):
    obj = Accessory(**payload)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return {"ok": True, "item": obj}


@router.delete("/sarees/{item_id}")
def delete_saree(item_id: int, session: Session = Depends(get_session), _=Depends(require_admin)):
    obj = session.get(Saree, item_id)
    if not obj:
        return {"ok": True}
    session.delete(obj)
    session.commit()
    return {"ok": True}


@router.delete("/blouses/{item_id}")
def delete_blouse(item_id: int, session: Session = Depends(get_session), _=Depends(require_admin)):
    obj = session.get(Blouse, item_id)
    if not obj:
        return {"ok": True}
    session.delete(obj)
    session.commit()
    return {"ok": True}


@router.delete("/accessories/{item_id}")
def delete_accessory(item_id: int, session: Session = Depends(get_session), _=Depends(require_admin)):
    obj = session.get(Accessory, item_id)
    if not obj:
        return {"ok": True}
    session.delete(obj)
    session.commit()
    return {"ok": True}


@router.put("/sarees/{item_id}")
def update_saree(item_id: int, payload: dict, session: Session = Depends(get_session), _=Depends(require_admin)):
    obj = session.get(Saree, item_id)
    if not obj:
        return {"ok": False, "error": "not found"}, 404
    for k, v in payload.items():
        if hasattr(obj, k):
            setattr(obj, k, v)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return {"ok": True, "item": obj}


@router.put("/blouses/{item_id}")
def update_blouse(item_id: int, payload: dict, session: Session = Depends(get_session), _=Depends(require_admin)):
    obj = session.get(Blouse, item_id)
    if not obj:
        return {"ok": False, "error": "not found"}, 404
    for k, v in payload.items():
        if hasattr(obj, k):
            setattr(obj, k, v)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return {"ok": True, "item": obj}


@router.put("/accessories/{item_id}")
def update_accessory(item_id: int, payload: dict, session: Session = Depends(get_session), _=Depends(require_admin)):
    obj = session.get(Accessory, item_id)
    if not obj:
        return {"ok": False, "error": "not found"}, 404
    for k, v in payload.items():
        if hasattr(obj, k):
            setattr(obj, k, v)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return {"ok": True, "item": obj}


@router.post("/upload/saree-layer")
async def upload_saree_layer(kind: str, file: UploadFile = File(...), _=Depends(require_admin)):
    # kind: body|pallu|border
    name = await save_upload(file, prefix=f"saree_{kind}")
    return {"ok": True, "path": f"/uploads/{name}"}


@router.post("/upload/blouse-template")
async def upload_blouse_template(file: UploadFile = File(...), _=Depends(require_admin)):
    name = await save_upload(file, prefix="blouse_tpl")
    return {"ok": True, "path": f"/uploads/{name}"}


@router.post("/upload/accessory")
async def upload_accessory(file: UploadFile = File(...), _=Depends(require_admin)):
    name = await save_upload(file, prefix="acc")
    return {"ok": True, "path": f"/uploads/{name}"}
