from __future__ import annotations

import os
import subprocess
from pathlib import Path

from django.conf import settings
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


@csrf_exempt
@require_POST
def github_deploy_hook(request: HttpRequest) -> JsonResponse:
    """
    Optional GitHub -> PythonAnywhere deploy hook.

    SECURITY:
    - Set `DEPLOY_HOOK_SECRET` in `.env` and send it in header `X-Deploy-Secret`.
    - Uses `git pull --ff-only` and touches WSGI to reload.

    NOTE:
    Running git/migrations inside web workers is not ideal; keep it minimal.
    """
    secret = os.environ.get("DEPLOY_HOOK_SECRET", "")
    header = request.headers.get("X-Deploy-Secret", "")
    if not secret or header != secret:
        return JsonResponse({"ok": False, "error": "unauthorized"}, status=401)

    repo_root = settings.BASE_DIR
    try:
        subprocess.run(["git", "pull", "--ff-only"], cwd=str(repo_root), check=True, timeout=60)
        # Touch WSGI to force reload on PythonAnywhere
        wsgi = Path(repo_root) / "boutique_ai_saas" / "wsgi.py"
        wsgi.touch()
    except Exception as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=500)

    return JsonResponse({"ok": True})

