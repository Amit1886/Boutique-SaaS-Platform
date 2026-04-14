from __future__ import annotations

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from ..extensions import db
from ..models import DesignerProgress

bp = Blueprint("designer", __name__)


@bp.get("/progress")
@jwt_required()
def get_progress():
    uid = int(get_jwt_identity())
    row = DesignerProgress.query.filter_by(user_id=uid).first()
    return {"ok": True, "progress": row.progress if row else {}}


@bp.post("/progress")
@jwt_required()
def set_progress():
    uid = int(get_jwt_identity())
    data = request.get_json(force=True, silent=True) or {}
    progress = data.get("progress") or {}
    if not isinstance(progress, dict):
        return {"ok": False, "error": "progress must be an object"}, 400
    row = DesignerProgress.query.filter_by(user_id=uid).first()
    if not row:
        row = DesignerProgress(user_id=uid, progress=progress)
        db.session.add(row)
    else:
        row.progress = progress
    db.session.commit()
    return {"ok": True}

