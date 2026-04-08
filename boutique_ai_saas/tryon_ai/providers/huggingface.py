from __future__ import annotations

import base64
import io
from pathlib import Path

import requests
from PIL import Image


def _headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"} if token else {}


def call_image_segmentation(image_bytes: bytes, token: str, model: str) -> list[dict]:
    """
    HF Inference API task: image-segmentation
    Response: list of {label, score, mask(base64)}.
    """
    url = f"https://api-inference.huggingface.co/models/{model}"
    res = requests.post(url, headers=_headers(token), data=image_bytes, timeout=90)
    res.raise_for_status()
    payload = res.json()
    if not isinstance(payload, list):
        raise ValueError("Unexpected HF image-segmentation response")
    return payload


def call_image_to_image(image_bytes: bytes, token: str, model: str, parameters: dict | None = None) -> bytes:
    """
    HF Inference API task: image-to-image

    NOTE: Many try-on workflows need *two* images (person + garment). The default HF task is single-image;
    use this only if your chosen model endpoint supports your expected inputs.
    """
    url = f"https://api-inference.huggingface.co/models/{model}"
    if parameters:
        import json

        body = {"inputs": base64.b64encode(image_bytes).decode("utf-8"), "parameters": parameters}
        res = requests.post(url, headers={**_headers(token), "Content-Type": "application/json"}, data=json.dumps(body), timeout=120)
    else:
        res = requests.post(url, headers=_headers(token), data=image_bytes, timeout=120)
    res.raise_for_status()
    return res.content
    def image_segmentation_mask(self, image_bytes: bytes, model: str, threshold: float = 0.25) -> Image.Image:
        """
        Calls Hugging Face Inference API for `image-segmentation`.

        Expected response: list of {label, score, mask(base64)}.
        """
        url = f"https://api-inference.huggingface.co/models/{model}"
        params = {"threshold": threshold}
        res = requests.post(url, headers=self._headers(), params=params, data=image_bytes, timeout=90)
        res.raise_for_status()
        payload = res.json()
        if not isinstance(payload, list) or not payload:
            raise ValueError("Unexpected HF response for image segmentation")

        # Prefer person label if present; otherwise highest score.
        persons = [p for p in payload if isinstance(p, dict) and "person" in str(p.get("label", "")).lower()]
        chosen = persons if persons else payload

        combined = None
        for seg in chosen:
            if not isinstance(seg, dict) or "mask" not in seg:
                continue
            mask_b64 = seg["mask"]
            mask_bytes = base64.b64decode(mask_b64)
            mask_img = Image.open(io.BytesIO(mask_bytes)).convert("L")
            combined = mask_img if combined is None else Image.eval(ImageChops.lighter(combined, mask_img), lambda x: x)

        if combined is None:
            # fallback first segment
            mask_bytes = base64.b64decode(payload[0]["mask"])
            combined = Image.open(io.BytesIO(mask_bytes)).convert("L")
        return combined


def remove_background_hf(input_path: Path, output_path: Path, token: str, model: str) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image_bytes = input_path.read_bytes()
    payload = call_image_segmentation(image_bytes=image_bytes, token=token, model=model)
    if not payload:
        raise ValueError("Unexpected HF RMBG response")

    # Prefer "person" label(s) if present, otherwise pick highest score segment.
    segments = [p for p in payload if isinstance(p, dict) and "mask" in p]
    persons = [s for s in segments if "person" in str(s.get("label", "")).lower()]
    chosen = persons if persons else [max(segments, key=lambda x: float(x.get("score", 0) or 0))]

    # Combine masks by maximum (OR-like)
    mask = None
    for seg in chosen:
        mask_bytes = base64.b64decode(seg["mask"])
        m = Image.open(io.BytesIO(mask_bytes)).convert("L")
        if mask is not None and m.size != mask.size:
            m = m.resize(mask.size, Image.Resampling.NEAREST)
        mask = m if mask is None else Image.frombytes("L", m.size, bytes([max(a, b) for a, b in zip(mask.tobytes(), m.tobytes())]))
    if mask is None:
        raise ValueError("No mask found in HF response")

    with Image.open(io.BytesIO(image_bytes)) as im:
        im = im.convert("RGBA")
        # Normalize mask to alpha
        alpha = mask.resize(im.size, Image.Resampling.BILINEAR)
        im.putalpha(alpha)
        im.save(output_path, format="PNG")
    return output_path
