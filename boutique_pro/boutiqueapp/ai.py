"""
Dummy AI / image processing functions.

These are fully functional placeholders that you can later replace with:
- HuggingFace background-removal model
- Stable Diffusion / Try-On model
- Any hosted inference API
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image


def remove_background(input_path: Path, output_path: Path) -> Path:
    """
    Dummy background removal.

    Current behavior:
    - Converts image to RGBA
    - Lightly "cleans" near-white pixels by making them transparent

    Replace this with a real background-removal model.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(input_path) as im:
        im = im.convert("RGBA")
        pixels = im.getdata()
        new_pixels = []
        for r, g, b, a in pixels:
            if r > 245 and g > 245 and b > 245:
                new_pixels.append((r, g, b, 0))
            else:
                new_pixels.append((r, g, b, a))
        im.putdata(new_pixels)
        im.save(output_path, format="PNG")
    return output_path


def generate_virtual_tryon(user_img_path: Path, template_img_path: Path, output_path: Path) -> Path:
    """
    Dummy virtual try-on generator.

    Current behavior:
    - Resizes the template to match user's image width (keeps aspect ratio)
    - Alpha-composites template over the user image

    Replace this with a real try-on pipeline (e.g., SD-based) later.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(user_img_path) as base:
        base = base.convert("RGBA")
        with Image.open(template_img_path) as overlay:
            overlay = overlay.convert("RGBA")
            target_w = base.size[0]
            ratio = target_w / max(1, overlay.size[0])
            target_h = max(1, int(overlay.size[1] * ratio))
            overlay = overlay.resize((target_w, target_h), Image.Resampling.LANCZOS)
            y_offset = int(base.size[1] * 0.12)
            canvas = Image.new("RGBA", base.size, (0, 0, 0, 0))
            canvas.paste(overlay, (0, y_offset), overlay)
            out = Image.alpha_composite(base, canvas)
            out.save(output_path, format="PNG")
    return output_path

