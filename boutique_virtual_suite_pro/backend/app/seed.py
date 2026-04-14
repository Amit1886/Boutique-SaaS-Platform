from __future__ import annotations

from .extensions import db
from .models import Moodboard, Product


def seed_defaults() -> None:
    moods = [
        ("festive", "Festive", "Tyohaar", "#db2777", "Festive picks"),
        ("party", "Party", "Party", "#7c3aed", "Party night"),
        ("bridal", "Bridal", "Dulhan", "#ef4444", "Bridal couture"),
        ("office", "Office", "Office", "#0ea5e9", "Office chic"),
        ("traditional", "Traditional", "Paramparik", "#f59e0b", "Traditional classics"),
    ]
    for key, en, hi, color, banner in moods:
        if not Moodboard.query.filter_by(key=key).first():
            db.session.add(Moodboard(key=key, name_en=en, name_hi=hi, theme_color=color, banner=banner))

    if Product.query.count() < 40:
        samples = [
            ("Rose Silk Saree", "saree", "https://picsum.photos/seed/saree1/800/1000", "rose", "silk", "Royal Bridal", "Bridal", 4999),
            ("Indigo Georgette Saree", "saree", "https://picsum.photos/seed/saree2/800/1000", "indigo", "georgette", "Bold Party", "Party", 2599),
            ("Minimal Cotton Saree", "saree", "https://picsum.photos/seed/saree3/800/1000", "slate", "cotton", "Modern Minimalist", "Office", 1799),
            ("Temple Jewelry Set", "jewelry", "https://picsum.photos/seed/jewel1/800/1000", "gold", "metal", "Classic Traditional", "Traditional", 1999),
            ("Sequin Party Blouse", "blouse", "https://picsum.photos/seed/blouse1/800/1000", "violet", "poly", "Bold Party", "Party", 1299),
        ]
        for i in range(1, 81):
            base = samples[i % len(samples)]
            db.session.add(
                Product(
                    name=f"{base[0]} #{i}",
                    category=base[1],
                    image_url=base[2],
                    base_color=base[3],
                    fabric=base[4],
                    style_tag=base[5],
                    mood_tag=base[6],
                    price=base[7],
                )
            )
    db.session.commit()

