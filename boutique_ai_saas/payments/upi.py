from __future__ import annotations

import urllib.parse
from pathlib import Path

import qrcode


def upi_payment_link(upi_id: str, payee_name: str, amount: str, note: str) -> str:
    params = {
        "pa": upi_id,
        "pn": payee_name,
        "am": amount,
        "cu": "INR",
        "tn": note,
    }
    return "upi://pay?" + urllib.parse.urlencode(params, safe=":/")


def upi_qr_png(link: str, out_path: Path) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img = qrcode.make(link)
    img.save(out_path)
    return out_path

