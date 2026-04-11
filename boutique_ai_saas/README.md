# boutique_ai_saas (Django SaaS scaffold)

This project is generated as an enterprise-style Boutique SaaS platform with multi-vendor routing, plans/features, try-on session flow, dashboards, POS, inventory, tailor workflow, order tracking, and a DRF + JWT API layer.

## Run (Windows / PowerShell)

1. Install Python 3.12+ and ensure `py` works.
2. `cd boutique_ai_saas`
3. `py -m venv .venv`
4. `.\.venv\Scripts\Activate.ps1`
5. `py -m pip install -r requirements.txt`
6. `py manage.py migrate`
7. `py manage.py createsuperuser`
8. `py manage.py runserver`

## Demo vendor (auto-seeded on migrate)

- Username: `demo_vendor`
- Password: `demo12345`
- Store: `/demo/`

## Fixing `Could not find platform independent libraries <prefix>`

If you see that message before Django starts, clear these env vars in PowerShell before running:

```powershell
Remove-Item Env:PYTHONHOME -ErrorAction SilentlyContinue
Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
```

## Key routes

- `/` SaaS landing (vendors + pricing)
- `/<vendor>/` Vendor storefront (path-based vendor routing)
- `/<vendor>/tryon/upload/` → templates → generate → confirm order
- `/order/track/<id>/` Tracking timeline
- `/vendor/dashboard/`, `/tailor/dashboard/`, `/admin/dashboard/`
- `/pos/`, `/inventory/`, `/pricing/`
- `/api/` DRF routes, `/api/token/` JWT

## PythonAnywhere (Free) deployment

### Folder layout (recommended)

- `~/boutique_ai_saas/static` (source)
- `~/boutique_ai_saas/staticfiles` (collectstatic output)
- `~/boutique_ai_saas/media` (uploads)
- `~/boutique_ai_saas/env` (optional)
- `~/boutique_ai_saas/logs` (optional)

### Production `.env` values (important)

Set these in `~/boutique_ai_saas/.env` (copy from `.env.example`):

- `DJANGO_DEBUG=0`
- `DJANGO_SECRET_KEY=<long-random-secret>`
- `DJANGO_ALLOWED_HOSTS=<yourusername>.pythonanywhere.com`
- `DJANGO_CSRF_TRUSTED_ORIGINS=https://<yourusername>.pythonanywhere.com`
- `MAIN_DOMAIN=<yourusername>.pythonanywhere.com` (optional; only needed for subdomain routing)

### First-time setup (manual)

1. Create a PythonAnywhere account and a web app (Manual configuration, Python 3.12)
2. Clone repo on PythonAnywhere:
   - `git clone <your-github-repo> boutique_ai_saas`
3. Create `.env` from `.env.example`:
   - `cp .env.example .env`
4. Run deploy script:
   - `bash scripts/pythonanywhere/deploy.sh`
5. On the Web tab, open the **WSGI configuration file** and point it to your project folder, then import the Django app (typical setup):
   - Add your project path: `/home/<yourusername>/boutique_ai_saas`
   - Set `DJANGO_SETTINGS_MODULE` to `boutique_ai_saas.settings`
   - Import `application` from `boutique_ai_saas.wsgi`
6. On the Web tab, add Static files mappings:
   - URL: `/static/` -> Directory: `/home/<yourusername>/boutique_ai_saas/staticfiles`
   - URL: `/media/` -> Directory: `/home/<yourusername>/boutique_ai_saas/media`

### GitHub → PythonAnywhere auto-deploy (free-friendly)

This repo includes an in-app deploy hook:
- URL: `/deploy/github/`
- Header required: `X-Deploy-Secret: <DEPLOY_HOOK_SECRET>`

Set these GitHub repo secrets:
- `PA_WEBAPP_URL` = `https://<yourusername>.pythonanywhere.com`
- `DEPLOY_HOOK_SECRET` = same as in PythonAnywhere `.env`

Optional (extra reload via API):
- `PA_USERNAME`
- `PA_API_TOKEN` (PythonAnywhere Account → API token)
- `PA_WEBAPP_DOMAIN` = `<yourusername>.pythonanywhere.com`
- `PA_HOST` = `www.pythonanywhere.com` (or `eu.pythonanywhere.com`)

## Android (WebView) app

Source: `android_webview_app/`

1. Edit `android_webview_app/app/build.gradle`:
   - Replace `BuildConfig.BASE_URL` with your PythonAnywhere URL
2. Build locally (Android Studio) or via GitHub Actions:
   - Workflow: `.github/workflows/android_build.yml`
   - Artifacts: `app-debug.apk`, `app-release.apk` (release is signed with debug key for installability)
