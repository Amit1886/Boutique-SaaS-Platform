from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw


def generate_invoice_pdf(order_id: int, vendor_name: str, product_name: str, amount: str, out_path: Path) -> Path:
    """
    Dummy invoice generator using Pillow (outputs a real PDF).

    TODO: Replace with a real invoice template + GST details + numbering.
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", (1240, 1754), (255, 255, 255))  # A4-ish
    d = ImageDraw.Draw(img)
    d.rectangle([40, 40, 1200, 1714], outline=(30, 41, 59), width=3)
    d.text((70, 70), f"INVOICE (Dummy)  Order #{order_id}", fill=(15, 23, 42))
    d.text((70, 130), f"Vendor: {vendor_name}", fill=(51, 65, 85))
    d.text((70, 170), f"Product: {product_name}", fill=(51, 65, 85))
    d.text((70, 210), f"Amount: {amount}", fill=(51, 65, 85))
    d.text((70, 270), "Thank you for your order.", fill=(51, 65, 85))
    img.save(out_path, "PDF")
    return out_path

