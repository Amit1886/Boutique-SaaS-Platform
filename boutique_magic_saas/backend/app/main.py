from __future__ import annotations

from datetime import date

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select

from .config import get_settings
from .db import engine, init_db
from .models import Accessory, Blouse, FestivalTheme, Saree, UXFlags
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

        # Seed festival themes if none exist (approximate dates; admin can edit exact ranges)
        any_theme = session.exec(select(FestivalTheme)).first()
        if not any_theme:
            y = date.today().year
            session.add(
                FestivalTheme(
                    name="Holi",
                    start_date=date(y, 3, 1),
                    end_date=date(y, 3, 31),
                    theme_color="#0ea5e9",
                    banner_text="Holi Color Bloom",
                )
            )
            session.add(
                FestivalTheme(
                    name="Navratri",
                    start_date=date(y, 10, 1),
                    end_date=date(y, 10, 15),
                    theme_color="#7c3aed",
                    banner_text="Navratri Nights",
                )
            )
            session.add(
                FestivalTheme(
                    name="Diwali",
                    start_date=date(y, 10, 20),
                    end_date=date(y, 11, 10),
                    theme_color="#f59e0b",
                    banner_text="Diwali Glow",
                )
            )
            session.add(
                FestivalTheme(
                    name="Wedding Season",
                    start_date=date(y, 11, 1),
                    end_date=date(y, 12, 31),
                    theme_color="#db2777",
                    banner_text="Wedding Season Magic",
                )
            )

        # Seed demo catalog (keeps UI usable without admin uploads)
        any_saree = session.exec(select(Saree)).first()
        if not any_saree:
            session.add(Saree(name="Rose Silk Saree", price=2999, primary_color="#db2777", tags="wedding,festive"))
            session.add(Saree(name="Ocean Blue Georgette", price=2399, primary_color="#0ea5e9", tags="party"))
            session.add(Saree(name="Royal Purple Banarasi", price=4999, primary_color="#7c3aed", tags="bridal"))

        any_blouse = session.exec(select(Blouse)).first()
        if not any_blouse:
            session.add(Blouse(name="Classic Round Neck", price=799, primary_color="#7c3aed", tags="round,match"))
            session.add(Blouse(name="Sweetheart Neck", price=899, primary_color="#db2777", tags="sweetheart"))
            session.add(Blouse(name="High Neck (Festive)", price=999, primary_color="#f59e0b", tags="highneck"))

        any_acc = session.exec(select(Accessory)).first()
        if not any_acc:
            session.add(Accessory(name="Kundan Earrings", price=399, primary_color="#f59e0b", tags="jewelry"))
            session.add(Accessory(name="Pearl Belt", price=499, primary_color="#ffffff", tags="belt"))
            session.add(Accessory(name="Pallu Clip", price=199, primary_color="#0f172a", tags="clip"))
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

# Optional: serve built React frontend in production (SPA fallback).
frontend_dist = (settings.base_dir.parent / "frontend" / "dist").resolve()
if frontend_dist.exists():

    @app.get("/{path_name:path}")
    def spa_fallback(path_name: str):
        p = (frontend_dist / path_name).resolve()
        if str(p).startswith(str(frontend_dist)) and p.is_file():
            return FileResponse(p)
        return FileResponse(frontend_dist / "index.html")
