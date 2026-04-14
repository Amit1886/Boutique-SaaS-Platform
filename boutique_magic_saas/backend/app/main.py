from __future__ import annotations

from datetime import date

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select

from .config import get_settings
from .db import engine, init_db
from .models import FestivalTheme, UXFlags
from .routes import admin, gallery, mannequin, mood, products, share, theme, ux

settings = get_settings()

app = FastAPI(title="Boutique Magic SaaS", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

uploads_dir = settings.upload_dir
uploads_dir.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(uploads_dir)), name="uploads")


@app.on_event("startup")
def _startup():
    init_db()
    with Session(engine) as session:
        # Seed UX flags
        for key in [
            "magic_mirror",
            "pallu_gravity",
            "tailor_jinn",
            "color_bloom",
            "teleport_anim",
            "shadow_sync",
            "aura_effect",
            "ripple_reveal",
        ]:
            existing = session.exec(select(UXFlags).where(UXFlags.key == key)).first()
            if not existing:
                session.add(UXFlags(key=key, enabled=True))

        # Seed festival themes if none exist
        any_theme = session.exec(select(FestivalTheme)).first()
        if not any_theme:
            session.add(
                FestivalTheme(
                    name="Wedding Season",
                    start_date=date(date.today().year, 11, 1),
                    end_date=date(date.today().year, 12, 31),
                    theme_color="#db2777",
                    banner_text="Wedding Season Magic",
                )
            )
            session.add(
                FestivalTheme(
                    name="Diwali",
                    start_date=date(date.today().year, 10, 20),
                    end_date=date(date.today().year, 11, 10),
                    theme_color="#f59e0b",
                    banner_text="Diwali Glow",
                )
            )
        session.commit()


@app.get("/api/health")
def health():
    return {"ok": True}


app.include_router(products.router, prefix="/api", tags=["products"])
app.include_router(gallery.router, prefix="/api", tags=["gallery"])
app.include_router(mannequin.router, prefix="/api", tags=["mannequin"])
app.include_router(theme.router, prefix="/api", tags=["theme"])
app.include_router(mood.router, prefix="/api", tags=["mood"])
app.include_router(share.router, prefix="/api", tags=["share"])
app.include_router(admin.router, prefix="/api", tags=["admin"])
app.include_router(ux.router, prefix="/api", tags=["ux"])
