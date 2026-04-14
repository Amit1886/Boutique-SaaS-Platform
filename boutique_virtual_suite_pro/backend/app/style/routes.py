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
            {"key": "royal", "label_en": "Royal", "label_hi": "Royal", "image_url": "https://picsum.photos/seed/bvp_q1_royal/600/420"},
            {"key": "minimal", "label_en": "Minimal", "label_hi": "Minimal", "image_url": "https://picsum.photos/seed/bvp_q1_minimal/600/420"},
            {"key": "bold", "label_en": "Bold", "label_hi": "Bold", "image_url": "https://picsum.photos/seed/bvp_q1_bold/600/420"},
        ],
    },
    {
        "id": "q2",
        "title_en": "Preferred palette",
        "title_hi": "Pasandeeda rang",
        "choices": [
            {"key": "warm", "label_en": "Warm", "label_hi": "Garam", "image_url": "https://picsum.photos/seed/bvp_q2_warm/600/420"},
            {"key": "cool", "label_en": "Cool", "label_hi": "Thande", "image_url": "https://picsum.photos/seed/bvp_q2_cool/600/420"},
            {"key": "neutral", "label_en": "Neutral", "label_hi": "Neutral", "image_url": "https://picsum.photos/seed/bvp_q2_neutral/600/420"},
        ],
    },
    {
        "id": "q3",
        "title_en": "Occasion",
        "title_hi": "Mauka",
        "choices": [
            {"key": "bridal", "label_en": "Bridal", "label_hi": "Dulhan", "image_url": "https://picsum.photos/seed/bvp_q3_bridal/600/420"},
            {"key": "party", "label_en": "Party", "label_hi": "Party", "image_url": "https://picsum.photos/seed/bvp_q3_party/600/420"},
            {"key": "office", "label_en": "Office", "label_hi": "Office", "image_url": "https://picsum.photos/seed/bvp_q3_office/600/420"},
        ],
    },
    {
        "id": "q4",
        "title_en": "Fabric feel",
        "title_hi": "Kapde ka ehsaas",
        "choices": [
            {"key": "silk", "label_en": "Silk", "label_hi": "Resham", "image_url": "https://picsum.photos/seed/bvp_q4_silk/600/420"},
            {"key": "cotton", "label_en": "Cotton", "label_hi": "Kapas", "image_url": "https://picsum.photos/seed/bvp_q4_cotton/600/420"},
            {"key": "georgette", "label_en": "Georgette", "label_hi": "Georgette", "image_url": "https://picsum.photos/seed/bvp_q4_georgette/600/420"},
        ],
    },
    {
        "id": "q5",
        "title_en": "Work detail",
        "title_hi": "Kaam ka detail",
        "choices": [
            {"key": "heavy", "label_en": "Heavy", "label_hi": "Heavy", "image_url": "https://picsum.photos/seed/bvp_q5_heavy/600/420"},
            {"key": "medium", "label_en": "Medium", "label_hi": "Medium", "image_url": "https://picsum.photos/seed/bvp_q5_medium/600/420"},
            {"key": "light", "label_en": "Light", "label_hi": "Light", "image_url": "https://picsum.photos/seed/bvp_q5_light/600/420"},
        ],
    },
    {
        "id": "q6",
        "title_en": "Jewelry style",
        "title_hi": "Jewelry style",
        "choices": [
            {"key": "temple", "label_en": "Temple", "label_hi": "Temple", "image_url": "https://picsum.photos/seed/bvp_q6_temple/600/420"},
            {"key": "diamond", "label_en": "Diamond", "label_hi": "Diamond", "image_url": "https://picsum.photos/seed/bvp_q6_diamond/600/420"},
            {"key": "minimal", "label_en": "Minimal", "label_hi": "Minimal", "image_url": "https://picsum.photos/seed/bvp_q6_minimal/600/420"},
        ],
    },
    {
        "id": "q7",
        "title_en": "Signature look",
        "title_hi": "Signature look",
        "choices": [
            {"key": "classic", "label_en": "Classic", "label_hi": "Classic", "image_url": "https://picsum.photos/seed/bvp_q7_classic/600/420"},
            {"key": "modern", "label_en": "Modern", "label_hi": "Modern", "image_url": "https://picsum.photos/seed/bvp_q7_modern/600/420"},
            {"key": "fusion", "label_en": "Fusion", "label_hi": "Fusion", "image_url": "https://picsum.photos/seed/bvp_q7_fusion/600/420"},
        ],
    },
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
