# Boutique Magic SaaS (FastAPI + React)

Premium “magic” try-on UX (no AI): camera overlay, blend-mode saree layers, tilt gravity, bloom background, teleport sparkle, aura glow, ripple pattern reveal, 3D mannequin rotate, draping guide, saved looks + WhatsApp share.

## Local Run

### Backend (FastAPI)

```bash
cd boutique_magic_saas/backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8008
```

### Frontend (React)

```bash
cd boutique_magic_saas/frontend
npm install
cp .env.example .env
npm run dev
```

- Frontend: `http://127.0.0.1:5174`
- Backend: `http://127.0.0.1:8008`

## Admin

- Open `http://127.0.0.1:5174/admin`
- Set the same `ADMIN_TOKEN` in `backend/.env` and in the Admin page (stored in `localStorage`)
- Upload saree layers (body/pallu/border PNG) to make the overlay fit correctly

## Build Frontend For Production (served by backend)

```bash
cd boutique_magic_saas/frontend
npm install
npm run build
```

When `frontend/dist` exists, the backend serves it with SPA fallback (so your PythonAnywhere app can serve both UI + API).

## PythonAnywhere

See `boutique_magic_saas/deployment/pythonanywhere/README.md`.
