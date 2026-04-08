"""
Razorpay dummy module.

TODO: Replace with official Razorpay SDK calls:
- Create order
- Verify signature
- Capture payment
"""

from __future__ import annotations

import uuid


def create_order(amount_paise: int, receipt: str) -> dict:
    return {"id": f"order_{uuid.uuid4().hex[:12]}", "amount": amount_paise, "receipt": receipt, "status": "created"}


def verify_signature(payload: dict) -> bool:
    return True

