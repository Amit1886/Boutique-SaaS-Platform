from __future__ import annotations

from datetime import datetime

from sqlalchemy import UniqueConstraint

from .extensions import db


class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class User(db.Model, TimestampMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(190), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(120), default="", nullable=False)
    language = db.Column(db.String(5), default="en", nullable=False)  # en/hi

    personality = db.relationship("StyleProfile", uselist=False, back_populates="user", cascade="all,delete-orphan")


class Product(db.Model, TimestampMixin):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), nullable=False)
    category = db.Column(db.String(40), nullable=False)  # saree/blouse/accessories/jewelry
    image_url = db.Column(db.String(500), default="", nullable=False)
    base_color = db.Column(db.String(40), default="pink", nullable=False)
    fabric = db.Column(db.String(80), default="", nullable=False)
    style_tag = db.Column(db.String(80), default="", nullable=False)  # e.g. Modern Minimalist
    mood_tag = db.Column(db.String(80), default="", nullable=False)  # Festive/Party/Bridal/Office/Traditional
    price = db.Column(db.Integer, default=0, nullable=False)


class Favorite(db.Model, TimestampMixin):
    __tablename__ = "favorites"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False, index=True)

    __table_args__ = (UniqueConstraint("user_id", "product_id", name="uq_fav_user_product"),)


class TrylistItem(db.Model, TimestampMixin):
    __tablename__ = "trylist"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False, index=True)
    position = db.Column(db.Integer, default=0, nullable=False)

    __table_args__ = (UniqueConstraint("user_id", "product_id", name="uq_try_user_product"),)


class Moodboard(db.Model, TimestampMixin):
    __tablename__ = "moodboards"
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(40), unique=True, nullable=False)  # festive/party/bridal/office/traditional
    name_en = db.Column(db.String(60), nullable=False)
    name_hi = db.Column(db.String(60), nullable=False)
    theme_color = db.Column(db.String(20), nullable=False)
    banner = db.Column(db.String(200), default="", nullable=False)


class UserMood(db.Model, TimestampMixin):
    __tablename__ = "user_moods"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    mood_key = db.Column(db.String(40), nullable=False)


class PersonalityTest(db.Model, TimestampMixin):
    __tablename__ = "personality_tests"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    answers = db.Column(db.JSON, default=dict, nullable=False)
    result_key = db.Column(db.String(60), nullable=False)


class StyleProfile(db.Model, TimestampMixin):
    __tablename__ = "style_profiles"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    personality_key = db.Column(db.String(80), default="", nullable=False)

    user = db.relationship("User", back_populates="personality")


class UserFeed(db.Model, TimestampMixin):
    __tablename__ = "user_feed"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    product_ids = db.Column(db.JSON, default=list, nullable=False)


class DesignerProgress(db.Model, TimestampMixin):
    __tablename__ = "designer_progress"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False, index=True)
    progress = db.Column(db.JSON, default=dict, nullable=False)
