# PythonAnywhere (FastAPI via WSGI bridge)

PythonAnywhere uses WSGI. This project ships a WSGI wrapper using `a2wsgi` so you can run FastAPI as a WSGI app.

## Steps

1) Upload/clone repo to `~/boutique_magic_saas`
2) Create virtualenv and install requirements:
   - `python3.10 -m venv ~/.virtualenvs/boutique_magic_saas`
   - `source ~/.virtualenvs/boutique_magic_saas/bin/activate`
   - `pip install -r ~/boutique_magic_saas/backend/requirements.txt`
3) Create env file:
   - copy `backend/.env.example` to `backend/.env` and set `ADMIN_TOKEN`
4) Web tab:
   - Set source code directory to `~/boutique_magic_saas/backend`
   - Use WSGI file `deployment/pythonanywhere/wsgi.py`
5) Reload

