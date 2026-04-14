from __future__ import annotations

from flask import Blueprint, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from werkzeug.security import check_password_hash, generate_password_hash

from ..extensions import db
from ..models import User

bp = Blueprint("auth", __name__)


@bp.post("/signup")
def signup():
    data = request.get_json(force=True, silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    name = (data.get("name") or "").strip()
    language = (data.get("language") or "en").strip()[:5]
    if not email or "@" not in email:
        return {"ok": False, "error": "Valid email required"}, 400
    if len(password) < 6:
        return {"ok": False, "error": "Password must be at least 6 chars"}, 400
    if User.query.filter_by(email=email).first():
        return {"ok": False, "error": "Email already exists"}, 409

    u = User(email=email, password_hash=generate_password_hash(password), name=name, language=language)
    db.session.add(u)
    db.session.commit()
    token = create_access_token(identity=str(u.id))
    return {"ok": True, "token": token, "user": {"id": u.id, "email": u.email, "name": u.name, "language": u.language}}


@bp.post("/login")
def login():
    data = request.get_json(force=True, silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    u = User.query.filter_by(email=email).first()
    if not u or not check_password_hash(u.password_hash, password):
        return {"ok": False, "error": "Invalid credentials"}, 401
    token = create_access_token(identity=str(u.id))
    return {"ok": True, "token": token, "user": {"id": u.id, "email": u.email, "name": u.name, "language": u.language}}


@bp.get("/user")
@jwt_required()
def user():
    uid = int(get_jwt_identity())
    u = User.query.get(uid)
    if not u:
        return {"ok": False, "error": "Not found"}, 404
    return {"ok": True, "user": {"id": u.id, "email": u.email, "name": u.name, "language": u.language}}

