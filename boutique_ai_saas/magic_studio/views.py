from __future__ import annotations

import base64
import json
import os
from datetime import date, datetime
from pathlib import Path
from urllib.parse import quote

from django.conf import settings
from django.http import FileResponse, HttpRequest, HttpResponse, JsonResponse
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Accessory, Blouse, FestivalTheme, Moodboard, Saree, SavedLook, UXFlag


def _admin_token() -> str:
    return (os.environ.get("MAGIC_ADMIN_TOKEN") or os.environ.get("ADMIN_TOKEN") or "change-me").strip()


def _require_admin(request: HttpRequest) -> None:
    token = (request.headers.get("X-Admin-Token") or "").strip()
    if not token or token != _admin_token():
        raise PermissionError("admin token required")


def _json_body(request: HttpRequest) -> dict:
    if not request.body:
        return {}
    try:
        return json.loads(request.body.decode("utf-8"))
    except Exception:
        return {}


def _magic_upload_root() -> Path:
    return Path(settings.MEDIA_ROOT) / "magic_uploads"


def _save_bytes(prefix: str, content: bytes, ext: str) -> str:
    root = _magic_upload_root()
    root.mkdir(parents=True, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")
    safe_prefix = "".join([c for c in prefix if c.isalnum() or c in ("_", "-")])[:24] or "file"
    name = f"{safe_prefix}_{ts}.{ext.lstrip('.')}"
    (root / name).write_bytes(content)
    return f"/uploads/{name}"


@require_http_methods(["GET"])
def serve_upload(request: HttpRequest, path: str) -> HttpResponse:
    root = _magic_upload_root().resolve()
    target = (root / path).resolve()
    if not str(target).startswith(str(root)) or not target.exists() or not target.is_file():
        return HttpResponse(status=404)
    return FileResponse(open(target, "rb"))


@require_http_methods(["GET"])
def spa(request: HttpRequest) -> HttpResponse:
    dist = Path(__file__).resolve().parent / "spa_dist"
    index = dist / "index.html"
    if not index.exists():
        return HttpResponse(
            "Magic Studio SPA not built yet. Build it once: `cd boutique_magic_saas/frontend && npm install && npm run build`.",
            content_type="text/plain",
            status=200,
        )

    rel = request.path.replace("/magic/", "", 1).lstrip("/")
    candidate = (dist / rel).resolve() if rel else index.resolve()
    if rel and str(candidate).startswith(str(dist.resolve())) and candidate.exists() and candidate.is_file():
        return FileResponse(open(candidate, "rb"))
    return FileResponse(open(index, "rb"))


@require_http_methods(["GET"])
def health(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"ok": True})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def sarees(request: HttpRequest) -> JsonResponse:
    if request.method == "GET":
        items = list(Saree.objects.all().values())
        return JsonResponse({"ok": True, "items": items})
    try:
        _require_admin(request)
    except PermissionError as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=403)
    payload = _json_body(request)
    obj = Saree.objects.create(**{k: v for k, v in payload.items() if k in {f.name for f in Saree._meta.fields}})
    return JsonResponse({"ok": True, "item": {**payload, "id": obj.id}})


@csrf_exempt
@require_http_methods(["PUT", "DELETE"])
def saree_detail(request: HttpRequest, item_id: int) -> JsonResponse:
    try:
        _require_admin(request)
    except PermissionError as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=403)
    obj = Saree.objects.filter(pk=item_id).first()
    if not obj:
        return JsonResponse({"ok": True})
    if request.method == "DELETE":
        obj.delete()
        return JsonResponse({"ok": True})
    payload = _json_body(request)
    for k, v in payload.items():
        if hasattr(obj, k):
            setattr(obj, k, v)
    obj.save()
    return JsonResponse({"ok": True, "item": payload})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def blouses(request: HttpRequest) -> JsonResponse:
    if request.method == "GET":
        items = list(Blouse.objects.all().values())
        return JsonResponse({"ok": True, "items": items})
    try:
        _require_admin(request)
    except PermissionError as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=403)
    payload = _json_body(request)
    obj = Blouse.objects.create(**{k: v for k, v in payload.items() if k in {f.name for f in Blouse._meta.fields}})
    return JsonResponse({"ok": True, "item": {**payload, "id": obj.id}})


@csrf_exempt
@require_http_methods(["PUT", "DELETE"])
def blouse_detail(request: HttpRequest, item_id: int) -> JsonResponse:
    try:
        _require_admin(request)
    except PermissionError as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=403)
    obj = Blouse.objects.filter(pk=item_id).first()
    if not obj:
        return JsonResponse({"ok": True})
    if request.method == "DELETE":
        obj.delete()
        return JsonResponse({"ok": True})
    payload = _json_body(request)
    for k, v in payload.items():
        if hasattr(obj, k):
            setattr(obj, k, v)
    obj.save()
    return JsonResponse({"ok": True, "item": payload})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def accessories(request: HttpRequest) -> JsonResponse:
    if request.method == "GET":
        items = list(Accessory.objects.all().values())
        return JsonResponse({"ok": True, "items": items})
    try:
        _require_admin(request)
    except PermissionError as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=403)
    payload = _json_body(request)
    obj = Accessory.objects.create(**{k: v for k, v in payload.items() if k in {f.name for f in Accessory._meta.fields}})
    return JsonResponse({"ok": True, "item": {**payload, "id": obj.id}})


@csrf_exempt
@require_http_methods(["PUT", "DELETE"])
def accessory_detail(request: HttpRequest, item_id: int) -> JsonResponse:
    try:
        _require_admin(request)
    except PermissionError as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=403)
    obj = Accessory.objects.filter(pk=item_id).first()
    if not obj:
        return JsonResponse({"ok": True})
    if request.method == "DELETE":
        obj.delete()
        return JsonResponse({"ok": True})
    payload = _json_body(request)
    for k, v in payload.items():
        if hasattr(obj, k):
            setattr(obj, k, v)
    obj.save()
    return JsonResponse({"ok": True, "item": payload})


@csrf_exempt
@require_http_methods(["POST"])
def upload_saree_layer(request: HttpRequest) -> JsonResponse:
    try:
        _require_admin(request)
    except PermissionError as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=403)
    kind = (request.GET.get("kind") or "body").strip()
    f = request.FILES.get("file")
    if not f:
        return JsonResponse({"ok": False, "error": "file required"}, status=400)
    content = f.read()
    path = _save_bytes(f"saree_{kind}", content, "png")
    return JsonResponse({"ok": True, "path": path})


@csrf_exempt
@require_http_methods(["POST"])
def upload_blouse_template(request: HttpRequest) -> JsonResponse:
    try:
        _require_admin(request)
    except PermissionError as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=403)
    f = request.FILES.get("file")
    if not f:
        return JsonResponse({"ok": False, "error": "file required"}, status=400)
    content = f.read()
    path = _save_bytes("blouse_tpl", content, "png")
    return JsonResponse({"ok": True, "path": path})


@csrf_exempt
@require_http_methods(["POST"])
def upload_accessory(request: HttpRequest) -> JsonResponse:
    try:
        _require_admin(request)
    except PermissionError as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=403)
    f = request.FILES.get("file")
    if not f:
        return JsonResponse({"ok": False, "error": "file required"}, status=400)
    content = f.read()
    path = _save_bytes("acc", content, "png")
    return JsonResponse({"ok": True, "path": path})


@require_http_methods(["GET"])
def gallery_looks(request: HttpRequest) -> JsonResponse:
    items = list(SavedLook.objects.all().values())
    return JsonResponse({"ok": True, "items": items})


@csrf_exempt
@require_http_methods(["POST"])
def gallery_save(request: HttpRequest) -> JsonResponse:
    payload = _json_body(request)
    data_url = (payload.get("image_card_png") or "").strip()
    if data_url.startswith("data:image"):
        try:
            header, b64 = data_url.split(",", 1)
            raw = base64.b64decode(b64.encode("utf-8"))
            img_path = _save_bytes("look_card", raw, "png")
        except Exception:
            img_path = ""
    else:
        img_path = ""
    obj = SavedLook.objects.create(
        user_name=(payload.get("user_name") or "Guest")[:120],
        saree_id=payload.get("saree_id"),
        blouse_id=payload.get("blouse_id"),
        accessories_json=payload.get("accessories_json") or "[]",
        image_card_png=img_path,
    )
    return JsonResponse({"ok": True, "item": {"id": obj.id, **payload, "image_card_png": img_path, "created_at": now().isoformat()}})


@require_http_methods(["GET"])
def mannequin(request: HttpRequest) -> JsonResponse:
    bodies = [
        {"key": "slim", "label": "Slim", "scale": 0.95},
        {"key": "curvy", "label": "Curvy", "scale": 1.0},
        {"key": "plus", "label": "Plus-size", "scale": 1.1},
    ]
    return JsonResponse({"ok": True, "bodies": bodies})


@require_http_methods(["GET"])
def festival(request: HttpRequest) -> JsonResponse:
    today = date.today()
    all_rows = list(FestivalTheme.objects.all().values())
    active = None
    for row in all_rows:
        if row["start_date"] <= today <= row["end_date"]:
            active = row
            break
    return JsonResponse({"ok": True, "active": active, "all": all_rows})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def user_moodboard(request: HttpRequest) -> JsonResponse:
    if request.method == "GET":
        user_name = (request.GET.get("user_name") or "Guest")[:120]
        row = Moodboard.objects.filter(user_name=user_name).values().first()
        return JsonResponse({"ok": True, "item": row})
    payload = _json_body(request)
    user_name = (payload.get("user_name") or "Guest")[:120]
    mood_key = (payload.get("mood_key") or "festive")[:40]
    obj, _ = Moodboard.objects.update_or_create(user_name=user_name, defaults={"mood_key": mood_key})
    return JsonResponse({"ok": True, "item": {"user_name": obj.user_name, "mood_key": obj.mood_key}})


@csrf_exempt
@require_http_methods(["POST"])
def look_share(request: HttpRequest) -> JsonResponse:
    payload = _json_body(request)
    user_name = payload.get("user_name") or "Guest"
    look_name = payload.get("look_name") or "My Look"
    price = payload.get("price") or ""
    text = f"{look_name} | {user_name} | {price} | {datetime.now().strftime('%Y-%m-%d')}"
    wa = f"https://wa.me/?text={quote(text)}"
    return JsonResponse({"ok": True, "whatsapp_url": wa, "text": text})


@require_http_methods(["GET"])
def uxflags(request: HttpRequest) -> JsonResponse:
    items = list(UXFlag.objects.all().values("key", "enabled"))
    return JsonResponse({"ok": True, "items": items})


@csrf_exempt
@require_http_methods(["GET"])
def admin_uxflags(request: HttpRequest) -> JsonResponse:
    try:
        _require_admin(request)
    except PermissionError as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=403)
    items = list(UXFlag.objects.all().values("key", "enabled"))
    return JsonResponse({"ok": True, "items": items})


@csrf_exempt
@require_http_methods(["POST"])
def admin_uxflag_set(request: HttpRequest, key: str) -> JsonResponse:
    try:
        _require_admin(request)
    except PermissionError as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=403)
    payload = _json_body(request)
    enabled = bool(payload.get("enabled", True))
    obj, _ = UXFlag.objects.update_or_create(key=key, defaults={"enabled": enabled})
    return JsonResponse({"ok": True, "item": {"key": obj.key, "enabled": obj.enabled}})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def admin_festivals(request: HttpRequest) -> JsonResponse:
    try:
        _require_admin(request)
    except PermissionError as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=403)
    if request.method == "GET":
        items = list(FestivalTheme.objects.all().values())
        return JsonResponse({"ok": True, "items": items})
    payload = _json_body(request)
    obj = FestivalTheme.objects.create(**payload)
    return JsonResponse({"ok": True, "item": {"id": obj.id, **payload}})

