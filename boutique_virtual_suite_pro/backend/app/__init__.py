from __future__ import annotations

from flask import Flask

from .config import Config
from .cli import register_cli
from .extensions import cors, db, jwt, migrate
from .routes import register_routes


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config())

    cors.init_app(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    register_routes(app)
    register_cli(app)

    @app.get("/api/health")
    def health():
        return {"ok": True}

    return app
