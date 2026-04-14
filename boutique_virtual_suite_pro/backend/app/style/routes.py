from __future__ import annotations

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from ..extensions import db
from ..models import PersonalityTest, StyleProfile

bp = Blueprint("style", __name__)


QUESTIONS = [
    {
        "id": "q1",
        "title_en": "Pick a vibe",
        "title_hi": "Apna vibe chunein",
        "choices": [
            {"key": "royal", "label_en": "Royal", "label_hi": "Royal"},
            {"key": "minimal", "label_en": "Minimal", "label_hi": "Minimal"},
            {"key": "bold", "label_en": "Bold", "label_hi": "Bold"},
        ],
    },
    {
        "id": "q2",
        "title_en": "Preferred palette",
        "title_hi": "Pasandeeda rang",
        "choices": [
            {"key": "warm", "label_en": "Warm", "label_hi": "Garam"},
            {"key": "cool", "label_en": "Cool", "label_hi": "Thande"},
            {"key": "neutral", "label_en": "Neutral", "label_hi": "Neutral"},
        ],
    },
    {"id": "q3", "title_en": "Occasion", "title_hi": "Mauka", "choices": [{"key": "bridal", "label_en": "Bridal", "label_hi": "Dulhan"}, {"key": "party", "label_en": "Party", "label_hi": "Party"}, {"key": "office", "label_en": "Office", "label_hi": "Office"}]},
    {"id": "q4", "title_en": "Fabric feel", "title_hi": "Kapde ka ehsaas", "choices": [{"key": "silk", "label_en": "Silk", "label_hi": "Resham"}, {"key": "cotton", "label_en": "Cotton", "label_hi": "Kapas"}, {"key": "georgette", "label_en": "Georgette", "label_hi": "Georgette"}]},
    {"id": "q5", "title_en": "Work detail", "title_hi": "Kaam ka detail", "choices": [{"key": "heavy", "label_en": "Heavy", "label_hi": "Heavy"}, {"key": "medium", "label_en": "Medium", "label_hi": "Medium"}, {"key": "light", "label_en": "Light", "label_hi": "Light"}]},
    {"id": "q6", "title_en": "Jewelry style", "title_hi": "Jewelry style", "choices": [{"key": "temple", "label_en": "Temple", "label_hi": "Temple"}, {"key": "diamond", "label_en": "Diamond", "label_hi": "Diamond"}, {"key": "minimal", "label_en": "Minimal", "label_hi": "Minimal"}]},
    {"id": "q7", "title_en": "Signature look", "title_hi": "Signature look", "choices": [{"key": "classic", "label_en": "Classic", "label_hi": "Classic"}, {"key": "modern", "label_en": "Modern", "label_hi": "Modern"}, {"key": "fusion", "label_en": "Fusion", "label_hi": "Fusion"}]},
]


def _score_personality(answers: dict) -> str:
    # Simple deterministic mapping (non-AI).
    tags = " ".join([str(v) for v in answers.values()]).lower()
    if "bridal" in tags or "royal" in tags or "heavy" in tags:
        return "Royal Bridal"
    if "minimal" in tags and "neutral" in tags:
        return "Modern Minimalist"
    if "bold" in tags or "party" in tags:
        return "Bold Party"
    return "Classic Traditional"


@bp.get("/test/questions")
def questions():
    return {"ok": True, "questions": QUESTIONS}


@bp.post("/test/submit")
@jwt_required()
def submit():
    uid = int(get_jwt_identity())
    data = request.get_json(force=True, silent=True) or {}
    answers = data.get("answers") or {}
    if not isinstance(answers, dict) or len(answers) < 3:
        return {"ok": False, "error": "answers required"}, 400
    result_key = _score_personality(answers)

    t = PersonalityTest(user_id=uid, answers=answers, result_key=result_key)
    db.session.add(t)

    sp = StyleProfile.query.filter_by(user_id=uid).first()
    if not sp:
        sp = StyleProfile(user_id=uid, personality_key=result_key)
        db.session.add(sp)
    else:
        sp.personality_key = result_key
    db.session.commit()
    return {"ok": True, "result": {"personality": result_key}}


@bp.get("/personality")
@jwt_required()
def personality():
    uid = int(get_jwt_identity())
    sp = StyleProfile.query.filter_by(user_id=uid).first()
    return {"ok": True, "personality": sp.personality_key if sp else ""}

