from __future__ import annotations

from flask import Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required

from ..extensions import db
from ..models import Product, StyleProfile, UserFeed, UserMood

bp = Blueprint("feed", __name__)


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


@bp.get("/personalized")
@jwt_required()
def personalized():
    uid = int(get_jwt_identity())

    # Cache feed rows per user; regenerate if missing.
    feed = UserFeed.query.filter_by(user_id=uid).first()
    if not feed or not feed.product_ids:
        sp = StyleProfile.query.filter_by(user_id=uid).first()
        um = UserMood.query.filter_by(user_id=uid).first()
        style = (sp.personality_key if sp else "").strip()
        mood_key = (um.mood_key if um else "").strip()

        q = Product.query
        if style:
            q = q.filter(Product.style_tag.ilike(style))
        if mood_key:
            # mood_key is a key; for simplicity match partial
            q = q.filter(Product.mood_tag.ilike(f"%{mood_key}%"))
        products = q.order_by(Product.id.desc()).limit(60).all()
        ids = [p.id for p in products]
        if not feed:
            feed = UserFeed(user_id=uid, product_ids=ids)
            db.session.add(feed)
        else:
            feed.product_ids = ids
        db.session.commit()

    products = Product.query.filter(Product.id.in_(feed.product_ids)).all() if feed.product_ids else []
    products_by_id = {p.id: p for p in products}
    ordered = [products_by_id[i] for i in feed.product_ids if i in products_by_id]
    return {"ok": True, "products": [_product_dict(p) for p in ordered]}

