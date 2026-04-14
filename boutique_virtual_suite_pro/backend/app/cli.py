from __future__ import annotations

from flask import Flask

from .seed import seed_defaults


def register_cli(app: Flask) -> None:
    @app.cli.command("seed")
    def seed():
        seed_defaults()
        print("seeded")

