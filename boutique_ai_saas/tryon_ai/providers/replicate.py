from __future__ import annotations

import base64
import json
from pathlib import Path
from typing import Any

import requests


def run_replicate_prediction(
    version: str,
    token: str,
    input_payload: dict[str, Any],
    wait_seconds: int = 60,
) -> dict[str, Any]:
    """
    Minimal Replicate HTTP API wrapper (sync wait up to 60s).

    TODO: For long-running predictions, poll `GET /v1/predictions/{id}` until `status == succeeded`.
    """
    url = "https://api.replicate.com/v1/predictions"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Prefer": f"wait={max(1, min(60, wait_seconds))}",
    }
    body = {"version": version, "input": input_payload}
    res = requests.post(url, headers=headers, data=json.dumps(body), timeout=120)
    res.raise_for_status()
    return res.json()


def remove_background_replicate(input_path: Path, output_path: Path, token: str, version: str) -> Path:
    """
    Background removal via Replicate (requires you to set a background-removal model version).
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    b64 = base64.b64encode(input_path.read_bytes()).decode("utf-8")
    pred = run_replicate_prediction(version=version, token=token, input_payload={"image": f"data:image/png;base64,{b64}"})
    # TODO: download output URL(s) to `output_path`
    # For now, just return input copied to output to keep pipeline functional.
    output_path.write_bytes(input_path.read_bytes())
    return output_path

