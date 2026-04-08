from __future__ import annotations

import time
from pathlib import Path

from django.conf import settings

from .ai import generate_2d_tryon, remove_background as remove_background_dummy
from .models import AITaskHistory, TryOnSession
from .providers.huggingface import remove_background_hf


def log_task(
    session: TryOnSession | None,
    provider: str,
    task_type: str,
    status: str,
    request_meta: dict | None = None,
    response_meta: dict | None = None,
    error: str = "",
    duration_ms: int | None = None,
) -> None:
    AITaskHistory.objects.create(
        session=session,
        provider=provider,
        task_type=task_type,
        status=status,
        request_meta=request_meta or {},
        response_meta=response_meta or {},
        error=error,
        duration_ms=duration_ms or 0,
    )


def remove_background(input_path: Path, output_path: Path, session: TryOnSession | None = None) -> Path:
    """
    Free-tier friendly pipeline:
    1) Try HuggingFace Inference API if configured
    2) Fallback to local dummy background removal
    """
    start = time.time()
    if getattr(settings, "HF_API_TOKEN", "") and getattr(settings, "HF_RMBG_MODEL", ""):
        try:
            out = remove_background_hf(
                input_path=input_path,
                output_path=output_path,
                token=settings.HF_API_TOKEN,
                model=settings.HF_RMBG_MODEL,
            )
            log_task(
                session,
                provider="huggingface",
                task_type="remove_background",
                status="succeeded",
                request_meta={"model": settings.HF_RMBG_MODEL},
                duration_ms=int((time.time() - start) * 1000),
            )
            return out
        except Exception as e:
            log_task(
                session,
                provider="huggingface",
                task_type="remove_background",
                status="failed",
                request_meta={"model": settings.HF_RMBG_MODEL},
                error=str(e),
                duration_ms=int((time.time() - start) * 1000),
            )

    out = remove_background_dummy(input_path, output_path)
    log_task(
        session,
        provider="dummy",
        task_type="remove_background",
        status="succeeded",
        duration_ms=int((time.time() - start) * 1000),
    )
    return out


def generate_tryon(user_bg_removed: Path, template_path: Path, output_path: Path, session: TryOnSession | None = None) -> Path:
    """
    Try-on generator (dummy overlay by default).
    TODO: wire HF_TRYON_MODEL / Replicate try-on model and store output.
    """
    start = time.time()
    out = generate_2d_tryon(user_bg_removed, template_path, output_path)
    log_task(session, provider="dummy", task_type="generate_tryon", status="succeeded", duration_ms=int((time.time() - start) * 1000))
    return out

