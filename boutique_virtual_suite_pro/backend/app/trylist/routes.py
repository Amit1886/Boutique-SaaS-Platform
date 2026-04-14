from __future__ import annotations

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from ..extensions import db
from ..models import Product, TrylistItem

bp = Blueprint("trylist", __name__)


@bp.post("/add")
@jwt_required()
def add():
    uid = int(get_jwt_identity())
    data = request.get_json(force=True, silent=True) or {}
    product_id = int(data.get("product_id") or 0)
    p = Product.query.get(product_id)
    if not p:
        return {"ok": False, "error": "Invalid product"}, 400
    existing = TrylistItem.query.filter_by(user_id=uid, product_id=product_id).first()
    if existing:
        return {"ok": True, "item": {"id": existing.id, "product_id": existing.product_id, "position": existing.position}}
    max_pos = db.session.query(db.func.max(TrylistItem.position)).filter(TrylistItem.user_id == uid).scalar() or 0
    item = TrylistItem(user_id=uid, product_id=product_id, position=int(max_pos) + 1)
    db.session.add(item)
    db.session.commit()
    return {"ok": True, "item": {"id": item.id, "product_id": item.product_id, "position": item.position}}


@bp.post("/remove")
@jwt_required()
def remove():
    uid = int(get_jwt_identity())
    data = request.get_json(force=True, silent=True) or {}
    product_id = int(data.get("product_id") or 0)
    item = TrylistItem.query.filter_by(user_id=uid, product_id=product_id).first()
    if not item:
        return {"ok": True}
    db.session.delete(item)
    db.session.commit()
    return {"ok": True}


@bp.get("/all")
@jwt_required()
def all_items():
    uid = int(get_jwt_identity())
    items = TrylistItem.query.filter_by(user_id=uid).order_by(TrylistItem.position.asc()).all()
    product_ids = [i.product_id for i in items]
    products = {p.id: p for p in Product.query.filter(Product.id.in_(product_ids)).all()} if product_ids else {}
    return {
        "ok": True,
        "items": [
            {
                "product_id": i.product_id,
                "position": i.position,
                "product": {
                    "id": products.get(i.product_id).id,
                    "name": products.get(i.product_id).name,
                    "category": products.get(i.product_id).category,
                    "image_url": products.get(i.product_id).image_url,
                    "base_color": products.get(i.product_id).base_color,
                    "fabric": products.get(i.product_id).fabric,
                    "style_tag": products.get(i.product_id).style_tag,
                    "mood_tag": products.get(i.product_id).mood_tag,
                    "price": products.get(i.product_id).price,
                }
                if products.get(i.product_id)
                else None,
            }
            for i in items
        ],
    }


@bp.post("/reorder")
@jwt_required()
def reorder():
    uid = int(get_jwt_identity())
    data = request.get_json(force=True, silent=True) or {}
    order = data.get("order") or []
    if not isinstance(order, list):
        return {"ok": False, "error": "order must be a list"}, 400
    # Expect list of product_ids in desired order.
    ids = [int(x) for x in order if str(x).isdigit() or isinstance(x, int)]
    if not ids:
        return {"ok": True}
    existing = {i.product_id: i for i in TrylistItem.query.filter_by(user_id=uid).all()}
    pos = 1
    for pid in ids:
        item = existing.get(pid)
        if not item:
            continue
        item.position = pos
        pos += 1
    db.session.commit()
    return {"ok": True}
