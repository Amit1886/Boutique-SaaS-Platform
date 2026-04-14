from __future__ import annotations

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from ..models import Moodboard, Product, StyleProfile, UserMood

bp = Blueprint("products", __name__)


def _product_dict(p: Product) -> dict:
    return {
        "id": p.id,
        "name": p.name,
        "category": p.category,
        "image_url": p.image_url,
        "base_color": p.base_color,
        "fabric": p.fabric,
        "style_tag": p.style_tag,
        "mood_tag": p.mood_tag,
        "price": p.price,
    }


@bp.get("/all")
def all_products():
    products = Product.query.order_by(Product.id.desc()).limit(500).all()
    return {"ok": True, "products": [_product_dict(p) for p in products]}


@bp.get("/by-mood")
def by_mood():
    mood = (request.args.get("mood") or "").strip()
    products = Product.query.filter(Product.mood_tag.ilike(f"%{mood}%")).order_by(Product.id.desc()).limit(200).all()
    return {"ok": True, "products": [_product_dict(p) for p in products]}


@bp.get("/by-style")
def by_style():
    style = (request.args.get("style") or "").strip()
    products = Product.query.filter(Product.style_tag.ilike(f"%{style}%")).order_by(Product.id.desc()).limit(200).all()
    return {"ok": True, "products": [_product_dict(p) for p in products]}


@bp.get("/recommended")
@jwt_required()
def recommended():
    uid = int(get_jwt_identity())
    sp = StyleProfile.query.filter_by(user_id=uid).first()
    um = UserMood.query.filter_by(user_id=uid).first()
    style = (sp.personality_key if sp else "").strip()
    mood_key = (um.mood_key if um else "").strip()
    mood = Moodboard.query.filter_by(key=mood_key).first()
    mood_name = (mood.name_en if mood else "").strip()

    q = Product.query
    if style:
        q = q.filter(Product.style_tag.ilike(style))
    if mood_name:
        q = q.filter(Product.mood_tag.ilike(mood_name))
    products = q.order_by(Product.id.desc()).limit(50).all()
    return {"ok": True, "products": [_product_dict(p) for p in products]}
