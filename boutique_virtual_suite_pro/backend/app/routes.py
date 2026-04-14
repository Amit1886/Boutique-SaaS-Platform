from __future__ import annotations

from flask import Flask

from .auth.routes import bp as auth_bp
from .designer.routes import bp as designer_bp
from .favorites.routes import bp as favorites_bp
from .feed.routes import bp as feed_bp
from .mood.routes import bp as mood_bp
from .products.routes import bp as products_bp
from .style.routes import bp as style_bp
from .trylist.routes import bp as trylist_bp


def register_routes(app: Flask) -> None:
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(designer_bp, url_prefix="/api/designer")
    app.register_blueprint(favorites_bp, url_prefix="/api/favorites")
    app.register_blueprint(mood_bp, url_prefix="/api/mood")
    app.register_blueprint(trylist_bp, url_prefix="/api/trylist")
    app.register_blueprint(style_bp, url_prefix="/api/style")
    app.register_blueprint(products_bp, url_prefix="/api/products")
    app.register_blueprint(feed_bp, url_prefix="/api/feed")
