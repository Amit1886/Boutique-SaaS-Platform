# Boutique Magic SaaS (FastAPI + React)

## Run (Local)

### Backend

```bash
cd boutique_magic_saas/backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8008
```

### Frontend

```bash
cd boutique_magic_saas/frontend
npm install
cp .env.example .env
npm run dev
```

Frontend: `http://127.0.0.1:5174`  
Backend: `http://127.0.0.1:8008`

