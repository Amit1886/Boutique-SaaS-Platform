from __future__ import annotations

import urllib.parse


def whatsapp_link(phone: str, message: str) -> str:
    """
    Generates a click-to-chat link.
    Phone should include country code, digits only (e.g. 919999999999).
    """
    phone_digits = "".join([c for c in phone if c.isdigit()])
    text = urllib.parse.quote(message)
    if phone_digits:
        return f"https://wa.me/{phone_digits}?text={text}"
    return f"https://wa.me/?text={text}"

