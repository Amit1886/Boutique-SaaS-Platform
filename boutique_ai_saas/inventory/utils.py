from __future__ import annotations


def estimate_fabric_usage_meters(category: str, height_in: float | None) -> float:
    """
    Dummy fabric usage calculator.

    TODO: replace with real formula per garment + vendor patterns.
    """
    h = height_in or 62.0
    base = 5.5 if category == "saree" else 2.0
    return round(base * (h / 62.0), 2)

