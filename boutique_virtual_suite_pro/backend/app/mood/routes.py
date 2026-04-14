from __future__ import annotations

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from ..extensions import db
from ..models import Moodboard, UserMood

bp = Blueprint("mood", __name__)


@bp.get("/list")
def list_moods():
    moods = Moodboard.query.order_by(Moodboard.id.asc()).all()
    return {
        "ok": True,
        "moods": [
            {"key": m.key, "name_en": m.name_en, "name_hi": m.name_hi, "theme_color": m.theme_color, "banner": m.banner}
            for m in moods
        ],
    }


@bp.post("/apply")
@jwt_required()
def apply_mood():
    data = request.get_json(force=True, silent=True) or {}
    key = (data.get("key") or "").strip().lower()
    m = Moodboard.query.filter_by(key=key).first()
    if not m:
        return {"ok": False, "error": "Invalid mood"}, 400
    uid = int(get_jwt_identity())
    um = UserMood.query.filter_by(user_id=uid).first()
    if not um:
        um = UserMood(user_id=uid, mood_key=key)
        db.session.add(um)
    else:
        um.mood_key = key
    db.session.commit()
    return {"ok": True, "mood": {"key": m.key, "theme_color": m.theme_color, "banner": m.banner}}

