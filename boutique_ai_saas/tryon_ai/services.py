from __future__ import annotations

import time
from pathlib import Path
import shutil

from django.conf import settings

from .ai import (
    ai_fitting_recommend as _ai_fitting_recommend,
    ai_measurement_detect as _ai_measurement_detect,
    generate_2d_tryon,
    generate_3d_body_model as _generate_3d_body_model,
    generate_blouse_design_image,
    remove_background as remove_background_dummy,
    change_background as _change_background,
)
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


# ---------------------------------------------------------------------------
# Required public APIs (placeholders, but end-to-end functional)
# ---------------------------------------------------------------------------


def generate_tryon_image(user_bg_removed: Path, template_path: Path, output_path: Path, session: TryOnSession | None = None) -> Path:
    return generate_tryon(user_bg_removed, template_path, output_path, session=session)


def generate_video_tryon(input_video: Path, output_video: Path, session: TryOnSession | None = None) -> Path:
    """
    Placeholder: copy input video to output video.
    Replace with real video-to-video try-on pipeline.
    """
    start = time.time()
    output_video.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(input_video, output_video)
    log_task(session, provider="dummy", task_type="generate_video_tryon", status="succeeded", duration_ms=int((time.time() - start) * 1000))
    return output_video


def generate_3d_body_model(img_path: Path, session: TryOnSession | None = None) -> dict:
    start = time.time()
    out = _generate_3d_body_model(img_path)
    log_task(session, provider="dummy", task_type="generate_3d_body_model", status="succeeded", response_meta=out, duration_ms=int((time.time() - start) * 1000))
    return out


def ai_measurement_detect(img_path: Path, session: TryOnSession | None = None) -> dict:
    start = time.time()
    out = _ai_measurement_detect(img_path)
    log_task(session, provider="dummy", task_type="ai_measurement_detect", status="succeeded", response_meta=out, duration_ms=int((time.time() - start) * 1000))
    return out


def ai_fitting_recommend(measurements: dict, session: TryOnSession | None = None) -> dict:
    start = time.time()
    out = _ai_fitting_recommend(measurements)
    log_task(session, provider="dummy", task_type="ai_fitting_recommend", status="succeeded", response_meta=out, duration_ms=int((time.time() - start) * 1000))
    return out


def generate_blouse_design(options: dict, output_path: Path, session: TryOnSession | None = None) -> Path:
    start = time.time()
    out = generate_blouse_design_image(options, output_path)
    log_task(session, provider="dummy", task_type="generate_blouse_design", status="succeeded", request_meta=options, duration_ms=int((time.time() - start) * 1000))
    return out


def change_background(img_path: Path, output_path: Path, background: str, session: TryOnSession | None = None) -> Path:
    start = time.time()
    out = _change_background(img_path, output_path, background=background)
    log_task(session, provider="dummy", task_type="change_background", status="succeeded", request_meta={"background": background}, duration_ms=int((time.time() - start) * 1000))
    return out


def generate_cutting_pdf(
    measurements: dict,
    output_path: Path,
    blueprint_type: str = "blouse",
    session: TryOnSession | None = None,
) -> Path:
    """
    Generate a PDF blueprint (reportlab when available).
    """
    start = time.time()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas

        c = canvas.Canvas(str(output_path), pagesize=A4)
        w, h = A4
        title = "Blouse Cutting Sheet" if blueprint_type == "blouse" else "Saree Fall/Pico Sheet"
        c.setFont("Helvetica-Bold", 16)
        c.drawString(40, h - 60, f"{title} (AI Placeholder)")
        c.setFont("Helvetica", 11)
        y = h - 100
        c.drawString(40, y, f"Type: {blueprint_type}")
        y -= 22
        for k, v in measurements.items():
            c.drawString(40, y, f"{k}: {v}")
            y -= 18
            if y < 80:
                c.showPage()
                y = h - 60
        c.rect(30, 30, w - 60, h - 60)
        c.showPage()
        c.save()
    except Exception as e:
        # Fallback: create a readable plain-text PDF-like file.
        output_path.write_text("Blueprint generator needs reportlab. Error: " + str(e), encoding="utf-8")

    log_task(session, provider="dummy", task_type="generate_cutting_pdf", status="succeeded", duration_ms=int((time.time() - start) * 1000))
    return output_path
