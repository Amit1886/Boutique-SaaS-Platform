from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class ProductBase(SQLModel):
    name: str
    price: int = 0
    primary_color: str = "#db2777"
    tags: str = ""


class Saree(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # Layer PNGs for try-on (optional)
    layer_body_png: str = ""  # relative path in uploads
    layer_pallu_png: str = ""
    layer_border_png: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Blouse(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    template_png: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Accessory(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    image_png: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)


class SavedLook(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_name: str = "Guest"
    saree_id: Optional[int] = None
    blouse_id: Optional[int] = None
    accessories_json: str = "[]"
    image_card_png: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Moodboard(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_name: str = "Guest"
    mood_key: str = "festive"
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class FestivalTheme(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    start_date: date
    end_date: date
    theme_color: str = "#db2777"
    banner_text: str = ""


class UXFlags(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    key: str = Field(index=True, unique=True)
    enabled: bool = True

