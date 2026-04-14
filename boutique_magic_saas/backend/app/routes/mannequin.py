from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("/3d/mannequin")
def mannequin():
    return {
        "ok": True,
        "bodies": [
            {"key": "slim", "label": "Slim", "scale": 0.92},
            {"key": "curvy", "label": "Curvy", "scale": 1.0},
            {"key": "plus", "label": "Plus-size", "scale": 1.08},
        ],
    }

