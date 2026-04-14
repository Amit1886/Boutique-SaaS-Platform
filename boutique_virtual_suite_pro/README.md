# Boutique Virtual Suite Pro

Modern Boutique SaaS ecosystem (Flask + React/Vite) with moodboard UX, designer flow, trylist queue, favorites, live preview, and personalization.

## Structure

- `backend/` Flask REST API (JWT, SQLAlchemy, migrations)
- `frontend/` React + Vite + Tailwind + DaisyUI + Zustand
- `design-system/` theme tokens and UI guidelines
- `database/` SQLite DB location (default)
- `deployment/` PythonAnywhere + Vercel setup
- `scripts/` helper scripts

## Backend (Flask)

### Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### Migrations

```bash
flask --app run.py db upgrade
flask --app run.py seed
flask --app run.py run
```

Backend runs at `http://127.0.0.1:5000`.

## Frontend (React)

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Frontend runs at `http://127.0.0.1:5173`.

## API Routes (summary)

- `POST /api/auth/signup`
- `POST /api/auth/login`
- `GET /api/auth/user`
- `GET /api/mood/list`
- `POST /api/mood/apply`
- `POST /api/trylist/add`
- `POST /api/trylist/remove`
- `GET /api/trylist/all`
- `GET /api/style/test/questions`
- `POST /api/style/test/submit`
- `GET /api/style/personality`
- `GET /api/products/all`
- `GET /api/products/by-mood?mood=...`
- `GET /api/products/by-style?style=...`
- `GET /api/feed/personalized`

