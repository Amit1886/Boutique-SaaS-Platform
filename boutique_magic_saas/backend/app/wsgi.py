from __future__ import annotations

from a2wsgi import ASGIMiddleware

from .main import app

application = ASGIMiddleware(app)

