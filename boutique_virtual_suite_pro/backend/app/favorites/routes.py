from __future__ import annotations

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from ..extensions import db
from ..models import Favorite, Product

bp = Blueprint("favorites", __name__)


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
@jwt_required()
def all_favs():
    uid = int(get_jwt_identity())
    favs = Favorite.query.filter_by(user_id=uid).order_by(Favorite.id.desc()).limit(500).all()
    ids = [f.product_id for f in favs]
    products = {p.id: p for p in Product.query.filter(Product.id.in_(ids)).all()} if ids else {}
    out = []
    for f in favs:
        p = products.get(f.product_id)
        out.append({"product_id": f.product_id, "product": _product_dict(p) if p else None})
    return {"ok": True, "favorites": out}


@bp.post("/add")
@jwt_required()
def add():
    uid = int(get_jwt_identity())
    data = request.get_json(force=True, silent=True) or {}
    product_id = int(data.get("product_id") or 0)
    p = Product.query.get(product_id)
    if not p:
        return {"ok": False, "error": "Invalid product"}, 400
    if Favorite.query.filter_by(user_id=uid, product_id=product_id).first():
        return {"ok": True}
    db.session.add(Favorite(user_id=uid, product_id=product_id))
    db.session.commit()
    return {"ok": True}


@bp.post("/remove")
@jwt_required()
def remove():
    uid = int(get_jwt_identity())
    data = request.get_json(force=True, silent=True) or {}
    product_id = int(data.get("product_id") or 0)
    fav = Favorite.query.filter_by(user_id=uid, product_id=product_id).first()
    if not fav:
        return {"ok": True}
    db.session.delete(fav)
    db.session.commit()
    return {"ok": True}

